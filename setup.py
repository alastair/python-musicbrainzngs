#!/usr/bin/env python

from setuptools import setup

from musicbrainzngs import musicbrainz

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name="musicbrainzngs",
    version=musicbrainz._version,
    description="Python bindings for the MusicBrainz NGS and"
    " the Cover Art Archive webservices",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    author="Alastair Porter",
    author_email="alastair@porter.net.nz",
    url="https://python-musicbrainzngs.readthedocs.io/",
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
    packages=['musicbrainzngs'],
    install_requires=[
        'requests>=2.5.0'
    ],
    tests_require=[
        'requests-mock'
    ],
    license='BSD 2-clause',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: BSD License",
        "License :: OSI Approved :: ISC License (ISCL)",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Database :: Front-Ends",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ]
)
