# Flask Task List Application

## About
A simple web-based task list application built with Python (Flask) and HTML/CSS/JavaScript.

## Features
- **Add Tasks**: Create tasks with a title (mandatory), description, due date, and priority (High, Medium, Low).
- **View Tasks**:
    - List all tasks with their title, priority, due date, status, and description.
    - Visual cues for task priority (colored borders).
    - Visual cues for overdue tasks (red and bold due date).
- **Edit Tasks**: Modify any detail of an existing task.
- **Complete Tasks**: Mark tasks as 'Completed' or revert to 'Pending'. Completed tasks are visually distinct (grayed out, line-through).
- **Delete Tasks**: Remove tasks from the list with a confirmation prompt.
- **Filtering**:
    - By Status: View 'All Tasks', 'Pending' tasks, or 'Completed' tasks.
    - By Due Date: Filter tasks due 'Today', 'Tomorrow', 'Next 7 Days', or those that are 'Overdue'.
    - Filters can be combined (e.g., "Pending tasks due Today").
- **Sorting**:
    - Sort tasks by 'Due Date', 'Priority', or 'Creation Date'.
    - Sorting can be done in 'Ascending' or 'Descending' order.
    - Sorting works in conjunction with active filters.
- **Search**:
    - Search tasks by keywords found in their title or description.
    - Search works in conjunction with active filters and sorting.
- **Responsive (Basic)**: The application has a basic layout that should be usable on different screen sizes, though not extensively optimized.

## Setup and Installation
1.  **Prerequisites**:
    *   Python 3.x
    *   Flask (can be installed via pip)
2.  **Clone the repository (if applicable)**:
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```
3.  **Install dependencies**:
    ```bash
    pip install Flask
    ```
4.  **Running the Application**:
    ```bash
    python app.py
    ```
    The application will usually be available at `http://127.0.0.1:5000/` in your web browser.

## Updated File Structure
```
/
|-- app.py               # Main Flask application logic, routes, and data handling
|-- templates/
|   |-- index.html       # Main page to display tasks
|   |-- add_task.html    # Form to add a new task
|   |-- edit_task.html   # Form to edit an existing task
|-- static/
|   |-- estilo.css       # CSS styles for the application
|   |-- theme.js         # JavaScript for theme toggling
|-- README.md            # This file
```

## Future Enhancements (Not Implemented)
-   User accounts and authentication.
-   Persistent storage (e.g., using SQLite or another database instead of in-memory storage).
-   Subtasks.
-   Reminders/Notifications.
-   More advanced UI/UX with dedicated CSS frameworks and JavaScript interactions.
