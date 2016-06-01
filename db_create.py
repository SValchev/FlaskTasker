from project import db, bcrypt

from project.models import User

db.drop_all()

print(db.create_all())

db.session.add(User(username="admin", email="admin@admin.admin", password=bcrypt.generate_password_hash("admin")))
db.session.add(User(username="user", email="user@user.user", password=bcrypt.generate_password_hash("user")))

print(db)

db.session.commit()


# with sqlite3.connect(DATABASE_PATH) as connection:
#     cursor = connection.cursor()
#
#     #Create table
#     cursor.execute("""
#     CREATE TABLE tasks
#     (task_id INTEGER PRIMARY KEY AUTOINCREMENT,
#     name TEXT NOT NULL,
#     due_date TEXT NOT NULL,
#     prioraty INTEGER NOT NULL,
#     status INTEGER NOT NULL)
#     """)
#
#     #Insert Dummmies
#     dummies = [
#     ("Finish this tutorial", "03/25/2015", 10, 1),
#     ("Finish RealPython 2", "03/25/2015", 10, 1)
#     ]
#
#     cursor.executemany("""
#     INSERT INTO tasks(name, due_date, prioraty, status)
#     VALUES(?, ?, ?, ?)
#     """, dummies)
