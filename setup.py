import os
import os.path
import re
import sys
import sysconfig
from distutils import util
from typing import Any, Dict, List, Tuple

import pkg_resources
from setuptools import Extension, setup

IS_DEBUG = os.getenv("CYKSUID_DEBUG", "")

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


def check_option(name: str) -> bool:
    cli_arg = "--" + name
    if cli_arg in sys.argv:
        sys.argv.remove(cli_arg)
        return True

    env_var = name.replace("-", "_").upper()
    if os.environ.get(env_var) in ("true", "1"):
        return True

    return False


USE_CYTHON = check_option("cython") or check_option("with-cython")

if check_option("no-cython") or check_option("without-cython"):
    USE_CYTHON = False

if USE_CYTHON and not HAS_CYTHON:
    print("WARNING: Cython not installed.  Building without Cython.")
    USE_CYTHON = False


if USE_CYTHON:
    suffix = ".pyx"
else:
    suffix = ".cpp"

extra_compile_args: List[str] = []
if sys.platform != "win32":
    extra_compile_args.append("-Wno-write-strings")
    extra_compile_args.append("-Wno-invalid-offsetof")
    extra_compile_args.append("-Wno-sign-compare")
    extra_compile_args.append("-Wno-unused-variable")
    extra_compile_args.append("-std=c++14")

if sys.platform == "darwin":
    extra_compile_args.append("-Wno-shorten-64-to-32")
    extra_compile_args.append("-Wno-deprecated-register")

    # https://developer.apple.com/documentation/xcode_release_notes/xcode_10_release_notes
    # C++ projects must now migrate to libc++ and are recommended to set a
    # deployment target of macOS 10.9 or later, or iOS 7 or later.
    if sys.platform == "darwin":
        mac_target = str(sysconfig.get_config_var("MACOSX_DEPLOYMENT_TARGET"))
        if mac_target and (
            pkg_resources.parse_version(mac_target)
            < pkg_resources.parse_version("10.9.0")
        ):
            os.environ["MACOSX_DEPLOYMENT_TARGET"] = "10.9"
            os.environ["_PYTHON_HOST_PLATFORM"] = re.sub(
                r"macosx-[0-9]+\.[0-9]+-(.+)", r"macosx-10.9-\1", util.get_platform()
            )

# MSVS default is dymanic
if sys.platform == "win32":
    extra_compile_args.append("/MT")

if "clang" in os.popen("$CC --version 2> /dev/null").read():
    extra_compile_args.append("-Wno-shorten-64-to-32")

ext_modules = [
    Extension(
        "cyksuid.fast_base62",
        sources=["cyksuid/fast_base62" + suffix, "cyksuid/cbase62.cc"],
        define_macros=ext_macros,
        include_dirs=ext_include_dirs,
        extra_compile_args=extra_compile_args,
        language="c++",
    ),
    Extension(
        "cyksuid._ksuid",
        sources=["cyksuid/_ksuid" + suffix],
        define_macros=ext_macros,
        include_dirs=ext_include_dirs,
        extra_compile_args=extra_compile_args,
        language="c++",
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
    version="2.0.0",
    description="Cython implementation of ksuid",
    ext_modules=ext_modules,
    long_description=open("README.md").read() if os.path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    url="https://github.com/timonwong/cyksuid",
    author="Timon Wong",
    author_email="timon86.wang@gmail.com",
    license="BSD",
    packages=["cyksuid"],
    package_data={
        "cyksuid": ["*.pyx", "*.pxd", "*.pyi", "py.typed", "*.h", "*.cc", "*.cpp"],
    },
    keywords="ksuid",
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Cython",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
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
