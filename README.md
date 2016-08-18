Cisco_SNMPv3 tool.
==================


This version has been tested with Mac OS 10.9.5 and Python 3.

The Cisco_SNMPv3 tool bulk edits ASAOS and IOS devices for SNMP v3, priv mode only.

Usage:

You have a few options.

To get help use the -h argument.

     python3 snmp_v3_tool.py -h

===================================


The minimum arguments are only --host or --host_file, you will be prompted for the other augments.

     python3 snmp_v3_tool.py --host_file=asa.hosts

==================================================


Use all arguments at once (Less secure, passwords will be loaded on the screen). You will need to use 'quotes' in arguments that include special characters and spaces.


     python3 snmp_v3_tool.py --host_file=asa.hosts
                             --username=USERNAME
                             --password='PASSWORD'
                             --enable='EN_PASSWORD'
                             --group=SNMPGROUP
                             --snmp_host=10.10.10.10
                             --snmp_user=SNMPMGR
                             --int_name=INSIDE
                             --snmp_v3_auth='SNMP_AUTH'
                             --snmp_v3_priv='SNMP_PRIV'
                             --snmp_v3_encr='aes 128'
                             --snmp_contact='Wile E. Coyote | wile.e.coyote@acme.com'

=====================================================================================


Use most arguments, you will be prompted for the other arguments.

     python3 snmp_v3_tool.py --host_file=asa.hosts
                             --username=USERNAME
                             --group=SNMPGROUP
                             --snmp_host=10.10.10.10
                             --snmp_user=SNMPMGR
                             --int_name=INSIDE
                             --snmp_v3_auth='SNMP_AUTH'
                             --snmp_v3_priv='SNMP_PRIV'
                             --snmp_v3_encr='aes 128'
                             --snmp_contact='Wile E. Coyote | wile.e.coyote@acme.com'

=====================================================================================
