from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import Integer, String
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# Initialize object without passing the app
db = SQLAlchemy()

# Flask app configuration here
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy with the app
db.init_app(app)


class User(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String)


# Define Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(100))

    complete = db.Column(db.Boolean, default=False)

    priority = db.Column(db.Integer, default=5)
    priority_title = db.Column(db.String(100))
    priority_color = db.Column(db.String(100))

    tags = db.Column(db.String(100))

    description = db.Column(db.String(1000))

    image = db.Column(db.String(100))

    # Initialize new Task instance
    def __init__(self, title, priority=5, priority_title="", priority_color="", tags="", description="", image=""):
        self.title = title
        self.priority = priority
        self.priority_title = priority_title
        self.priority_color = priority_color
        self.tags = tags
        self.description = description
        self.image = image

    def __repr__(self):
        return "<Task: {}>".format(self.title)

# Route for the index page
@app.route('/')
def index():
    # Query all tasks from the database
    task_list = Task.query.all()
    # Render index.html and pass the task list
    return render_template('front/index.html', task_list=task_list)


@app.route("/users/create", methods=["GET", "POST"])
def user_create():
    if request.method == "POST":
        user = User(
            username=request.form["username"],
            email=request.form["email"],
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("user_detail", id=user.id))

    return render_template("front/pages/users/create.html")


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

    return render_template('front/index.html')

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

    return render_template('front/index.html', task=task)

@app.route('/delete-task/<int:task_id>')
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)

    db.session.delete(task)
    db.session.commit()

    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Initialize the database
    app.run(debug=True)