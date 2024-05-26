from flask import Flask
import config
from exts import db, mail
from blueprints.auth import bp as auth_bp
from blueprints.qa import bp as qa_bp
from flask_migrate import Migrate
from model import UserModel, EmailCaptchaModel


app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
migrate = Migrate(app, db)
mail.init_app(app)
app.register_blueprint(auth_bp)
app.register_blueprint(qa_bp)


if __name__ == '__main__':
    app.run(debug=True)
