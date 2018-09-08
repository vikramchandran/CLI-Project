import argparse
import logging
import time
import datetime
from cliparser.communicator import Communicator




class Parser(Communicator):

    def sendloggingrequest(self, url, action, filename, user):
        def logdata():
            timeatuse = time.time()
            formattedtime = datetime.datetime.fromtimestamp(timeatuse).strftime('%Y-%m-%d %H:%M:%S')
            loggingdata = {'user': user, 'date&time': formattedtime, 'filename': filename[1:],
                           'action': action}
            logging.info("I am now printing the log data: ")
            logging.info(loggingdata)
            logging.info('\n')
            return loggingdata
        logdata()
        #Uncomment the below line when the url endpoint is given by Carmen
        #return requests.post(url, data=logdata(action, filename, user), allow_redirects=False)


    def runparser(self):
        parser = argparse.ArgumentParser()
        subparser = parser.add_subparsers()

        accolade_group = subparser.add_parser('storage')
        accolade_subparser2 = accolade_group.add_subparsers()

        accolade_remove = accolade_subparser2.add_parser('remove')
        accolade_remove.set_defaults(which='remove')
        accolade_remove.add_argument('rkey', help="Name of the file to be removed")

        accolade_upload = accolade_subparser2.add_parser('upload')
        accolade_upload.set_defaults(which='upload')
        accolade_upload.add_argument('file', help="Name of the file that will be uploaded")
        accolade_upload.add_argument('--replace', help="Include on command line if replacing another file",
                                     action='store_true')

        accolade_dirupload = accolade_subparser2.add_parser('dirupload')
        accolade_dirupload.set_defaults(which='dirupload')
        accolade_dirupload.add_argument('directory', help="Absolute path to the directory that will be copied")
        args = vars(parser.parse_args())
        which = args['which']
        usercode = self.hashfunc(self.username)
        filename = self.interact(which, args, usercode)
        self.sendloggingrequest('input after request given', which, filename, self.username)
        # sendloggingrequest(filename, which, filename, user)

