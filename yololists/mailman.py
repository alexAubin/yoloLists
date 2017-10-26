# No lock needed in this script, because we don't change data.

import string
import os
import cgi
import time

import sys
sys.path.append("/usr/lib/mailman/")

from Mailman import mm_cfg, Utils, MailList, Errors
from Mailman.UserDesc import UserDesc
from Mailman.htmlformat import *
from Mailman.Logging.Syslog import syslog

# Arrange option types in a nice integer-indexed dict...
option_types_raw = ["Radio",
                    "Toggle",
                    "String",
                    "Email",
                    "Host",
                    "Number",
                    "Text",
                    "EmailList",
                    "EmailListEx",
                    "FileUpload",
                    "Select",
                    "Topics",
                    "HeaderFilter",
                    "Checkbox"]
option_types = {}

for option_type in option_types_raw:
    id_ = getattr(mm_cfg, option_type)
    option_types[id_] = option_type



class Mailman():

    def __init__(self):
        self._lists = Utils.list_names()
        self._lists.sort()


    def domain(self):
        return Utils.get_domain()


    def owner(self):
        return Utils.get_site_email()


    def _list(self, list_name):
        assert isinstance(list_name, basestring)
        assert list_name in self._lists

        return MailList.MailList(list_name, lock=0)

    def list(self, list_name):

        l = self._list(list_name)

        return { "name": list_name,
                 "display_name": l.real_name,
                 "adversited": bool(l.advertised),
                 "web_url": l.web_page_url,
                 "description" : l.description,
                 "email": l.GetListEmail(),
                 "language": l.preferred_language
               }

    def lists(self, advertised=True):
        assert isinstance(advertised, bool)

        output = [ self.list(name) for name in self._lists ]

        if advertised:
            output = [ l for l in output if l["adversited"] ]

        return output


    def subscribe(self, list_name, user_email, user_fullname=""):
        assert isinstance(list_name, basestring)
        assert isinstance(user_email, basestring)
        assert isinstance(user_fullname, basestring)

        # Validate list name
        if list_name not in self._lists:
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


    def admin_cagetories(self, list_name):

        return self._list(list_name).GetConfigCategories()


    def admin_category_view(self, list_name, category):

        l = self._list(list_name)

        category_view = l.GetConfigInfo(category, "")

        # Pop the title
        title = category_view[0]
        category_view = category_view[1:]

        # Init a clean directory to decribe the view
        category_view_clean = { "title": title, "subsubcats": []}

        # Find each subsubcategory title and add the options...
        i = -1
        for line in category_view:
            if isinstance(line, basestring):
                category_view_clean["subsubcats"].append({"title": line, "options": []})
                i = i+1
            else:
                # If this does not pass then meh, check admin.py in Mailman code
                # around line 660 :|
                assert hasattr(l, line[0])
                assert len(line) >= 5

                option = { "name": line[0],
                           "display_name": string.capwords(line[0].replace('_', ' ')),
                           "type": option_types[line[1]],
                           "params": line[2],
                           # This stuff is pretty useless ? Not clear in
                           # Mailman's code if it's even used...
                           #"dependencies": line[3],
                           "description": line[4],
                           "value" : getattr(l, line[0])
                         }
                option["display_name"] = option["display_name"].replace("Msg", "Message")
                if (option["type"] == "Radio" and len(option["params"]) == 2):
                    option["type"] = "Toggle"

                if (option["type"] == "Toggle" and isinstance(option["value"], bool)):
                    option["value"] = int(option["value"])

                option["extra_description"] = line[5] if len(line) >= 6 else None
                category_view_clean["subsubcats"][i]["options"].append(option)

        return category_view_clean


def main():

    m = Mailman()

    print(m.lists())
    m.subscribe("mailman", "root@yolo.plop", "Root")



if __name__ == "__main__":
    main()
