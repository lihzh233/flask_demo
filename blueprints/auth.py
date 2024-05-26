from flask import Blueprint, render_template, request, jsonify
from exts import mail, db
from flask_mail import Message
import random
from model import EmailCaptchaModel


random.seed()
bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/login")
def login():
    return "login"


@bp.route("/register")
def register():
    return render_template("regist.html")


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
