
from flask import Flask
from mailman import Mailman

app = Flask(__name__)


@app.route('/')
def mainpage():
    return str(Mailman().lists())
