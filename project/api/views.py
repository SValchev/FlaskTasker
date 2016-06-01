from functools import wraps

from flask import url_for, redirect, Blueprint, render_template, flash, session, jsonify,make_response

from project import db
from project.models import Task

############
## config ##
############

api_blueprint = Blueprint('api', __name__)


######################
## helper functions ##
######################

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if "logged_in" in session:
            return test(*args, **kwargs)
        else:
            flash("You need to log in first!")
            return redirect(url_for("users.login"))

    return wrap


def open_tasks():
    return db.session.query(Task).filter_by(status='1').order_by(Task.due_date.asc())


def closed_tasks():
    return db.session.query(Task).filter_by(status='0').order_by(Task.due_date.asc())


############
## routes ##
############

@api_blueprint.route("/api/v1/tasks")
def api_tasks():
    results = db.session.query(Task).limit(10).offset(0).all()
    json_result = []

    for result in results:
        data = {
            "task_id": result.task_id,
            "name": result.name,
            "due date": str(result.due_date),
            "poste date": str(result.poste_date),
            "prioraty": result.prioraty,
            "status": result.status
        }

        json_result.append(data)

    return jsonify(items=json_result)


@api_blueprint.route("/api/v1/tasks/<int:task_id>")
def api_tasks_id(task_id):
    result = db.session.query(Task).filter_by(task_id=task_id).first()

    if result:
        json_result = {
            "task_id": result.task_id,
            "name": result.name,
            "due date": str(result.due_date),
            "poste date": str(result.poste_date),
            "prioraty": result.prioraty,
            "status": result.status}

        code = 200
    else:
        result = {"error": "No element with that kind of id"}
        code = 404
    return make_response(result=result,code=code)
