#!/usr/bin/env python
#coding: UTF-8
#
# Wrapper for a report file. Provides methods to extract values from a report
# as well as categorize it.
#
# Copyright (c) 2013 Samuel Groß
#

import re

class Report:


    _rx = {
            'id'      : re.compile('.*Incident Identifier:\s*(?P<id>[0-9a-fA-F-]*)', re.MULTILINE),
            'os'      : re.compile('^OS Version:\s*(?P<os>.*) \(.*\)', re.MULTILINE),
            'device'  : re.compile('^Hardware Model:\s*(?P<device>.*)', re.MULTILINE),
            'pc'      : re.compile('^.*pc:\s*(?P<pc>[0-9a-fA-Fx]*)', re.MULTILINE),
            'process' : re.compile('^Process:\s*(?P<process>.*) \[(?P<pid>[0-9]*)\]', re.MULTILINE),
            'type'    : re.compile('^Exception Type:\s*(.*) \((?P<type>.*)\)', re.MULTILINE),
            'ufa'     : re.compile('^Exception (Subtype|Codes):\s*(.*) at (?P<fa>.*)', re.MULTILINE),
            'kbase'   : re.compile('^Kernel text base: (?P<kbase>[0-9a-fA-Fx]*)', re.MULTILINE),
            'kfa'     : re.compile('^.*far: (?P<fa>[0-9a-fA-Fx]*)', re.MULTILINE),
            'procto'  : re.compile('Reason:\s*(?P<process>[A-Za-z0-9\.]*)', re.MULTILINE)             # process in timeout crashes
         }

    def __init__(self, file):
        self._raw = file.read()
        self.filename = file.name

    def get_mappings(self):
        """Get the linked modules at the time of the crash.

        The mappings are returnes as a list of tripes: (start_addr, end_addr, name)
        """
        regex = re.compile('\s*0x(?P<lower>[0-9a-fA-F]*) - 0x(?P<upper>[0-9a-fA-F]*)\s*(?P<name>\w*)')
        return regex.findall(self._raw)

    def extract(self, val):
        """Extract a value from the report."""
        return self._rx[val].search(self._raw)

    def extract_all(self):
        """Extract as much information as possible.

        Returns a dictionairy containing the names and values of the extracted values.
        """
        res = {}
        for key, regex in self._rx.items():
            match = regex.search(self._raw)
            if match:
                res.update(match.groupdict())
        return res

    def is_usable(self):
        # detect unusable reports produced by some iPad models which just contain "CRC ERR"
        return not 'CRC ERR' in self._raw

    def is_kernel_crash(self):
        return 'panic' in self._raw

    def is_wdt_timeout(self):
        return 'WDT timeout' in self._raw

    def is_uland_timeout(self):
        return 'RPCTimeout message received to terminate' in self._raw or 'failed to resume in time' in self._raw

    def is_lowmem_crash(self):
        return 'Largest process' in self._raw
