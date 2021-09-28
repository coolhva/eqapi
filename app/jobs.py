from app import scheduler
from app.api import queryQueue
from app.settings import getSetting, saveSetting
from datetime import datetime
from flask import current_app


def updateQueue():
    with scheduler.app.app_context():
        scheduler.app.logger.info('running job update_queue')
        utcdatestr = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')

        if (getSetting('api_username') == '' or
           getSetting('api_password') == ''):
            saveSetting('last_error',
                        f"{utcdatestr}: No username or password set")
            scheduler.app.logger.info('No username or password set')
            return

        saveSetting('last_queue_update', utcdatestr)
        queryQueue()


def AddUpdateJob():
    interval = getSetting('update_queue_interval')
    try:
        interval = int(interval)
    except (ValueError, TypeError):
        interval = 300

    scheduler.add_job(
        func=updateQueue,
        trigger="interval",
        seconds=interval,
        misfire_grace_time=10,
        id="update_queue",
        name="Update queue from API",
        replace_existing=True
    )

    current_app.logger.info('Added job update_queue to scheduler')
