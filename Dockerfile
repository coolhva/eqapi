FROM python:3.9-slim

RUN adduser --disabled-password eqapi
WORKDIR /home/eqapi

COPY requirements.txt requirements.txt

RUN python -m venv venv
RUN venv/bin/pip install --upgrade pip
RUN venv/bin/pip install --upgrade wheel
RUN venv/bin/pip install --upgrade setuptools
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY app app
COPY migrations migrations
COPY eqapi.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV LOG_TO_STDOUT True
ENV FLASK_APP eqapi.py

RUN chown -R eqapi:eqapi ./
USER eqapi

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
