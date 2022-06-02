from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
# from flask_session import Session

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://pfano:Bl@ck99..@localhost/student_forum_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'False'
app.config['SECRET_KEY'] = 'thetrytweyeuri'
# app.config['SESSION_TYPE'] = 'sqlalchemy'

db = SQLAlchemy(app)

# app.config['SESSION_SQLALCHEMY'] = db
# Session(app)

bcrypt = Bcrypt(app)

loginmanager = LoginManager(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

admin = Admin(app, name="Student Forum")


from Forum.Main.routes import main
from Forum.Users.routes import users 
from Forum.Posts.routes import posts 
from Forum.Market.routes import market
from Forum.Bursary.routes import bursary
from Forum.Friends.routes import friends
from Forum.Apis.routes import api
from Forum.Chatting.routes import chat
from Forum.Organizations.routes import organization
from Forum.Job.routes import job
from Forum.Residence.routes import residence

app.register_blueprint(main)
app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(market)
app.register_blueprint(bursary)
app.register_blueprint(friends)
app.register_blueprint(api)
app.register_blueprint(chat)
app.register_blueprint(organization)
app.register_blueprint(job)
app.register_blueprint(residence)

from Forum.models import *

admin.add_view(AdminModelView(User, db.session))
admin.add_view(AdminModelView(Product, db.session))
admin.add_view(AdminModelView(Post, db.session))
admin.add_view(AdminModelView(Bursary, db.session))

admin.add_view(AdminModelView(Organization, db.session))
admin.add_view(AdminModelView(Comment, db.session))
admin.add_view(AdminModelView(ProductComment, db.session))
admin.add_view(AdminModelView(Job, db.session))
admin.add_view(AdminModelView(Residence, db.session))
