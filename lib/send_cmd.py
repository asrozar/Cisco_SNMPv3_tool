#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# (C) Copyright [2014] Avery Rozar

__author__ = 'Avery Rozar'

from lib.prompts import *


def send_command(child, cmd):
    child.sendline(cmd)
    child.expect(PROMPT)
    #print(child.before)