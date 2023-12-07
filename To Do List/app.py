from flask import Flask, request, render_template, redirect, url_for
from datetime import datetime

app = Flask(__name__)
tasks = []
next_id = 0

@app.route('/', methods=['GET', 'POST'])
def index():
    global next_id
    if request.method == 'POST':
        task_content = request.form['task']
        # Check if the task already exists
        if task_content and not any(task['description'] == task_content for task in tasks):
            new_task = {'id': next_id, 'description': task_content, 'completed': False, 'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            tasks.append(new_task)
            next_id += 1
        # Optionally, you can handle the case where the task already exists
    return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task['id'] != task_id]
    return redirect(url_for('index'))

@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    for task in tasks:
        if task['id'] == task_id:
            task['completed'] = not task['completed']
            break
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)