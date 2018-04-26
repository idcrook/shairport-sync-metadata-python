# -*- coding: utf-8 -*-

__author__ = '@idcrook'

from os import path
there = path.abspath(path.dirname(path.dirname(__file__)))

# Adapted from https://packaging.python.org/guides/single-sourcing-package-version/
with open(path.join(there, 'VERSION')) as version_file:
    version = version_file.read().strip()

__version__ = version
VERSION = version
