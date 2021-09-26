"""Email.Cloud Queue Management

This application allows you to manage the queue of Email.Cloud through a
webapplication.

Author: henk.vanachterberg@broadcom.com
"""
from app import create_app, db
from app.api import queryQueue

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
