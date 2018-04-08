#!/user/bin/env python
# -*- coding: utf-8 -*-
from bottle import route, run, template, request, static_file, url, get, post, response, error
import sys, codecs
sys.stdout = codecs.getwriter("utf-8")(sys.stdout)

@route("/")
def html_index():
    return template("index")

@route("/static/<filepath:path>", name="static_file")
def static(filepath):
    return static_file(filepath, root="./static")


@get("/login")
def login():
    return """
        <form action="/login" method="post">
            Username: <input name="username" type="text" />
            Password: <input name="password" type="password" />
            <input value="Login" type="submit" />
        </form>
    """
@route("/login", method="POST")
def do_login():
    username = request.forms.get("username")
    password = request.forms.get("password")
    if check_login(username, password):
        response.set_cookie("account", username, secret="some-secret-key")
        return template("index", name=username)
    else:
        return "<p>Failed !</p>"
def check_login(username, password):
  if username == "admin" and password=="password":
    return True
  else:
    return False


@error(404)
def error404(error):
    return template("404")

run(host="localhost", port=8000, debug=True, reloader=True)
