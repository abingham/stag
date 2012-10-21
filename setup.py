import sys

import distribute_setup
distribute_setup.use_setuptools()

from setuptools import setup, find_packages

setup(
    name = 'stag',
    version = '0.1',
    packages = find_packages(),

    # metadata for upload to PyPI
    author = 'Austin Bingham',
    author_email = 'austin.bingham@gmail.com',
    description = 'A polyglot, extensible source code indexer.',
    license = 'MIT',
    keywords = 'source indexing',
    url = 'http://github.com/abingham/stag',

    entry_points = {
        'console_scripts': [
            'stag = stag.app:main',
            ],
        },

    install_requires=[
        'baker',
        'pykka',
    ],
)