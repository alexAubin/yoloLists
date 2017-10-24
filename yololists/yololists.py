
from flask import Flask, render_template, jsonify, request
from mailman import Mailman
from HTMLParser import HTMLParser

app = Flask(__name__)
h = HTMLParser()


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


@app.route('/admin')
def admin():

    list_name = "mailman"

    data = { "categories":
            [ { "name":k, "display_name": h.unescape(v[0]) }
                for k, v in Mailman().admin_cagetories(list_name).items() ],
             "current_category": Mailman().admin_category_view(list_name, "general")
           }

    print data["current_category"]["title"]

    return render_template("admin.html", **data)



