from flask import Flask, render_template, session
from dotenv import load_dotenv

load_dotenv() 
import os


app=Flask(__name__)

app.secret_key=os.environ["SECRET_KEY"]
flag_value =    open("./flag").read().rstrip()


def derived_level(sess,secret_key):
    user=sess.get("user","")
    role=sess.get("role","")
    if role =="admin" and user==secret_key[::-1]:
        return "superadmin"
    return "user"


@app.route("/")
def index():
    if "user" not in session:
        session["user"]="guest"
        session["role"]="user"
    return render_template("index.html")

@app.route("/admin")
def admin():
    level = derived_level(session,app.secret_key)
    if level == "superadmin":
        return render_template("admin.html",flag=flag_value)
    return "Access denied.\n",403



if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8000,debug=False)