
from flask import Flask, render_template
from mailman import Mailman

app = Flask(__name__)


@app.route('/')
def index():
    data = { "lists": Mailman().lists() }

    return render_template("index.html", **data)
