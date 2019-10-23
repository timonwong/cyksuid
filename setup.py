import os.path
import sys
from setuptools import setup, Extension
from distutils import ccompiler, msvccompiler


info = {}
filename = os.path.join('cyksuid', '__version__.py')
exec(compile(open(filename, "rb").read().replace(b'\r\n', b'\n'), filename, 'exec'), info)
VERSION = info['__version__']


try:
    from Cython.Build import cythonize
    has_cython = True
except ImportError:
    has_cython = False


is_dev = 'dev' in VERSION
use_cython = is_dev or '--cython' in sys.argv or '--with-cython' in sys.argv

if '--no-cython' in sys.argv:
    use_cython = False
    sys.argv.remove('--no-cython')
if '--without-cython' in sys.argv:
    use_cython = False
    sys.argv.remove('--without-cython')
if '--cython' in sys.argv:
    sys.argv.remove('--cython')
if '--with-cython' in sys.argv:
    sys.argv.remove('--with-cython')


if use_cython and not has_cython:
    if is_dev:
        raise RuntimeError('Cython required to build dev version of cyksuid.')
    print('WARNING: Cython not installed.  Building without Cython.')
    use_cython = False


if use_cython:
    suffix = '.pyx'
else:
    suffix = '.c'


include_dirs = []
if ccompiler.new_compiler().compiler_type == 'msvc' and msvccompiler.get_build_version() == 9:
    root = os.path.abspath(os.path.dirname(__file__))
    include_dirs.append(os.path.join(root, 'include', 'msvc9'))


ext_modules = []
for modname in ['fast_base62', 'ksuid']:
    ext_modules.append(Extension('cyksuid.' + modname.replace('/', '.'),
                                 ['cyksuid/' + modname + suffix],
                                 include_dirs=include_dirs))


if use_cython:
    try:
        from Cython.Compiler.Options import get_directive_defaults
        directive_defaults = get_directive_defaults()
    except ImportError:
        # for Cython < 0.25
        from Cython.Compiler.Options import directive_defaults
    directive_defaults['embedsignature'] = True
    directive_defaults['binding'] = True
    ext_modules = cythonize(ext_modules)


setup(
    name='cyksuid',
    version=VERSION,
    description='Cython implementation of ksuid',
    ext_modules=ext_modules,
    long_description=(open('README.rst').read() if os.path.exists('README.rst') else ''),
    url='https://github.com/timonwong/cyksuid',
    author='Timon Wong',
    author_email='timon86.wang@gmail.com',
    license='BSD',
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
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
    install_requires=[],
    zip_safe=False,
)
