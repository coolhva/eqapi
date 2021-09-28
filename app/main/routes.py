from flask import (render_template, flash, redirect, url_for, request,
                   current_app)
from flask_login import current_user, login_required
from datetime import datetime
from sqlalchemy.sql.elements import and_
from app import db, scheduler
from app.jobs import AddUpdateJob
from app.models import DomainQueue, GlobalQueue, Domain
from app.main.forms import EditProfileForm, SettingsForm
from app.settings import getSetting, saveSetting
from app.api import testConnection
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
    domains = Domain.query.all()
    return render_template('queue.html', title='Queue', domains=domains)


@bp.route('/data/<from_date>/<to_date>',
          defaults={'domain': None}, methods=['GET'])
@bp.route('/data/<from_date>/<to_date>/<domain>', methods=['GET'])
@login_required
def data(from_date, to_date, domain):

    startdate = datetime.strptime(from_date, "%Y%m%d%H%M")
    enddate = datetime.strptime(to_date, "%Y%m%d%H%M")

    if domain is None:
        # global queue

        rdata = {
            'labels': [],
            'data': {
                'TotalMessagesInbound': [],
                'TotalMessagesOutbound': [],
                'MeanTimeInQueueInbound': [],
                'MeanTimeInQueueOutbound': [],
                'LongestTimeInInbound': [],
                'LongestTimeInOutbound': []
                }
            }

        qdata = db.session.query(
            GlobalQueue
            ).filter(
                GlobalQueue.datetime.between(startdate, enddate)
            ).all()
        for entry in qdata:
            rdata['labels'].append(datetime.strftime(
                entry.datetime, "%Y-%m-%d %H:%M:%S"))
            rdata['data']['TotalMessagesInbound'].append(
                entry.TotalMessagesInbound)
            rdata['data']['TotalMessagesOutbound'].append(
                entry.TotalMessagesOutbound)
            rdata['data']['MeanTimeInQueueInbound'].append(
                entry.MeanTimeInQueueInbound)
            rdata['data']['MeanTimeInQueueOutbound'].append(
                entry.MeanTimeInQueueOutbound)
            rdata['data']['LongestTimeInInbound'].append(
                entry.LongestTimeInInbound)
            rdata['data']['LongestTimeInOutbound'].append(
                entry.LongestTimeInOutbound)
    else:
        # domain queue

        rdata = {
            'labels': [],
            'data': {
                'ReceiveQueueCountInbound': [],
                'ReceiveQueueCountOutbound': [],
                'DeliveryQueueCountInbound': [],
                'DeliveryQueueCountOutbound': [],
                'LongestTimeInReceiveQueueInbound': [],
                'LongestTimeInReceiveQueueOutbound': [],
                'LongestTimeInDeliveryQueueInbound': [],
                'LongestTimeInDeliveryQueueOutbound': [],
                'MeanTimeInReceiveQueueInbound': [],
                'MeanTimeInReceiveQueueOutbound': [],
                'MeanTimeInDeliveryQueueInbound': [],
                'MeanTimeInDeliveryQueueOutbound': []
                }
            }

        qdata = db.session.query(
            DomainQueue
            ).join(
                Domain
            ).filter(
                and_(DomainQueue.datetime.between(startdate, enddate),
                     Domain.domainname == domain)
            ).all()
        for entry in qdata:
            rdata['labels'].append(datetime.strftime(
                entry.datetime, "%Y-%m-%d %H:%M:%S"))
            rdata['data']['ReceiveQueueCountInbound'].append(
                entry.ReceiveQueueCountInbound)
            rdata['data']['ReceiveQueueCountOutbound'].append(
                entry.ReceiveQueueCountOutbound)
            rdata['data']['DeliveryQueueCountInbound'].append(
                entry.DeliveryQueueCountInbound)
            rdata['data']['DeliveryQueueCountOutbound'].append(
                entry.DeliveryQueueCountOutbound)
            rdata['data']['LongestTimeInReceiveQueueInbound'].append(
                entry.LongestTimeInReceiveQueueInbound)
            rdata['data']['LongestTimeInReceiveQueueOutbound'].append(
                entry.LongestTimeInReceiveQueueOutbound)
            rdata['data']['LongestTimeInDeliveryQueueInbound'].append(
                entry.LongestTimeInDeliveryQueueInbound)
            rdata['data']['LongestTimeInDeliveryQueueOutbound'].append(
                entry.LongestTimeInDeliveryQueueOutbound)
            rdata['data']['MeanTimeInReceiveQueueInbound'].append(
                entry.MeanTimeInReceiveQueueInbound)
            rdata['data']['MeanTimeInReceiveQueueOutbound'].append(
                entry.MeanTimeInReceiveQueueOutbound)
            rdata['data']['MeanTimeInDeliveryQueueInbound'].append(
                entry.MeanTimeInDeliveryQueueInbound)
            rdata['data']['MeanTimeInDeliveryQueueOutbound'].append(
                entry.MeanTimeInDeliveryQueueOutbound)
    return rdata


@bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    form = SettingsForm()
    job = scheduler.get_job('update_queue')
    if form.validate_on_submit():
        saveSetting('update_queue_interval', form.interval.data)
        saveSetting('disable_registration', form.disable_registration.data)

        if (form.api_username.data != '' and form.api_password.data != ''):
            result = testConnection(form.api_username.data,
                                    form.api_password.data)
            if not result['status']:
                flash(result['message'], 'danger')
                return render_template('settings.html', title='Settings',
                                       form=form)
            saveSetting('api_username', form.api_username.data)
            saveSetting('api_password', form.api_password.data)
            flash('Connection to API successful, settings saved', 'success')
        else:
            flash('Settings has been saved', 'success')

        AddUpdateJob()
        return redirect(url_for('main.settings'))
    elif request.method == 'GET':
        form.api_username.data = getSetting('api_username')
        form.api_password.data = getSetting('api_password')
        form.interval.data = getSetting('update_queue_interval', '300')
        form.disable_registration.data = int(getSetting('disable_registration',
                                                        '0'))

    return render_template('settings.html', title='Settings', form=form,
                           last_error=getSetting('last_error'),
                           job=datetime.strftime(
                                job.next_run_time, "%Y-%m-%d %H:%M:%S"))
