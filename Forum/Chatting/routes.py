from flask import Blueprint, render_template, redirect
from flask_login import login_required


chat = Blueprint('Chat', __name__)


@chat.route('/chat')
@login_required
def chat_friends():
    return render_template('chatting.html')

@chat.route('/chat/message')
@login_required
def chat_message():
    pass



