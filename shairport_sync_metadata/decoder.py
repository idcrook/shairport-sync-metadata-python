# -*- coding: utf-8 -*-
"""This is the decoder module.

This module cantains MetadataDecoder class, which decodes metadata information
provided from shairport-sync. It assumes the metadata was encoded by an
AirPlay-style server (such as iTunes) or shairport-sync itself.
"""

from datetime import datetime, timedelta
import logging

from shairport_sync_metadata import VERSION
from shairport_sync_metadata.CoverArt import CoverArt

logger = logging.getLogger(__name__)


# Code adapted from
# https://github.com/brookstalley/live-mir/blob/master/metadataparser.py
# (MIT License)
class MetadataDecoder(object):
    __instance = None

    def __new__(cls):
        if MetadataDecoder.__instance is None:
            MetadataDecoder.__instance = object.__new__(cls)

        MetadataDecoder.__instance.fieldList = {
            # ssnc values
            "PICT": ["picture", cls.pictHandler],
            "pcen": ["pictureend", cls.rtptime_handler],
            "pcst": ["picturestart", cls.rtptime_handler],
            "mdst": ["metadatastart", cls.rtptime_handler],
            "stal": ["metadatastall", cls.string_handler],
            "mden": ["metadataend", cls.rtptime_handler],
            "snua": ["useragent", cls.string_handler],
            "snam": ["appleclientname", cls.string_handler],
            "pbeg": ["playbegin", cls.zero_byte_handler],
            "pend": ["playend", cls.zero_byte_handler],
            "pfls": ["playflush", cls.zero_byte_handler],
            "prsm": ["playresume", cls.zero_byte_handler],
            "pffr": ["playfirstframereceived", cls.zero_byte_handler],
            "pvol": ["playvolume", cls.play_volume_handler],
            "daid": ["dacpid", cls.intHandler],
            "acre": ["activeremotetoken", cls.string_handler],
            "prgr": ["playprogress", cls.progress_handler],
            "caps": ["playstate", cls.one_byte_handler],
            "flsr": ["flushtime", cls.rtptime_handler],

            # need better handlers
            "clip": ["clientip", cls.string_handler],  # (value b'10.0.1.144')
            "svip": ["serverip", cls.string_handler],  # (value b'10.0.1.62')
            "dapo": ["remoteportnumber",
                     cls.string_handler],  # (value b'3689')

            # Core values
            "mikd": ["itemkind", cls.one_byte_handler],
            "minm": ["itemname", cls.string_handler],
            "mper": ["persistentid", cls.eight_byte_handler],
            "miid": ["itemid", cls.four_byte_handler],
            "asal": ["songalbum", cls.string_handler],
            "asar": ["songartist", cls.string_handler],
            "ascm": ["songcomment", cls.string_handler],
            "asco": ["songcompilation", cls.bool_handler],
            "asbr": ["songbitrate", cls.two_byte_handler],
            "ascp": ["songcomposer", cls.string_handler],
            "asda": ["songdateadded",
                     cls.date_handler],  # often datetime.now()
            "aspl": ["songdateplayed", cls.date_handler],
            "asdm": ["songdatemodified", cls.date_handler],
            "asdc": ["songdisccount", cls.two_byte_handler],
            "asdn": ["songdiscnumber", cls.two_byte_handler],
            "aseq": ["songeqpreset", cls.string_handler],
            "asgn": ["songgenre", cls.string_handler],
            "asdt": ["songdescription", cls.string_handler],
            "asrv": ["songrelativevolume", cls.one_byte_handler],
            "assr": ["songsamplerate", cls.four_byte_handler],
            "assz": ["songsize", cls.four_byte_handler],
            "asst": ["songstarttime", cls.four_byte_handler],
            "assp": ["songstoptime", cls.four_byte_handler],
            "astm": ["songtime", cls.four_byte_handler],
            "astc": ["songtrackcount", cls.two_byte_handler],
            "astn": ["songtracknumber", cls.two_byte_handler],
            "asur": ["songuserrating", cls.one_byte_handler],
            "asyr": ["songyear", cls.two_byte_handler],
            "asfm": ["songformat", cls.string_handler],
            "asdb": ["songdisabled", cls.bool_handler],
            "asdk": ["songdatakind", cls.one_byte_handler],
            "asbt": ["songbeatsperminute", cls.two_byte_handler],
            "agrp": ["songgrouping", cls.string_handler],
            "ascd": ["songcodectype", cls.string_handler],
            "ascs": ["songcodecsubtype", cls.intHandler],
            "asct": ["songcategory", cls.string_handler],
            "ascn": ["songcontentdescription", cls.string_handler],
            "ascr": ["songcontentrating", cls.intHandler],
            "asri": ["songartistid", cls.eight_byte_handler],
            "asai": ["songalbumid", cls.intHandler],
            "askd": ["songlastskipdate", cls.date_handler],
            "assn": ["songsortname", cls.string_handler],
            "assu": ["songsortalbum", cls.string_handler],
            "asaa": ["songalbumartist", cls.string_handler],
            "asbk": ["bookmarkable", cls.bool_handler],
            "asbo": ["songbookmark", cls.four_byte_handler],
            "asdr": ["songdatereleased", cls.date_handler],
            "ased": ["songextradata", cls.two_byte_handler],
            "asgp": ["songgapless", cls.bool_handler],
            "ashp": ["songhasbeenplayed", cls.bool_handler],
            "asls": ["songlongsize", cls.eight_byte_handler],
            "aspu": ["songpodcasturl", cls.string_handler],
            "assa": ["sortartist", cls.string_handler],
            "assc": ["sortcomposer", cls.string_handler],
            "assl": ["sortalbumartist", cls.string_handler],
            "asss": ["sortseriesname", cls.string_handler],
            "aeNV": ["itunesnormvolume", cls.intHandler],
            "aePC": ["itunesispodcast", cls.bool_handler],
            "aeHV": ["ituneshasvideo", cls.bool_handler],
            "aeMK": ["itunesmediakind", cls.intHandler],
            "aeSN": ["itunesseriesname", cls.string_handler],
            "aeEN": ["itunesepisodenumberstring", cls.string_handler],
            "aeSU": ["itunesseasonnumber", cls.four_byte_handler],
            "aeES": ["itunesepisodesort", cls.four_byte_handler],
            "aeMk": ["itunesextendedmediakind", cls.four_byte_handler],
            "aeGD": ["itunesgaplessencdr", cls.four_byte_handler],
            "aeGE": ["itunesgaplessencdel", cls.four_byte_handler],
            "aeGH": ["itunesgaplessheur", cls.four_byte_handler],
            "aeGR": ["itunesgaplessresy", cls.eight_byte_handler],
            "aeGU": ["itunesgaplessdur", cls.eight_byte_handler],
            "aeHD": ["itunesishdvideo", cls.bool_handler],
            "aeSE": ["itunesstorepersid", cls.eight_byte_handler],
            "aeXD": ["itunesxid", cls.string_handler],
            "aeDR": ["itunesdrmuserid", cls.eight_byte_handler],
            "aeND": ["itunesnondrmuserid", cls.eight_byte_handler],
            "aeK1": ["itunesdrmkey1id", cls.eight_byte_handler],
            "aeK2": ["itunesdrmkey2id", cls.eight_byte_handler],
            "aeDV": ["itunesdrmversions", cls.four_byte_handler],
            "aeDP": ["itunesdrmplatformid", cls.four_byte_handler],
            "aeAI": ["itunesitmsartistid", cls.four_byte_handler],
            "aePI": ["itunesitmsplaylistid", cls.four_byte_handler],
            "aeCI": ["itunesitmscomposerid", cls.four_byte_handler],
            "aeGI": ["itunesitmsgenreid", cls.four_byte_handler],

            # found more unknowns during testing
            "aeCM": ["unknownaeCM", cls.default_string_handler],
            "aeCR": ["unknownaeCR", cls.default_string_handler],
            "aeCS": ["unknownaeCS", cls.default_string_handler],
            "aeDL": ["unknownaeDL", cls.default_string_handler],
            "aeFA": ["unknownaeFA", cls.default_string_handler],
            "aeGs": ["unknownaeGs", cls.default_string_handler],
            "aeMX": ["unknownaeMX", cls.default_string_handler],
            "aeSI": ["unknownaeSI", cls.eight_byte_handler],
            "aels": ["unknownaels", cls.default_string_handler],
            "ajAE": ["unknownajAE", cls.default_string_handler],
            "ajAS": ["unknownajAS", cls.default_string_handler],
            "ajAT": ["unknownajAT", cls.default_string_handler],
            "ajAV": ["unknownajAV", cls.default_string_handler],
            "ajal": ["unknownajal", cls.default_string_handler],
            "ajcA": ["unknownajcA", cls.default_string_handler],
            "ajuw": ["unknownajuw", cls.default_string_handler],
            "amvc": ["unknownamvc", cls.default_string_handler],
            "amvm": ["unknownamvm", cls.default_string_handler],
            "amvn": ["unknownamvn", cls.default_string_handler],
            "asac": ["unknownasac", cls.two_byte_handler],
            "asas": ["unknownasas", cls.default_string_handler],
            "ases": ["unknownases", cls.default_string_handler],
            "askp": ["unknownaskp", cls.default_string_handler],
            "aslr": ["unknownaslr", cls.default_string_handler],
            "aspc": ["unknownaspc", cls.default_string_handler],
            "asrs": ["unknownasrs", cls.default_string_handler],
            "awrk": ["unknownawrk", cls.default_string_handler],
            "mext": ["unknownmext", cls.two_byte_handler],
            "meia": ["unknownmeia", cls.four_byte_handler],
            "meip": ["unknownmeip", cls.four_byte_handler]
        }
        return MetadataDecoder.__instance

    def ParseItem(self, typ, code, rawItem):
        assert isinstance(rawItem, (bytes, bytearray))

        rawData = rawItem
        # logger.debug("Looking up {}:{} {}".format(typ, code, rawData))
        try:
            fieldInfo = self.fieldList[code]
        except KeyError:
            logger.warning('Key not found: {} (value {})'.format(
                code, rawData))
            return

        # override handler on mdst for 'core'
        if (typ == 'core' and code == 'mdst'):
            data = self.one_byte_handler(rawData)
        else:
            data = fieldInfo[1](self, rawData)
        fieldName = fieldInfo[0]
        logger.debug("Setting %s : %s to %s" % (code, fieldName, data))

        item = {"type": typ, "code": code, "name": fieldName, "value": data}
        return item

    def default_string_handler(self, rawData):
        if rawData == b'\x00':
            return 0
        elif rawData == b'\x00\x00':
            return 0
        elif rawData == b'\x00\x00\x00\x00':
            return 0
        elif rawData == b'\x00\x00\x00\x00\x00\x00\x00\x00':
            return 0

        return self.string_handler(rawData)

    def string_handler(self, rawData):
        try:
            return rawData.decode("utf-8")
        except UnicodeDecodeError:
            logger.warning('Unable to decode binary data {}'.format(rawData))
            return rawData

    def bool_handler(self, rawData):
        if (rawData[0] > 0):
            return True
        else:
            return False

    def intHandler(self, rawData):
        return 0

    def pictHandler(self, rawData):
        cover_art = CoverArt(binary=rawData)
        if cover_art.binary is not None:
            size = len(cover_art.binary)
        else:
            size = 0
        logger.debug('PICT {} size={}'.format(
            cover_art.as_dict(base64=False), size))
        return cover_art

    def zero_byte_handler(self, rawData):
        """Used for fields whose presence is the message"""
        return True

    def one_byte_handler(self, rawData):
        return int(rawData[0])

    def two_byte_handler(self, rawData):
        #stringed = rawData.decode("utf-8")
        return (rawData[0] << 8) + rawData[1]

    def four_byte_handler(self, rawData):
        return (rawData[0] << 24) + (rawData[1] << 16) + (
            rawData[2] << 8) + rawData[3]

    def eight_byte_handler(self, rawData):
        return (rawData[0] << 56) + (rawData[1] << 48) + (rawData[2] << 40) + (
            rawData[3] << 32) + (rawData[4] << 24) + (rawData[5] << 16) + (
                rawData[6] << 8) + rawData[7]

    # http://www.neotitans.com/resources/python/python-unsigned-32bit-value.html
    def to_int32_signed(self, x):
        if x > 0xFFFFFFFF:
            raise OverflowError

        if x > 0x7FFFFFFF:
            x = int(0x100000000 - x)
            if x < 2147483648:
                return -x
            else:
                return -2147483648
        return x

    def date_handler(self, rawData):
        intTime = self.four_byte_handler(rawData)
        intTime_signed = self.to_int32_signed(intTime)
        # an uninitialized value seems to be represented by
        # decimal intTime : 2212144096 intTime 32-bit signed : -2082823200
        # logger.debug('intTime : {} intTime 32-bit signed : {}'.format(intTime, intTime_signed))
        if (intTime_signed < 0):
            # intTime_31bit = int(bin(intTime_signed & 0x7fffffff), 2)
            timestamp = datetime(1970, 1,
                                 1) + timedelta(seconds=intTime_signed)
        else:
            timestamp = datetime(1970, 1,
                                 1) + timedelta(seconds=intTime_signed)
        # logger.debug(timestamp)
        return timestamp

    # def time_handler(self, rawData):
    #     stringTime = rawData.decode("utf-8")
    #     logger.debug('time_handler: {}'.format(stringTime))
    #     try:
    #         # need this approach since .fromtimestamp is ValueError: timestamp out of range for platform time    # https://stackoverflow.com/questions/36179914/timestamp-out-of-range-for-platform-localtime-gmtime-function
    # OverflowError: timestamp out of range for platform time_t
    #         timestamp = datetime(1970, 1, 1) + timedelta(seconds=int(stringTime)/100)
    #         logger.debug(timestamp)
    #         return timestamp
    #     except ValueError:
    #         logger.warning('ValueError for value {}'.format(rawData))
    #         return rawData

    def rtptime_handler(self, rawData):
        stringTime = rawData.decode("utf-8")
        logger.debug('rtptime_handler: {}'.format(stringTime))
        try:
            rtptime = int(stringTime)
            return rtptime
        except ValueError:
            logger.warning('ValueError for value {}'.format(rawData))
            return rawData

    def progress_handler(self, rawData):
        stringTimes = rawData.decode("utf-8")
        timeList = stringTimes.split("/")
        progress = {
            "start": int(timeList[0]),
            "current": int(timeList[1]),
            "end": int(timeList[2])
        }
        logger.debug('progress: {}'.format(progress))
        return progress

    def play_volume_handler(self, rawData):
        volumesString = rawData.decode("utf-8")
        volumesList = volumesString.split(",")
        volumes = {
            'airplay_volume': float(volumesList[0]),
            'volume': float(volumesList[1]),
            'lowest_volume': float(volumesList[2]),
            'highest_volume': float(volumesList[3]),
        }
        # logger.debug('volumes: {}'.format(volumes))
        return volumes
