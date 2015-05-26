"""
models.py

App Engine datastore models

"""
from google.appengine.ext import ndb

ITEMS = 4


class Post(ndb.Model):
    created_at = ndb.DateTimeProperty(auto_now_add=True)
    title = ndb.StringProperty(required=True)
    # slug = ndb.StringProperty(required=True)
    body = ndb.TextProperty(required=True)
    author = ndb.UserProperty()
