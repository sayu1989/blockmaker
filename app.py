#!/user/bin/env python
# -*- coding: utf-8 -*-
from bottle import route, run, template, request, static_file, url, get, post, response, error
import sys, codecs
import oauth2
import webbrowser as web
import tweepy
import jinja2
from bottle import TEMPLATE_PATH, jinja2_template as template
sys.stdout = codecs.getwriter("utf-8")(sys.stdout)

TEMPLATE_PATH.append("./template")

@route("/")
def html_index():
    auth = tweepy.OAuthHandler("0V0gxq8Gbqu52x1YGIwbGOjRR", "xoOfOV5sh0tpbQLazDMMEIqVyWpEB8yqCf5q3gL1V6ZuG28qz2", "http://127.0.0.1:8000/back")
    redirect_url = auth.get_authorization_url()

    # テンプレートファイルを開く
    return template('index.j2', redirect_url=redirect_url)

@route('/back', method='GET')
def callback():
    # Let's say this is a web app, so we need to re-build the auth handler
    auth = tweepy.OAuthHandler("0V0gxq8Gbqu52x1YGIwbGOjRR", "xoOfOV5sh0tpbQLazDMMEIqVyWpEB8yqCf5q3gL1V6ZuG28qz2")
    token = request.GET.get('oauth_token')
    verifier = request.GET.get('oauth_verifier')
    auth.request_token = { 'oauth_token' : token, 'oauth_token_secret' : verifier }
    auth.get_access_token(verifier)

    key = auth.access_token
    secret = auth.access_token_secret

    auth.set_access_token(key,secret)
    api = tweepy.API(auth)

    # プロフィール情報を取得
    myinfo = api.me()
    myname = myinfo.screen_name
    myid = myinfo.name
    myimage = myinfo.profile_image_url

    return """
        <p>ログインが完了しました。<br />
        <img src='"""+str(myimage)+"""' />
        ユーザー名は"""+str(myname)+"""ユーザーIDは"""+str(myid)+"""<br />
        ここでDBの登録処理とログイン判定を行い、元の画面に戻します。</p>
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
    return "<p>not found</p>"

run(host="localhost", port=8000, debug=True, reloader=True)
