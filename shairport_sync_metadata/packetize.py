# -*- coding: utf-8 -*-
"""This is the packetize module.

It accesses metadata stream, parses it, and uses MetadataDecoder decoder to
process metadata information, through the Packetize function.
"""

import base64
import binascii
import logging
import math
import re
import sys

from shairport_sync_metadata import VERSION
from shairport_sync_metadata.decoder import MetadataDecoder

logger = logging.getLogger(__name__)
metadata_parser = MetadataDecoder()


def start_item(line):
    regex = r"<item><type>(([A-Fa-f0-9]{2}){4})</type><code>(([A-Fa-f0-9]{2}){4})</code><length>(\d*)</length>"
    matches = re.findall(regex, line)
    typ = str(binascii.unhexlify(matches[0][0]), 'ascii')
    code = str(binascii.unhexlify(matches[0][2]), 'ascii')
    length = int(matches[0][4])
    return (typ, code, length)


def start_data(line):
    # debug_line = 'line(start_data):{}'.format(line.rstrip()) ; logger.debug(debug_line)
    try:
        assert line == '<data encoding="base64">\n'
    except AssertionError:
        if line.startswith("<data"):
            return 0
        return -1
    return 0


def read_data(line, length):
    # debug_line = 'data_length={}, line:{}'.format(length, line.rstrip()) ; logger.debug(debug_line)

    # convert length to base64 character count
    b64size = 4 * math.ceil((length) / 3)
    try:
        data = base64.b64decode(line[:b64size])
    except TypeError:
        logger.error('TypeError on line(data_length={}): {}'.format(
            length, line))
    except UnicodeDecodeError:
        logger.error('UnicodeDecodeError on line(data_length={}): {}'.format(
            length, line))
        print(data)
        data = ""
    except binascii.Error:
        logger.error('binascii.Error on line(data_length={}): {}'.format(
            length, line))
        print(data)
        data = ""
    return data


def process_metadata(item):
    """Logs some designated interesting metadata"""
    if item["name"] == "songalbum":
        logger.info('Song Album : {}'.format(item["value"]))
    if item["name"] == "songartist":
        logger.info('Song Artist : {}'.format(item["value"]))
    if item["name"] == "itemname":
        logger.info('Item Name : {}'.format(item["value"]))
    if item["name"] == "songdatereleased":
        logger.info('Released : {}'.format(item["value"]))


def Packetize(fifo=None, packet_handlers=None):
    """Read from metadata FIFO and parse metadata.

    Keyword arguments:
    fifo -- the fifo that the metadata is being shared on.
    packet_handlers -- list of callbacks for designated metadata lifecycle
    markers.

    TODO
     - implement packet_handlers hooks.
    """
    with open(fifo, 'r') as fi:
        while True:
            line = fi.readline()
            if not line:  #EOF
                break
            sys.stdout.flush()
            if not line.startswith("<item>"):
                continue
            typ, code, length = start_item(line)

            data = b""
            if (length > 0):
                line2 = fi.readline()
                r = start_data(line2)
                if (r == -1):
                    continue
                line3 = fi.readline()
                data = read_data(line3, length)
                logger.debug('type={} code={} len={}'.format(
                    typ, code, length))
                if code != 'PICT':
                    # logger.debug('data={}'.format(data))
                    pass

            # check some required parameters
            if (typ != 'core' and typ != 'ssnc'):
                logger.error('Unknown type "{}"'.format(typ))

            # peek at some special codes
            if (typ == "ssnc" and code == "mdst"):
                logger.info('metadata START')
            if (typ == "ssnc" and code == "mden"):
                logger.info('metadata   END')

            # parse this metadata item
            item = metadata_parser.ParseItem(typ, code, data)
            if (item is None):
                logger.warning(
                    "Could not get valid metadata item for {}".format(data))
            else:
                process_metadata(item)
