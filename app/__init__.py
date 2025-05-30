import os
from flask import Flask
from .models import db, User
from flask_login import LoginManager

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    # 아래 두 줄로 DB 경로를 app 폴더로 고정
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, 'site.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .routes import bp
    app.register_blueprint(bp)

    from .auth import auth_bp
    app.register_blueprint(auth_bp)

    return app