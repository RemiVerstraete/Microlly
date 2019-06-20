import os, click
from flask import Flask, render_template, url_for, request, flash, redirect, abort
from peewee import *
from flask_security import Security, PeeweeUserDatastore, login_required
from model import User, Publication, create_tables, drop_tables, database
from form import ExtendedRegisterForm, SimplePublicationForm, PublicationForm
from flask_mail import Mail

app = Flask(__name__)
app.config['DEBUG']=True

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_REGISTER_URL'] = '/register'
app.config['SECURITY_SEND_REGISTER_EMAIL'] = False
app.config['SECURITY_CONFIRMABLE'] = False
app.config['SECURITY_PASSWORD_HASH'] = 'sha512_crypt'

app.config['SECURITY_PASSWORD_SALT'] = app.config['SECRET_KEY']

user_datastore = PeeweeUserDatastore(database, User, '', '')

security = Security(app, user_datastore, register_form=ExtendedRegisterForm)

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
    publications = Publication.select()
    return render_template('blog.html', publications=publications)

@app.route('/new', methods=['GET','POST'])
def new_post():
    publication = Publication()
    form = PublicationForm()
    if form.validate_on_submit():
        form.populate_obj(publication)
        publication.save()
        flash('Hooray ! Publication send !')
        return redirect(url_for('blog'))
    return render_template('new_publication.html', form=form)

@app.route('/edit/<int:post_id>', methods=['GET','POST'])
@login_required
def edit_post(post_id):
    try:
        publication = Publication.get(post_id)
    except Publication.DoesNotExist:
        abort(404)

    if request.method == 'POST':
        form = PublicationForm(request.form, obj=publication)
        if form.validate():
            form.populate_obj(publication)
            publication.save()
            flash('Your entry has been saved')
    else:
        form = PublicationForm(obj=publication)

    return render_template('dinosaurs/form.html', form=form, publication=publication)
