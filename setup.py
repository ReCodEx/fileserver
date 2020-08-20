#!/usr/bin/env python3

from setuptools import setup
from fileserver import __version__


setup(name='recodex-fileserver',
      version=__version__,
      description='Store and serve ReCodEx submissions and other files via HTTP',
      author='Jan Buchar',
      author_email='',
      url='https://github.com/ReCodEx/fileserver',
      license="MIT",
      keywords=['ReCodEx', 'files', 'HTTP'],
      classifiers=["Development Status :: 5 - Production/Stable",
                   "Intended Audience :: Developers",
                   "License :: OSI Approved :: MIT License",
                   'Operating System :: POSIX :: Linux',
                   "Programming Language :: Python",
                   "Programming Language :: Python :: 3",
                   "Programming Language :: Python :: 3.6",
                   "Programming Language :: Python :: 3.8"],
      packages=['fileserver'],
      setup_requires=['pytest-runner'],
      tests_require=['pytest', 'pytest-mock', 'pytest-flask'],
      entry_points={'console_scripts': ['recodex-fileserver = fileserver.py']}
      )
