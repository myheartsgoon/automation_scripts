#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" This script is used to execute command on multiple Linux machines using root user. (pexpect method) """

import pexpect
import time

def ssh_cmd(ip, passwd, cmd):
    ret = -1
    ssh = pexpect.spawn('ssh root@%s "%s"' % (ip, cmd))
    try:
        i = ssh.expect(['password:', 'continue connecting (yes/no)?'], timeout=5)
        if i == 0 :
            ssh.sendline(passwd)
        elif i == 1:
            ssh.sendline('yes\n')
            ssh.expect('password: ')
            ssh.sendline(passwd)
        r = ssh.read()
        print r
        ret = 0
    except pexpect.EOF:
        print "EOF"
        ssh.close()
        ret = -1
    except pexpect.TIMEOUT:
        print "TIMEOUT"
        ssh.close()
        ret = -2
    return ret

if __name__ == '__main__':
    start = time.time()
    cmd = 'uname -a'  # list of command you want to execute.
    username = "root"
    passwd = "pa$sW0rd"    # root password
    ip_list = ['192.168.18.100', '192.168.18.101']  # you can add ip into this list, or you can read from files.
    for ip in ip_list:
        ssh_cmd(ip, passwd, cmd)

    stop = time.time()
    print 'Spent time: %s' % (stop-start)