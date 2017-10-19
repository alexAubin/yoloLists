# No lock needed in this script, because we don't change data.

import os
import cgi
import time

import sys
sys.path.append("/usr/lib/mailman/")

from Mailman import mm_cfg
from Mailman import Utils
from Mailman import MailList
from Mailman import Errors
from Mailman import i18n
from Mailman.htmlformat import *
from Mailman.Logging.Syslog import syslog

# Set up i18n
_ = i18n._
i18n.set_language(mm_cfg.DEFAULT_SERVER_LANGUAGE)


class Mailman():

    def __init__(self):

        pass

    def domain(self):
        return Utils.get_domain()


    def owner(self):
        return Utils.get_site_email()


    def list(self, listname):

        mlist = MailList.MailList(listname, lock=0)

        return { "name": mlist.real_name,
                 "adversited": mlist.advertised,
                 "web_url": mlist.web_page_url,
                 "description" : mlist.description
               }

    def lists(self, advertised=True):

        raw_list = Utils.list_names()
        raw_list.sort()

        output = [ self.list(name) for name in raw_list ]

        if advertised:
            output2 = [ l for l in output if l["adversited"] ]
            output = output2

        return output



def main():

    m = Mailman()

    print m.domain()
    print m.owner()
    print m.lists()



if __name__ == "__main__":
    main()
