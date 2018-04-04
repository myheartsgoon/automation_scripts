#!/usr/bin/env python
""" This script is used for get all instances information from an AWS account
    Author: Shi, Weiwen
"""
from boto.sts import STSConnection
from boto.regioninfo import RegionInfo

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

def list_instances(account, mfa_token):
    try:
        sts_connection = STSConnection()

        assumedRoleObject = sts_connection.assume_role(
            role_arn="arn:aws:iam::" + str(account) + ":role/aws-admin",
            role_session_name="AssumeRoleSession1",
            mfa_serial_number='arn:aws:iam::111111111111:mfa/user',
            mfa_token=mfa_token
        )
        from boto.ec2.connection import EC2Connection
        connection = EC2Connection(
            aws_access_key_id=assumedRoleObject.credentials.access_key,
            aws_secret_access_key=assumedRoleObject.credentials.secret_key,
            security_token=assumedRoleObject.credentials.session_token,
            region=RegionInfo(name="us-east-1",
                              endpoint='ec2.' + 'us-east-1' + '.amazonaws.com')
        )
        reservation = connection.get_all_instances()
        print('{0}{1:<30} {2:^25} {3:^15} {4:^20} {5:>15}'.format(BOLD, 'Instance Name', 'Instance ID',
                                                                  'Instance Type', 'Instance Private IP',
                                                                  'Instance State', ENDC))
        for i in reservation:
            instance = i.instances[0]
            state = instance.state
            print('{0}{1:<30}{2} {3:^25} {4:^15} {5:^20} {6}{7:>15}{8}'.format(OKBLUE, instance.tags.get('Name'), ENDC,
                                                                               instance.id, instance.instance_type,
                                                                               instance.private_ip_address,
                                                                               OKGREEN if (state == 'running') else FAIL,
                                                                               state, ENDC))
    except Exception as e:
        print(e)

def main():
    """main entrance"""
    account = input("Please input the account number: ")
    mfa_token = input("Please input the MFA token: ")
    list_instances(account, mfa_token)

if __name__ == '__main__':
    main()

