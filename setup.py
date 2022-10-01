import os.path
import sys
from setuptools import setup, Extension
from distutils import ccompiler, msvccompiler


info = {}
filename = os.path.join("cyksuid", "__version__.py")
exec(
    compile(open(filename, "rb").read().replace(b"\r\n", b"\n"), filename, "exec"), info
)
VERSION = info["__version__"]


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


include_dirs = []
if (
    ccompiler.new_compiler().compiler_type == "msvc"
    and msvccompiler.get_build_version() == 9
):
    root = os.path.abspath(os.path.dirname(__file__))
    include_dirs.append(os.path.join(root, "include", "msvc9"))


ext_modules = []
for modname in ["fast_base62", "ksuid"]:
    ext_modules.append(
        Extension(
            "cyksuid." + modname.replace("/", "."),
            ["cyksuid/" + modname + suffix],
            include_dirs=include_dirs,
        )
    )


if USE_CYTHON:
    compiler_directives = {
        "embedsignature": True,
        "binding": True,
        "language_level": "3",
    }
    ext_modules = cythonize(ext_modules, compiler_directives=compiler_directives)


setup(
    name="cyksuid",
    version=VERSION,
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
        "cyksuid": ["*.pyx", "*.pxd"],
    },
    keywords="ksuid",
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
