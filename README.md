# shairport-sync-metadata

Shairport-sync metadata reader and consumer

## Usage

**Command line output**

```
python3 ./bin/print_metadata.py -c /tmp/shairport-sync-metadata
```


## Installing

TBD: PyPi


## Developing

```
pip3 install -e .
cd bin/
# Assumes metadata pipe at /tmp/shairport-sync-metadata
python3 ./output_text.py
````

## TODO

 - [x] form python package structure
 - [x] metadata XML stream parser
 - [ ] metadata coverart wrapper class
 - [ ] event emitter on the parser, refactoring as appropriate
