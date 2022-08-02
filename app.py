from flask import Flask,render_template,url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'    #telling our app where the database is located

db = SQLAlchemy(app)  #initializing our database

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return f"{self.content} completed!!"


@app.route("/", methods = ["POST", "GET"])
def Task():
    if request.method == "POST":
        content = request.form["content"]

        task = Todo(content = content)
        try:
            db.session.add(task)
            db.session.commit()
            return redirect("/")
        except:
            return "Error!!"
    else:
        tasks = Todo.query.order_by("date_created")

        return render_template("home.html", tasks = tasks)


@app.route("/delete/<int:id>/")
def deleteTask(id):
    task = Todo.query.get(id)

    try:
        db.session.delete(task)
        db.session.commit()
        return redirect("/")
    except:
        return "A problem occurred deleting the task"


@app.route("/update/<int:id>/", methods = ["GET", "POST"])
def updateTask(id):
    task = Todo.query.get(id)
    if request.method == "POST":
        task.content = request.form["content"]
        
        try:
            db.session.commit()
            return redirect("/")
        except:
            return "Error occurred while updating task"

    else:
        return render_template("update.html", task = task)


if __name__ == "__main__":
    app.run(debug = True)



