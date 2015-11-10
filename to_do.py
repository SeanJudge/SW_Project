#!flask/bin/python
import flask
from flask import Flask, jsonify, abort, make_response, request, url_for, render_template

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
@app.route('/')
def index():
    #return flask.redirect(flask.url_for('get_tasks'))
    return render_template('to_do.html')

# -------------------------------------------------------- #
# 	       Request for task list     	           #
# -------------------------------------------------------- #
@app.route('/todo/api/get_tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': [make_public_task(task) for task in tasks]})

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
    return jsonify({'task': task}), 201

# -------------------------------------------------------- #
# 	       Request to edit a task   	           #
# -------------------------------------------------------- #
@app.route('/todo/api/update_task/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.form:
        abort(400)
    if 'title' in request.form and type(request.form['title']) != unicode:
        abort(400)
    if 'description' in request.form and type(request.form['description']) is not unicode:
        abort(400)
    if 'done' in request.form and type(request.form['done']) is not bool:
        abort(400)
    task[0]['title'] = request.form.get('title', task[0]['title'])
    task[0]['description'] = request.form.get('description', task[0]['description'])
    task[0]['done'] = request.form.get('done', task[0]['done'])
    return jsonify({'task': task[0]})

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
# 	      Public helper version of a task              #
# -------------------------------------------------------- #
def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id=task['id'], _external=True)
        else:
            new_task[field] = task[field]
    return new_task

# -------------------------------------------------------- #
# 		           Main	         	           #
# -------------------------------------------------------- #  
if __name__ == '__main__':
    app.run(debug=True)
