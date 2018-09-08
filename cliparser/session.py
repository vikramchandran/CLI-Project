import boto3
import logging
import hashlib
from cliparser._version import __version__ as version
import pipdate
import getpass



class Session(object):
    session = boto3.Session(profile_name='test')
    s3res = session.resource('s3')
    s3client = session.client('s3')
    # logging.basicConfig(format='%(message)s', level=logging.INFO)
    username = input('Username: ')
    password = getpass.getpass('Passcode: ')



    def hashfunc(self, input):
        return hashlib.sha256('{}'.format(input).encode('utf-8')).hexdigest()

    def checkforupdate(self):
        update = pipdate.check('accoladecli', version)
        if update is not "":
            print('\n')
            print('This version of accoladecli is outdated. Re-install by typing "pip install accoladecli --upgrade" on command line!')
            print('\n')
