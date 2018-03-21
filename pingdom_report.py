#!/usr/bin/env python
# coding: utf-8
"""
	This script is used to download PDF report for 
	certain Pingdom Uptime check from Pingdom.
"""

import requests
import datetime
import os


email = os.environ.get('pingdom_user')
password = os.environ.get('pingdom_password')
utc_now = datetime.datetime.utcnow()
delta = datetime.timedelta(days=1)      # The duration for check is 1 day, you can customize it.
start_time = utc_now - delta
pingdom_id = "2425848"   # The pindgom uptime check ID
report_url = "https://my.pingdom.com/data/report/uptime/{id}?from={start_time}&to={utc_now}".format(
			id=pingdom_id, start_time=start_time.isoformat(), utc_now=utc_now.isoformat())
login_url = "https://my.pingdom.com"
params ={"email": email, "password": password }

# Post login page in order to get cookies for subsequent request.
r = requests.post(login_url, data=params)
# Get report content
r = requests.get(report_url, cookies = r.cookies, stream=True)


# Download the report, and name the report with download date in it.
with open("report-{0}.pdf".format(utc_now.strftime('%Y-%m-%d')), "wb") as f:
    for block in r.iter_content(1024):
        f.write(block)

