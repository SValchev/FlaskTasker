from flask import render_template, redirect, flash, url_for, request, session, Blueprint
from functools import wraps
from .forms import AddTaskForm
from project.models import Task
from project import db
from datetime import datetime

###########
##configs##
###########

tasks_blueprint = Blueprint("tasks", __name__)


####################
##helper functions##
####################

def get_open_tasks():
    result = db.session.query(Task)

    if session["role"] != "admin":
        result = result.filter_by(user_id=session["current_user"])

    return result.filter_by(status='1').order_by(
        Task.due_date.asc()).order_by(Task.prioraty.asc())


def get_closed_tasks():
    result = db.session.query(Task)

    if session["role"] != "admin":
        result = result.filter_by(user_id=session["current_user"])

    return result.filter_by(status='0').order_by(
        Task.due_date.asc()).order_by(Task.prioraty.asc())


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash("Error in the {} field - {}".format(getattr(form, field).label.text, error), "error")


def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash("You need to logg in first!")
            return redirect(url_for('users.login'))

    return wrap


#################
##route handels##
#################

@tasks_blueprint.route('/tasks/')
@login_required
def tasks():
    open_tasks = get_open_tasks()

    closed_tasks = get_closed_tasks()

    return render_template(
        'tasks.html',
        form=AddTaskForm(request.form),
        open_tasks=open_tasks,
        closed_tasks=closed_tasks,
        username=session["user_name"]
    )


@tasks_blueprint.route('/add/', methods=['POST'])
def add():
    form = AddTaskForm(request.form)
    error = None

    if request.method == 'POST':
        if form.validate_on_submit():
            name = request.form['name']
            due_date = datetime.strptime(request.form['due_date'], '%m/%d/%Y')
            prioraty = request.form['prioraty']

            print(due_date)

            new_task = Task(
                name=name,
                due_date=due_date,
                poste_date=datetime.utcnow(),
                prioraty=prioraty,
                status='1',
                user_id=session['current_user'],
            )

            db.session.add(new_task)
            db.session.commit()

            flash("New task has been added succsefully!")
            return redirect(url_for('tasks.tasks'))
        else:
            return render_template(
                'tasks.html',
                open_tasks=get_open_tasks(),
                closed_tasks=get_closed_tasks(),
                error=error, form=form
            )

    return render_template('tasks.html', form=form)


@tasks_blueprint.route('/complete/<int:current_task_id>/')
@login_required
def complete(current_task_id):
    current_task = db.session.query(Task).filter_by(task_id=current_task_id)
    if session['current_user'] == current_task.first().user_id or session["user_role"] == "admin":
        current_task.update({'status': '0'})
        db.session.commit()
        flash("Task has been marked as complete succsefully!")
        return redirect(url_for('tasks.tasks'))

    flash("You can not mark as complete task that does not belong to you!")
    return redirect(url_for('tasks.tasks'))


@tasks_blueprint.route('/delete/<int:current_task_id>')
@login_required
def delete(current_task_id):
    current_task = db.session.query(Task).filter_by(task_id=current_task_id)
    if session['current_user'] == current_task.first().user_id or session["user_role"] == "admin":
        current_task.delete()
        db.session.commit()
        flash("Task has been removed succsefully!")
        return redirect(url_for('tasks.tasks'))

    flash("You can not delete task that does not belong to you!")
    return redirect(url_for('tasks.tasks'))
