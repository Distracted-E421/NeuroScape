from flask import Flask, render_template, request, redirect, url_for
from db import db, Task, init_db

app = Flask(__name__,)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize db
init_db(app)

@app.route('/')
def index():
    return render_template('src/html/index.html')


@app.route('/create-task', methods=['GET', 'POST'])
def create_task():
    if request.method == 'POST':
        title = request.form['title']
        priority = request.form['priority']
        priority_title = request.form['priority_title']
        priority_color = request.form['priority_color']
        tags = request.form['tags']
        description = request.form['description']
        image = request.form['image']

        task = Task(title=title, priority=priority, priority_title=priority_title, priority_color=priority_color, tags=tags, description=description, image=image)
        db.session.add(task)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('templates/create_task.html')


@app.route('/update-task/<int:task_id>', methods=['GET', 'POST'])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)

    if request.method == 'POST':
        task.title = request.form['title']
        task.priority = request.form['priority']
        task.priority_title = request.form['priority_title']
        task.priority_color = request.form['priority_color']
        task.tags = request.form['tags']
        task.description = request.form['description']
        task.image = request.form['image']

        db.session.commit()

        return redirect(url_for('index'))

    return render_template('update_task.html', task=task)

@app.route('/delete-task/<int:task_id>')
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)

    db.session.delete(task)
    db.session.commit()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)