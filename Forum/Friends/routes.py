from flask import Blueprint, render_template, redirect, url_for
from Forum.models import User

friends = Blueprint('Friends', __name__)


@friends.route('/friends')
def meet_friends():
    friend  = User.query.all()

    return render_template('friends.html', title = 'Meet new Friends', friends = friend)





