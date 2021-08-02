from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

# DATABASE MODEL CLASS
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # RETURN ID OF NEW QUERY CREATED
    def __repr__(self):
        return '<Task %r>' % self.id

# INDEX PAGE ROUTE
@app.route('/', methods=['POST', 'GET'])
def index():
    selected = []
    clones   = []
    if request.method == 'POST':
        task_content = None
        selected     = None

        # SEE IF A NEW  QUERY WAS ADDED OR IF 
        # QUERIES WERE SELECTED TO BE CLONED 
        try:
            task_content = request.form['task']
            new_task = Todo(task=task_content)
        except:
            selected = request.form.getlist('selected')
            print(selected)

        # QUERY ADDED
        if task_content:   
            try:
                db.session.add(new_task)
                db.session.commit()
                return redirect('/')
            except:
                return 'Error at adding task'
        
        # QUERIES SELECTED TO BE DELETED (NOW CLONED)
        elif selected:
            tasks = Todo.query.order_by(Todo.id).all()
            
            # CONVERT STR LIST INTO INT LIST
            for i in range(0, len(selected)):
                selected[i] = int(selected[i])

            for task in tasks:
                if task.id in selected:
                    clones.append(task)
            
            return render_template('index.html', tasks=tasks, clones=clones)
        
        #    for id in selected:
        #        delete(id)
        #    return redirect("/")
    
        else:
            return 'Error at processing query'

    # DISPLAY ALL RECORDS FROM DATABASE
    else:
        tasks = Todo.query.order_by(Todo.id).all()
        return render_template('index.html', tasks = tasks)

# DELETE QUERIES
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'Error at deleting task', task_to_delete

# MAIN
if __name__ == '__main__':
    app.run(debug=True)