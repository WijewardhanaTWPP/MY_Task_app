#Imports
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime as DateTime

#my app 
app = Flask(__name__)
Scss(app, static_dir='static', asset_dir='assets')
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)

#Data class(Row of data)
class Mytask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    complete = db.Column(db.Integer, default=0)
    date = db.Column(db.DateTime, default=DateTime.utcnow)
    def __repr__(self):
        return f"Task {self.id}"


#Home route
@app.route('/')
def index():
    return render_template('index.html')

# Add a new task
@app.route('/', methods=['POST'])
def add_task():
    current_task = request.form['content']
    new_task = Mytask(content=current_task)
    db.session.add(new_task)
    db.session.commit()
    return redirect("/")

# Get all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Mytask.query.order_by(Mytask.date).all()
    return render_template('show.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete_task(id: int):
    task_delete = Mytask.query.get_or_404(id)
    try:
        db.session.delete(task_delete)
        db.session.commit()
        return redirect('/tasks')
    except:
        return "There was a problem deleting that task"
    
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_task(id: int):
    task = Mytask.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/tasks')
        except:
            return "There was a problem updating that task"
    else:
        return render_template('edit.html', task=task)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    app.run(host="0.0.0.0", port=5000, debug=True)