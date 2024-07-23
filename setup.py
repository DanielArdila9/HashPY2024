import os
import sys
from setuptools import setup, Extension, Command
import numpy

class BuildLibhashpy(Command):
    description = 'Build Fortran library using Makefile'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.system('make -f hashpy/src/Makefile')

# Define source files for the Fortran extension
srcdir = os.path.join('hashpy', 'src')
srcf = [
    'fmamp_subs.f', 'fmech_subs.f', 'uncert_subs.f', 'util_subs.f',
    'pol_subs.f', 'vel_subs.f', 'station_subs.f', 'vel_subs2.f'
]
src_list = [os.path.join(srcdir, src) for src in srcf]

ext_args = {
    'sources': src_list,
    'include_dirs': [numpy.get_include()],
    'f2py_options': ['--quiet']
}

# Handle installation to Antelope Python if detected
if 'antelope' in sys.executable:
    python_folder = '/opt/antelope/python{}'.format('.'.join(map(str, sys.version_info[:3])))
    ANT_EXT_ARGS = get_linker_args_for_virtualenv(python_folder)
    ext_args.update(ANT_EXT_ARGS)

# Force usage of gfortran
os.environ['FORTRAN'] = 'gfortran'

# Setup arguments
s_args = {
    'name': 'HASHpy',
    'version': '0.6.0',
    'description': 'Routines for running HASH algorithms',
    'author': 'Mark Williams',
    'url': 'https://github.com/markcwill/hashpy',
    'packages': ['hashpy', 'hashpy.io', 'hashpy.plotting'],
    'package_data': {
        'hashpy': [
            'src/*.inc', 'src/Makefile', 'data/*', 'scripts/*', 'src/*.f'
        ]
    },
    'cmdclass': {'build_libhashpy': BuildLibhashpy},
    'ext_modules': [Extension('hashpy.libhashpy', **ext_args)],
    'scripts': ['hashpy/scripts/dbhash', 'hashpy/scripts/hash_driver2.py', 'hashpy/scripts/hash_utils.py']
}

# Additional setup for Antelope environment
if 'ANTELOPE' in os.environ:
    ant_bin = os.path.join(os.environ['ANTELOPE'], 'bin')
    ant_pf = os.path.join(os.environ['ANTELOPE'], 'data', 'pf')
    s_args['data_files'] = [
        (ant_bin, ['hashpy/scripts/dbhash']),
        (ant_pf, ['hashpy/data/dbhash.pf'])
    ]

# Execute setup
setup(**s_args)
