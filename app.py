from flask import Flask, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'  # Define o caminho para o banco de dados SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Define the Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    due_date = db.Column(db.Date, nullable=True)
    priority = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(20), default='Pending')
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

# Create the database tables
with app.app_context():
    db.create_all()

@app.route('/all_tasks')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/')
def view_tasks():
    today = datetime.date.today()

    status_filter = request.args.get('status_filter', 'pending')
    date_filter = request.args.get('date_filter', 'all')
    search_query = request.args.get('search_query', '').strip()
    sort_by = request.args.get('sort_by', 'created_at')
    order = request.args.get('order', 'asc')

    # Start with all tasks
    query = Task.query

    # Stage 1: Filter by status
    if status_filter == 'completed':
        query = query.filter_by(status='Completed')
    elif status_filter == 'pending' or status_filter == 'all':  # 'all' now behaves like 'pending'
        query = query.filter_by(status='Pending')

    # Stage 2: Filter by date
    if date_filter == 'today':
        query = query.filter(Task.due_date == today)
    elif date_filter == 'tomorrow':
        tomorrow = today + datetime.timedelta(days=1)
        query = query.filter(Task.due_date == tomorrow)
    elif date_filter == 'next_7_days':
        next_week = today + datetime.timedelta(days=7)
        query = query.filter(Task.due_date.between(today, next_week))
    elif date_filter == 'overdue':
        query = query.filter(Task.due_date < today, Task.status == 'Pending')

    # Stage 3: Filter by search query
    if search_query:
        query = query.filter(
            (Task.title.ilike(f"%{search_query}%")) |
            (Task.description.ilike(f"%{search_query}%"))
        )

    # Stage 4: Apply sorting
    if sort_by == 'due_date':
        if order == 'asc':
            query = query.order_by(Task.due_date.asc())
        else:
            query = query.order_by(Task.due_date.desc())
    elif sort_by == 'priority':
        priority_order = db.case(
            [(Task.priority == 'High', 1), (Task.priority == 'Medium', 2), (Task.priority == 'Low', 3)],
            else_=4
        )
        if order == 'asc':
            query = query.order_by(priority_order)
        else:
            query = query.order_by(priority_order.desc())
    else:  # Default to created_at
        if order == 'asc':
            query = query.order_by(Task.created_at.asc())
        else:
            query = query.order_by(Task.created_at.desc())

    tasks = query.all()

    return render_template('index.html', tasks=tasks, today=today,
                           current_sort_by=sort_by, current_order=order,
                           current_status_filter=status_filter, current_date_filter=date_filter,
                           current_search_query=search_query)

@app.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        due_date_str = request.form.get('due_date')
        priority = request.form.get('priority', 'Medium') # Default to 'Medium'

        if not title:
            # For now, let's assume title is always provided or handle error later
            pass

        due_date = None
        if due_date_str:
            try:
                due_date = datetime.datetime.strptime(due_date_str, '%Y-%m-%d').date()
            except ValueError:
                # Handle invalid date format if necessary, for now, it will be None
                pass
        
        new_task = Task(
            title=title,
            description=description,
            due_date=due_date,
            priority=priority,
            status='Pending',
            created_at=datetime.datetime.now()
        )
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('view_tasks', status_filter='pending', date_filter='all'))
    else: # GET request
        return render_template('add_task.html')

@app.route('/toggle_complete/<int:task_id>')
def toggle_complete(task_id):
    task = Task.query.get(task_id)
    if task:
        task.status = 'Completed' if task.status != 'Completed' else 'Pending'
        db.session.commit()
    return redirect(url_for('view_tasks'))

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    task_to_edit = Task.query.get(task_id)
    
    if task_to_edit is None:
        return redirect(url_for('view_tasks'))

    if request.method == 'POST':
        task_to_edit.title = request.form.get('title', task_to_edit.title)
        task_to_edit.description = request.form.get('description', task_to_edit.description)
        due_date_str = request.form.get('due_date')
        if due_date_str: # Only update if a new date is provided
            try:
                task_to_edit.due_date = datetime.datetime.strptime(due_date_str, '%Y-%m-%d').date()
            except ValueError:
                # Keep the old date if the new one is invalid
                pass 
        elif 'due_date' in request.form and not due_date_str: # If due_date field was submitted empty
            task_to_edit.due_date = None

        task_to_edit.priority = request.form.get('priority', task_to_edit.priority)
        # No need to update 'created_at' or 'id' or 'status' here (status is handled by toggle_complete)
        db.session.commit()
        return redirect(url_for('view_tasks'))
    else: # GET request
        return render_template('edit_task.html', task=task_to_edit)

@app.route('/delete_task/<int:task_id>', methods=['GET'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/completed_tasks')
def completed_tasks():
    tasks = Task.query.filter_by(status='Completed').all()
    return render_template('index.html', tasks=tasks)

if __name__ == '__main__':
    app.run(debug=True)
