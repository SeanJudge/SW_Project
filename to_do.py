#!flask/bin/python
import flask
from flask import Flask, jsonify, abort, make_response, request, url_for, render_template, redirect
import sqlite3
import datetime
from flask import g # flask global context

app = Flask(__name__)

# -------------------------------------------------------- #
# 	            Database functions   	           #
# -------------------------------------------------------- #

# Used to convert contents of database in to usable rows
def dict_factory(cursor, row):
    result_dict = {}
    for index, column in enumerate(cursor.description):
        result_dict[column[0]] = row[index]
    return result_dict

# Obtain handle to database
def get_db():
    db = getattr(g, 'orgy_database', None)
    if db is None:
        db = g.orgy_database = sqlite3.connect("orgy.db")
        db.row_factory = dict_factory
    return db

# Closing connection to database
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, 'orgy_database', None)
    if db is not None:
        db.close()

# Default user for database until I can distinguish between users
USER = 1

# -------------------------------------------------------- #
# 	                Default root    	           #
# -------------------------------------------------------- #
@app.route('/', methods=['GET'])
def index():
    # Extract data from database and store todos in list
    arguments = (USER,)
    cursor = get_db().execute("SELECT * FROM todos WHERE user=?", arguments)
    todos = cursor.fetchall()
    cursor = get_db().execute("SELECT * FROM deadlines WHERE user=?", arguments)
    deadlines = cursor.fetchall()

    # Determining number of days left until deadline
    date_today = datetime.date.today()
    for deadline in deadlines:
        date_elems = deadline['date'].strip().split("/")
        due_date = datetime.date(int(date_elems[2]), int(date_elems[1]), int(date_elems[0]))
        time_left = due_date - date_today
        days_left = time_left.days
        if days_left > 30:
            deadline['date'] = str(days_left)
            deadline['width'] = str(100)
        else:
            deadline['date'] = str(days_left)
            deadline['width'] = int((float(days_left)/float(30))*100)

    cursor.close()

    return render_template('to_do.html', todos=todos, deadlines=deadlines)      # Render to_do page and pass tasks to be processed by Jinja script


# -------------------------------------------------------- #
# 	       Request for to add new task   	           #
# -------------------------------------------------------- #
@app.route('/todo/api/create_task', methods=['POST'])
def create_task():
    # Abort if request doesn't exist
    if not request.form or not 'title' in request.form:
        abort(400)

    arguments = (request.form.get("title", None), request.form.get("description", None), USER)
    cursor = get_db().execute("INSERT INTO todos (title, desc, user) VALUES (?, ?, ?)", arguments)
    get_db().commit()
    cursor.close()

    return redirect("/")

# -------------------------------------------------------- #
# 	       Request for to add new deadline   	           #
# -------------------------------------------------------- #
@app.route('/todo/api/create_deadline', methods=['POST'])
def create_deadline():
    # Abort if request doesn't exist
    if not request.form or not 'title' in request.form:
        abort(400)

    arguments = (request.form.get("title", None), request.form.get("date", None), USER)
    cursor = get_db().execute("INSERT INTO deadlines (title, date, user) VALUES (?, ?, ?)", arguments)
    get_db().commit()
    cursor.close()

    return redirect("/")


# -------------------------------------------------------- #
# 	       Toggle a task checkbox   	           #
# -------------------------------------------------------- #
@app.route('/todo/api/toggle_task/<int:task_id>', methods=['GET'])
def toggle_task(task_id):

    arguments = (USER, task_id)
    cursor = get_db().execute("SELECT status FROM todos WHERE user=? AND id=?", arguments)
    todo = cursor.fetchall()
    cursor.close()

    if len(todo) == 0:
        abort(404)

    new_status = todo[0]['status'] ^ 1

    arguments = (new_status, USER, task_id)
    cursor = get_db().execute("UPDATE todos SET status=? WHERE user=? AND id=?", arguments)
    get_db().commit()
    cursor.close()

    return redirect("/")

# -------------------------------------------------------- #
# 	       Request to delete a task   	           #
# -------------------------------------------------------- #
@app.route('/todo/api/delete_task/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})

# -------------------------------------------------------- #
# 	       Error handler for error 404                 #
# -------------------------------------------------------- #
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

# -------------------------------------------------------- #
# 		           Main	         	           #
# -------------------------------------------------------- #  
if __name__ == '__main__':
    app.run(debug=True)
