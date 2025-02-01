from alembic import op
import sqlalchemy as sa

# Revision identifiers, used by Alembic.
revision = '830aaeba8175'
down_revision = '67d91087915c'
branch_labels = None
depends_on = None

def upgrade():
    # Create the users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('role', sa.Enum('Manager', 'Employee', name='user_role'), nullable=False),
        sa.Column('department_id', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )

    # Create the departments table
    op.create_table(
        'departments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('manager_id', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['manager_id'], ['users.id'], name='fk_departments_manager_id_users'),
        sa.UniqueConstraint('manager_id')
    )

    # Create the tasks table
    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('status', sa.Enum('Pending', 'In Progress', 'Completed', 'On Hold', name='task_status'), nullable=True),
        sa.Column('priority', sa.String(), nullable=True),
        sa.Column('created_by_user_id', sa.Integer(), nullable=False),
        sa.Column('due_date', sa.Date(), nullable=True),
        sa.Column('comments_text', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['created_by_user_id'], ['users.id'], name='fk_tasks_created_by_user_id_users')
    )

    # Create the task_assignment table
    op.create_table(
        'task_assignment',
        sa.Column('task_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['task_id'], ['tasks.id'], name='fk_task_assignment_task_id_tasks'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='fk_task_assignment_user_id_users'),
        sa.PrimaryKeyConstraint('task_id', 'user_id')
    )

    # Create the comments table
    op.create_table(
        'comments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('task_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('comment', sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['task_id'], ['tasks.id'], name='fk_comments_task_id_tasks'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='fk_comments_user_id_users')
    )

def downgrade():
    # Drop the comments table
    op.drop_table('comments')

    # Drop the task_assignment table
    op.drop_table('task_assignment')

    # Drop the tasks table
    op.drop_table('tasks')

    # Drop the departments table
    op.drop_table('departments')

    # Drop the users table
    op.drop_table('users')