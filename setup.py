#!/usr/bin/env python

from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name='too_short',
    version='1.1',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/elliott-ribner/tooshort',
    download_url="https://github.com/elliott-ribner/tooshort/releases/tag/1.1.tar.gz",
    license='MIT',
    description='Module to simplify supervised ml work with sklearn',
    packages=['too_short'],  # same as name # list folders, not files
    # external packages as dependencies
    install_requires=['sklearn', 'pandas', 'numpy',
                      'imbalanced-learn'],
)
