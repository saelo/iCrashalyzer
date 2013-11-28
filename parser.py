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

    """ Shared regular expressions """
    srx = [
       re.compile('^Incident Identifier:\s*(?P<id>[0-9a-fA-F-]*)', re.MULTILINE),
       re.compile('^OS Version:\s*(?P<os>.*) \(.*\)', re.MULTILINE)
          ]

    """ Userland regular expressions """
    urx = [
       re.compile('^Process:\s*(?P<process>.*) \[(?P<pid>[0-9]*)\]', re.MULTILINE),
       re.compile('^Exception Type:\s*(.*) \((?P<type>.*)\)', re.MULTILINE),
       re.compile('^Exception Subtype:\s*(.*) at (?P<fa>.*)', re.MULTILINE),
       re.compile('^.*pc: (?P<pc>[0-9a-fA-Fx]*)', re.MULTILINE)
          ]

    """ Kernel regular expressions """
    krx = [
       re.compile('^.*far: (?P<fa>[0-9a-fA-Fx]*)', re.MULTILINE),
       re.compile('^.*pc: (?P<pc>[0-9a-fA-Fx]*)', re.MULTILINE),
       re.compile('^Kernel text base: (?P<kbase>[0-9a-fA-Fx]*)', re.MULTILINE)
          ]


    def analyze(self, crashlog):
        crash = Crash()

        if '<key>' in crashlog:
            # xml file, extract description first
            regex = re.compile('.*<key>description</key>\s*<string>(?P<desc>.*?)</string>.*', re.DOTALL)
            match = regex.match(crashlog)
            if match:
                crashlog = match.group('desc')
            else:
                print("[!] failed to extract description from xml file, parsing might fail")

        # determine if it's a userland or kernel crash
        if 'Kernel version' in crashlog:
            crash.domain = Crash.KERNEL
            crash.type = Crash.KFAULT       # set type to generic kernel fault
            rx = self.krx
        else:
            crash.domain = Crash.USERLAND
            rx = self.urx

        # extract relevant information
        for regex in rx + self.srx:
            match = regex.search(crashlog)
            if match:
                # add attributes to crash object
                for key, value in match.groupdict().iteritems():
                    setattr(crash, key, value)
            else:
                print("[!] failed to extract some information, please report this")

        return crash

    def process(self, f):
        buf = f.read()
        crash = self.analyze(buf)
        crash.filename = f.name
        return crash
