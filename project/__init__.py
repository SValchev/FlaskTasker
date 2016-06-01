import datetime

from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt


app = Flask(__name__)
app.config.from_object('project._config')
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from project.users.views import users_blueprint
from project.tasks.views import tasks_blueprint
from project.api.views import api_blueprint

@app.errorhandler(404)
def errorhendler_404(error):
    if app.debug is not True:
        now = datetime.datetime.now()
        r = request.url
        with open("error.log", "a") as f:
            f.write("\n error 404 {} : {}".format(r, now))
    return render_template("404.html"), 404


@app.errorhandler(500)
def errorhendler_500(error):
    if app.debug is not True:
        now = datetime.datetime.now()
        r = request.url
        with open("error.log", "a") as f:
            f.write("\n error 500 {} : {}".format(r, now))
    return render_template("500.html"), 500


# register blueprints
app.register_blueprint(users_blueprint)
app.register_blueprint(tasks_blueprint)
app.register_blueprint(api_blueprint)
