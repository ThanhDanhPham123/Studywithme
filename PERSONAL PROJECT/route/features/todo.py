from flask import render_template, url_for, request, redirect, Blueprint,session
from datetime import datetime
from db import db
from auth import login_required

todo = Blueprint('todo', __name__)

# Model for the to-do list
class TodoItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    deadline = db.Column(db.DateTime, nullable=True)
    completed = db.Column(db.Boolean, default=False)

@todo.route("/to_do_list", methods=["GET", "POST"])
@login_required
def todo_view():
    if request.method == "POST":
        task = request.form["task"]
        deadline_str = request.form.get("deadline") # Get the deadline from the form, if provided
        deadline = datetime.strptime(deadline_str, "%Y-%m-%d") if deadline_str else None # Convert the deadline string to a datetime object, or None if not provided
        # Create a new task and add it to the database
        new_task = TodoItem(task=task, deadline=deadline)
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for("todo.todo_view"))
    # Sort the tasks by deadline, with nulls last
    todos = TodoItem.query.order_by(
        TodoItem.deadline.asc().nullslast()
    ).all()
    username = session.get('username')
    return render_template('todo.html', todos=todos,username=username)

@todo.route("/todo/delete/<int:todo_id>")
@login_required
def delete_task(todo_id):
    task = TodoItem.query.get_or_404(todo_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("todo.todo_view"))