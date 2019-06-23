import os, click
from flask import Flask, render_template, url_for, request, flash, redirect, abort
from peewee import *
from flask_security import Security, PeeweeUserDatastore, login_required, current_user
from playhouse.flask_utils import PaginatedQuery, object_list
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

app.config['SECURITY_PASSWORD_SALT'] = 'Gloire au dieu Mathieu'

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

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error/404.html', error=e), 404

@app.errorhandler(403)
def unauthorized(e):
    return render_template('error/403.html', error=e), 403

@app.route('/', methods=['GET'])
def blog():
    return object_list('posts/blog.html',Publication.select(),context_variable='publications',paginate_by=10)

@app.route('/new', methods=['GET','POST'])
@login_required
def new_post():
    publication = Publication()
    form = PublicationForm()
    if form.validate_on_submit():
        form.populate_obj(publication)
        publication.author = current_user.id
        publication.save()
        flash('Hooray ! Publication send !')
        return redirect(url_for('blog'))
    return render_template('posts/new_publication.html', form=form)

@app.route('/edit/<int:post_id>', methods=['GET','POST'])
@login_required
def edit_post(post_id):
    try:
        publication = Publication.get(post_id)
    except Publication.DoesNotExist:
        abort(404)

    if (publication.author != current_user):
        abort(403)
    
    if request.method == 'POST':
        form = PublicationForm(request.form, obj=publication)
        if form.validate():
            form.populate_obj(publication)
            publication.save()
            flash('Your publication has been saved')
    else:
        form = PublicationForm(obj=publication)

    return render_template('posts/edit_publication.html', form=form, publication=publication)

@app.route('/delete/<int:post_id>')
def delete_post(post_id):
    Publication.delete_by_id(post_id)
    flash('Your publication has been deleted !')
    return redirect('/')

@app.route('/user_publication/<int:user_id>/', methods=['GET'])
def user_publication(user_id):
    try:
        user = User.get(user_id)
    except User.DoesNotExist:
        abort(404)
    return object_list('posts/user_publication.html',user.publications,context_variable='publications',paginate_by=4,page_var='page',check_bounds=True,**{'user':user})