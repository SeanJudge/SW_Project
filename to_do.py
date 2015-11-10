#!flask/bin/python
import flask
from flask import Flask, jsonify, abort, make_response, request, url_for, render_template, redirect

app = Flask(__name__)


# -------------------------------------------------------- #
# 	  Task structure(To be implemented in database)    #
# -------------------------------------------------------- #
tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]

# -------------------------------------------------------- #
# 	                Default root    	           #
# -------------------------------------------------------- #
@app.route('/', methods=['GET'])
def index():
    return render_template('to_do.html', tasks=tasks)

# -------------------------------------------------------- #
# 	       Request for task list     	           #
# -------------------------------------------------------- #
@app.route('/todo/api/get_tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': [task for task in tasks]})

# -------------------------------------------------------- #
# 	       Request for specific task      	           #
# -------------------------------------------------------- #
@app.route('/todo/api/get_task/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})


# -------------------------------------------------------- #
# 	       Request for to add new task   	           #
# -------------------------------------------------------- #
@app.route('/todo/api/create_task', methods=['POST'])
def create_task():
    if not request.form or not 'title' in request.form:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.form['title'],
        'description': request.form.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return redirect("/")

# -------------------------------------------------------- #
# 	       Toggle a task checkbox   	           #
# -------------------------------------------------------- #
@app.route('/todo/api/toggle_task/<int:task_id>', methods=['GET'])
def toggle_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]  #

    if len(task) == 0:
        abort(404)

    task[0]['done'] = not task[0]['done']
    
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
