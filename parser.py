#!/usr/bin/env python
#coding: UTF-8
#
# Parses crash report files and constructs crash objects from them.
#
# Copyright (c) 2013 Samuel Groß
#

from crash import Crash
import re

class CrashParser:


    """ Available regular expressions """
    rx = {
            'id'      : re.compile('.*Incident Identifier:\s*(?P<id>[0-9a-fA-F-]*)', re.MULTILINE),
            'os'      : re.compile('^OS Version:\s*(?P<os>.*) \(.*\)', re.MULTILINE),
            'device'  : re.compile('^Hardware Model:\s*(?P<device>.*)', re.MULTILINE),
            'pc'      : re.compile('^.*pc: (?P<pc>[0-9a-fA-Fx]*)', re.MULTILINE),
            'process' : re.compile('^Process:\s*(?P<process>.*) \[(?P<pid>[0-9]*)\]', re.MULTILINE),
            'type'    : re.compile('^Exception Type:\s*(.*) \((?P<type>.*)\)', re.MULTILINE),
            'ufa'     : re.compile('^Exception (Subtype|Codes):\s*(.*) at (?P<fa>.*)', re.MULTILINE),
            'kbase'   : re.compile('^Kernel text base: (?P<kbase>[0-9a-fA-Fx]*)', re.MULTILINE),
            'kfa'     : re.compile('^.*far: (?P<fa>[0-9a-fA-Fx]*)', re.MULTILINE),
            'procto'  : re.compile('Reason:\s*(?P<process>\w*):', re.MULTILINE)             # process in timeout crashes
         }


    def extract(self, val, report, crash):
        """ Extract a value from the report and store it in the crash object """
        match = self.rx[val].search(report)
        if match:
            # add attributes to crash object
            for key, value in match.groupdict().items():
                setattr(crash, key, value)
        else:
            print('[!] failed to extract some information, please report this')

    def process(self, report):
        crash = Crash()

        # extract basic information
        self.extract('id', report, crash)
        self.extract('os', report, crash)
        self.extract('device', report, crash)

        if 'Largest process' in report:
            # crashed due to low memory
            crash.domain = Crash.USERLAND
            crash.type = Crash.LOWMEM
            return crash

        if 'iBoot version' in report:
            # kernel panic
            crash.domain = Crash.KERNEL
            if 'WDT timeout' in report:         # basic detection for panics caused by the watchdog timer
                crash.type = Crash.TIMEOUT
            else:
                crash.type = Crash.KFAULT
                self.extract('pc', report, crash)
                if int(crash.numeric_os()[0]) < 6:
                    # no KASLR before iOS 6
                    crash.kbase = '0x80002000'  # assume default base address
                else:
                    self.extract('kbase', report, crash)
                self.extract('kfa', report, crash)
        else:
            # userland crash
            crash.domain = Crash.USERLAND
            if 'RPCTimeout message received to terminate' in report:
                crash.type = Crash.TIMEOUT
                self.extract('procto', report, crash)
            else:
                self.extract('pc', report, crash)
                self.extract('process', report, crash)
                self.extract('type', report, crash)
                if crash.type == crash.SIGSEGV or crash.type == crash.SIGBUS:
                    self.extract('ufa', report, crash)

        return crash
