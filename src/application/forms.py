"""
forms.py

Web forms based on Flask-WTForms

See: http://flask.pocoo.org/docs/patterns/wtforms/
     http://wtforms.simplecodes.com/

"""

from lib.wtforms import Form
from lib.wtforms import validators
from lib.wtforms.ext.appengine.ndb import model_form

from models import Post


# App Engine ndb model form example
PostForm = model_form(Post, Form, field_args={'title': {"validators": [validators.Required()]},
                                              'body': {"validators": [validators.Required()]}})
