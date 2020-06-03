import os
import urllib
from datetime import timedelta
basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    MONGO_URI = 'mongodb+srv://user9304:'+urllib.parse.quote("P@ssword")+'@cluster0-zowuw.mongodb.net/test?retryWrites=true&w=majority'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "Anything_keep_for_generating_key"
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=5)
