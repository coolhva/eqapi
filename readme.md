# Email.Cloud Queue API Management
This repo contains the source code for the Email.Cloud Queue API (EQAPI) docker container.

## Running the docker container
Clone or Download and extract the ZIP file of this repository and issue the following command to build the docker container:

```shell
docker build -t eqapi .
```
Then issue the following command to run the docker container:
```shell
docker run --name eqapi -d -p 8000:5000 -v /docker/db:/home/eqapi/db eqapi:latest
```
This will start a docker container listening on port 8000 on the docker host and binds the folder ```/docker/db``` to the folder where the docker container stores its (SQLite) database. The ```-v /docker/db:/home/eqapi/db``` parameter is optional, without the parameter it will use the db inside the container.

**Optional environment variables**

|Environment variable|Default|Description
|:---|:---|:--|
|SECRET_KEY|7Ghy648FibRfcgQ...AxdTFB2Brz|Used by the Flask server to encrypt sessions|
|SQLALCHEMY_DATABASE_URI|sqlite://./db/app.db|Used to point to a database that holds the users and domains|
|SERVER_NAME|Empty|External url used generate link in password reset email (test first without setting this parameter)|
|PREFERRED_URL_SCHEME|http|Used in conjunction with SERVER_NAME, https if TLS is used (test first without setting this parameter)|
|LOG_TO_STDOUT|False|If True logs will send to STDOUT|
|ADMIN_EMAIL|Empty|Administrator email to receive errors from the application|
|MAIL_SERVER|Empty|IP or DNS name of mail server|
|MAIL_PORT|25|TCP Port of mailserver|
|MAIL_USE_TLS|Empty|If set to True it will use TLS when sending email|
|MAIL_USERNAME|Empty|Username for the mailserver|
|MAIL_PASSWORD|Empty|Password for the mailserver|
|MAIL_FROM|Empty|From Email address used in password reset mail|
|EQAPI_URL|https://emailqueue.emailsecurity.symantec.com/|Base URL for IOC API|
|SCHEDULER_API_ENABLED|False|When set it enables the scheduler API (/scheduler/jobs e.g.)|

1. Go to http://dockerhost:8000/

   Register yourself a new user and enter your ClientNet credentials for the API in settings (it is recommended to create a seperate API user in the ClientNet portal).

2. Now you can start using the application by showing the current IOC's, use the + sign to add new IOC's or use the bulk upload functionality.

## Run code in your development environment

1. Download/clone this repository
2. In the root directory issue the ``` python -m venv venv``` command to create a virtual environment
3. Activate the virtual environment, e.g. in linux ``` source venv/bin/activate```
4. Install requirements via ```pip install -r requirements.txt```
5. Create database folder with ```mkdir db```
6. Create database with ```flask db upgrade```
7. Start flask ```flask run```
8. Visit the web application at http://localhost:5000/
