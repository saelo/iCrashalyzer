#!/usr/bin/env python
#coding: UTF-8
#
# Analyzes crashes.
#
# Copyright (c) 2013 Samuel Groß
#

from crash import Crash

class CrashAnalyzer:

    
    NULLPTR_THRESHOLD = 0x1000

    def process(self, crash):
        # check for null pointer
        if int(crash.fa, 16) < self.NULLPTR_THRESHOLD:
            crash.type = Crash.NULLPTR

        # check architecture
        if len(crash.fa) <= 10:
            crash.arch = '32bit'
        else:
            crash.arch = '64bit'
