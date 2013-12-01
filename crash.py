#!/usr/bin/env python
#coding: UTF-8
#
# Defines the crash class, represents a crash.
#
# Copyright (c) 2013 Samuel Groß
#

class Crash:


    """ Verbosity level - determines how much str(crash) spits out """
    verbosity = 1

    """ Crash domain """
    KERNEL   = 'KERNEL'
    USERLAND = 'USERLAND'

    """ Crash types """
    SIGSEGV = 'SIGSEGV'
    NULLPTR = 'NULLPTR'
    SIGABRT = 'SIGABRT'
    SIGBUS  = 'SIBBUS'
    TIMEOUT = 'TIMEOUT'
    KFAULT  = 'KFAULT'      # basically every kernel panic that's not a null pointer dereference

    """ Predefined memory regions """
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

    def __eq__(self, other):
        #
        # two crashes are (very likely) equal if they occurred on the same
        # offset from the same memory region
        #
        return self.region == other.region and self.rpc == other.rpc and not self.region == '-' and not self.rpc == '-'

    def __str__(self):
        if self.type == self.TIMEOUT:
            str = "%s - %s" % (self.domain, self.type)
            if self.domain == self.USERLAND:
                str += " in %s" % self.process
            if self.verbosity > 1:
                str += "\n    %s - %s" % (self.os, self.device)
        else:
            str = "%s - %s, type: %s, faulting address: %s" % (self.domain, self.arch, self.type, self.fa)
            if self.verbosity > 1:
                if self.domain == self.USERLAND:
                    str += "\n    process: %s, " % self.process
                else:
                    str += "\n    "
                str += "pc: %s, offset %s from %s" % (self.pc, self.rpc, self.region)
                str += "\n    %s - %s" % (self.os, self.device)

        if self.verbosity > 2:
            str += "\n    %s -- crash id: %s" % (self.filename, self.id)
        return str
