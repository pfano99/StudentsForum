from flask import Blueprint,render_template, redirect, url_for, request
from flask_login import current_user, login_required
from Forum.models import Post, User

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')



@main.route('/home')
@login_required
def home():
    if current_user.is_authenticated:
        posts = current_user.followed_user_posts()
    else:
        posts = Post.query.order_by(Post.date_created.desc()).all()
    return render_template('home.html', title = 'Student Forum', posts = posts)


@main.route('/about')
def about():
    return 'the about page'




