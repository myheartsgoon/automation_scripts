#!/bin/bash
### Script to monitor configuration files ###

# Replace <Email address list> with your own email list
# Comma Seperate 'email1,email2,email3' 
MLIST="<Email address list>"
HOSTNAME=`hostname -s | tr [a-z] [A-Z]`

# This is the input file for script to read the conf file and its MD5 value.
# If you want to add a new conf file for monitoring, run command "md5sum /etc/XXX.conf >> /root/input" 
INPUT="/root/input"


# Monitor part, if MD5 value for conf file is not same as value in input file, send the alert mail.
while read line
do
	MD5=`echo $line | awk '{print $1}'`
	FN=`echo $line | awk '{print $2}'`
	if [ $MD5 != `md5sum $FN | awk '{print $1}'` ]
	then
		echo -e "$FN on ${HOSTNAME} is modified by someone, please check it ASAP."|mail -s "Alert: ${HOSTNAME} $FN is modified" ${MLIST}
	fi
done < $INPUT
