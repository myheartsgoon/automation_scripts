#!/usr/bin/env python
"docstring: this is the script for fetching ec2 detailed list for all accounts"
# Script for fetching ec2 list for all accounts

from boto.ec2.connection import EC2Connection
from boto.sts import STSConnection
from boto.regioninfo import RegionInfo
from datetime import datetime as dt
import json
import datetime
import time
import sys
import csv
import os

ACCOUNT_JSON_PATH = "@option.awsAccountPath@"
REGION_NAME = "@option.Region@"
OUTPUT_FILE = "@option.OutputFile@"

def list_ec2_for_all_account(params_dict):
    account_list = []
    with open(params_dict['account_json_path'], 'rb') as f:
        for line in f:
            line = line.partition('#')[0]
            line = line.rstrip()
            if line:
                account_list.append(line)

    # Open Output File
    print params_dict['output_path']
    f = open(params_dict['output_path'], 'w')
    writer = csv.writer(f)
    writer.writerow(('customer account', 'region', 'instance id', 'instance name', 'instance private_ip', 'instance public_ip'))

    # Connect to EC2 in this region
    for account_no in account_list:
        for region in params_dict['regions'].split(','):
            print "Connecting to AWS account: " + account_no + " region: " + region
            # Create an STSConnection object that represents a live connection to AWS.
            sts_connection = STSConnection()


            try:
                # Call the assume_role method of the STSConnection object and pass the role
                # ARN and a role session name.
                assumedRoleObject = sts_connection.assume_role(
                    role_arn="arn:aws:iam::"+ account_no +":role/aws-admin",
                    role_session_name="AssumeRoleSession1"
                    )        

                from boto.ec2.connection import EC2Connection
                connection = EC2Connection(
                    aws_access_key_id=assumedRoleObject.credentials.access_key,
                    aws_secret_access_key=assumedRoleObject.credentials.secret_key,
                    security_token=assumedRoleObject.credentials.session_token,
                    region=RegionInfo(name=region,
                                      endpoint='ec2.' + region + '.amazonaws.com')
                    )        

                # Fetch EC2 list and write it to CSV
                reservations = connection.get_all_instances()
                for reservation in reservations:
                    for instance in reservation.instances:
                        instance_name = "No Name"
                        if 'Name' in instance.tags:
                            instance_name = instance.tags['Name']
                        print ("customer accout: %s region: %s instance id: %s instance name: %s instance private_ip: %s instance public_ip: %s" % (account_no, region, instance.id, instance_name, instance.private_ip_address, instance.ip_address))
                        writer.writerow((account_no, region, instance.id, instance_name, instance.private_ip_address, instance.ip_address))

            except:
                print ("Failed to connect to account %s" % (account_no))

    f.close()

def main():
    "main entrance"

    params_dict = {}
    params_dict['regions'] = REGION_NAME
    params_dict['account_json_path'] = ACCOUNT_JSON_PATH
    params_dict['output_path'] = OUTPUT_FILE

    list_ec2_for_all_account(params_dict)

if __name__ == '__main__':
    main()