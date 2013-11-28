#!/usr/bin/env python
#coding: UTF-8
#
# Analyzes crash reports.
#
# Copyright (c) 2013 Samuel Groß
#

from crash import Crash
from parser import CrashParser

class CrashAnalyzer:

    
    NULLPTR_THRESHOLD = 0x1000

    parser = CrashParser()

    def process(self, file):
        report = file.read()
        crash = self.parser.process(report)
        crash.filename = file.name

        # check for null pointer dereference
        try:
            if int(crash.fa, 16) < self.NULLPTR_THRESHOLD:
                crash.type = Crash.NULLPTR
        except ValueError:
            pass

        # determine architecture
        if len(crash.fa) <= 10:
            crash.arch = '32bit'
        else:
            crash.arch = '64bit'

        return crash
