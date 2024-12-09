from flask import Flask, render_template,url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
basedir = os.path.abspath(os.path.dirname(__file__))


app= Flask(__name__)

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String,DateTime
engine = create_engine('sqlite:///todo.db', echo = True)
meta = MetaData()

Todo_l = Table(
   'todo', meta, 
    Column('id',Integer,primary_key=True),
    Column('content',String(200),nullable=False),
    Column('completed',Integer, default=0),
    Column('date_created',DateTime, default=datetime.utcnow),
)
conn = engine.connect()
#ins = students.insert().values(name = 'Ravi', lastname = 'Kapoor')
#conn = engine.connect()
#result = conn.execute(ins)



'''
'''
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+ os.path.join(basedir, 'test.db')
db=SQLAlchemy(app)

class Todo(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    content = db.Column(db.String(200),nullable=False)
    completed =db.Column(db.Integer, default=0)
    date_created =db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id
'''
'''

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        print("lol")
        tasks = Todo.query.order_by(Todo.date_created).all()
        '''        
        tasks = engine.connect().execute(Todo_l.select().order_by(Todo.date_created))
        print(tasks)'''
        print('fuck')
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task)



if __name__ == "__main__":
    app.run(debug=True)