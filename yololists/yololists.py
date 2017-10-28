
from flask import Flask, render_template, jsonify, request
from mailman import Mailman

app = Flask(__name__)


@app.route('/')
def index():
    data = { "lists": Mailman().lists() }

    return render_template("index.html", **data)


@app.route('/subscribe', methods=['POST'])
def subscribe():

    # Get the FORM data
    required_fields = [ "list-name", "email" ]
    if [ f for field in required_fields if field not in request.form ]:
        return jsonify({ "status": "NOTOK", "message": "Missing form data :/" })

    if request.form["antispam"] != "":
        return jsonify({ "status": "NOTOK", "message": "Sneaky spammer :|" })

    list_name = request.form["list-name"]
    email = request.form["email"]

    # Attempt to subscribe
    try:
        Mailman().subscribe(list_name, email)
    # Return messages depending on outcome
    except Exception as e_:
        e = str(e_)
        if e == "UnknownList":
            message = "Uh oh, the list you are attempting to subscribe to doesn't exist?"
        elif e == "SelfSubscribe":
            message = "Nice try, but you can't subscribe the list to itself ;)"
        elif e == "BadEmail":
            message = "Sorry, this does not look like a valid email address :/"
        elif e == "HostileEmail":
            message = "Sorry, this looks like an hostile email address and cannot be subscribed :/"
        elif e == "MemberBanned":
            message = "This email has been banned from subscribing to this list."
        else:
            message = "An unknown error happened. Sorry about that :(" + str(e)

        return jsonify({ "status": "NOTOK", "message": message})
    else:
        message = "Cool! Please check your inbox to proceed with the confirmation ;)."
        return jsonify({ "status": "OK", "message": message })


@app.route('/admin/')
@app.route('/admin/<category>/')
@app.route('/admin/<category>/<subcategory>/')
def admin(category="general", subcategory=None):

    list_name = "mailman"

    navbar = { "main":      [ ("general",    "General"   ),
                              ("members",    "Members"   ),
                              ("moderation", "Moderation"),
                              ("nondigest",  "Delivery"  ),
                              ("privacy",    "Privacy"   )
                            ],
               "advanced" : [ ("language",   "Languages" ),
                              ("archive",    "Archives"  ),
                              ("digest",     "Digests"   ),
                              ("passwords",  "Security"  ),
                              ("bouce",      "Boucing"   ),
                              ("autoreply",  "Auto-reply"),
                              ("topics",     "Topics"    )
                             ]
             }


    all_categories = Mailman().admin_cagetories(list_name)

    for c in all_categories:
        if c["name"] == category:
            this_category = c
            break

    assert category in [ c["name"] for c in all_categories ]

    this_category_view = Mailman().admin_category_view(list_name, category)
    this_category_view["name"]          = category
    this_category_view["display_title"] = this_category["display_name"]

    data = { "navbar": navbar,
             "categories": all_categories,
             "current_category": this_category_view }

    return render_template("admin.html", **data)


@app.route('/members/')
def members():

    list_name = "mailman"

    data = { "members" : Mailman().members(list_name)
           }

    return render_template("members.html", **data)


@app.route('/moderation/')
def moderation():

    list_name = "mailman"

    return jsonify(Mailman().get_held_messages(list_name))
