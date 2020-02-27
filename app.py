from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return '<Task %r>' % self.id

    def to_json(self):
        return '{' \
               '"id": self.id' \
               '"content": self.content' \
               '"completed": self.completed' \
               '"date_created": self.date_created' \
               '}'


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        if task_content == '':
            task_content = 123
        new_task = Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding the form'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>', methods=['GET'])
def delete(id):
    to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'Couldn\'t delete'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    to_update = Todo.query.get_or_404(id)
    if request.method == 'GET':
        # return render_template('update.html', task=json.dumps({"id": to_update.id, "content": to_update.content, "completed": to_update.completed, "date_created": to_update.date_created}))
        return render_template('update.html', task=to_update)
    elif request.method == 'POST':
        to_update.content = request.form['content']
        to_update.completed = request.form['completed']
        db.session.commit()
        return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
