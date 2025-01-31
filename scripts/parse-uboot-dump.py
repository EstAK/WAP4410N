#!/usr/bin/env python3
"""
Author : Matt Brown 
Source : https://github.com/nmatt0/firmwaretools/blob/master/parse-uboot-dump.py
"""
import re
import sys

infile = sys.argv[1]
outfile = sys.argv[2]

i = open(infile,"r")
o = open(outfile,"wb")

for line in i.readlines():
    line = line.strip()
    if re.match(r'^[0-9a-f]{8}:',line):
        line = line.split(":")
        if len(line) == 2:
            line = line[1]
            line = line.replace(" ","")[:32]
            data = bytes.fromhex(line)
            o.write(data)
