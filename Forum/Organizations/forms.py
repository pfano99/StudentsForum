from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import StringField,SubmitField, PasswordField, BooleanField

class OrgRegistrationForm(FlaskForm):
    name = StringField('Organization name', validators=[DataRequired()])
    email = StringField('Organization email', validators=[DataRequired()])
    telephone  = StringField('Telephone Number', validators=[DataRequired()])
    website = StringField('Website link', validators=[])
    location = StringField('Location', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    image = FileField('Company Logo', validators=[ FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Submit')    


class OrgLoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()]) 
    password = PasswordField('Password', validators=[DataRequired()]) 
    remember_me = BooleanField('Remember me?')
    submit = SubmitField('Submit')