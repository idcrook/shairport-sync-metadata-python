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
 - [ ] event emitter on the parser, refactoring as appropriate
 - [ ] example app to display on character LCD
 - [ ] example app to display on graphical LCD
