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
    KFAULT  = 'KFAULT'      # basically every kernel panic that's not a null pointer dereference

    def __init__(self):
        # initialize available fields, mainly as a reference
        self.id       = '-'         # crash id - 'Incident Identifier'
        self.domain   = '-'         # crash domain - kernel or userland
        self.arch     = '-'         # machine architecture
        self.fa       = '-'         # faulting address
        self.pc       = '-'         # address of the faulting instruction
        self.kbase    = '-'         # kernel base address
        self.type     = '-'         # crash type, Null Pointer Dereference, SIGSEGV, ...
        self.process  = '-'         # faulting process
        self.filename = '-'         # name of the crash report file
        

    def __eq__(self, other):
        return False

    def __str__(self):
        return "%s - %s, type: %s, process: %s, faulting address: %s pc: %s -- %s id: %s" % (self.domain, self.arch, self.type, self.process, self.fa, self.pc, self.filename, self.id)
