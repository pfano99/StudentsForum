from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    content = TextAreaField('content')
    image = FileField('Image', validators=[FileAllowed(['png', 'jpeg', 'jpg'])])
    submit = SubmitField('Post')

class CommentForm(FlaskForm):
    content = TextAreaField('content', validators=[DataRequired()])
    submit = SubmitField('Comment')




