import os
import os.path
import sys
from typing import Any, Dict, List, Tuple
from setuptools import setup, Extension
from distutils import ccompiler, msvccompiler

IS_DEBUG = os.getenv("CY_DEBUG", "")

ext_macros: List[Tuple[str, str]] = []
ext_cythonize_kwargs: Dict[str, Any] = {
    "force": True,
    "compiler_directives": {},
}
ext_include_dirs = []

if IS_DEBUG == "1":
    print("Build in debug mode")
    # Adding cython line trace for coverage report
    ext_macros += ("CYTHON_TRACE_NOGIL", "1"), ("CYTHON_TRACE", "1")
    # Adding upper directory for supporting code coverage when running
    # tests inside the cython package
    ext_include_dirs += [".."]
    # Some extra info for cython compiler
    ext_cythonize_kwargs.update(
        {
            "gdb_debug": True,
            "annotate": True,
            "compiler_directives": {
                "linetrace": True,
                "profile": True,
                "binding": True,
            },
        }
    )


try:
    from Cython.Build import cythonize

    HAS_CYTHON = True
except ImportError:
    HAS_CYTHON = False


USE_CYTHON = "--cython" in sys.argv or "--with-cython" in sys.argv

if "--no-cython" in sys.argv:
    USE_CYTHON = False
    sys.argv.remove("--no-cython")
if "--without-cython" in sys.argv:
    USE_CYTHON = False
    sys.argv.remove("--without-cython")
if "--cython" in sys.argv:
    sys.argv.remove("--cython")
if "--with-cython" in sys.argv:
    sys.argv.remove("--with-cython")

if USE_CYTHON and not HAS_CYTHON:
    print("WARNING: Cython not installed.  Building without Cython.")
    USE_CYTHON = False


if USE_CYTHON:
    suffix = ".pyx"
else:
    suffix = ".c"


ext_include_dirs += ["cyksuid"]
if (
    ccompiler.new_compiler().compiler_type == "msvc"
    and msvccompiler.get_build_version() == 9
):
    root = os.path.abspath(os.path.dirname(__file__))
    ext_include_dirs.append(os.path.join(root, "include", "msvc9"))


ext_modules = [
    Extension(
        "cyksuid.fast_base62",
        sources=["cyksuid/fast_base62" + suffix, "cyksuid/cbase62.c"],
        define_macros=ext_macros,
        include_dirs=ext_include_dirs,
    ),
    Extension(
        "cyksuid.ksuid",
        sources=["cyksuid/ksuid" + suffix],
        define_macros=ext_macros,
        include_dirs=ext_include_dirs,
    ),
]


if USE_CYTHON:
    ext_cythonize_kwargs["compiler_directives"].update(
        {
            "language_level": "3",
            "embedsignature": True,
            "binding": True,
        }
    )
    ext_modules = cythonize(ext_modules, **ext_cythonize_kwargs)


setup(
    name="cyksuid",
    version="2.0.0dev",
    description="Cython implementation of ksuid",
    ext_modules=ext_modules,
    long_description=(
        open("README.rst").read() if os.path.exists("README.rst") else ""
    ),
    url="https://github.com/timonwong/cyksuid",
    author="Timon Wong",
    author_email="timon86.wang@gmail.com",
    license="BSD",
    packages=["cyksuid"],
    package_data={
        "cyksuid": ["*.pyx", "*.pxd", "*.pyi", "py.typed"],
    },
    keywords="ksuid",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Cython",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    install_requires=[],
    zip_safe=False,
)
