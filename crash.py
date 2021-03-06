#!/usr/bin/env python
#coding: UTF-8
#
# Defines the crash class, representing a crash.
#
# Copyright (c) 2013 Samuel Groß
#

import re

class Crash:


    verbosity  = 1          # determines how much information will be returned by the __str__ method
    output_all = False      # if set to true the string representation of this crash will simply list all properties

    KERNEL   = 'KERNEL'
    USERLAND = 'USERLAND'

    SIGSEGV = 'SIGSEGV'
    SIGABRT = 'SIGABRT'
    SIGBUS  = 'SIGBUS'
    SIGTRAP = 'SIGTRAP'
    NULLPTR = 'NULLPTR'
    TIMEOUT = 'TIMEOUT'
    LOWMEM  = 'LOWMEM'
    KFAULT  = 'KFAULT'      # basically every kernel panic that's not a null pointer dereference

    REGION_KERNEL = "kernel base"


    def __init__(self):
        # initialize available fields, mainly as a reference
        self.id       = '-'         # crash id - 'Incident Identifier'
        self.domain   = '-'         # crash domain - kernel or userland
        self.arch     = '-'         # machine architecture
        self.os       = '-'         # operating system name
        self.device   = '-'         # device name
        self.fa       = '-'         # faulting address
        self.pc       = '-'         # address of the faulting instruction
        self.rpc      = '-'         # relative address of the faulting instruction
        self.kbase    = '-'         # kernel base address
        self.type     = '-'         # crash type, Null Pointer Dereference, SIGSEGV, ...
        self.process  = '-'         # faulting process
        self.region   = '-'         # name of the memory region in which the crash occurred
        self.filename = '-'         # name of the crash report file

    def is_complete(self):
        """Return true if this crash contains all needed information."""
        res = not (self.id == '-' or self.os == '-' or self.device == '-' or
                   self.filename == '-' or self.type == '-')
        if self.domain == self.KERNEL:
            res &= not self.kbase == '-'
        else:
            if not self.type == self.LOWMEM:
                res &= not self.process == '-'
        if not (self.type == self.TIMEOUT or self.type == self.LOWMEM or
                self.type == self.SIGABRT or self.type == self.SIGTRAP):
            # if pc == fa then the process tried to execute invalid memory
            # in this case no relative pc (and region) can be determined
            if not self.pc == self.fa:
                res &= not (self.region == '-' or self.fa == '-' or self.pc == '-' or self.rpc == '-')
            else:
                res &= not self.pc == '-'

        return res

    def __eq__(self, other):
        """Return true if the two crashes are equal.

        Two crashes are (very likely) equal if they occurred on the same
        offset from the same memory region.
        """
        return self.region == other.region and self.rpc == other.rpc and not self.region == '-' and not self.rpc == '-'

    def __str__(self):
        if self.output_all:
            str = ''
            for key, value in vars(self).items():
                if not key.startswith('_') and not key.isupper():
                    str += "%s: %s\n" % (key, value)
            return str

        if self.type == self.LOWMEM:
            return "%s - %s" % (self.domain, self.type)

        elif self.type == self.TIMEOUT:
            str = "%s - %s" % (self.domain, self.type)
            if self.domain == self.USERLAND:
                str += " in %s" % self.process
            if self.verbosity > 1:
                str += "\n    %s - %s" % (self.os, self.device)

        else:
            str = "%s - %s, type: %s, faulting address: %s" % (self.domain, self.arch,
                # if the crash type is a SIGTRAP (breakpoint) display address of BREAKPOINT (pc) as faulting address
                    self.type, self.fa if not self.type == self.SIGTRAP else self.pc)
            if self.verbosity > 1:
                if self.domain == self.USERLAND:
                    str += "\n    process: %s, " % self.process
                else:
                    str += "\n    "
                str += "pc: %s" % (self.pc)
                if not self.pc == self.fa:
                    str += ", offset %s from %s" % (self.rpc, self.region if not self.domain == self.KERNEL else self.kbase)
                str += "\n    %s - %s" % (self.os, self.device)

        if self.verbosity > 2:
            str += "\n    %s -- crash id: %s" % (self.filename, self.id)

        return str
