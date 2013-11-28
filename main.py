#!/usr/bin/env python
#coding: UTF-8
#
# Copyright (c) 2013 Samuel Groß
#

from parser import CrashParser
from analyzer import CrashAnalyzer
import argparse 


parser = argparse.ArgumentParser(prog='iCrashalyzer', description='Analyze iOS crash reports.')
parser.add_argument('f', nargs='+', metavar='file', help='file(s) to analyze')
parser.add_argument('-o', '--output', metavar='file', help='write the result to a file instead of stdout')
parser.add_argument('-u', '--unique', action='store_true', help='only output unique crashes')

args = parser.parse_args()

parser = CrashParser()
analyzer = CrashAnalyzer()
crashes = []
for entry in args.f:
    with open(entry, 'r') as file:
        crash = parser.process(file)
        analyzer.process(crash)
        crashes.append(crash)

if args.unique:
    raise NotImplementedError("coming soon")

out = None
if args.output:
    out = open(args.output, 'w+')

for crash in crashes:
    if out:
        out.write(str(crash))
    else:
        print(crash)

if out:
    out.close()
