#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" This script is used to execute command on multiple Linux machines in parallel using root user. (paramiko method) """

import paramiko
import threading
import time

def ssh2(ip,username,passwd,cmd):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip,22,username,passwd,timeout=5)
        
        for m in cmd:
            stdin, stdout, stderr = ssh.exec_command(m)
            out = stdout.readlines()
            for o in out:
                print o,
        print '%s\tOK\n'%(ip)
        ssh.close()
    except :
        print '%s\tError\n'%(ip)


if __name__=='__main__':
    cmd = ['uname -a', 'free -h']  # list of command you want to execute.
    username = "root"
    passwd = "pa$sW0rd"    # password
    ip_list = ['192.168.18.100', '192.168.18.101']  # you can add ip into this list, or you can read from files.

    print "Begin......"
    start = time.time()
    for ip in ip_list:
        a=threading.Thread(target=ssh2,args=(ip,username,passwd,cmd))
        a.start()

    stop = time.time()
    print 'Spent time: %s' % (stop - start)