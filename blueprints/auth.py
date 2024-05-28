from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session
from exts import mail, db
from flask_mail import Message
import random
from models import EmailCaptchaModel, UserModel
from .forms import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash


random.seed()
bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()
            if user:
                if check_password_hash(user.password, password):
                    return redirect(url_for("qa.index"))
                else:
                    print("密码错误！")
                    return redirect(url_for("auth.login"))
            else:
                print("用户不存在！")
                return redirect(url_for("auth.login"))
        else:
            print(form.errors)
            return redirect(url_for("auth.login"))


@bp.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("regist.html")
    else:
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            user = UserModel(username=username, email=email, password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("auth.login"))
        else:
            print(form.errors)
            return redirect(url_for("auth.register"))





@bp.route("/captcha/email")
def get_email_captcha():
    email = request.args.get("email")
    captcha = ''.join([str(random.randint(0, 9)) for i in range(4)])
    message = Message(subject="flask_demo验证码", recipients=[email], body=f"flask_demo验证码: {captcha}")
    mail.send(message)

    existing_email = EmailCaptchaModel.query.filter_by(email=email).first()
    if existing_email:
        existing_email.captcha = captcha
        db.session.commit()
        return jsonify({"code": 200, "message": "更新验证码。", "data": None})

    db.session.add(EmailCaptchaModel(email=email, captcha=captcha))
    db.session.commit()

    return jsonify({"code": 200, "message": "新增验证码。", "data": None})


@bp.route("/mail/test")
def mail_test():
    message = Message(subject="邮箱测试", recipients=["1061878605@qq.com"], body="这是一条测试邮件。")
    mail.send(message)
    return "mail test."
