# Report shop site

This is a project for report shopping site using:

- Python3.7.6
- Flask 1.1
- Flask-Admin 1.5.4
- Flask-Mail 0.9.1
- Flask-msearch 0.2.9
- SQLAlchemy 1.3.17


## Run
run.py

## To deploy on Heroku
- To install heroku command
    - brew tap heroku/brew && brew install heroku
- To install psycopg2 to use PostgreSQL via SQLAlchemy
    - conda install -c anaconda psycopg2
- To install gunicorn to run on WSGI server for Python
    - conda install -c anaconda gunicorn
- To export requirements (Didn't use pip freeze to avoid including direct references)
    - pip list --format=freeze > requirements.txt
    *Remove some modules if you face some issues during the installation on heroku
- To create Procfile (this command is used when gunicorn run)
    - create Procfile under the project and include "web: gunicorn run:app"
- To create runtime.txt
    - create runtime.txt under the project and include python version
- To login heroku
    - heroku login
- To create app on heroku
    - heroku create {appname}
- Add addon for postgresql
    - heroku addons:create heroku-postgresql:hobby-dev
- To update database URI for postgres on Heroku
    - SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
- To commit on git (example)
    - git add .
    - git commit
- To push to Heroku
    - git push heroku master
    *Remove some modules on requirements.txt if you face some issues during the installation on heroku
- To check if the DB is PostgreSQL 
    - heroku run python
      - import os
      - a = os.environ.get('DATABASE_URL')
      - print(a)  * you can see the postgres://*****
    - To create table
      - from flaskblog import create_app, db
      - app = create_app()
      - app.app_context().push()
      - db.create_all()
- To use email 
    - heroku config:set MAIL_USERNAME={your username}
    - heroku config:set MAIL_PASSWORD={your password}