import logging
import requests
import json
from cliparser.session import Session
import boto3

class Token(Session):
    def getacctoken(self):
        #logging.basicConfig(format='%(message)s', level=logging.INFO)

        token_url = "https://login-test3.myaccolade.com/token"

        logging.info('\n')


        client_id = 'etp-admin'
        client_secret = 'AJ8t1jknpgd2flqM2-JAs3cIi3EV3Y02jk_WPeMl1LfGRSbZyoIiXx50rCPYbfHKTNgXDTOaE0xCpMwZpexbmIY'

        data = {'grant_type': 'password', 'username': self.username, 'password': self.password}

        # May have to include if not working:verify=False,
        access_token_response = requests.post(token_url, data=data, allow_redirects=False, auth=(client_id, client_secret))

        logging.info("Lets now print the type of the access_token_response:")
        logging.info(type(access_token_response))
        logging.info('\n')
        logging.info("Here are the headers of the access_token_response:")
        logging.info(access_token_response.headers)
        logging.info('\n')
        logging.info("Now printing the type of the headers:")
        logging.info(type(access_token_response.headers))
        logging.info('\n')

        logging.info("Here are the text of the access_token_reponse:")
        logging.info(access_token_response.text)
        logging.info('\n')

        tokens = json.loads(access_token_response.text)
        logging.info("let's now print the type of the tokens:")
        logging.info(type(tokens))
        logging.info('\n')
        logging.info("I am now printing the access token: " + "\n" + tokens['access_token'])
        logging.info('\n')
        logging.info("I am now printing the id token: " + "\n" + tokens['id_token'])
        return tokens['id_token']

    def tradeoff(self, token):
        uh = self.hashfunc('UnitedHealth')
        at = self.hashfunc('Aetna')
        ks = self.hashfunc('Kaiser')
        ws = self.hashfunc('Wellpoint')

        jsonrestr = {
            "Id": "S3PolicyRestrictions",
            "Statement": [
                {
                    "Sid": "IPDeny",
                    "Effect": "Deny",
                    "Principal": {
                        "AWS": "*"
                    },
                    "Action": "s3:*",
                    "Resource": "*",
                    "Condition": {
                        "NotIpAddress": {
                            "aws:SourceIp": "72.309.38.2/32"
                            # "aws:SourceIp": ["72.309.38.2/32", "Insert more IP's here in list format"]

                        }
                    }
                },
                {
                    "Sid": "KeyAllow",
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": "s3:*",
                    "Resource": ["arn:aws:s3:::examplebucket/" + uh, "arn:aws:s3:::examplebucket/" + at,
                                 "arn:aws:s3:::examplebucket/" + ks,
                                 "arn:aws:s3:::examplebucket/" + ws],
                }
            ]
        }

        policyrestr = json.dumps(jsonrestr)
        client = boto3.client('sts')
        assumed_role_object = client.assume_role_with_web_identity(
            # RoleArn="arn:aws:iam::ACCOUNT-ID-WITHOUT-HYPHENS:role/ROLE-NAME",
            RoleArn="arn:aws:iam::vikramchandran:role/user-pegasus",
            RoleSessionName="practicesession", WebIdentityToken=token)

        accesskey = assumed_role_object['Credentials']['AccessKeyId']
        secretaccesskey = assumed_role_object['Credentials']['SecretAccessKey']
        sessiontoken = assumed_role_object['Credentials']['SessionToken']

        logging.info("Credentials are: " + "\n")
        logging.info("AccessKey Id: %s" % accesskey)
        logging.info("SecretAccessKey: %s" % secretaccesskey)
        logging.info("SessionToken: %s" % sessiontoken)

        session = boto3.Session(profile_name='test', aws_access_key_id=accesskey, aws_secret_access_key=secretaccesskey,
                                aws_session_token=sessiontoken, policy=policyrestr)
        return session

