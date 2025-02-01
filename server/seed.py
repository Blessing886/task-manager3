from random import randint, choice as rc

# Remote library imports
from models import User, Task, TaskAssignment, Comment, Department

# Local imports
from app import app
from models import db
from datetime import date

with app.app_context():
    print("Deleting existing data...")
    User.query.delete()
    Department.query.delete()
    Task.query.delete()
    TaskAssignment.query.delete()
    Comment.query.delete()
    db.session.commit()
    
    users = []
    departments = []
    tasks = []
    task_assignment = []
    comments = []

    

    # user instances
    print("Creating users...")
    users.append(User(name = 'Nelson Oketch', email = 'nelson@gmail.com', role = 'Manager'))
    users.append(User(name = 'Tina Moraa', email = 'tina@gmail.com', role = 'Manager'))
    users.append(User(name = 'Richard Medo', email = 'medo@gmail.com', role = 'Employee'))
    users.append(User(name = 'Betty Aziz', email = 'betty@gmail.com', role = 'Employee'))
    users.append(User(name = 'Ness Wafula', email = 'ness@gmail.com', role = 'Employee'))
    users.append(User(name = 'Mejju Kombo', email = 'mejju@gmail.com', role = 'Employee'))

    db.session.add_all(users)
    db.session.commit()

    # department instances
    print("Creating departments...")
    departments.append(Department(name = 'Electrical Engineering', description = 'Handles electrical and electronic issues.', manager_id=users[0].id))
    departments.append(Department(name = 'Mechanical Engineering', description = 'Handles mechanical related issues.', manager_id=users[1].id))

    db.session.add_all(departments)
    db.session.commit()

    # assigning users to departments
    print("Assigning users to departments...")
    users[0].department = departments[0]
    users[1].department = departments[1]
    users[2].department = departments[0]
    users[3].department = departments[1]
    users[4].department = departments[0]
    users[5].department = departments[1]

    db.session.commit()

    # Tasks
    print("Creating tasks...")
    tasks.append(Task(
        title = 'Wellheads A3 control valves maintainance',
        description = 'Conduct routine maintanance.',
        status = 'In Progress',
        priority = 'Medium',
        created_by_user_id = users[0].id,
        due_date = date(2025, 2, 13)
    ))

    tasks.append(Task(
        title = 'Wellheads A1 turbine troubleshooting',
        description = 'Determine the cause of increase in vibrations.',
        status = 'Pending',
        priority = 'High',
        created_by_user_id = users[1].id,
        due_date = date(2025, 2, 10)
    ))

    db.session.add_all(tasks)
    db.session.commit()

    # taskassignments
    print("Assigning tasks...")
    task_assignment.append(TaskAssignment(task_id = tasks[0].id, user_id = users[2].id))
    task_assignment.append(TaskAssignment(task_id = tasks[1].id, user_id = users[5].id))

    db.session.add_all(task_assignment)
    db.session.commit()

    # comments
    print("Creating comments...")
    comments.append(Comment(task_id = tasks[0].id, user_id = users[2].id, comment = 'Will be done by end of day.'))
    comments.append(Comment(task_id = tasks[1].id, user_id = users[5].id, comment = 'Assembled the turbine today, waiting for the instrumentations team to complete sensor connections.'))

    db.session.add_all(comments)
    db.session.commit()

    print("Database seeded successfully!") 
