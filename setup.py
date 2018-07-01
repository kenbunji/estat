# -*- coding:utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
import os

from setuptools import setup, find_packages

try:
    with open('README.rst') as f:
        readme = f.read()
except IOError:
    readme = ''


def _requires_from_file(filename):
    return open(filename).read().splitlines()


# version
here = os.path.dirname(os.path.abspath(__file__))
version = next((line.split('=')[1].strip().replace("'", '')
                for line in open(os.path.join(here,
                                              'estat',
                                              '__init__.py'))
                if line.startswith('__version__ = ')),
               '0.0.dev0')

setup(
    name="estat",
    version=version,
    url='https://github.com/bunjiken/estat',
    author='kenbunji',
    author_email='kenbunji@gmail.com',
    maintainer='kenbunji',
    maintainer_email='kenbunji@gmail.com',
    description='Download data from Japanese Government Statistics and save it as CSV format files',
    long_description=readme,
    # packages=find_packages(),
    install_requires=_requires_from_file('requirements.txt'),
    license="MIT",
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License'
    ],
    # packages=['estat'],
    packages=find_packages(),
    # py_modules = ['estat.download'],
    entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
      download = estat:download
    """
)
