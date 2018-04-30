#!/usr/bin/perl

# cat itunes_specific_codes.raw | perl process_raw.pl > itunes_specific_codes.md

while (<>) {
    s/\| \|/|\n|/g;
    print ;
}
