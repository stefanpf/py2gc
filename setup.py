#!/usr/bin/env python

from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name='py2gc',
    version='1.0',
    description='Add events to a Google Calendar from the command line.',
    license="MIT",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Stefan Pfeuffer',
    author_email='mail@stefanpfeuffer.com',
    url="https://github.com/stefanpf/py2gc",
    packages=['py2gc'],
    install_requires=['httplib2', 'argparse', 'oauth2client', 'google-api-python-client'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
