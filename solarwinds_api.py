#!/usr/bin/env python
# coding: utf-8
""" This script is used for: 
    1. Get node information based on IP address in SoalrWinds 
    2. Unmanage node based on node ID
    3. Remanage node based on node ID
    Before run this script, make sure you can connect 
    your SolarWinds URL on port 17778 with HTTPS.
e.g. "https://<sw_url>:17778/SolarWinds/InformationService/v3/Json/Query"
"""

import requests
import json
import os
from datetime import datetime
from requests.auth import HTTPBasicAuth

# Get SolarWinds URL, username and password from system variables
sw_url = os.environ.get('SW_URL')
username = input('Enter your SolarWinds username: ')
password = getpass.getpass('Enter your password: ')


# Get node information based on IP address and return node status and node id
def get_node_info(ipaddress):
    query = "SELECT NodeID, Status FROM Orion.Nodes WHERE IPAddress = '{0}'".format(ipaddress)
    try:
        res = requests.get('https://{0}:17778/SolarWinds/InformationService/v3/Json/Query?query={1}'.format(sw_url, query), 
                           verify=False, auth=HTTPBasicAuth(username, password))
    except:
        print('Unable to get node information!')
    else:
        if res.status_code != 200:
            print('Unable to get node information!')
        else:
            data = json.loads(res.text)
            node_id = data.get("results")[0].get("NodeID")
            status = data.get("results")[0].get("Status")
            return (node_id, status)
    

# Unmanage node based on node id
def unmanage_node(node_id):
    now = datetime.utcnow().isoformat()
    data = ['N:'+str(node_id), now ,'9998-12-31T12:00:00.000Z', False]
    try:
        res = requests.post('https://{0}:17778/SolarWinds/InformationService/v3/Json/Invoke/Orion.Nodes/Unmanage'.format(sw_url), 
                            json=data, verify=False, auth=HTTPBasicAuth(username, password))
    except:
        print('Unmanage node failed, please try again!')
    else:
        if res.status_code != 200:
            print('Unmanage node failed, please try again!')
        else:
            print('Unmanage node successfully!')


# Remanage node based on noe ID
def remanage(node_id):
    data = ['N:'+str(node_id)]
    try:
        res = requests.post('https://{0}:17778/SolarWinds/InformationService/v3/Json/Invoke/Orion.Nodes/Remanage'.format(sw_url), 
                            json=data, verify=False, auth=HTTPBasicAuth(username, password))
    except:
        print('Remanage node failed, please try again!')
    else:
        if res.status_code != 200:
            print('Remanage node failed, please try again!')
        else:
            print('Remanage node successfully!')


node_info = get_node_info('10.10.10.10')
unmanage_node(node_info[0])
#remanage(node_info[0])




