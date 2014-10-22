#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
(C) Copyright [2014] Avery Rozar

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

         ...
    .:::|#:#|::::.
 .:::::|##|##|::::::.
 .::::|##|:|##|:::::.
  ::::|#|:::|#|:::::
  ::::|#|:::|#|:::::
  ::::|##|:|##|:::::
  ::::.|#|:|#|.:::::
  ::|####|::|####|::
  :|###|:|##|:|###|:
  |###|::|##|::|###|
  |#|::|##||##|::|#|
  |#|:|##|::|##|:|#|
  |#|##|::::::|##|#|
   |#|::::::::::|#|
    ::::::::::::::
      ::::::::::
       ::::::::
        ::::::
          ::
"""
__author__ = 'Avery Rozar'

import pexpect
from modules.cmds import *


def config_mode(user, host, passwd, en_passwd):
    ssh_newkey = 'Are you sure you want to continue connecting (yes/no)?'
    constr = 'ssh ' + user + '@' + host
    child = pexpect.spawn(constr)
    ret = child.expect([pexpect.TIMEOUT, ssh_newkey, '[P|p]assword:'])
    if ret == 0:
        print '[-] Error Connecting to ' + host
        return
    if ret == 1:
        child.sendline('yes')
        new_ret = child.expect([pexpect.TIMEOUT, '[P|p]assword:'])
        if new_ret == 0:
            print '[-] Could not accept new key from ' + host
            return
        if new_ret == 1:
            child.sendline(passwd)
            auth = child.expect(['.>', '.#'])
            if auth == 0:
                child.sendline('enable')
                child.sendline(en_passwd)
                enable = child.expect(['[P|p]assword:', '.#'])
                if enable == 0:
                    print 'enable password for ' + host + ' is incorrect'
                    return
                if enable == 1:
                    child.sendline(CONFT)
                    child.expect(['.#'])
                    return child
    child.sendline(passwd)
    auth = child.expect(['[P|p]assword:', '.>', '.#'])
    if auth == 0:
        print 'User password is incorrect'
        return
    if auth == 1:
        child.sendline('enable')
        child.sendline(en_passwd)
        enable = child.expect(['[P|p]assword:', '.#'])
        if enable == 0:
            print 'enable password for ' + host + ' is incorrect'
            return
        if enable == 1:
            child.sendline(CONFT)
            child.expect(['.#'])
            return child
    if auth == 2:
        child.sendline(CONFT)
        child.expect(['.#'])
        return child
    else:
        print 'Failed to log in to ' + host


def enable_mode(user, host, passwd, en_passwd):
    ssh_newkey = 'Are you sure you want to continue connecting (yes/no)?'
    constr = 'ssh ' + user + '@' + host
    child = pexpect.spawn(constr)
    ret = child.expect([pexpect.TIMEOUT, ssh_newkey, '[P|p]assword:'])
    if ret == 0:
        print '[-] Error Connecting to ' + host
        return
    if ret == 1:
        child.sendline('yes')
        new_ret = child.expect([pexpect.TIMEOUT, '[P|p]assword:'])
        if new_ret == 0:
            print '[-] Could not accept new key from ' + host
            return
        if new_ret == 1:
            child.sendline(passwd)
            auth = child.expect(['.>', '.#'])
            if auth == 0:
                child.sendline('enable')
                child.sendline(en_passwd)
                enable = child.expect(['[P|p]assword:', '.#'])
                if enable == 0:
                    print 'enable password for ' + host + ' is incorrect'
                    return
                if enable == 1:
                    child.sendline(CONFT)
                    child.expect(['.#'])
                    return child
    child.sendline(passwd)
    auth = child.expect(['[P|p]assword:', '.>', '.#'])
    if auth == 0:
        print 'User password is incorrect'
        return
    if auth == 1:
        child.sendline('enable')
        child.sendline(en_passwd)
        enable = child.expect(['[P|p]assword:', '.#'])
        if enable == 0:
            print 'enable password for ' + host + ' is incorrect'
            return
        if enable == 1:
            child.expect(['.#'])
            return child
    if auth == 2:
        child.expect(['.#'])
        return child
    else:
        print 'Failed to log in to ' + host