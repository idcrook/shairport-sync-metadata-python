# -*- coding: utf-8 -*-

__author__ = '@idcrook'


from datetime import datetime, timedelta
import logging

from shairport_sync_metadata import VERSION

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
            "PICT" : ["picture", cls.pictHandler],
            "pcen" : ["pictureend",  cls.rtptime_handler],
            "pcst" : ["picturestart", cls.rtptime_handler],
            "mdst" : ["metadatastart", cls.rtptime_handler],
            "stal" : ["metadatastall", cls.string_handler],
            "mden" : ["metadataend", cls.rtptime_handler],
            "snua" : ["useragent", cls.string_handler],
            "snam" : ["appleclientname", cls.string_handler],
            "pbeg" : ["playbegin", cls.zero_byte_handler],
            "pend" : ["playend", cls.zero_byte_handler],
            "pfls" : ["playflush", cls.zero_byte_handler],
            "prsm" : ["playresume", cls.zero_byte_handler],
            "pffr" : ["playfirstframereceived", cls.zero_byte_handler],
            "pvol" : ["playvolume", cls.play_volume_handler],
            "daid" : ["dacpid", cls.intHandler],
            "acre" : ["activeremotetoken", cls.intHandler],
            "prgr" : ["playprogress", cls.progress_handler],
            "caps" : ["playstate", cls.one_byte_handler],
            "flsr" : ["flushtime", cls.rtptime_handler],

        # need better handlers
            "clip" : ["clientip", cls.string_handler], # (value b'10.0.1.144')
            "svip" : ["serverip", cls.string_handler], # (value b'10.0.1.62')
            "dapo" : ["remoteportnumber", cls.string_handler], # (value b'3689')

        # Core values
            "mikd" : ["itemkind", cls.one_byte_handler],
            "minm" : ["itemname", cls.string_handler],
            "mper" : ["persistentid", cls.eight_byte_handler],
            "miid" : ["itemid", cls.four_byte_handler],
            "asal" : ["songalbum", cls.string_handler],
            "asar" : ["songartist", cls.string_handler],
            "ascm" : ["songcomment", cls.string_handler],
            "asco" : ["songcompilation", cls.bool_handler],
            "asbr" : ["songbitrate", cls.two_byte_handler],
            "ascp" : ["songcomposer", cls.string_handler],
            "asda" : ["songdateadded", cls.date_handler],
            "aspl" : ["songdateplayed", cls.date_handler],
            "asdm" : ["songdatemodified", cls.date_handler],
            "asdc" : ["songdisccount", cls.two_byte_handler],
            "asdn" : ["songdiscnumber", cls.two_byte_handler],
            "aseq" : ["songeqpreset", cls.string_handler],
            "asgn" : ["songgenre", cls.string_handler],
            "asdt" : ["songdescription", cls.string_handler],
            "asrv" : ["songrelativevolume", cls.one_byte_handler],
            "assr" : ["songsamplerate", cls.four_byte_handler],
            "assz" : ["songsize", cls.four_byte_handler],
            "asst" : ["songstarttime", cls.four_byte_handler],
            "assp" : ["songstoptime", cls.four_byte_handler],
            "astm" : ["songtime", cls.four_byte_handler],
            "astc" : ["songtrackcount", cls.two_byte_handler],
            "astn" : ["songtracknumber", cls.two_byte_handler],
            "asur" : ["songuserrating", cls.one_byte_handler],
            "asyr" : ["songyear", cls.two_byte_handler],
            "asfm" : ["songformat", cls.string_handler],
            "asdb" : ["songdisabled", cls.bool_handler],
            "asdk" : ["songdatakind", cls.one_byte_handler],
            "asbt" : ["songbeatsperminute", cls.two_byte_handler],
            "agrp" : ["songgrouping", cls.string_handler],
            "ascd" : ["songcodectype", cls.string_handler],
            "ascs" : ["songcodecsubtype", cls.intHandler],
            "asct" : ["songcategory", cls.string_handler],
            "ascn" : ["songcontentdescription", cls.string_handler],
            "ascr" : ["songcontentrating", cls.intHandler],
            "asri" : ["singartistid", cls.intHandler],
            "asai" : ["songalbumid", cls.intHandler],
            "askd" : ["songlastskipdate", cls.date_handler],
            "assn" : ["songsortname", cls.string_handler],
            "assu" : ["songsortalbum", cls.string_handler],
            "aeNV" : ["itunesnormvolume", cls.intHandler],
            "aePC" : ["itunesispodcast", cls.bool_handler],
            "aeHV" : ["ituneshasvideo", cls.bool_handler],
            "aeMK" : ["itunesmediakind", cls.intHandler],
            "aeSN" : ["itunesseriesname", cls.string_handler],
            "aeEN" : ["itunesepisodenumber", cls.string_handler],

        # found more unknowns during testing
            "aeAI" : ["unknownaeAI", cls.string_handler],
            "aeCM" : ["unknownaeCM", cls.string_handler],
            "aeCR" : ["unknownaeCR", cls.string_handler],
            "aeCS" : ["unknownaeCS", cls.string_handler],
            "aeDL" : ["unknownaeDL", cls.string_handler],
            "aeDP" : ["unknownaeDP", cls.string_handler],
            "aeDR" : ["unknownaeDR", cls.string_handler],
            "aeDV" : ["unknownaeDV", cls.string_handler],
            "aeES" : ["unknownaeES", cls.string_handler],
            "aeFA" : ["unknownaeFA", cls.string_handler],
            "aeGD" : ["unknownaeGD", cls.string_handler],
            "aeGE" : ["unknownaeGE", cls.string_handler],
            "aeGH" : ["unknownaeGH", cls.string_handler],
            "aeGR" : ["unknownaeGR", cls.string_handler],
            "aeGU" : ["unknownaeGU", cls.string_handler],
            "aeGs" : ["unknownaeGs", cls.string_handler],
            "aeHD" : ["unknownaeHD", cls.string_handler],
            "aeK1" : ["unknownaeK1", cls.string_handler],
            "aeK2" : ["unknownaeK2", cls.string_handler],
            "aeMX" : ["unknownaeMX", cls.string_handler],
            "aeMk" : ["unknownaeMk", cls.string_handler],
            "aeND" : ["unknownaeND", cls.string_handler],
            "aePI" : ["unknownaePI", cls.string_handler],
            "aeSE" : ["unknownaeSE", cls.string_handler],
            "aeSI" : ["unknownaeSI", cls.eight_byte_handler],
            "aeSU" : ["unknownaeSU", cls.string_handler],
            "aeXD" : ["unknownaeXD", cls.string_handler],
            "aels" : ["unknownaels", cls.string_handler],
            "ajAE" : ["unknownajAE", cls.string_handler],
            "ajAS" : ["unknownajAS", cls.string_handler],
            "ajAT" : ["unknownajAT", cls.string_handler],
            "ajAV" : ["unknownajAV", cls.string_handler],
            "ajal" : ["unknownajal", cls.string_handler],
            "ajcA" : ["unknownajcA", cls.string_handler],
            "ajuw" : ["unknownajuw", cls.string_handler],
            "amvc" : ["unknownamvc", cls.string_handler],
            "amvm" : ["unknownamvm", cls.string_handler],
            "amvn" : ["unknownamvn", cls.string_handler],
            "asaa" : ["unknownasaa", cls.string_handler],
            "asac" : ["unknownasac", cls.string_handler],
            "asas" : ["unknownasas", cls.string_handler],
            "asbk" : ["unknownasbk", cls.string_handler],
            "asdr" : ["unknownasdr", cls.four_byte_handler],
            "ased" : ["unknownased", cls.string_handler],
            "ases" : ["unknownases", cls.string_handler],
            "asgp" : ["unknownasgp", cls.string_handler],
            "ashp" : ["unknownashp", cls.string_handler],
            "askp" : ["unknownaskp", cls.string_handler],
            "aslr" : ["unknownaslr", cls.string_handler],
            "asls" : ["unknownasls", cls.string_handler],
            "aspc" : ["unknownaspc", cls.string_handler],
            "aspu" : ["unknownaspu", cls.string_handler],
            "asrs" : ["unknownasrs", cls.string_handler],
            "assa" : ["unknownassa", cls.string_handler],
            "assc" : ["unknownassc", cls.string_handler],
            "assl" : ["unknownassl", cls.string_handler],
            "asss" : ["unknownasss", cls.string_handler],
            "awrk" : ["unknownawrk", cls.string_handler],

            "mext" : ["unknownmext", cls.string_handler],
            "meia" : ["unknownmeia", cls.string_handler],
            "meip" : ["unknownmeip", cls.string_handler]
        }
        return MetadataDecoder.__instance

    def ParseItem(self, typ, code, rawItem):
        assert isinstance(rawItem, (bytes, bytearray))

        type = typ
        rawData = rawItem
        # logger.debug("Looking up {}:{} {}".format(typ, code, rawData))
        try:
            fieldInfo = self.fieldList[code]
        except KeyError:
            print("Key not found: %s (value %s)" % (code, rawData))
            return

        data = fieldInfo[1](self, rawData)
        fieldName = fieldInfo[0]
        logger.debug("Setting %s : %s to %s" % (code, fieldName, data))

        item = {"type" : type, "code" : code, "name" : fieldName, "value" : data}
        return item

    def string_handler(self, rawData):
        try:
            return rawData.decode("utf-8")
        except UnicodeDecodeError:
            logger.debug('Unable to decode binary data {}'.format(rawData))
            return rawData

    def bool_handler(self, rawData):
        if (rawData[0]>0):
            return True
        else:
            return False

    def intHandler(self, rawData):
        return 0

    def pictHandler(self, rawData):
        return 0

    def zero_byte_handler(self, rawData):
        """Used for fields whose presence is the message"""
        return True

    def one_byte_handler(self, rawData):
        return int(rawData[0])

    def two_byte_handler(self, rawData):
        #stringed = rawData.decode("utf-8")
        return (rawData[0] << 8) + rawData[1]

    def four_byte_handler(self, rawData):
        return (rawData[0] << 24) + (rawData[1] << 16) + (rawData[2] << 8) + rawData[3]

    def eight_byte_handler(self, rawData):
        return (rawData[0] << 56) + (rawData[1] << 48) + (rawData[2] << 40) + (rawData[3] << 32) +(rawData[4] << 24) + (rawData[5] << 16) + (rawData[6] << 8) + rawData[7]

    def date_handler(self, rawData):
        return datetime.now()

    # def time_handler(self, rawData):
    #     stringTime = rawData.decode("utf-8")
    #     logger.debug('time_handler: {}'.format(stringTime))
    #     try:
    #         # need this approach since .fromtimestamp is ValueError: timestamp out of range for platform time_t
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
        progress = {"start" : int(timeList[0]), "current" : int(timeList[1]), "end" : int(timeList[2])}
        logger.debug('progress: {}'.format(progress))
        return progress

    def play_volume_handler(self, rawData):
        return 9999999999
