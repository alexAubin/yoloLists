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
        assert isinstance(list_name, basestring)

        mlist = MailList.MailList(list_name, lock=0)

        return { "name": list_name,
                 "display_name": mlist.real_name,
                 "adversited": bool(mlist.advertised),
                 "web_url": mlist.web_page_url,
                 "description" : mlist.description,
                 "email": mlist.GetListEmail(),
                 "language": mlist.preferred_language
               }

    def lists(self, advertised=True):
        assert isinstance(advertised, bool)

        raw_list = Utils.list_names()
        raw_list.sort()

        output = [ self.list(name) for name in raw_list ]

        if advertised:
            output = [ l for l in output if l["adversited"] ]

        return output


    def subscribe(self, list_name, user_email, user_fullname=""):
        assert isinstance(list_name, basestring)
        assert isinstance(user_email, basestring)
        assert isinstance(user_fullname, basestring)

        # Validate list name
        known_list_names = [ l["name"] for l in self.lists() ]
        if list_name not in known_list_names:
            raise Exception("UnknownList")

        # Get the list
        the_list = self.list(list_name)

        # Validate email
        if user_email == the_list["email"]:
            raise Exception("SelfSubscribe")

        # Canonicalize full name
        user_fullname = Utils.canonstr(user_fullname)

        try:
            mlist = MailList.MailList(list_name, lock=1)
            mlist.AddMember(UserDesc(user_email, user_fullname))
            mlist.Save()
            return "OK"
        except Errors.MembershipIsBanned:
            raise Exception("MemberBanned")
        except Errors.MMBadEmailError:
            raise Exception("BadEmail")
        except Errors.MMHostileAddress:
            raise Exception("HostileEmail")
        except Errors.MMAlreadyAMember:
            return "AlreadyMember"
        except Errors.MMSubscribeNeedsConfirmation:
            return "NeedConfirmation"
        except Errors.MMNeedApproval:
            return "NeedApproval"
        except Exception as e:
            raise Exception("UnknownError")
        finally:
            mlist.Unlock()

def main():

    m = Mailman()

    print(m.lists())
    m.subscribe("mailman", "root@yolo.plop", "Root")



if __name__ == "__main__":
    main()
