from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import StringField,SubmitField,SelectField, PasswordField, TextAreaField

from wtforms.fields.html5 import DateField

class ResidenceForm(FlaskForm):

    name = StringField('Residence Name', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    room_type =  SelectField('Category', choices=(['Single Room', 'Sharing Room', 'Both Single and Sharing']))
    price = StringField('Prices', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[])
    rules = TextAreaField('Rules', validators=[])
    entertainment = TextAreaField('Entertainment', validators=[])
    safety_and_sec = TextAreaField('Saftey And Security', validators=[])

    submit = SubmitField('Submit')



