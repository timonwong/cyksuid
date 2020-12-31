# -*- coding: utf-8 -*-

"""
Parts of this file were taken from the pandas project
(https://github.com/pandas-dev/pandas) which have been
permitted for use under the BSD license.
"""

from __future__ import print_function

import argparse
import os.path
import sys
import multiprocessing
from setuptools import setup, Command, Extension
from setuptools.command.build_ext import build_ext
from setuptools.command.sdist import sdist
from distutils import ccompiler, msvccompiler
from distutils.version import LooseVersion


cmdclass = {}
info = {}
filename = os.path.join('cyksuid', '__version__.py')
exec(compile(open(filename, "rb").read().replace(b'\r\n', b'\n'), filename, 'exec'), info)
VERSION = info['__version__']
del info

MIN_CYTHON_VER = '0.27.0'

try:
    from Cython import Tempita, __version__ as _CYTHON_VERSION
    from Cython.Build import cythonize

    _CYTHON_INSTALLED = _CYTHON_VERSION >= LooseVersion(MIN_CYTHON_VER)
except ImportError:
    _CYTHON_VERSION = None
    _CYTHON_INSTALLED = False
    cythonize = lambda x, *args, **kwargs: x  # dummy func


class CheckSDist(sdist):
    """Custom sdist that ensures Cython has compiled all pyx files to c."""

    _pyxfiles = [
        "cyksuid/fast_base62.pyx",
        "cyksuid/ksuid.pyx",
    ]

    def initialize_options(self):
        sdist.initialize_options(self)

    def run(self):
        if False and "cython" in cmdclass:
            self.run_command("cython")
        else:
            # If we are not running cython then
            # compile the extensions correctly
            pyx_files = [(self._pyxfiles, "c")]

            for pyxfiles, extension in pyx_files:
                for pyxfile in pyxfiles:
                    sourcefile = pyxfile[:-3] + extension
                    msg = (
                        "%s-source file %s' not found.\n"
                        "Run 'setup.py cython' before sdist."
                    ) % (extension, sourcefile)
                    assert os.path.isfile(sourcefile), msg
        sdist.run(self)


class CheckingBuildExt(build_ext):
    """
    Subclass build_ext to get clearer report if Cython is necessary.
    """

    def _check_cython_extensions(self, extensions):
        for ext in extensions:
            for src in ext.sources:
                if not os.path.exists(src):
                    print("%s: -> [%s]" % (ext.name, ext.sources))
                    raise Exception("Cython-generated file '%s' not found." % src)

    def build_extensions(self):
        self._check_cython_extensions(self.extensions)
        build_ext.build_extensions(self)


class CythonCommand(build_ext):
    """
    Custom distutils command subclassed from Cython.Distutils.build_ext
    to compile pyx->c, and stop there. All this does is override the
    C-compile method build_extension() with a no-op.
    """

    def build_extension(self, ext):
        pass


class DummyBuildSrc(Command):
    """numpy's build_src command interferes with Cython's build_ext."""

    user_options = []

    def initialize_options(self):
        self.py_modules_dict = {}

    def finalize_options(self):
        pass

    def run(self):
        pass


cmdclass.update({'build_ext': CheckingBuildExt, 'sdist': CheckSDist})

if _CYTHON_INSTALLED:
    suffix = ".pyx"
    cmdclass["cython"] = CythonCommand
else:
    suffix = ".c"
    cmdclass["build_src"] = DummyBuildSrc


def maybe_cythonize(extensions, *args, **kwargs):
    if "clean" in sys.argv or "sdist" in sys.argv:
        # See https://github.com/cython/cython/issues/1495
        return extensions
    elif not _CYTHON_INSTALLED:
        if _CYTHON_VERSION:
            raise RuntimeError(
                "Cannot cythonize with old Cython version (%s "
                "installed, needs %s)" % (_CYTHON_VERSION, MIN_CYTHON_VER)
            )
        raise RuntimeError("Cannot cythonize without Cython installed.")

    # reuse any parallel arguments provided for compilation to cythonize
    parser = argparse.ArgumentParser()
    parser.add_argument("--parallel", "-j", type=int, default=1)
    parsed, _ = parser.parse_known_args()

    kwargs["nthreads"] = parsed.parallel
    return cythonize(extensions, *args, **kwargs)


include_dirs = []
if ccompiler.new_compiler().compiler_type == 'msvc' and msvccompiler.get_build_version() == 9:
    root = os.path.abspath(os.path.dirname(__file__))
    include_dirs.append(os.path.join(root, 'include', 'msvc9'))


ext_modules = []
for modname in ['fast_base62', 'ksuid']:
    ext_modules.append(Extension('cyksuid.' + modname.replace('/', '.'),
                                 ['cyksuid/' + modname + suffix],
                                 include_dirs=include_dirs))


def setup_package():
    cython_directives = {
        "linetrace": False,
        "language_level": 2,
        "embedsignature": True,
        "binding": True,
    }

    setup(
        name='cyksuid',
        version=VERSION,
        description='Cython implementation of ksuid',
        ext_modules=maybe_cythonize(ext_modules, compiler_directives=cython_directives),
        long_description=(open('README.rst').read() if os.path.exists('README.rst') else ''),
        url='https://github.com/timonwong/cyksuid',
        author='Timon Wong',
        author_email='timon86.wang@gmail.com',
        license='BSD',
        cmdclass=cmdclass,
        packages=['cyksuid'],
        package_data={
            'cyksuid': ['*.pyx', '*.pxd'],
        },
        keywords='ksuid',
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: BSD License',
            'Operating System :: OS Independent',
            'Programming Language :: Cython',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Topic :: Scientific/Engineering',
            'Topic :: Software Development',
            'Topic :: Software Development :: Libraries',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Topic :: Utilities',
        ],
        install_requires=[],
        zip_safe=False,
    )


if __name__ == "__main__":
    # Freeze to support parallel compilation when using spawn instead of fork
    multiprocessing.freeze_support()
    setup_package()
