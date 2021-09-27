from app import scheduler
from app.api import queryQueue
from app.settings import getSetting, saveSetting
from datetime import datetime


def updateQueue():
    with scheduler.app.app_context():
        utcdatestr = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')

        if (getSetting('api_username') == '' or
           getSetting('api_password') == ''):
            saveSetting('last_error',
                        f"{utcdatestr}: No username or password set")
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
