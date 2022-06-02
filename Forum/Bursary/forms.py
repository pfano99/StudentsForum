from flask_wtf import  FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Email, URL, Optional, Length
from flask_wtf.file import FileAllowed, FileField
from wtforms.widgets.html5 import URLInput

from wtforms.fields.html5 import DateField
 
class BursaryForm(FlaskForm):
    web_link = StringField('Website Link', validators=[DataRequired()])
    bursary_name = StringField('Bursary Name', validators=[DataRequired()])
    opening_date = DateField('Open date', format='%Y-%m-%d')
    closing_date = DateField('Close date', format='%Y-%m-%d')
    requirements = TextAreaField('Requirements', validators=[DataRequired()])
    how_to_apply = TextAreaField('How to apply', validators=[DataRequired()])
    document = FileField('Bursary Document', validators = [FileAllowed(['pdf','doc', 'docx']), Optional()])
    submit = SubmitField('Submit')
 
