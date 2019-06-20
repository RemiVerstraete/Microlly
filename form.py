from flask_wtf import FlaskForm
from flask_security.forms import RegisterForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired, Length
from wtfpeewee.orm import model_form
from model import Publication

class ExtendedRegisterForm(RegisterForm):
    first_name = StringField('First Name', [DataRequired()])
    last_name = StringField('Last Name', [DataRequired()])
    username = StringField('Username', [DataRequired()])

class PublicationForm(FlaskForm):
    title = StringField('Title', [DataRequired()])
    body = StringField('Body', [DataRequired()])

SimplePublicationForm = model_form(Publication)