from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
login_manager = LoginManager()

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
    migration = Migrate(app, db)

    login_manager.init_app(app)

    login_manager.login_view = '/'

    with app.app_context():
        from application.modals import User, Role, UserRoles
        db.create_all()

        roles = Role.query.all()
        if not roles:
            role1 = Role(name = 'Admin')
            role2 = Role(name = 'Influcener')
            role3 = Role(name = 'Sponser')
            db.session.add_all([role1, role2, role3])
            db.session.commit()

        admin = Role.query.filter_by(role_id = 1)
        if not admin:
            from application.hash import hashpw
            new_admin = User(email = 'admin@admin.com', password = hashpw('mahi028')) 
            db.session.add(new_admin)
            db.session.commit()

            admin_role1 = UserRoles(user_id = 1, role_id = 1)
            admin_role2 = UserRoles(user_id = 1, role_id = 2)
            admin_role3 = UserRoles(user_id = 1, role_id = 3)
            db.session.add_all([admin_role1, admin_role2, admin_role3])

    from application.controllers.dashboard import home
    from application.controllers.auth import user_auth
    from application.controllers.sponser import sponser
    from application.controllers.influencer import influencer

    app.register_blueprint(home, url_prefix = '/')
    app.register_blueprint(user_auth, url_prefix = '/auth')
    app.register_blueprint(sponser, url_prefix = '/sponser')
    app.register_blueprint(influencer, url_prefix = '/user')

    # from application.api import api_name
    # api.add_resource(api_name, "/api_url")

    return app

