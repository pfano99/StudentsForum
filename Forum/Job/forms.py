from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import StringField,SubmitField,SelectField, PasswordField, TextAreaField

from wtforms.fields.html5 import DateField

class JobForm(FlaskForm):
    job_title = StringField('Job Title', validators=[DataRequired()])
    open_date = DateField('Open date', format='%Y-%m-%d')
    closing_date = DateField('Close date', format='%Y-%m-%d')
    job_type = SelectField('Category', choices=(['Apprenticeship', 'Internship', 'Part time', 'Full time']))
    requirements = TextAreaField('Requirements', validators=[])
    job_description = TextAreaField('Job description', validators=[])
    salary = StringField('Salary', validators=[])
    # Sector = 
   
    job_link = StringField('Job Link', validators=[])
    province = SelectField('Provinces', choices=([ 'Eastern Cape', 'Free State', 'Gauteng', 'KwaZulu-Natal', 'Limpopo', 'Mpumalanga', 'Northern Cape', 'North West', 'Western Cape']))
    city = StringField('City', validators=[])
    submit = SubmitField('Submit')



