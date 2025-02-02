# TASK MANAGEMENT SYSTEM SERVER

--Blessing Okora

## Overview

This is a Flask-based task management application server that allows users to manage tasks, departments, and user assignments. The application uses PostgreSQL as the database and Flask-SQLAlchemy for relational mapping. The server is designed to run from the server directory in the project structure.

## Features

- User Management: Create, read, update, and delete users.
- Department Management: Manage departments and assign managers.
- Task Management: Create, assign, update, and delete tasks.
- Task Assignment: Assign tasks to users and manage task assignments.
- Comments: Add and delete comments on tasks.
- Search Functionality: Search for users, departments, and tasks by name or description.

## View Deployed Site

- Visit the deployed application at : [task-manager3] (https://task-manager3-cl1c.onrender.com)

## Technologies Used

- Flask: A lightweight WSGI web application framework.
- PostgreSQL: A powerful, open-source relational database system.
- SQLAlchemy: A SQL toolkit and ORM for Python.
- Flask-Migrate: Handles SQLAlchemy database migrations for Flask applications.
- Flask-CORS: Enables Cross-Origin Resource Sharing (CORS) for Flask applications.

## Project Structure

## Getting Started

### Prerequisites
- Python(at least version 3.8.13) and Pip installed in your machine.

### Installation
- Clone the repository: https://github.com/Blessing886/task-manager3.git
- Navigate into the "task-manager3" repository.
- Install dependacies
```bash
pip install -r requirements.txt
```
- cd into server directory.
- Install PostgreSQL and create a new database.
- Set the DATABASE_URI environment variable to point to your PostgreSQL database.
- Run migrations
```
flask db init
flask db migrate
flask db upgrade
```
- Seed the database by running:
```
python seed.py
```
- Run the server:
```
gurnicorn app:app
```

### Database models
- The application uses the following models:
- User: Represents a user with attributes like name, email, role, and department.
- Department: Represents a department with attributes like name, description, and manager.
- Task: Represents a task with attributes like title, description, status, priority, and due date.
- TaskAssignment: Represents the many-to-many relationship between tasks and users.
- Comment: Represents comments made by users on tasks.

### API Endpoints

#### Users
- GET /users: Get all users (by name or email).
- GET /users/<int:id>: Get a specific user by ID.
- POST /users: Create a new user.
- PUT /users/<int:id>: Update an existing user.
- DELETE /users/<int:id>: Delete a user.

#### Departments
-GET /departments: Get all departments.
- GET /departments/<int:id>: Get a specific department by ID.
- POST /departments: Create a new department.
- PUT /departments/<int:id>: Update an existing department.
- DELETE /departments/<int:id>: Delete a department.

#### Tasks
- GET /tasks: Get all tasks.
- GET /tasks/<int:id>: Get a specific task by ID.
- POST /tasks: Create a new task.
- PUT /tasks/<int:id>: Update an existing task.
- DELETE /tasks/<int:id>: Delete a task. 

#### Task Assignments
- POST /tasks/<int:task_id>/assignments: Assign a user to a task.
- DELETE /tasks/<int:task_id>/assignments/<int:user_id>: Remove a user from a task.

#### Comments
- GET /tasks/<int:task_id>/comments: Get all comments for a task.
- POST /tasks/<int:task_id>/comments: Add a comment to a task.
- DELETE /comments/<int:comment_id>: Delete a comment.

#### User Tasks and Comments
- GET /users/<int:user_id>/tasks: Get all tasks assigned to a user.
- GET /users/<int:user_id>/comments: Get all comments made by a user.

## Related Repositories

- Repository: [task-manager-frontend repository] (https://github.com/Blessing886/task-manager-frontend.git)
- Deployed site: [live url] (https://task-bridge.netlify.app/)

## Licence

MIT License

Copyright (c) 2025 Blessing Okora

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.