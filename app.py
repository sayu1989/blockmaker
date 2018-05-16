#!/user/bin/env python
# -*- coding: utf-8 -*-
from bottle import route, run, template, request, static_file, url, get, post, response, error
import bottle
import os
import sys, codecs
import oauth2
import webbrowser as web
import tweepy
import jinja2
from bottle import TEMPLATE_PATH, jinja2_template as template
import bottle
import os

sys.stdout = codecs.getwriter("utf-8")(sys.stdout)
TEMPLATE_PATH.append("./template")

app = bottle.app()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, 'static')

@route("/")
def html_index():
    # マイページにcallback
    myAuth = tweepy.OAuthHandler("0V0gxq8Gbqu52x1YGIwbGOjRR", "xoOfOV5sh0tpbQLazDMMEIqVyWpEB8yqCf5q3gL1V6ZuG28qz2", "http://127.0.0.1:8000/mypage")
    myLogin_url = myAuth.get_authorization_url()

    # 作成ページにcallback
    createAuth = tweepy.OAuthHandler("0V0gxq8Gbqu52x1YGIwbGOjRR", "xoOfOV5sh0tpbQLazDMMEIqVyWpEB8yqCf5q3gL1V6ZuG28qz2", "http://127.0.0.1:8000/create")
    create_url = createAuth.get_authorization_url()

    # テンプレートファイルを開く
    return template('index.j2', myLogin_url=myLogin_url, create_url=create_url )

@route('/mypage')
def mypage():
    if request.GET.get('oauth_token'):
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

        response.set_cookie('myname', myname, secret="myname-sec")
        response.set_cookie('myid', myid, secret="myid-sec")
        response.set_cookie('myimage', myimage, secret="myid-image")

        # ユーザーテーブルの全TwitterIDから検索して true false

        #if #このTwitterIDがサイト内に登録済みの場合
          # データベースから該当のユーザーIDを取得して変数に格納
        #else 新規登録ユーザーの場合
          # SQLに格納
          #INSERT 〜〜〜〜〜〜〜 新しくレコードを追加
          #追加したユーザーIDを変数に格納

    else:
        myname = 'わしのなまえ'
        myid = 'slkajf'
        myimage = 'sample.png'
        import mysql.connector

        conn = mysql.connector.connect(user='root', password='coro22nero', host='localhost', database='blockmaker_db')
        cur = conn.cursor()

        #cur.execute("select * from users;")

        #for row in cur.fetchall():
        cur.execute("select twitter_name from users;")
        twitter_id =  cur.fetchall()

        cur.close
        conn.close

    return template('mypage.j2', myname=myname, myid=myid, myimage=myimage,rows = twitter_id )

# ゲーム作成画面
@route('/create')
def mypage():
    myname = request.get_cookie('myname')
    myid = request.get_cookie('myid')
    myimage = request.get_cookie('myimage')
    # プロフィール情報を取得
    return template('create.j2', myname=myname, myid=myid, myimage=myimage)

@route('/create2', method=["GET", "POST"])
def create_block():
    imageMiddleGet = request.forms.get('imageBottom')
    imageBottomGet = request.forms.get('imageMiddle')
    imageMiddle = response.set_cookie('imageMiddle', imageMiddleGet, secret="image-middle")
    imageBottom = response.set_cookie('imageBottom', imageBottomGet, secret="image-bottom")
    # ユーザー情報
    myname = request.get_cookie('myname')
    myid = request.get_cookie('myid')
    myimage = request.get_cookie('myimage')
    return template('create2.j2', imageMiddle=imageMiddleGet, imageBottom=imageBottomGet, myname=myname, myid=myid, myimage=myimage )

@route('/create3', method=["GET", "POST"])
def create_block():
    imageMiddleGet = request.forms.get('imageBottom')
    imageBottomGet = request.forms.get('imageMiddle')
    imageMiddle = response.set_cookie('imageMiddle', imageMiddleGet, secret="image-middle")
    imageBottom = response.set_cookie('imageBottom', imageBottomGet, secret="image-bottom")
    # ユーザー情報
    myname = request.get_cookie('myname')
    myid = request.get_cookie('myid')
    myimage = request.get_cookie('myimage')
    return template('create2.j2', imageMiddle=imageMiddleGet, imageBottom=imageBottomGet, myname=myname, myid=myid, myimage=myimage )


# static file CSS
@app.route('/static/css/<filename:path>')
def static_css(filename):
    return static_file(filename, root=STATIC_DIR+"/css")

# static file image
@app.route('/static/img/<filename:path>')
def static_img(filename):
    return static_file(filename, root=STATIC_DIR+"/img")

# static JS
@app.route('/static/js/<filename>')
def js_dir(filename):
    return static_file(filename, root=STATIC_DIR+"/js")

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
