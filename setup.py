#
# setup.py file for compiling HASH and installing hashpy
#
import os
import sys
from setuptools import setup, Extension
import numpy

# Function to get linker args for a virtual environment
def get_linker_args_for_virtualenv(virtualenv=None):
    """Return linker args relative to a virtual env"""
    np_inc = os.path.join('lib', 'python{}.{}'.format(*sys.version_info[:2]), 'site-packages', 'numpy', 'core', 'include')
    inc_dirs = [os.path.join(virtualenv, inc) for inc in ('include', np_inc)]
    lib_dirs = [os.path.join(virtualenv, 'lib')]
    return {'include_dirs': inc_dirs, 'library_dirs': lib_dirs}

# Define source files for the Fortran extension
srcdir = os.path.join('hashpy', 'src')
srcf = [
    'fmamp_subs.f', 'fmech_subs.f', 'uncert_subs.f', 'util_subs.f',
    'pol_subs.f', 'vel_subs.f', 'station_subs.f', 'vel_subs2.f',
    'station_subs_5char.f'
]
src_list = [os.path.join(srcdir, src) for src in srcf]
ext_args = {
    'sources': src_list,
    'include_dirs': [numpy.get_include()]
}

# Handle installation to Antelope Python if detected
if 'antelope' in sys.executable:
    python_folder = '/opt/antelope/python{}'.format('.'.join(map(str, sys.version_info[:3])))
    ANT_EXT_ARGS = get_linker_args_for_virtualenv(python_folder)
    ext_args.update(ANT_EXT_ARGS)

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
    'ext_modules': [Extension('hashpy.libhashpy', **ext_args)],
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
