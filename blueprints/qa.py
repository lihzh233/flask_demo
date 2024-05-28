from flask import Blueprint, request, render_template, g, redirect, url_for
from models import QuestionModel, AnswerModel
from blueprints.forms import QuestionForm, AnswerForm
from exts import db
from decorators import login_required

bp = Blueprint("qa", __name__, url_prefix="/")


@bp.route("/")
def index():
    questions = QuestionModel.query.order_by(QuestionModel.id.desc()).all()
    return render_template("index.html", questions=questions)


@bp.route("/qa/publish", methods=["GET", "POST"])
@login_required
def publish_question():
    if request.method == "GET":
        return render_template("question.html")
    else:
        form = QuestionForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            question = QuestionModel(title=title, content=content, author_id=g.user.id)
            db.session.add(question)
            db.session.commit()
            return redirect(url_for("qa.index"))
        else:
            print(form.errors)
            return redirect(url_for("qa.index"))


@bp.route("/qa/detail/<qa_id>")
def qa_detail(qa_id):
    question = QuestionModel.query.get(qa_id)
    return render_template("detail.html", question=question)


# @bp.route("/qa/answer/publish", methods=['POST'])
@bp.post("/qa/answer/publish")
@login_required
def answer_publish():
    form = AnswerForm(request.form)
    if form.validate():
        content = form.content.data
        question_id = form.question_id.data
        answer = AnswerModel(question_id=question_id, content=content, author_id=g.user.id)
        db.session.add(answer)
        db.session.commit()
        return redirect(url_for("qa.qa_detail", qa_id=question_id))
    else:
        print(form.errors)
        return redirect(url_for("qa.qa_detail", qa_id=request.form.get("question_id")))
