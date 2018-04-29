#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import base64
import binascii
import codecs
import json
import logging
import math
import os
import re
import shutil
import sys
import tempfile

from shairport_sync_metadata import reader
from shairport_sync_metadata import decoder
from shairport_sync_metadata.metadata import TrackInfo

# configure tempfile dir
name =  os.path.basename(__file__)
tempdirname = tempfile.mkdtemp(prefix='shairport-sync-metadata-', dir=tempfile.tempdir)

# set up logging to file
logging_filename = '{}.log'.format(os.path.join(tempdirname, os.path.basename(__file__)))
print('-I- Using log file {}'.format(logging_filename), file=sys.stderr)
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename=logging_filename,
                    filemode='w')
# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
# set a format which is simpler for console use
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('').addHandler(console)

logger = logging.getLogger(__name__)

logger.info('testing')

# started with code from
# https://github.com/surekap/MMM-ShairportMetadata/blob/master/shairport-metadata.py

def start_item(line):
    regex = r"<item><type>(([A-Fa-f0-9]{2}){4})</type><code>(([A-Fa-f0-9]{2}){4})</code><length>(\d*)</length>"
    matches = re.findall(regex, line)
    #print(matches)
    # python2 only # typ = matches[0][0].decode('hex')
    # python2 only # code = matches[0][2].decode('hex')
    #typ = codecs.decode(matches[0][0], 'hex').decode()
    #code = codecs.decode(matches[0][2], 'hex').decode()
    #typ = base64.b16decode(matches[0][0], casefold=True).decode()
    #code = base64.b16decode(matches[0][2], casefold=True).decode()
    typ = str(binascii.unhexlify(matches[0][0]), 'ascii')
    code = str(binascii.unhexlify(matches[0][2]), 'ascii')
    length = int(matches[0][4])
    return (typ, code, length)

def start_data(line):
    # logger.debug(line)
    try:
        assert line == '<data encoding="base64">\n'
    except AssertionError:
        if line.startswith("<data"):
            return 0
        return -1
    return 0

def read_data(line, length):
    # convert to base64 size
    b64size = 4*math.ceil((length)/3) ;
    #if length < 100: print (line, end="")
    try:
        data = base64.b64decode(line[:b64size])
        # Assume it is a PICT and do not attempt to decode the binary data
        if length > 1000:
            # print (data[:4])
            return data
        data = data.decode()
    except TypeError:
        data = ""
        pass
    except UnicodeDecodeError:
        print(data)
        data = ""
        pass
    return data

def guessImageMime(magic):
    # print(magic[:4])
    if magic.startswith(b'\xff\xd8'):
        return 'image/jpeg'
    elif magic.startswith(b'\x89PNG\r\n\x1a\r'):
        return 'image/png'
    else:
        return "image/jpg"

# cat /tmp/shairport-sync-metadata | /usr/bin/python3 ./output_text.py
if __name__ == "__main__":

    metadata = {}
    fi = sys.stdin
    while True:
        line = sys.stdin.readline()
        if not line:    #EOF
            break
        #print(line, end="")
        sys.stdout.flush()
        if not line.startswith("<item>"):
            continue
        typ, code, length = start_item(line)
        #print (typ, code, length)

        data = ""
        if (length > 0):
            line2 = fi.readline()
            #print('line2:{}'.format(line2), end="")
            r = start_data(line2)
            if (r == -1):
                continue
            line3 = fi.readline()
            #print('line3:{}'.format(line3), end="")
            data = read_data(line3, length)

        # Everything read
        if (typ == 'core'):
            #logger.debug(code)
            #logger.debug(data)

            if (code == "asal"):
                metadata['songalbum'] = data
                print(data)
            elif (code == "asar"):
                metadata['songartist'] = data
            #elif (code == "ascm"):
            #    metadata['Comment'] = data
            #elif (code == "asgn"):
            #    metadata['Genre'] = data
            elif (code == "minm"):
                metadata['itemname'] = data
            #elif (code == "ascp"):
            #    metadata['Composer'] = data
            #elif (code == "asdt"):
            #    metadata['File Kind'] = data
            #elif (code == "assn"):
            #    metadata['Sort as'] = data
            #elif (code == "clip"):
            #    metadata['IP'] = data

        if (typ == "ssnc" and code == "pfls"):
            metadata = {}
            print (json.dumps({}))
            sys.stdout.flush()
        if (typ == "ssnc" and code == "pend"):
            metadata = {}
            print (json.dumps({}))
            sys.stdout.flush()
        if (typ == "ssnc" and code == "PICT"):
            # print(typ, code, length, len(data))
            if (len(data) == 0):
                print (json.dumps({"image": ""}))
            else:
                mime = guessImageMime(data)
                print(mime)
                if (mime == 'image/png'):
                    temp_file = tempfile.NamedTemporaryFile(prefix="image_", suffix=".png", delete=False, dir=tempdirname)
                elif  (mime == 'image/jpeg'):
                    temp_file = tempfile.NamedTemporaryFile(prefix="image_", suffix=".jpeg", delete=False, dir=tempdirname)
                else:
                    temp_file = tempfile.NamedTemporaryFile(prefix="image_", suffix=".jpg", delete=False, dir=tempdirname)

                with temp_file as file:
                    file.write(data)
                    logger.info('Wrote file {}'.format(temp_file.name))

            sys.stdout.flush()

        if (typ == "ssnc" and code == "mden"):
            logger.debug('metadata end')
            print (json.dumps(metadata))
            sys.stdout.flush()
            metadata = {}

    # this never gets called in current code
    shutil.rmtree(tempdir)
