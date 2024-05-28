from flask import Flask, session, g
from sqlalchemy.testing.pickleable import User

import config
from exts import db, mail
from blueprints.auth import bp as auth_bp
from blueprints.qa import bp as qa_bp
from flask_migrate import Migrate
from models import UserModel, EmailCaptchaModel


app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
migrate = Migrate(app, db)
mail.init_app(app)
app.register_blueprint(auth_bp)
app.register_blueprint(qa_bp)


@app.before_request
def before_request():
    user_id = session.get('user_id')
    if user_id:
        g.user = UserModel.query.get(user_id)
    else:
        g.user = None


@app.context_processor
def context_processor():
    return {'user': g.user}


if __name__ == '__main__':
    app.run(debug=True)
