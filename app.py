import os, click
from flask import Flask, render_template
from peewee import *
from flask_security import Security, PeeweeUserDatastore, login_required
from model import User, Publication, create_tables, drop_tables, database
from form import ExtendedRegisterForm

app = Flask(__name__)
app.config['DEBUG']=True

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_REGISTER_URL'] = '/register'

user_datastore = PeeweeUserDatastore(database, User, '', '')

security = Security(app, user_datastore,
         register_form=ExtendedRegisterForm)

@app.cli.command()
def initdb():
    """Create database"""
    create_tables()
    click.echo('Initialized the database')

@app.cli.command()
def dropdb():
    """Drop database tables"""
    drop_tables()
    click.echo('Dropped tables from database')

@app.route('/')
@login_required
def blog():
    return render_template('blog.html')

'''@app.route('/register')
def register():
    return render_template('security/register_user.html')'''