"""
This module is to run application for flaskblog
"""

from flaskblog import db, create_app


app = create_app()
# from flask_script import Manager


# manager = Manager(app)
# @manager.command

if __name__ == '__main__':
    # app = create_app()
    # ctx = app.app_context()
    # ctx.push()
    # db.create_all()
    app.run(debug=True)


"""
In order to initiate SQL, need to command below
To access sql ser

1) Make sure to activate the appropriate virtual environment to work
   with all needed packages.
2) Open a Python interpreter at the root of your project directory
   (in the same directory as run.py).
3) Execute the following code (without comments if you wish):

from flaskblog import create_app, db
app = create_app()
# context to run outside the application (no need to launch the server)
ctx = app.app_context()
ctx.push()  # start working on database after that command

# Database manipulations here
# ...
ctx.pop()  # exit from the app
exit()
"""
