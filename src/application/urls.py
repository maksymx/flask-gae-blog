"""
urls.py

URL dispatch route mappings and error handlers

"""
from lib.flask import render_template

from application import app
from application import views


# URL dispatch rules
# App Engine warm up handler
# See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests
app.add_url_rule('/_ah/warmup', 'warmup', view_func=views.warmup)

# Home page
app.add_url_rule('/', 'home', view_func=views.home)

# Detailed post
app.add_url_rule('/post/<int:pid>', 'post_detailed', view_func=views.post_detailed)

# Say hello
app.add_url_rule('/hello/<username>', 'say_hello', view_func=views.say_hello)

# Contrived admin-only view example
app.add_url_rule('/admin_only', 'admin_only', view_func=views.admin_only)


app.add_url_rule('/admin_only/post/add/', 'add_post', methods=['GET', 'POST'],  view_func=views.add_post)
app.add_url_rule('/admin_only/post/<int:pid>/edit/', 'edit_post', methods=['GET', 'POST'],  view_func=views.edit_post)
app.add_url_rule('/admin_only/post/<int:pid>/delete/', 'delete_post', methods=["GET", "DELETE"],  view_func=views.delete_post)

# Examples list page (cached)
# app.add_url_rule('/examples/cached', 'cached_examples', view_func=views.cached_examples, methods=['GET'])

# Error handlers
# Handle 404 errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Handle 500 errors
@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500
