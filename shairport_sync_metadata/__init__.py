# -*- coding: utf-8 -*-

__author__ = '@idcrook'

import logging
from os import path
there = path.abspath(path.dirname(path.dirname(__file__)))

# Adapted from https://packaging.python.org/guides/single-sourcing-package-version/
with open(path.join(there, 'VERSION')) as version_file:
    version = version_file.read().strip()
__version__ = version
VERSION = version
logger = logging.getLogger(__name__)

#logger.info('version={}'.format(VERSION))
