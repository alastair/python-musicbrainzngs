#!/usr/bin/env python

from distutils.core import setup
from distutils.core import Command

from musicbrainzngs import musicbrainz

class test(Command):
    description = "run automated tests"
    user_options = [
        ("tests=", None, "list of tests to run (default all)"),
        ("verbosity=", "v", "verbosity"),
        ]

    def initialize_options(self):
        self.tests = []
        self.verbosity = 1

    def finalize_options(self):
        if self.tests:
            self.tests = self.tests.split(",")
        if self.verbosity:
            self.verbosity = int(self.verbosity)

    def run(self):
        import os.path
        import glob
        import sys
        import unittest

        build = self.get_finalized_command('build')
        self.run_command ('build')
        sys.path.insert(0, build.build_purelib)
        sys.path.insert(0, build.build_platlib)

        names = []
        for filename in glob.glob("test/test_*.py"):
            name = os.path.splitext(os.path.basename(filename))[0]
            if not self.tests or name in self.tests:
                names.append("test." + name)
        tests = unittest.defaultTestLoader.loadTestsFromNames(names)
        t = unittest.TextTestRunner(verbosity=self.verbosity)
        result = t.run(tests)
        sys.exit(not result.wasSuccessful())

setup(
    name="musicbrainzngs",
    version=musicbrainz._version,
    description="Python bindings for the MusicBrainz NGS and"
    " the Cover Art Archive webservices",
    author="Alastair Porter",
    author_email="alastair@porter.net.nz",
    url="https://python-musicbrainzngs.readthedocs.org/",
    packages=['musicbrainzngs'],
    cmdclass={'test': test },
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

