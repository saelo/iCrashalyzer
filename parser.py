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


    """ Userland regular expressions """
    urx = [
       re.compile('^Process:\s*(?P<process>.*) \[(?P<pid>[0-9]*)\]', re.MULTILINE),
       re.compile('^OS Version:\s*(?P<os>.*) \(.*\)', re.MULTILINE),
       re.compile('^Exception Type:\s*(.*) \((?P<type>.*)\)', re.MULTILINE),
       re.compile('^Exception Subtype:\s*(.*) at (?P<fa>.*)', re.MULTILINE)
          ]


    def _analyze_userland(self, crashlog):
        crash = Crash()
        crash.domain = Crash.USERLAND

        if '<key>' in crashlog:
            # xml file, extract description first
            regex = re.compile('.*<key>description</key>\s*<string>(?P<desc>.*?)</string>.*', re.DOTALL)
            match = regex.match(crashlog)
            if match:
                crashlog = match.group('desc')
            else:
                print("[!] failed to extract description from xml file, parsing might fail")
        
        for regex in self.urx:
            match = regex.search(crashlog)
            if match:
                # add attributes to crash object
                for key, value in match.groupdict().iteritems():
                    setattr(crash, key, value)

        return crash

    def _analyze_kernel(self, crashlog):
        crash = Crash()
        crash.domain = Crash.KERNEL
        return crash

    def analyze(self, crashlog):
        # determine if it's a userland or kernel crash
        if 'Kernel version' in crashlog:
            return self._analyze_kernel(crashlog)
        else:
            return self._analyze_userland(crashlog)

    def process(self, f):
        buf = f.read()
        crash = self.analyze(buf)
        crash.filename = f.name
        return crash
