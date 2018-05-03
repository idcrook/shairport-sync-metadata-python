# -*- coding: utf-8 -*-
"""Provides CoverArt image wrapper class.

It is intended as a sink for binary metadata for the "album art" picture that
is provided in stream metadata.
"""
import base64
from base64 import encodebytes
import logging

logger = logging.getLogger(__name__)


# adapted from https://github.com/luckydonald/shairport-decoder/blob/master/shairportdecoder/metadata.py
class CoverArt(object):
    def __init__(self, binary=None, mime=None, extension=None):
        self._binary = binary  # the actual file bytes
        self._base64 = None  # base64 encoding
        self._mime = mime  # e.g. "image/png"
        self._extension = extension  # e.g. "png"

    @property
    def base64(self):
        if self._base64:
            return self._base64
        if self._binary:
            self._base64 = encodebytes(self._binary)
            return self._base64
        else:
            return None

    @property
    def binary(self):
        if self._binary:
            return self._binary

    def _guessImageMime(self, magic):
        logger.debug(magic[:4])
        if magic.startswith(b'\xff\xd8'):
            return 'image/jpeg'
        elif magic.startswith(b'\x89PNG\r\n\x1a\r'):
            return 'image/png'
        else:
            return "image/jpg"

    @property
    def mime(self):
        if self._mime:
            return self._mime
        if self.binary:
            self._mime = self._guessImageMime(self.binary)
            return self._mime
        else:
            return None

    @property
    def extension(self):
        recognized_mime_types = {
            'image/jpeg': 'jpeg',
            'image/png': 'png',
            'image/jpg': 'jpg',
        }
        if self.mime in recognized_mime_types:
            self._extension = recognized_mime_types[self.mime]
        return self._extension

    def as_dict(self, base64=False):
        data_dict = {
            "mime": self.mime,
            "extension": self.extension,
        }
        if base64:
            data_dict["base64"] = self.base64
        return data_dict
