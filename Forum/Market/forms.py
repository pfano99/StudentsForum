from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, NumberRange
from flask_wtf.file import FileField, FileAllowed

class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[ DataRequired() ])
    condition = SelectField('Condition', choices=(['Good', 'Ok', 'Bad' ]))
    price = IntegerField('Price', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    category = SelectField('Category', choices=(['Books', 'Electronic', 'Other']))
    image = FileField('Product Pictures', validators=[ FileAllowed(['jpeg', 'png', 'jpg']) ])
    submit = SubmitField('Sell')




