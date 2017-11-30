#!/usr/bin/env python3
from setuptools import setup

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
        'tabulate'
    ],
    packages=[
        'blameandshame'
    ],
    entry_points = {
        'console_scripts': [ 'blameandshame = blameandshame.cli:main' ]
    }
)
