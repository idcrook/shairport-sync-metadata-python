# -*- coding: utf-8 -*-
"""A python-based shairport-sync metadata parser/processor."""

__author__ = 'David Crook'
__copyright__ = 'Copyright 2018'
__credits__ = 'shairport-sync'
__license__ = 'MIT'
__maintainer__ = 'David Crook'
__email__ = 'idcrook@users.noreply.github.com'

import logging
from os import path
there = path.abspath(path.dirname(path.dirname(__file__)))

# Adapted from https://packaging.python.org/guides/single-sourcing-package-version/
with open(path.join(there, 'VERSION')) as version_file:
    __version__ = version_file.read().strip()
VERSION = __version__

logger = logging.getLogger(__name__)
#logger.info('version={}'.format(VERSION))

# clean up namespace
del (there, version_file, logger)
