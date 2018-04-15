#!/user/bin/env python
# -*- coding: utf-8 -*-
from bottle import route, run, template, request, static_file, url, get, post, response, error
import sys, codecs
import oauth2
import webbrowser as web
from twython import Twython, TwythonError
sys.stdout = codecs.getwriter("utf-8")(sys.stdout)

@route("/")
def html_index():
    consumer = oauth2.Consumer(key="0V0gxq8Gbqu52x1YGIwbGOjRR", secret="xoOfOV5sh0tpbQLazDMMEIqVyWpEB8yqCf5q3gL1V6ZuG28qz2")
    client = oauth2.Client(consumer)
    resp, content = client.request("https://api.twitter.com/oauth/request_token", "GET")

    # Tokenを辞書型にセット
    str = content.decode('utf-8')
    list = [t.split() for t in str.split("&")]
    d = ({})
    for t in list:
        a = t[0].split("=")
        d.update({ a[0] : a[1] }) # dの中身は文字列

    #d = {'oauth_token': '5k04iwAAAAAA1OhDAAABXO9D4lk', 'oauth_token_secret': 'ITYIIQVh9Iga6ue4ox8jwjO0sml7RTJU', 'oauth_callback_confirmed': 'true'}

    # 認証用ページを開く
    url = "https://api.twitter.com/oauth/authorize?oauth_token=" + d['oauth_token']
    return """
        <h1>ブロック崩しメーカー</h1>
        <div><a href='"""+url+"""'>認証ページへ</a></div>
        """

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
