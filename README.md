# shairport-sync-metadata

Shairport-sync metadata reader and consumer

 - Python3 only.
 - Tested on Raspberry Pi Model 1 B rev 2 with an add-on DAC.


## Usage

**Command line output**

```
python3 ./bin/print_metadata.py --cleanup /tmp/shairport-sync-metadata
```


## Installing


TBD: PyPi


## Developing

```
git clone https://github.com/idcrook/shairport-sync-metadata-python.git
cd shairport-sync-metadata-python
pip3 install -e .
cd bin/
# Assumes metadata pipe at /tmp/shairport-sync-metadata
cat /tmp/shairport-sync-metadata | python3 output_text.py
python3 ./bin/print_metadata.py --verbose /tmp/shairport-sync-metadata
```

## TODO

 - [x] ~form python package structure~
 - [x] ~metadata XML stream parser~
 - [x] ~metadata coverart wrapper class~
 - [x] ~ASCII art coverart demo~ (example in `output_text.py`)
 - [ ] event emitter on the parser, refactoring as appropriate
 - [ ] example app to display on character LCD
 - [ ] example app to display on graphical LCD


### Example `output_text.py` output

Command:
    `cat /tmp/shairport-sync-metadata | python3 bin/output_text.py`

Output:

```text
{"songalbum": "Galaxy Garden", "songartist": "Lone", "itemname": "As a Child (feat. Machinedrum)"}
image/jpeg
__main__    : INFO     Wrote file /tmp/shairport-sync-metadata-sluzr5o3/image_x0n4kmtd.jpeg
__main__    : DEBUG    loading image for ascii art
PIL.Image   : DEBUG    Error closing: 'NoneType' object has no attribute 'close'

;.  .;.         ..
A232Ar;. .       ..  ::.            .::.
3G&@&#H2r;        ..;:;r          .Ahhhhr
3#@@@@9hAr:.  ... .:r:Asr:        :3hHHH2
rh9@@@@HA;.   .:;rrrsAAsA;:        :s2Ar.
2G@@@9#Hs;;..::::;s23h3A;:.
###hhArr.;r..::sss3Hh3HhA;:.    .
2s;:.    ...::r3h323h2s32;.. :rrr.
.         .srAh2AssA2A3GGhs;.;rrA2s;.
         .r332;;A;rs32HGGhh2:;sAAAAr:.
        .r332A:A32AhHHhhHAsAsr;::..:::22;A:.
   .:;rsr;ssAAs33srsr2hA2ArAAAssss;;::2A.;.
     .;2; ;;2;:rrrA;s2hAA2AhHh32332A3.
:::::;r;;rAA;......:rAr232rAsssssrsh9; ..:..
ssrrrrrrrAAA:.;.:.:;:;r;;:::;;;;rrr22r;;;;;;
....r2;..;rr.:;;;:;;;::;:;;r;;;;;r;r;;:..:..
:;:;sr:::;;..:;::::rs::::;r;:;r;;rAsr:;sA;..
sssr;rssrrrr;rrsAr;rssrrr;;;..........:r;;::
sssrsAAsrrrrrrrrrrsrssss;r;:::.....::..;:;:r
sssrrrrsrrrrr;;;;;;rrrrsrssrr;;;;;;;...rrsss
;rrrrr;;r;r;r;;rrrrrrrrrrrrrrr;rrrsr;:::;::;
rrrrrr;;;rrrrr;rrrsssAsrrrsAsr;A2s::....:...
```
