import os
import random

basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE = 'flasktaskr.db'
CSRF_ENABLED = True
SECRET_KEY = b'6y\xa9\xdeP\xdfLhJ\x0f\x1b\x8e\xe6\xd0\xb0\x07\x89\n\xc8\\z\xe1\x93\xe4'

DATABASE_PATH = os.path.join(basedir, DATABASE)

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH
