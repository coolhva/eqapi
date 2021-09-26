from flask import (render_template, flash, redirect, url_for, request,
                   current_app)
from flask_login import current_user, login_required
from app import db
from app.main.forms import EditProfileForm, SettingsForm
from app.settings import getSetting, saveSetting
from app.api import testConnection, queryQueue
from app.main import bp


@bp.route('/favicon.ico')
def favicon():
    return current_app.send_static_file('favicon.ico')


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html', title='Home')


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        db.session.commit()
        flash('Your changes have been saved.', 'success')
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


@bp.route('/queue', methods=['GET'])
@login_required
def queue():
    queryQueue()
    return render_template('queue.html', title='Queue')


@bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    form = SettingsForm()
    if form.validate_on_submit():
        result = testConnection(form.api_username.data, form.api_password.data)
        if not result['status']:
            flash(result['message'], 'danger')
            return render_template('settings.html', title='Settings',
                                   form=form)
        saveSetting('api_username', form.api_username.data)
        saveSetting('api_password', form.api_password.data)
        flash('Connection to API successful, credentials saved', 'success')
        return redirect(url_for('main.settings'))
    elif request.method == 'GET':
        form.api_username.data = getSetting('api_username')
        form.api_password.data = getSetting('api_password')

    return render_template('settings.html', title='Settings', form=form)
