from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from flask import jsonify

from config import db

# Models go here!
class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    role = db.Column(db.Enum('Manager', 'Employee', name='user_role'), nullable=True)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))

    # Relationships
    department = db.relationship('Department', back_populates='users', foreign_keys=[department_id])
    created_tasks = db.relationship('Task', back_populates='created_by')
    assigned_tasks = db.relationship('Task', secondary='task_assignment', back_populates='assigned_users')
    comments = db.relationship('Comment', back_populates='user')
    managed_department = db.relationship('Department', back_populates='manager', foreign_keys='Department.manager_id')

class Department(db.Model, SerializerMixin):
    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
    manager_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=True)

    # relationships
    manager = db.relationship('User', back_populates='managed_department', foreign_keys=[manager_id])
    users = db.relationship('User', back_populates='department', foreign_keys=[User.department_id])

class Task(db.Model, SerializerMixin):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.Enum('Pending', 'In Progress', 'Completed', 'On Hold', name='task_status'))
    priority = db.Column(db.String)
    created_by_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    due_date = db.Column(db.Date)
    comments_text = db.Column(db.Text)

    # relationships
    created_by = db.relationship('User', back_populates='created_tasks')
    assigned_users = db.relationship('User', secondary='task_assignment', back_populates='assigned_tasks')
    comments = db.relationship('Comment', back_populates='task')

class TaskAssignment(db.Model, SerializerMixin):
    __tablename__ = 'task_assignment'

    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)

class Comment(db.Model, SerializerMixin):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    comment = db.Column(db.Text, nullable=False)

    # relationships
    task = db.relationship('Task', back_populates='comments')
    user = db.relationship('User', back_populates='comments')

