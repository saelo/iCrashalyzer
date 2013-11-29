#!/usr/bin/env python
#coding: UTF-8
#
# Analyzes crash reports.
#
# Copyright (c) 2013 Samuel Groß
#

from crash import Crash
from parser import CrashParser
import re

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

        # calculate relative address of faulting instruction
        if crash.domain == Crash.KERNEL:
            crash.region = Crash.REGION_KERNEL
            try:
                crash.rpc = '0x%x' % (int(crash.pc, 16) - int(crash.kbase, 16))
            except ValueError:
                pass
        else:
            try:
                # try to find memory region
                pc = int(crash.pc, 16)
                regex = re.compile('0x(?P<lower>[0-9a-fA-F]*) - 0x(?P<upper>[0-9a-fA-F]*) (?P<name>\w*)')
                results = regex.findall(report)
                for res in results:
                    lower, upper, name = res
                    if int(lower, 16) <= pc <= int(upper, 16):
                        # mapped region found
                        crash.rpc = '0x%x' % (pc - int(lower, 16))
                        crash.region = name
            except ValueError:
                pass

        return crash
