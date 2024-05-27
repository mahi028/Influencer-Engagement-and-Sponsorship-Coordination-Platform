from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_login import LoginManager
from flask_migrate import Migrate


db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__,
                static_folder="static",
                static_url_path="/st")
    api = Api(app)

    CORS(app)

    app.config["SECRET_KEY"] = '$2b$12$96I6WBOkALcat926zlh/D.PTqDzzpXh4sbUa9ynUfgYlldrEYLcFq'
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite3"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    

    db.init_app(app)
    migrate.init_app(app, db)

    login_manager.init_app(app)

    login_manager.login_view = '/login'

    with app.app_context():
        from application.modals import User, Role
        db.create_all()

        # role1 = Role(name = 'Admin')
        # role2 = Role(name = 'Influcener')
        # role3 = Role(name = 'Sponser')
        # db.session.add_all([role1, role2, role3])
        # db.session.commit()

    from application.controllers.index import home
    from application.controllers.auth import user_auth

    app.register_blueprint(home, url_prefix = '/home')
    app.register_blueprint(user_auth, url_prefix = '/')


    # from application.api import api_name
    # api.add_resource(api_name, "/api_url")

    return app
