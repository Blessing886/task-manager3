from flask import Flask, request, jsonify
from flask_restful import Resource
from datetime import date

# Local imports
from config import app, db
from models import User, Department, Task, TaskAssignment, Comment



@app.route('/')
def index():
    return '<h1>Project Server</h1>'

@app.route('/users', methods=['GET'])
def get_users():
    search_term = request.args.get('q', '').lower()
    users = User.query.all()
    if search_term:
        users = [user for user in users if search_term in user.name.lower() or search_term in user.email.lower()]
    users_data = []
    for user in users:
        user_data = {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'role': user.role,
            'department_id': user.department_id,
            'department': {
                'id': user.department.id,
                'name': user.department.name,
                'description': user.department.description,
                'manager_id': user.department.manager_id
            } if user.department else None
            
        }
        users_data.append(user_data)
    return jsonify(users_data), 200

@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if user:
        user_data = {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'role': user.role,
            'department_id': user.department_id,
            'department': {
                'id': user.department.id,
                'name': user.department.name,
                'description': user.department.description,
                'manager_id': user.department.manager_id
            } if user.department else None
        }
        return jsonify(user_data), 200
    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()

    if not data or not all(key in data for key in ['name', 'email', 'role']):
        return jsonify({"error": "Missing required fields: name, email, role"}), 400
    
    try:
        new_user = User(
            name=data['name'],
            email=data['email'],
            role=data['role'],
            department_id=data.get('department_id')
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User created successfully", "id": new_user.id}), 201
    except Exception as err:
        db.session.rollback()
        return jsonify({"error": str(err)}), 500

@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    data = request.get_json()
    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    user.role = data.get('role', user.role)
    user.department_id = data.get('department_id', user.department_id)
    
    try:
        db.session.commit()
        return jsonify({"message": "User updated successfully"}), 200
    except Exception as err:
        db.session.rollback()
        return jsonify({"error": str(err)}), 500

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully"}), 200
    except Exception as err:
        db.session.rollback()
        return jsonify({"error": str(err)}), 500
    
# Department routes

@app.route('/departments', methods=['GET'])
def get_departments():
    search_term = request.args.get('q', '').lower()
    departments = Department.query.all()

    if search_term:
        departments = [dept for dept in departments if search_term in dept.name.lower() or
                       search_term in dept.description.lower()]

    departments_data = []
    for department in departments:
        department_data = {
            'id': department.id,
            'name': department.name,
            'description': department.description,
            'manager_id': department.manager_id,
            'manager': {
                'id': department.manager.id,
                'name': department.manager.name
            } if department.manager else None 
        }
        departments_data.append(department_data)
    return jsonify(departments_data), 200

@app.route('/departments/<int:id>', methods=['GET'])
def get_department(id):
    department = Department.query.get(id)
    if department:
        department_data = {
            'id': department.id,
            'name': department.name,
            'description': department.description,
            'manager_id': department.manager_id,
            'manager': {
                'id': department.manager.id,
                'name': department.manager.name
            } if department.manager else None 
        }
        return jsonify(department_data), 200
    else:
        return jsonify({"error": "Department not found"}), 404
    
@app.route('/departments', methods=['POST'])
def create_department():
    data = request.get_json()
    if not data or not all(key in data for key in ['name', 'description', 'manager_id']):
        return jsonify({"error": "Missing required fields: name, description, manager_id"}), 400
    
    try:
        new_department = Department(
            name=data['name'],
            description=data['description'],
            manager_id=data['manager_id']
        )
        db.session.add(new_department)
        db.session.commit()
        
        return jsonify({"message": "Department created successfully", "id": new_department.id}), 201
    except Exception as err:
        db.session.rollback()
        return jsonify({"error": str(err)}), 500
    
@app.route('/departments/<int:id>', methods=['PUT'])
def update_department(id):
    department = Department.query.get(id)
    
    if not department:
        return jsonify({"error": "Department not found"}), 404
    
    data = request.get_json()
    department.name = data.get('name', department.name)
    department.description = data.get('description', department.description)
    department.manager_id = data.get('manager_id', department.manager_id)
    
    try:
        db.session.commit()
        return jsonify({"message": "Department updated successfully"}), 200
    except Exception as err:
        db.session.rollback()
        return jsonify({"error": str(err)}), 500
    
@app.route('/departments/<int:id>', methods=['DELETE'])
def delete_department(id):
    department = Department.query.get(id)
    
    if not department:
        return jsonify({"error": "Department not found"}), 404
    
    try:
        db.session.delete(department)
        db.session.commit()
        return jsonify({"message": "Department deleted successfully"}), 200
    except Exception as err:
        db.session.rollback()
        return jsonify({"error": str(err)}), 500
    
# task routes
@app.route('/tasks', methods=['GET'])
def get_tasks():
    search_term = request.args.get('q', '').lower()
    tasks = Task.query.all()
    if search_term:
        tasks = [task for task in tasks if search_term in task.title.lower() or
                 search_term in task.description.lower()]
        
    tasks_data = []
    for task in tasks:
        task_data = {
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'status': task.status,
            'priority': task.priority,
            'created_by': {
                'id': task.created_by.id,
                'name': task.created_by.name
            },
            'assigned_users': [
                {'id': user.id, 'name': user.name} for user in task.assigned_users
            ],
            'due_date': task.due_date,
            'comments_text': task.comments_text,
            'comments': [
                {'id': comment.id, 'comment': comment.comment} for comment in task.comments
            ]
        }
        tasks_data.append(task_data)
    return jsonify(tasks_data), 200

@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    task = Task.query.get(id)
    if task:
        task_data = {
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'status': task.status,
            'priority': task.priority,
            'created_by_user_id': task.created_by_user_id,
            'created_by': {
                'id': task.created_by.id,
                'name': task.created_by.name
            },
            'assigned_users': [
                {'id': user.id, 'name': user.name} for user in task.assigned_users
            ],
            'due_date': task.due_date,
            'comments_text': task.comments_text,
            'comments': [
                {'id': comment.id, 'comment': comment.comment} for comment in task.comments
            ]
        }
        return jsonify(task_data), 200
    else:
        return jsonify({"error": "Task not found"}), 404

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    if not data or not all(key in data for key in ['title', 'description', 'status', 'priority', 'created_by_user_id']):
        return jsonify({"error": "Missing required fields: title, description, status, priority, created_by_user_id"}), 400

    try:
        due_date = data.get('due_date')
        if due_date:
            due_date = date.fromisoformat(due_date)

        new_task = Task(
            title=data['title'],
            description=data.get('description', ''),
            status=data['status'],
            priority=data.get('priority', ''),
            created_by_user_id=data['created_by_user_id'],
            due_date=due_date,
            comments_text=data.get('comments_text', '')
        )
        db.session.add(new_task)
        db.session.commit()

        if 'assigned_users' in data:
            for user_id in data['assigned_users']:
                task_assignment = TaskAssignment(task_id=new_task.id, user_id=user_id)
                db.session.add(task_assignment)

        db.session.commit()
        return jsonify({"message": "Task created successfully", "id": new_task.id}), 201
    except Exception as err:
        db.session.rollback()
        return jsonify({"error": str(err)}), 500
    
@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    data = request.get_json()
    task = Task.query.get(id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.status = data.get('status', task.status)
    task.priority = data.get('priority', task.priority)
    due_date_str = data.get('due_date')
    if due_date_str:
        try:
            task.due_date = date.fromisoformat(due_date_str)
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400 
    task.comments_text = data.get('comments_text', task.comments_text)
    try:
        db.session.commit()
        if 'assigned_users' in data:
            task.assigned_users.clear()
            for user_id in data['assigned_users']:
                task_assignment = TaskAssignment(task_id=task.id, user_id=user_id)
                db.session.add(task_assignment)

        db.session.commit()
        return jsonify({"message": "Task updated successfully"}), 200
    except Exception as err:
        db.session.rollback()
        return jsonify({"error": str(err)}), 500
    
@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get(id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    try:
        db.session.delete(task)
        db.session.commit()
        return jsonify({"message": "Task deleted successfully"}), 200
    except Exception as err:
        db.session.rollback()
        return jsonify({"error": str(err)}), 500
    
# taskassignment
@app.route('/tasks/<int:task_id>/assignments', methods=['POST'])
def add_task_assignment(task_id):
    data = request.get_json()
    user_id = data.get('user_id')
    
    if not user_id:
        return jsonify({"error": "Missing user_id"}), 400
    
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    existing_assignment = TaskAssignment.query.filter_by(task_id=task_id, user_id=user_id).first()
    if existing_assignment:
        return jsonify({"message": "User already assigned to this task"}), 200
    task_assignment = TaskAssignment(task_id=task.id, user_id=user_id)
    db.session.add(task_assignment)
    db.session.commit()
    
    return jsonify({"message": "User assigned to task successfully"}), 201

@app.route('/tasks/<int:task_id>/assignments/<int:user_id>', methods=['DELETE'])
def remove_task_assignment(task_id, user_id):
    task = Task.query.get(task_id)
    
    if not task:
        return jsonify({"error": "Task not found"}), 404
    
    task_assignment = TaskAssignment.query.filter_by(task_id=task_id, user_id=user_id).first()
    if not task_assignment:
        return jsonify({"error": "Assignment not found"}), 404

    db.session.delete(task_assignment)
    db.session.commit()
    
    return jsonify({"message": "User assignment removed successfully"}), 200

# comment routes
@app.route('/tasks/<int:task_id>/comments', methods=['GET'])
def get_comments(task_id):
    comments = Comment.query.filter_by(task_id=task_id).all()
    if not comments:
        return jsonify({"message": "No comments found for this task"}), 200

    comments_list = [
        {"id": com.id, "user_id": com.user_id, "comment": com.comment} for com in comments]
    return jsonify(comments_list), 200

@app.route('/tasks/<int:task_id>/comments', methods=['POST'])
def add_comment(task_id):
    data = request.get_json()
    user_id = data.get('user_id')
    comment_text = data.get('comment')

    if not user_id or not comment_text:
        return jsonify({"error": "Missing required fields: user_id, comment"}), 400

    new_comment = Comment(task_id=task_id, user_id=user_id, comment=comment_text)
    db.session.add(new_comment)
    db.session.commit()

    return jsonify({"message": "Comment added successfully", "id": new_comment.id}), 201

@app.route('/comments/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    comment = Comment.query.get(comment_id)

    if not comment:
        return jsonify({"error": "Comment not found"}), 404

    db.session.delete(comment)
    db.session.commit()

    return jsonify({"message": "Comment deleted successfully"}), 200

# route to get tasks and comments for a user
@app.route('/users/<int:user_id>/tasks', methods=['GET'])
def get_user_tasks(user_id):
    tasks = Task.query.filter(Task.assigned_users.any(id=user_id)).all()
    tasks_data = [
        {
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'status': task.status,
            'priority': task.priority,
            'due_date': task.due_date,
            'comments': [
                {
                    'id': comment.id,
                    'comment': comment.comment,
                    'user_id': comment.user_id,
                    'task_id': comment.task_id
                } for comment in task.comments
            ] if task.comments else []
        } for task in tasks
    ]
    return jsonify(tasks_data), 200

@app.route('/users/<int:user_id>/comments', methods=['GET'])
def get_user_comments(user_id):
    comments = Comment.query.filter_by(user_id=user_id).all()
    comments_data = [
        {
            'id': comment.id,
            'comment': comment.comment,
            'user_id': comment.user_id,
            'task_id': comment.task_id
        } for comment in comments
    ]
    return jsonify(comments_data), 200

if __name__ == '__main__':
    app.run(port=5555, debug=True)
