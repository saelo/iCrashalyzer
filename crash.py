#!/usr/bin/env python
#coding: UTF-8
#
# Defines the crash class, represents a crash.
#
# Copyright (c) 2013 Samuel Groß
#

class Crash:
    """ Crash domain """
    KERNEL   = 'KERNEL'
    USERLAND = 'USERLAND'

    """ Crash types """
    SIGSEGV = 'SIGSEGV'
    NULLPTR = 'NULLPTR'
    SIGABRT = 'SIGABRT'
    SIGBUS  = 'SIBBUS'

    def __init__(self):
        # initialize available fields to none for now, mainly as a reference
        self.domain   = None         # crash domain - kernel or userland
        self.arch     = None         # machine architecture
        self.fa       = None         # faulting address
        self.type     = None         # crash type, Null Pointer Dereference, SIGSEGV, ...
        self.process  = None         # faulting process
        self.filename = None         # name of the crash report file
        

    def __eq__(self, other):
        return False

    def __str__(self):
        return "%s - %sbit, type: %s, process: %s, faulting address: %s -- %s" % (self.domain, self.arch, self.type, self.process, self.fa, self.filename)
