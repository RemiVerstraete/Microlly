from flask_security.forms import RegisterForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired, Length

class ExtendedRegisterForm(RegisterForm):
    first_name = StringField('First Name', [DataRequired()])
    last_name = StringField('Last Name', [DataRequired()])
