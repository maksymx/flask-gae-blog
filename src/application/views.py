"""
views.py

URL route handlers

Note that any handler params must match the URL route params.
For example the *say_hello* handler, handling the URL route '/hello/<username>',
  must be passed *username* as the argument.

"""
from google.appengine.api import users
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError

from lib.flask import request, render_template, flash, url_for, redirect
from lib.flask_cache import Cache

from application import app
from decorators import login_required, admin_required
from models import Post


# Flask-Cache (configured to use App Engine Memcache API)
cache = Cache(app)

def home():
    posts = Post.query()
    return render_template('base.html', posts=posts)

def say_hello(username):
    """Contrived example to demonstrate Flask's url routing capabilities"""
    return 'Hello %s' % username

@admin_required
def admin_only():
    """This view requires an admin account"""
    posts = Post.query()
    return render_template("admin/admin.html", posts=posts)

@admin_required
def add_post():
    """This view requires an admin account"""
    if request.method == 'POST':
        title = request.form.get('post-title').strip()
        post = Post(title=title, body=request.form.get('post-full'), author=users.get_current_user())
        try:
            post.put()
            post_id = post.key.id()
            flash(u'Post %s successfully saved.' % post_id, 'success')
            return redirect(url_for('admin_only'))
        except CapabilityDisabledError:
            flash(u'App Engine Datastore is currently in read-only mode.', 'info')
            return redirect(url_for('home'))
    return render_template("admin/add_post.html")

@admin_required
def edit_post(pid):
    """This view requires an admin account"""
    post = Post.get_by_id(pid)
    if request.method == 'POST':
        post.title = request.form.get('post-title').strip()
        post.body = request.form.get('post-full')
        post.put()
        flash(u'Post %s successfully saved.' % pid, 'success')
        return redirect(url_for('admin_only'))
    return render_template("admin/update_post.html", post=post)

@admin_required
def delete_post(pid):
    """This view requires an admin account"""
    post = Post.get_by_id(pid)
    if request.method == 'GET':
        try:
            post.key.delete()
            flash(u'Post %s successfully saved.' % pid, 'success')
            return redirect(url_for('home'))
        except CapabilityDisabledError:
            flash(u'App Engine Datastore is currently in read-only mode.', 'info')
            return redirect(url_for('home'))
    if request.method == "DELETE":
        pass

def post_detailed(pid):
    post = Post.get_by_id(pid)
    return render_template("post.html", post=post)


# @cache.cached(timeout=60)
# def cached_examples():
#     """This view should be cached for 60 sec"""
#     examples = ExampleModel.query()
#     return render_template('list_examples_cached.html', examples=examples)


def warmup():
    """App Engine warmup handler
    See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests

    """
    return ''
