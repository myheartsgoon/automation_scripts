#!/bin/bash
#### This script is used to execute command on multiple Linux machines in parallel using root user. (Shell script method)
#### Note: you need to set SSH keygen on the Linux server beforehand to allow SSH login passwordless.

start_time=`date +%s`
[ -e /tmp/fd1 ] || mkfifo /tmp/fd1
exec 3<>/tmp/fd1
rm -rf /tmp/fd1
for ((i=1;i<=5;i++))
do
    echo >&3
done
while read line
do
    read -u3
    {
    host=`echo $line| awk '{print $1}'`
    ssh  root@$host 'uname -a'
    echo 'success,'$host
    echo >&3
    }&
done < host.txt
stop_time=`date +%s`
echo "time: `expr $stop_time - $start_time`"
exec 3<&-
exec 3>&-
