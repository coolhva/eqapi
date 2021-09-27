"""Email.Cloud Queue Management

This application allows you to manage the queue of Email.Cloud through a
webapplication.

Author: henk.vanachterberg@broadcom.com
"""
from app import create_app, db
from app.models import GlobalQueue, DomainQueue
from app.api import queryQueue
from random import randrange

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db}


@app.cli.command('q')
def query():
    print('Updating queue statistics...')
    if queryQueue():
        print('Success')
    else:
        print('Error')


@app.cli.command('scramble')
def scramble():
    print('Scrambling data for demo purposes...')
    qdata = GlobalQueue.query.all()
    for entry in qdata:
        entry.TotalMessagesInbound = randrange(0, 10)
        entry.TotalMessagesOutbound = randrange(0, 10)
        entry.MeanTimeInQueueInbound = randrange(0, 30)
        entry.MeanTimeInQueueOutbound = randrange(0, 30)
        entry.LongestTimeInInbound = randrange(0, 50)
        entry.LongestTimeInOutbound = randrange(0, 50)

    qdata = DomainQueue.query.all()
    for entry in qdata:
        entry.ReceiveQueueCountInbound = randrange(0, 10)
        entry.ReceiveQueueCountOutbound = randrange(0, 10)
        entry.DeliveryQueueCountInbound = randrange(0, 10)
        entry.DeliveryQueueCountOutbound = randrange(0, 10)
        entry.LongestTimeInReceiveQueueInbound = randrange(0, 30)
        entry.LongestTimeInReceiveQueueOutbound = randrange(0, 30)
        entry.LongestTimeInDeliveryQueueInbound = randrange(0, 30)
        entry.LongestTimeInDeliveryQueueOutbound = randrange(0, 30)
        entry.MeanTimeInReceiveQueueInbound = randrange(0, 50)
        entry.MeanTimeInReceiveQueueOutbound = randrange(0, 50)
        entry.MeanTimeInDeliveryQueueInbound = randrange(0, 50)
        entry.MeanTimeInDeliveryQueueOutbound = randrange(0, 50)

    db.session.commit()

    print('All data has been scrambled, happy demoing!')
    return
