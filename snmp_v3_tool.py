#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# (C) Copyright [2014] Avery Rozar

__author__ = 'Avery Rozar'


from lib.cisco_mode import *
from lib.send_cmd import *
from lib.cmds import *
from getpass import getpass
from argparse import ArgumentParser, FileType
from os import system


def main():
    clear_screen()
    parser = ArgumentParser('--host --host_file --username --password --enable --group --snmp_user --snmp_host\
    --snmp_contact --int_name --snmp_v3_auth --snmp_v3_priv --snmp_v3_encr')
    parser.add_argument('--host', dest='host', type=str, help='specify a target host')
    parser.add_argument('--host_file', dest='hosts', type=FileType('r'), help='specify a target host file')
    parser.add_argument('--username', dest='user', type=str, help='specify a user name')
    parser.add_argument('--password', dest='passwd', type=str, help='specify a passwd')
    parser.add_argument('--enable', dest='en_passwd', type=str, help='specify an enable passwd')
    parser.add_argument('--group', dest='group', type=str, help='specify an snmp group')
    parser.add_argument('--snmp_user', dest='snmpuser', type=str, help='specify an snmp user')
    parser.add_argument('--snmp_host', dest='snmphost', type=str, help='specify an snmp server host')
    parser.add_argument('--snmp_contact', dest='snmpcontact', type=str, help='specify your snmp contact info')
    parser.add_argument('--int_name', dest='intname', type=str, help='specify interface name')
    parser.add_argument('--snmp_v3_auth', dest='snmpauth', type=str, help='specify the snmp user authentication')
    #parser.add_argument('--snmp_v3_hmac', dest='snmphmac', type=str, help='set snmp HMAC, md5 or sha')
    parser.add_argument('--snmp_v3_priv', dest='snmppriv', type=str, help='specify the snmp priv password')
    parser.add_argument('--snmp_v3_encr', dest='snmpencrypt', type=str, help='specify encryption, des, 3des, \
    or aes(128/192/256)')

    args = parser.parse_args()
    host = args.host
    hosts = args.hosts
    user = args.user
    passwd = args.passwd
    en_passwd = args.en_passwd
    group = args.group
    snmpuser = args.snmpuser
    snmphost = args.snmphost
    snmpcontact = args.snmpcontact
    intname = args.intname
    snmpauth = args.snmpauth
    snmppriv = args.snmppriv
    snmpencrypt = args.snmpencrypt

    if host is None and hosts is None:
        print('I need to know what host[s] to connect to')
        print(parser.usage)
        exit(0)

    if user is None:
        user = input('Enter your username: ')

    if passwd is None:
        passwd = getpass(prompt='User Password: ')

    if en_passwd is None:
        en_passwd = getpass(prompt='Enable Secret: ')

    if group is None:
        group = input('Enter your SNMP group: ')

    if snmpuser is None:
        snmpuser = input('Enter your SNMP user: ')

    if snmphost is None:
        snmphost = input('Enter your SNMP server address: ')

    if snmpcontact is None:
        snmpcontact = input('Who is your SNMP contact info: ')

    if intname is None:
        intname = input('If an ASA is being configured, enter the interface that it will use to connect to the SNMP'
                        ' server: ')

    if snmpauth is None:
        snmpauth = input('Enter the SNMP user auth string: ')

    if snmppriv is None:
        snmppriv = input('Enter the SNMP priv string: ')

    if snmpencrypt is None:
        snmpencrypt = input('Enter the type of encryption | des, 3des, or aes(128/192/256): ')

    if hosts:
        for line in hosts:
            host = line.rstrip()
            child = enable_mode(user, host, passwd, en_passwd)

            if child:
                child.sendline(SHOWVER)  # find out what Cisco OS we are working with
                what_os = child.expect([pexpect.TIMEOUT, '.IOS.', '.Adaptive.'])

                if what_os == 0:
                    print('show ver' + ' time out' + 'for ' + host)
                    return

                if what_os == 1:  # if it's an IOS device
                    child.sendcontrol('c')
                    child.expect(PRIV_EXEC_MODE)
                    child.sendline(IOSTERMLEN0)
                    child.expect(PRIV_EXEC_MODE)
                    child.sendline(CONFT)
                    child.expect(PRIV_EXEC_MODE)
                    send_command(child, SNMPGROUPCMD + group + V3PRIVCMD)
                    send_command(child, SNMPSRVUSRCMD + snmpuser + ' ' + group + V3AUTHCMD + SHAHMACCMD + snmpauth +
                                 PRIVCMD + snmpencrypt + ' ' + snmppriv)
                    send_command(child, SNMPSRVHOSTCMD + ' ' + snmphost + VERSION3CMD + PRIVCMD + snmpuser)
                    send_command(child, SNMPSRVCONTACTCMD + snmpcontact)
                    send_command(child, IOS_SNMPSRVENTRAPCMD)
                    send_command(child, ENDCMD)
                    send_command(child, WRME)
                    print('SNMPv3 has been configured on ' + host)
                    print('='*40)
                    print('\n'*2)
                    child.close()

                if what_os == 2:  # if it's an ASAOS device
                    child.sendline(QOUTMORE)
                    child.expect(PRIV_EXEC_MODE)
                    child.sendline(ASATERMPAGER0)
                    child.expect(PRIV_EXEC_MODE)
                    child.sendline(CONFT)
                    child.expect(PRIV_EXEC_MODE)
                    send_command(child, SNMPGROUPCMD + group + V3PRIVCMD)
                    send_command(child, SNMPSRVUSRCMD + snmpuser + ' ' + group + V3AUTHCMD + SHAHMACCMD + snmpauth +
                                 PRIVCMD + snmpencrypt + ' ' + snmppriv)
                    send_command(child, SNMPSRVHOSTCMD + intname + ' ' + snmphost + VERSION3CMD + snmpuser)
                    send_command(child, SNMPSRVCONTACTCMD + snmpcontact)
                    send_command(child, ASAOS_SNMPSRVENTRAPCMD)
                    send_command(child, WRME)
                    print('SNMPv3 has been configured on ' + host)
                    print('='*40)
                    print('\n'*2)
                    child.close()

    elif host:
        child = enable_mode(user, host, passwd, en_passwd)

        if child:
            child.sendline(SHOWVER)  # find out what Cisco OS we are working with
            what_os = child.expect([pexpect.TIMEOUT, '.IOS.', '.Adaptive.'])

            if what_os == 0:
                print('show ver' + ' time out' + 'for ' + host)
                return

            if what_os == 1:  # if it's an IOS device
                child.sendcontrol('c')
                child.expect(PRIV_EXEC_MODE)
                child.sendline(IOSTERMLEN0)
                child.expect(PRIV_EXEC_MODE)
                child.sendline(CONFT)
                child.expect(PRIV_EXEC_MODE)
                send_command(child, SNMPGROUPCMD + group + V3PRIVCMD)
                send_command(child, SNMPSRVUSRCMD + snmpuser + ' ' + group + V3AUTHCMD + SHAHMACCMD + snmpauth +
                             PRIVCMD + snmpencrypt + ' ' + snmppriv)
                send_command(child, SNMPSRVHOSTCMD + ' ' + snmphost + VERSION3CMD + PRIVCMD + snmpuser)
                send_command(child, SNMPSRVCONTACTCMD + snmpcontact)
                send_command(child, IOS_SNMPSRVENTRAPCMD)
                send_command(child, ENDCMD)
                send_command(child, WRME)
                print('SNMPv3 has been configured on ' + host)
                print('='*40)
                print('\n'*2)
                child.close()

            if what_os == 2:  # if it's an ASAOS device
                child.sendline(QOUTMORE)
                child.expect(PRIV_EXEC_MODE)
                child.sendline(ASATERMPAGER0)
                child.expect(PRIV_EXEC_MODE)
                child.sendline(CONFT)
                child.expect(PRIV_EXEC_MODE)
                send_command(child, SNMPGROUPCMD + group + V3PRIVCMD)
                send_command(child, SNMPSRVUSRCMD + snmpuser + ' ' + group + V3AUTHCMD + SHAHMACCMD + snmpauth +
                            PRIVCMD + snmpencrypt + ' ' + snmppriv)
                send_command(child, SNMPSRVHOSTCMD + intname + ' ' + snmphost + VERSION3CMD + snmpuser)
                send_command(child, SNMPSRVCONTACTCMD + snmpcontact)
                send_command(child, ASAOS_SNMPSRVENTRAPCMD)
                send_command(child, WRME)
                print('SNMPv3 has been configured on ' + host)
                print('='*40)
                print('\n'*2)
                child.close()


def clear_screen():
    system('clear')

if __name__ == '__main__':
  try:
    main()
  except (IOError, SystemExit):
    raise
  except KeyboardInterrupt:
    print('Crtl+C Pressed. Shutting down.')
