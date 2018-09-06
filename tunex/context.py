#!/usr/bin/env python

import boto3


class Context:
    def __init__(self, awssecret, awstoken, awsregion):
        self.boto3 = boto3.client('ec2',
                                  aws_access_key_id=awstoken,
                                  aws_secret_access_key=awssecret,
                                  region=awsregion)
        self.clusterlist = []
        self.build_context()

    # Retrieve active clusters created by tunex in the past
    def build_context(self):
