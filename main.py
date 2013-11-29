#!/usr/bin/env python
#coding: UTF-8
#
# Copyright (c) 2013 Samuel Groß
#

from crash import Crash
from analyzer import CrashAnalyzer
import argparse
import os


parser = argparse.ArgumentParser(prog='iCrashalyzer', description='Analyze iOS crash reports.')
parser.add_argument('f', nargs='+', metavar='file', help='file(s) to analyze')
parser.add_argument('-o', '--output', metavar='file', help='write the result to a file instead of stdout')
parser.add_argument('-u', '--unique', action='store_true', help='only output unique crashes')
parser.add_argument('-v', '--verbose', action='count', help='increases the verbosity level')
args = parser.parse_args()


analyzer = CrashAnalyzer()
crashes  = []
curr     = 1
for entry in args.f:
    if os.path.isfile(entry):
        with open(entry, 'r') as file:
            print("[*] processing file %i of %i" % (curr, len(args.f)))
            curr += 1
            crashes.append(analyzer.process(file))

if args.unique:
    unique_crashes = []
    for crash in crashes:
        if not crash in unique_crashes:
            unique_crashes.append(crash)
        else:
            print("[*] %s is (likely) a duplicate of %s" % (crash.id, unique_crashes[unique_crashes.index(crash)].id))

    crashes = unique_crashes

if args.verbose:
    Crash.verbosity += args.verbose

out = None
if args.output:
    out = open(args.output, 'w+')

for crash in crashes:
    if out:
        out.write(str(crash))
    else:
        print('\n' + str(crash))

if out:
    out.close()
