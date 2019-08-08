"""
    负责视图和路由
"""
import hashlib

from flask import request
from flask import redirect
from flask import render_template
from flask import jsonify

from FlaskDirtory.main import app
from FlaskDirtory.main import csrf
from FlaskDirtory.models import *
from FlaskDirtory.main import session
from FlaskDirtory.forms import TeacherForm


def setPassword(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    return md5.hexdigest()


def LoginVaild(fun):
    def inner(*args, **kwargs):
        username = request.cookies.get("username")
        id = request.cookies.get("user_id")
        session_username = session.get("username")
        if username and id and session_username:
            if username == session_username:
                return fun(*args, **kwargs)
        return redirect("/login/")
    return inner


@app.route("/students_list/", methods=['GET', 'POST'])
def students_list():
    students_list = Student.query.all()
    return render_template("students_list.html", **locals())


@app.route("/teachers_list/", methods=['GET', 'POST'])
def teachers_list():
    teachers_list = Teacher.query.all()
    return render_template("teachers_list.html", **locals())


@csrf.exempt
@app.route("/index/", methods=["GET","POST"])
@LoginVaild
def index():
    return render_template("index.html")


@csrf.exempt
@app.route("/register/", methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username and password:
            user = User()
            user.username = username
            user.password = setPassword(password)
            user.save()
        return redirect("/login/")
    return render_template("register.html")


@csrf.exempt
@app.route("/login/", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username and password:
            user = User.query.filter_by(username=username).first()
            if user and user.password == setPassword(password):
                # 进行跳转
                response = redirect("/index/")
                # 设置cookie
                response.set_cookie("username", username)
                response.set_cookie("user_id", str(user.id))
                # 设置session
                session["username"] = username
                # 返回跳转
                return response
    return render_template("login.html", **locals())


@app.route("/base/")
def base():
    return render_template("base.html")


@app.route("/logout/", methods=["GET", "POST"])
def logout():
    response = redirect("/login/")
    for key in request.cookies:
        response.delete_cookie(key)
    return response


@csrf.exempt  # 单视图函数避免csrf校验  添加csrf令牌
@app.route("/add_teacher/", methods=["GET", "POST"])
def add_teacher():
    teacher_form = TeacherForm()
    if request.method == "POST":
        name = request.form.get("name")
        age = request.form.get("age")
        gender = request.form.get("gender")
        course = request.form.get("course")

        t = Teacher()
        t.name = name
        t.age = age
        t.gender = gender
        t.course_id = int(course)
        t.save()
    return render_template("add_teacher.html", **locals())


@csrf.error_handler     # 重新定义403错误页
# @app.errorhandler(CSRFError)
@app.route("/csrf_403/")
def crsf_token_error(reason):
    print(reason)  # 错误信息 The CSRF token is missing
    return render_template("csrf_403.html", **locals())


@app.route("/userValid/", methods=["POST","GET"])
def UserValid():
    result = {"state": "", "content": ""}
    username = request.args.get("username")
    if username:
        user = User.query.filter_by("username")
        if user:
            result["state"] = 200
            result["content"] = "用户名已使用"
        else:
            result["state"] = 400
            result["content"] = "用户名可以使用"
    else:
        result["state"] = 200
        result["content"] = "用户名不能为空"
    return jsonify(result)
