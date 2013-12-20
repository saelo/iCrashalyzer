#!/usr/bin/env python
#coding: UTF-8
#
# Analyzes crash reports.
#
# Copyright (c) 2013 Samuel Groß
#

from crash import Crash
import re

class CrashAnalyzer:


    NULLPTR_THRESHOLD = 0x1000

    def analyze_report(self, report):
        """Analyze a report and return a crash object containing the information from it."""
        #
        # Extract information from the report and store it in a crash object.
        #
        crash = Crash()
        crash.filename = report.filename

        for key, value in report.extract_all().items():
            setattr(crash, key, value)

        # set additional properties
        if report.is_kernel_crash():
            crash.domain = Crash.KERNEL
            crash.type = Crash.KFAULT
            crash.region = Crash.REGION_KERNEL
            if crash.kbase == '-':
                # if the kernel base could not be extracted assume the default one
                # this will be the case for all crashes from devices before iOS 6
                # as there was no KASLR before that
                crash.kbase = '0x80002000'
        else:
            crash.domain = Crash.USERLAND
        if report.is_wdt_timeout() or report.is_uland_timeout():
            crash.type = Crash.TIMEOUT
        if report.is_lowmem_crash():
            crash.type = Crash.LOWMEM

        #
        # Analyze the crash further.
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
                mappings = report.get_mappings()
                pc = int(crash.pc, 16)
                for res in mappings:
                    lower, upper, name = res
                    if int(lower, 16) <= pc <= int(upper, 16):
                        # mapped region found
                        crash.rpc = '0x%x' % (pc - int(lower, 16))
                        crash.region = name
            except ValueError:
                pass

        # check if everything was extracted sucessfully
        # this is only done to detect changes in the crash report format
        if not crash.is_complete():
            print('[!] failed to extract some information, please report this')

        return crash
