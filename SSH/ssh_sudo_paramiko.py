#!/usr/bin/env python
#-*- coding: utf-8 -*-
""" This script is used to execute command on multiple Linux machines in parallel using sudo user. (paramiko method) """

import paramiko
import threading



def ssh2(ip,username,passwd,cmd):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip,22,username,passwd,timeout=5)

        for m in cmd:
            stdin, stdout, stderr = ssh.exec_command(m,  get_pty=True)
            stdin.write(passwd+'\n')
            for line in stdout:
                print line

        print '%s\tOK\n'%(ip)

        ssh.close()

    except Exception as e:

        print '%s\tError\t%s\n'%(ip, e)


if __name__=='__main__':
    cmd = ['sudo ls -ltr /var/log/']  # list of command you want to execute.
    username = "user1"  # sudo-to-root user
    passwd = "pa$sW0rd"    # password
    print "Begin......"

    ip_list = ['192.168.18.100', '192.168.18.101']  # you can add ip into this list, or you can read from files.
    for ip in ip_list:
        a=threading.Thread(target=ssh2,args=(ip,username,passwd,cmd))         # use threading.Thread method to run job in parallel.
        a.start()
