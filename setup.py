#!/usr/bin/env python

from setuptools import setup, find_packages

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name='py2gc',
    version='1.0.5',
    description='Add events to a Google Calendar from the command line.',
    license="MIT",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Stefan Pfeuffer',
    author_email='mail@stefanpfeuffer.com',
    url="https://github.com/stefanpf/py2gc",
    packages=find_packages(),
    scripts=['bin/py2gc', 'bin/py2gc.cmd'],
    install_requires=['httplib2', 'argparse', 'oauth2client', 'google-api-python-client', 'pathlib'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
