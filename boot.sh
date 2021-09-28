#!/bin/bash
source venv/bin/activate
mkdir ./db
export EQAPI_INIT=1
flask db upgrade
unset EQAPI_INIT=1
exec gunicorn -b :5000 --access-logfile - --error-logfile - eqapi:app
