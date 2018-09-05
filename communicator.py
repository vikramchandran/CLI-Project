import os
import botocore
from cliparser.session import Session




class Communicator(Session):

    # Requirements for OS implemention to work:
    # 1. Have clamav installed
    # 2. run 'cp freshclam.conf.sample freshclam.conf' on command line ,
    # 3. run 'freshclam' and remove "example" from freshclam.conf

    # Requirements for clamd implementation to work:
    # 1. Everything in OS, but add '&& cp clamd.conf.sample clamd.conf' to step 2.
    # 2. Remove "example" from clamd.conf also
    # 3. Must change local socket section in clamd.conf to '/var/run/clamav/clamd.ctl'

    # Must also update very 7 days by running "freshclam" on CL to update virus database
    def runscan(self, file):
        # Install clamav
        # Create config file with removal, remove stuff, change location in config for location, run daemon, etc.
        # Link: https://gist.github.com/mendozao/3ea393b91f23a813650baab9964425b9
        # Must redirect logging messages to get updates
        os.system('clamscan {} -o --no-summary'.format(file))

    def dirupload(self, which, args, bucketname, key):
        s3client = Session.s3client
        def uploadDirectory():
            for root, dirs, files in os.walk(args['directory']):
                for file in files:
                    local_path = os.path.join(root, file)
                    relative_path = os.path.relpath(local_path, args['directory'])
                    s3_path = os.path.join(key, relative_path)
                    if file != '.DS_Store':
                        # runscan(local_path)
                        s3client.upload_file(local_path, bucketname, s3_path)
        if which == 'dirupload':
            filename = args['directory']
            self.runscan(filename)
            uploadDirectory()
            print("Directory was successfully uploaded!")
        return filename

    def removefile(self, which, args, username):
        s3res = self.s3res
        if which == 'remove':
            filename = '/' + args['rkey']
            s3res.Object('accolade-platform-ext-dev-partners-577121982548', 'Hashed/' + username + filename).delete()
            print("File was successfuly removed!")
        return filename


    def upload(self, which, args, username):
        if which == 'upload':
            filename = '/' + args['file'].split('/')[-1]
            if args['replace']:
                try:
                    self.s3res.Object('accolade-platform-ext-dev-partners-577121982548', 'Hashed/' + username + filename).load()
                    self.s3res.Object('accolade-platform-ext-dev-partners-577121982548',
                                 'Hashed/' + username + filename).delete()
                    self.runscan(args['file'])
                    self.s3client.upload_file(args['file'], 'accolade-platform-ext-dev-partners-577121982548',
                                         'Hashed/' + username + filename)
                    print("File was successfully replaced!")
                except botocore.exceptions.ClientError:
                    # For now pretending that accolade-platform-ext-dev-partners-577121982548 is makeup bucket
                    self.runscan(args['file'])
                    self.s3client.upload_file(args['file'], 'accolade-platform-ext-dev-partners-577121982548',
                                         'Hashed/' + username + filename)
                    print("File was successfully replaced!")
            else:
                self.runscan(args['file'])
                self.s3client.upload_file(args['file'], 'accolade-platform-ext-dev-partners-577121982548',
                                     'Hashed/' + username + filename)
                print("File was successfully uploaded!")
        return filename



    def interact(self, which, args, username):
        if which == 'remove':
            filename = self.removefile(which, args, username)
        if which == 'dirupload':
            filename = self.dirupload(which, args, 'accolade-platform-ext-dev-partners-577121982548',
                                        'Hashed/' + username)
        if which == 'upload':
            filename = self.upload(which, args, username)
        return filename