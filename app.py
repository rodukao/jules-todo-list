import datetime
from flask import Flask, request, redirect, url_for, render_template

app = Flask(__name__)

tasks = []
next_task_id = 1

@app.route('/')
def view_tasks():
    global tasks
    today = datetime.date.today()
    
    status_filter = request.args.get('status_filter', 'pending')
    date_filter = request.args.get('date_filter', 'all')
    search_query = request.args.get('search_query', '').strip()
    sort_by = request.args.get('sort_by', 'created_at')
    order = request.args.get('order', 'asc')

    # Stage 1: Filter by status
    if status_filter == 'completed':
        processed_tasks = [task for task in tasks if task['status'] == 'Completed']
    elif status_filter == 'pending':
        processed_tasks = [task for task in tasks if task['status'] == 'Pending']
    else: # 'all' or any other value
        status_filter = 'all' # Normalize if an unexpected value was passed
        processed_tasks = list(tasks)

    # Stage 2: Filter by date (applied to the result of status filter)
    if date_filter == 'today':
        processed_tasks = [task for task in processed_tasks if task['due_date'] == today]
    elif date_filter == 'tomorrow':
        tomorrow = today + datetime.timedelta(days=1)
        processed_tasks = [task for task in processed_tasks if task['due_date'] == tomorrow]
    elif date_filter == 'next_7_days':
        next_week = today + datetime.timedelta(days=7)
        processed_tasks = [task for task in processed_tasks if task['due_date'] and today <= task['due_date'] <= next_week]
    elif date_filter == 'overdue':
        # Apply overdue filter: only relevant for pending tasks or all tasks (if status_filter is 'all')
        if status_filter == 'pending' or status_filter == 'all':
            processed_tasks = [task for task in processed_tasks if task['due_date'] and task['due_date'] < today and task['status'] == 'Pending']
        else: # If status_filter is 'completed', overdue filter yields no results
            processed_tasks = [] 
    # 'all' date_filter doesn't need specific logic here

    # Stage 3: Filter by search query (applied to the result of status and date filters)
    if search_query:
        query_lower = search_query.lower()
        temp_tasks = []
        for task in processed_tasks:
            title_match = query_lower in task['title'].lower()
            desc_match = task['description'] and query_lower in task['description'].lower()
            if title_match or desc_match:
                temp_tasks.append(task)
        processed_tasks = temp_tasks

    # Apply sorting to the fully filtered list
    priority_map = {'High': 1, 'Medium': 2, 'Low': 3}

    if sort_by == 'due_date':
        key_func = lambda task: (task['due_date'] is None, task['due_date'])
    elif sort_by == 'priority':
        key_func = lambda task: priority_map.get(task.get('priority'), 4)
    elif sort_by == 'created_at':
        key_func = lambda task: task['created_at']
    else: # Default sort if sort_by is unknown
        sort_by = 'created_at'
        key_func = lambda task: task['created_at']

    reverse_order = (order == 'desc')
    processed_tasks.sort(key=key_func, reverse=reverse_order)

    return render_template('index.html', tasks=processed_tasks, today=today,
                           current_sort_by=sort_by, current_order=order,
                           current_status_filter=status_filter, current_date_filter=date_filter,
                           current_search_query=search_query)

@app.route('/add', methods=['GET', 'POST'])
def add_task():
    global next_task_id, tasks
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
        
        new_task = {
            'id': next_task_id,
            'title': title,
            'description': description,
            'due_date': due_date,
            'priority': priority,
            'status': 'Pending',
            'created_at': datetime.datetime.now()
        }
        tasks.append(new_task)
        next_task_id += 1
        return redirect(url_for('view_tasks', status_filter='pending', date_filter='all'))
    else: # GET request
        return render_template('add_task.html')

@app.route('/toggle_complete/<int:task_id>')
def toggle_complete(task_id):
    global tasks
    for task in tasks:
        if task['id'] == task_id:
            if task['status'] == 'Pending':
                task['status'] = 'Completed'
            elif task['status'] == 'Completed':
                task['status'] = 'Pending'
            break # Exit loop once task is found and updated
    return redirect(url_for('view_tasks'))

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    global tasks
    task_to_edit = None
    for task in tasks:
        if task['id'] == task_id:
            task_to_edit = task
            break
    
    if task_to_edit is None:
        return redirect(url_for('view_tasks'))

    if request.method == 'POST':
        task_to_edit['title'] = request.form.get('title', task_to_edit['title'])
        task_to_edit['description'] = request.form.get('description', task_to_edit['description'])
        due_date_str = request.form.get('due_date')
        if due_date_str: # Only update if a new date is provided
            try:
                task_to_edit['due_date'] = datetime.datetime.strptime(due_date_str, '%Y-%m-%d').date()
            except ValueError:
                # Keep the old date if the new one is invalid
                pass 
        elif 'due_date' in request.form and not due_date_str: # If due_date field was submitted empty
            task_to_edit['due_date'] = None

        task_to_edit['priority'] = request.form.get('priority', task_to_edit['priority'])
        # No need to update 'created_at' or 'id' or 'status' here (status is handled by toggle_complete)
        return redirect(url_for('view_tasks'))
    else: # GET request
        return render_template('edit_task.html', task=task_to_edit)

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    global tasks
    # Find the task by id and remove it
    # Using a list comprehension to rebuild the list excluding the task to delete
    tasks = [task for task in tasks if task['id'] != task_id]
    return redirect(url_for('view_tasks'))

if __name__ == '__main__':
    app.run(debug=True)
