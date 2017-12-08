#!/usr/bin/env python3
from glob import glob
from setuptools import setup, find_packages

# https://blog.ionelmc.ro/2014/05/25/python-packaging/#the-structure
setup(
    name='blameandshame',
    version='0.0.1',
    description='TBA',
    long_description='TBA',
    author='Chris Timperley',
    author_email='christimperley@gmail.com',
    url='https://github.com/squaresLab/blameandshame',
    license='mit',
    install_requires=[
        'GitPython',
        'tabulate',
        'scipy'
    ],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    entry_points = {
        'console_scripts': [ 'blameandshame = blameandshame.cli:main' ]
    },
    test_suite = 'tests'
)
