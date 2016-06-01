from datetime import datetime

from project import db


class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)
    tasks = db.relationship('Task', backref='poster')

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        self.role = "user"

    def __repr__(self):
        return 'User: {}'.format(self.username)

    def __str__(self):
        return self.__repr__()


class Task(db.Model):
    __tablename__ = "tasks"

    task_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    poste_date = db.Column(db.Date, default=datetime.utcnow())
    prioraty = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    def __init__(self, name, due_date, poste_date, prioraty, status, user_id):
        self.name = name
        self.due_date = due_date
        self.poste_date = poste_date
        self.prioraty = prioraty
        self.status = status
        self.user_id = user_id

    def __repr__(self):
        return "<name {}>".format(self.name)

    def __str__(self):
        return self.__repr__()
