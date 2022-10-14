import os
import os.path
import re
import subprocess
import sys
import sysconfig
import warnings
from distutils import util
from distutils.command import build_ext
from typing import Any, Dict, List, Optional, Tuple, Union, cast

import pkg_resources
from setuptools import Extension, setup

IS_DEBUG = os.getenv("CYKSUID_DEBUG", "") == "1"

ext_macros: List[Tuple[str, str]] = []
ext_include_dirs = []

if IS_DEBUG:
    print("Build in debug mode")
    # Adding cython line trace for coverage report
    ext_macros += ("CYTHON_TRACE_NOGIL", "1"), ("CYTHON_TRACE", "1")
    # Adding upper directory for supporting code coverage when running
    # tests inside the cython package
    ext_include_dirs += [".."]
    # Some extra info for cython compiler


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


ext_modules = [
    Extension(
        "cyksuid.fast_base62",
        sources=["cyksuid/fast_base62" + suffix, "cyksuid/cbase62.cc"],
        define_macros=ext_macros,
        include_dirs=ext_include_dirs,
        language="c++",
    ),
    Extension(
        "cyksuid._ksuid",
        sources=["cyksuid/_ksuid" + suffix],
        define_macros=ext_macros,
        include_dirs=ext_include_dirs,
        language="c++",
    ),
]


class BuildExt(build_ext.build_ext):
    def initialize_options(self) -> None:
        super().initialize_options()
        self.cython_kwargs: Optional[Dict[str, Any]] = None
        self.cython_compiler_directives: Optional[dict] = None
        self.extra_compile_args: List[str] = []
        self.extra_link_args: List[str] = []

    def finalize_options(self) -> None:
        super().finalize_options()
        if self.cython_kwargs is None:
            self.cython_kwargs = {
                "force": True,
            }
        if self.cython_compiler_directives is None:
            self.cython_compiler_directives = {
                "language_level": "3",
                "embedsignature": True,
                "binding": True,
            }

        if IS_DEBUG:
            self.cython_kwargs.update(
                {
                    "gdb_debug": True,
                    "annotate": True,
                }
            )
            self.cython_compiler_directives.update(
                {
                    "linetrace": True,
                    "profile": True,
                    "binding": True,
                }
            )

    def build_extensions(self) -> None:
        is_msvc = self.compiler.compiler_type == "msvc"
        is_clang = hasattr(self.compiler, "compiler_cxx") and (  # noqa: F841
            "clang++" in self.compiler.compiler_cxx
        )
        is_windows = sys.platform[:3] == "win"
        is_mingw = is_windows and (
            self.compiler.compiler_type.lower()
            in ["mingw32", "mingw64", "mingw", "msys", "msys2", "gcc", "g++"]
        )

        check_args: List[str] = []
        if sys.platform == "darwin":
            check_args += [
                "-Wno-deprecated-register",
            ]

            # https://developer.apple.com/documentation/xcode_release_notes/xcode_10_release_notes
            # C++ projects must now migrate to libc++ and are recommended to set a
            # deployment target of macOS 10.9 or later, or iOS 7 or later.
            mac_target = str(sysconfig.get_config_var("MACOSX_DEPLOYMENT_TARGET"))
            if mac_target and (
                pkg_resources.parse_version(mac_target)
                < pkg_resources.parse_version("10.9.0")
            ):
                os.environ["MACOSX_DEPLOYMENT_TARGET"] = "10.9"
                os.environ["_PYTHON_HOST_PLATFORM"] = re.sub(
                    r"macosx-[0-9]+\.[0-9]+-(.+)",
                    r"macosx-10.9-\1",
                    util.get_platform(),
                )

        if is_msvc:
            self.extra_compile_args += [
                "/MT",
                "/O2",
                "/std:c++14",
            ]
        else:
            check_args += [
                "-Wno-write-strings",
                "-Wno-invalid-offsetof",
                "-Wno-sign-compare",
                "-Wno-unused-variable",
                "-Wno-shorten-64-to-32",
            ]
            self.add_extra_compile_args(check_args)

        if not is_mingw:
            self.add_highest_supported_cxx_standard()

        if not IS_DEBUG:
            self.add_O3()
            self.add_no_math_errno()
            self.add_no_trapping_math()
            if not is_windows:
                self.add_link_time_optimization()

        for e in self.extensions:
            e.extra_compile_args += self.extra_compile_args

        if USE_CYTHON:
            self.extensions = cythonize(
                self.extensions,
                compiler_directives=self.cython_compiler_directives,
                **cast(dict, self.cython_kwargs),
            )
        super().build_extensions()

    def add_extra_compile_args(self, args: List[str]) -> None:
        for arg in args:
            if self.test_supports_compile_arg(arg):
                self.extra_compile_args.append(arg)

    def add_highest_supported_cxx_standard(self):
        cxx17 = "-std=c++17"
        cxx14 = "-std=gnu++14"
        cxx11 = "-std=c++11"
        if self.test_supports_compile_arg(cxx17):
            self.extra_compile_args.append(cxx17)
        elif self.test_supports_compile_arg(cxx14):
            self.extra_compile_args.append(cxx14)
        elif self.test_supports_compile_arg(cxx11):
            self.extra_compile_args.append(cxx11)
        else:
            msg = "\n\n\nWarning: compiler does not support C++11, compilation of cyksuid might fail without it.\n\n\n"
            warnings.warn(msg)

    def add_O3(self):
        O3 = "-O3"
        if self.test_supports_compile_arg(O3):
            self.extra_compile_args.append(O3)

    def add_no_math_errno(self):
        arg_fnme = "-fno-math-errno"
        if self.test_supports_compile_arg(arg_fnme):
            self.extra_compile_args.append(arg_fnme)
            self.extra_link_args.append(arg_fnme)

    def add_no_trapping_math(self):
        arg_fntm = "-fno-trapping-math"
        if self.test_supports_compile_arg(arg_fntm):
            self.extra_compile_args.append(arg_fntm)
            self.extra_link_args.append(arg_fntm)

    def add_link_time_optimization(self):
        arg_lto = "-flto"
        if self.test_supports_compile_arg(arg_lto):
            self.extra_compile_args.append(arg_lto)
            self.extra_link_args.append(arg_lto)

    def test_supports_compile_arg(self, comm: Union[str, List[str]]) -> bool:
        if not hasattr(self.compiler, "compiler_cxx"):
            return False
        if not isinstance(comm, list):
            comm = [comm]

        is_supported = False

        try:
            if not isinstance(self.compiler.compiler_cxx, list):
                cmd = list(self.compiler.compiler_cxx)
            else:
                cmd = self.compiler.compiler_cxx
        except Exception as e:
            print("Error: could not get compiler_cxx: %s" % e)
            cmd = self.compiler.compiler_cxx

        print("--- Checking compiler support for option '%s'" % " ".join(comm), end="")
        fname = "cyksuid_compiler_testing.cpp"
        try:
            with open(fname, "w") as ftest:
                ftest.write("int main(int argc, char**argv) {return 0;}\n")

            val_good = subprocess.call(cmd + [fname])
            val = subprocess.call(cmd + comm + [fname])
            is_supported = val == val_good
        except Exception:
            is_supported = False
        finally:
            try:
                os.remove(fname)
            except Exception:
                pass
        print(" ... %s" % ("yes" if is_supported else "no"))
        return is_supported


setup(
    name="cyksuid",
    version="2.0.2",
    description="Cython implementation of ksuid",
    ext_modules=ext_modules,
    cmdclass={"build_ext": BuildExt},
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
    keywords=["ksuid"],
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
