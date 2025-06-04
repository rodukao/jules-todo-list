from flask import Flask, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'  # Define o caminho para o banco de dados SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# MODELO DE LISTA
class TaskList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    color = db.Column(db.String(20), nullable=True)
    tasks = db.relationship('Task', backref='task_list', lazy=True)

# Adiciona o campo de lista na Task
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    due_date = db.Column(db.Date, nullable=True)
    priority = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(20), default='Pending')
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    list_id = db.Column(db.Integer, db.ForeignKey('task_list.id'), nullable=True)

# CRIAÇÃO DAS TABELAS
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
    selected_id = request.args.get('selected', type=int)
    list_id = request.args.get('list_id', type=int)

    # Determinar o nome do filtro ativo
    if status_filter == 'pending' and date_filter == 'all':
        page_title = 'Pendentes'
    elif status_filter == 'pending' and date_filter == 'today':
        page_title = 'Hoje'
    elif status_filter == 'pending' and date_filter == 'next_7_days':
        page_title = 'Próximos 7 Dias'
    elif status_filter == 'pending' and date_filter == 'overdue':
        page_title = 'Vencidas'
    elif status_filter == 'completed' and date_filter == 'all':
        page_title = 'Concluídas'
    else:
        page_title = 'Tarefas'

    query = Task.query
    if list_id:
        query = query.filter(Task.list_id == list_id)
    if status_filter == 'completed':
        query = query.filter_by(status='Completed')
    elif status_filter == 'pending' or status_filter == 'all':
        query = query.filter_by(status='Pending')
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
    if search_query:
        query = query.filter(
            (Task.title.ilike(f"%{search_query}%")) |
            (Task.description.ilike(f"%{search_query}%"))
        )
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
    else:
        if order == 'asc':
            query = query.order_by(Task.created_at.asc())
        else:
            query = query.order_by(Task.created_at.desc())
    tasks = query.all()
    selected_task = None
    if selected_id:
        selected_task = Task.query.get(selected_id)
    all_lists = TaskList.query.all()
    selected_list = None
    if list_id:
        selected_list = TaskList.query.get(list_id)

    # Contadores para filtros
    counts = {
        'pendentes': Task.query.filter_by(status='Pending').count(),
        'hoje': Task.query.filter(Task.status=='Pending', Task.due_date==today).count(),
        'proximos_7': Task.query.filter(Task.status=='Pending', Task.due_date.between(today, today+datetime.timedelta(days=7))).count(),
        'vencidas': Task.query.filter(Task.status=='Pending', Task.due_date < today).count(),
        'concluidas': Task.query.filter_by(status='Completed').count(),
        'listas': {lista.id: Task.query.filter(Task.list_id==lista.id).count() for lista in TaskList.query.all()}
    }

    return render_template(
        'index.html',
        tasks=tasks,
        today=today,
        current_sort_by=sort_by,
        current_order=order,
        current_status_filter=status_filter,
        current_date_filter=date_filter,
        current_search_query=search_query,
        selected_task=selected_task,
        page_title=page_title,
        all_lists=all_lists,
        selected_list_id=list_id,
        selected_list=selected_list,
        counts=counts
    )

@app.route('/add', methods=['POST'])
def add_task():
    title = request.form.get('title')
    description = request.form.get('description')
    due_date_str = request.form.get('due_date')
    priority = request.form.get('priority', 'Medium')
    list_id = request.form.get('list_id', type=int)

    if not title:
        # Não adiciona tarefa sem título
        return redirect(url_for('view_tasks'))

    due_date = None
    if due_date_str:
        try:
            due_date = datetime.datetime.strptime(due_date_str, '%Y-%m-%d').date()
        except ValueError:
            pass

    new_task = Task(
        title=title,
        description=description,
        due_date=due_date,
        priority=priority,
        status='Pending',
        created_at=datetime.datetime.now(),
        list_id=list_id if list_id else None
    )
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('view_tasks', status_filter='pending', date_filter='all'))

@app.route('/toggle_complete/<int:task_id>', methods=['POST'])
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
        if due_date_str:
            try:
                task_to_edit.due_date = datetime.datetime.strptime(due_date_str, '%Y-%m-%d').date()
            except ValueError:
                pass
        elif 'due_date' in request.form and not due_date_str:
            task_to_edit.due_date = None
        task_to_edit.priority = request.form.get('priority', task_to_edit.priority)
        list_id = request.form.get('list_id', type=int)
        task_to_edit.list_id = list_id if list_id else None
        db.session.commit()
        return redirect(url_for('view_tasks'))
    else:
        all_lists = TaskList.query.all()
        return render_template('edit_task.html', task=task_to_edit, all_lists=all_lists)

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

@app.route('/layout_temp')
def layout_temp():
    today = datetime.date.today()

    status_filter = request.args.get('status_filter', 'pending')
    date_filter = request.args.get('date_filter', 'all')
    search_query = request.args.get('search_query', '').strip()
    sort_by = request.args.get('sort_by', 'created_at')
    order = request.args.get('order', 'asc')
    selected_id = request.args.get('selected', type=int)

    # Start with all tasks
    query = Task.query

    # Stage 1: Filter by status
    if status_filter == 'completed':
        query = query.filter_by(status='Completed')
    elif status_filter == 'pending' or status_filter == 'all':
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
    selected_task = None
    if selected_id:
        selected_task = Task.query.get(selected_id)

    return render_template(
        'layout_temp.html',
        tasks=tasks,
        today=today,
        current_sort_by=sort_by,
        current_order=order,
        current_status_filter=status_filter,
        current_date_filter=date_filter,
        current_search_query=search_query,
        selected_task=selected_task,
        page_title=None
    )

@app.route('/add_list', methods=['POST'])
def add_list():
    name = request.form.get('name')
    description = request.form.get('description')
    color = request.form.get('color')
    if not name:
        return redirect(url_for('view_tasks'))
    new_list = TaskList(name=name, description=description, color=color)
    db.session.add(new_list)
    db.session.commit()
    return redirect(url_for('view_tasks'))

@app.route('/select_list/<int:list_id>')
def select_list(list_id):
    return redirect(url_for('view_tasks', list_id=list_id))

@app.route('/edit_list/<int:list_id>', methods=['POST'])
def edit_list(list_id):
    lista = TaskList.query.get(list_id)
    if not lista:
        return redirect(url_for('view_tasks'))
    lista.name = request.form.get('name', lista.name)
    lista.description = request.form.get('description', lista.description)
    lista.color = request.form.get('color', lista.color)
    db.session.commit()
    return redirect(url_for('view_tasks', list_id=list_id))

@app.route('/delete_list/<int:list_id>')
def delete_list(list_id):
    lista = TaskList.query.get(list_id)
    if lista:
        # Atualiza as tarefas para ficarem sem lista
        Task.query.filter_by(list_id=list_id).update({Task.list_id: None})
        db.session.delete(lista)
        db.session.commit()
    return redirect(url_for('view_tasks'))

if __name__ == '__main__':
    app.run(debug=True)
