# No lock needed in this script, because we don't change data.

import os
import cgi
import time

import sys
sys.path.append("/usr/lib/mailman/")

from Mailman import mm_cfg, Utils, MailList, Errors
from Mailman.UserDesc import UserDesc
from Mailman.htmlformat import *
from Mailman.Logging.Syslog import syslog



class Mailman():

    def __init__(self):

        pass

    def domain(self):
        return Utils.get_domain()


    def owner(self):
        return Utils.get_site_email()


    def list(self, list_name):

        assert isinstance(list_name, basestring);

        mlist = MailList.MailList(list_name, lock=0)

        return { "name": list_name,
                 "display_name": mlist.real_name,
                 "adversited": mlist.advertised,
                 "web_url": mlist.web_page_url,
                 "description" : mlist.description,
                 "email": mlist.GetListEmail(),
                 "language": mlist.preferred_language
               }

    def lists(self, advertised=True):

        raw_list = Utils.list_names()
        raw_list.sort()

        output = [ self.list(name) for name in raw_list ]

        if advertised:
            output = [ l for l in output if l["adversited"] ]

        return output


    def subscribe(self, list_name, user_email, user_fullname=None):

        assert isinstance(list_name, basestring);
        assert isinstance(user_email, basestring);
        assert user_fullname == None or isinstance(user_fullname, basestring);

        # Validate list name
        known_list_names = [ l["name"] for l in self.lists() ]
        if list_name not in known_list_names:
            raise AssertionError("List name should be a string")

        thelist = self.list(list_name)

        # Validate email
        if user_email == thelist["email"]:
            raise Exception("Sneaky hacker, you can't subscribe the list to itself ;) !")

        # Canonicalize full name
        user_fullname = Utils.canonstr(user_fullname)

        try:
            mlist = MailList.MailList(list_name, lock=1)
            mlist.AddMember(UserDesc(user_email, user_fullname))
            mlist.Save()
        except Errors.MembershipIsBanned:
            print("membership banned")
        except Errors.MMBadEmailError:
            print("bad email")
        except Errors.MMHostileAddress:
            print("hostile address")
        except Errors.MMSubscribeNeedsConfirmation:
            print("need confirm")
        except Errors.MMNeedApproval:
            print("need approval")
        except Errors.MMAlreadyAMember:
            print("already member")
        finally:
            mlist.Unlock()

        print("returning")


def main():

    m = Mailman()

    print(m.lists())
    m.subscribe("mailman", "root@yolo.plop", "Root")



if __name__ == "__main__":
    main()
