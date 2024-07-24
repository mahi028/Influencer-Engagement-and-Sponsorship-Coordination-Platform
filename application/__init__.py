from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
login_manager = LoginManager()
migration = Migrate()

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
    login_manager.init_app(app)
    migration.init_app(app, db)

    with app.app_context():
        from application.modals import User, Role, UserRoles, Admin
        db.create_all()

        roles = Role.query.all()
        if not roles:
            role1 = Role(name = 'Admin')
            role2 = Role(name = 'Influcener')
            role3 = Role(name = 'Sponser')
            db.session.add_all([role1, role2, role3])
            db.session.commit()

        admin = UserRoles.query.filter_by(role_id = 1).first()
        if not admin:
            from application.hash import hashpw
            new_admin = User(email = 'admin@gmail.com', password = hashpw('mahi028')) 
            new_inf = User(email = 'inf@gmail.com', password = hashpw('mahi028')) 
            new_spn = User(email = 'spn@gmail.com', password = hashpw('mahi028')) 
            adm = Admin(admin_id = admin.user_id)
            db.session.add_all([new_admin, new_inf, new_spn, adm])
            db.session.commit()

            admin_role = UserRoles(user_id = 1, role_id = 1)
            inf_role = UserRoles(user_id = 2, role_id = 2)
            spn_role = UserRoles(user_id = 3, role_id = 3)
            db.session.add_all([admin_role, inf_role, spn_role])
            db.session.commit()

    from application.controllers.dashboard import home
    from application.controllers.auth import user_auth
    from application.controllers.sponser import sponser
    from application.controllers.influencer import influencer
    from application.controllers.admin import admin

    app.register_blueprint(home, url_prefix = '/')
    app.register_blueprint(user_auth, url_prefix = '/auth')
    app.register_blueprint(sponser, url_prefix = '/sponser')
    app.register_blueprint(influencer, url_prefix = '/user')
    app.register_blueprint(admin, url_prefix = '/admin')
    login_manager.login_view = '/auth/login'


    from application.api import Activities
    api.add_resource(Activities, "/api/activity/request_data/<string:type_of_data>")

    return app

