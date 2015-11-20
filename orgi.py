from flask import Flask				                # Import the Flask library
from flask import render_template		            # Importing from templates
from flask import request
from flask import redirect
from flask import g 	    			            # Global Object Variable
from flask import abort
from flask import make_response
from flask import jsonify
import flask
import httplib2
import datetime
from apiclient import discovery
from oauth2client import client
import sqlite3		    			                # SQL Lite


app = flask.Flask(__name__)				                # Creates a new website in a variable

# -------------------------------------------------------------------------------------- #
#				            Opening & Closing the Database				                 #		
# -------------------------------------------------------------------------------------- #
'''
@app.before_request				                    # Connecting with the database before every request 
def before_request():				                # from the browser
    #g.db = sqlite3.connect("emails.db")
    db = sqlite3.connect("emails.db")
    
@app.teardown_request				                # Closing the database after every request
def teardown_request(exception):
    if hasattr(g, 'db'):
        #g.db.close()
        db.close()
'''

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

USER = 0

#	+-----------------------------------------------------------------------+
#	| For database use in the terminal:					                    |
#	| 	run: sqlite3	  						                            |
# 	| in the sqlite mode, 							                        |
#	|  	run: ATTACH DATABASE 'emails.db' as 'email';	            		|
#	| 	run: .database							                            |
# 	| and the database should be listed there		                		|
#	| 	run: .table							                                |
#	| and it should list the tables					                    	|
#	| 	run: SELECT * from email.email_addresses;		                	|
#	| and this will display the contents of the table		            	|
#	|									                                    |
#	| You can send the database contents to a file. In the terminal:	    |
#	| 	run: sqlite3 emails.db .dump > emails.sql			                |
#	|									                                    |
#	| To create a new database, in the terminal:				            |
#	|	run: sqlite3 user_details.db					                    |
#	+-----------------------------------------------------------------------+
				




# Do the entire webpage tutorial instead
		

# -------------------------------------------------------------------------------------- #
# 				                     Login	                         					 #
# -------------------------------------------------------------------------------------- #

@app.route('/')
def index():
    return redirect("/login")

@app.route('/login')					                # Default Address	
def login():
    return render_template('login.html')

@app.route('/signin', methods = ['POST'])
def signin():
    email = request.form['email']
    password = request.form['password']
    print("The email address is '" + email + "'")
    print("The password address is '" + password + "'")

    db = sqlite3.connect("orgy.db")
    db.row_factory = sqlite3.Row

    def query_db(query, args=(), one=False):
        cur = db.execute(query, args)
        rv = cur.fetchall()
        cur.close()
        return (rv[0] if rv else None) if one else rv

    userX = query_db('select * from users where email = ? and password = ?',[email, password], one=True)
    
    cursor = get_db().execute("select * from users where email = ? and password = ?",[email, password])
    user = cursor.fetchall()
    cursor.close()
    
    if userX is None:
        print ('No such user')
        return redirect('/login')
    else:
        print ('Has a user')
        global USER
        USER = (user[0]['id'])
        print (USER)
        flask.session['user'] = USER
        return redirect('/google_auth')


    # Only user is: sean@hotmail.com  with a password of: jeep

# -------------------------------------------------------------------------------------- #
# 				                    Google API Handling				                 	 #
# -------------------------------------------------------------------------------------- #  


@app.route('/google_auth')
def google_auth():
  if 'user' not in flask.session:
    return redirect('/login')
  if 'credentials' not in flask.session:
    return flask.redirect(flask.url_for('oauth2callback'))
  credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
  if credentials.access_token_expired:
    return flask.redirect(flask.url_for('oauth2callback'))
  else:
    http_auth = credentials.authorize(httplib2.Http())
    drive_service = discovery.build('drive', 'v2', http_auth)
    files = drive_service.files().list().execute() 
    return redirect('/home')
    #return "You have accessed the drive successfully ------- "#+json.dumps(files)


@app.route('/oauth2callback')
def oauth2callback():
  flow = client.flow_from_clientsecrets(
      'client_secrets.json',
      scope='https://www.googleapis.com/auth/drive.metadata.readonly',
      redirect_uri=flask.url_for('oauth2callback', _external=True))
  #flow.params['include_granted_scopes'] = True
  if 'code' not in flask.request.args:
    auth_uri = flow.step1_get_authorize_url()
    return flask.redirect(auth_uri)
  else:
    auth_code = flask.request.args.get('code')
    credentials = flow.step2_exchange(auth_code)            
    flask.session['credentials'] = credentials.to_json()
    return flask.redirect(flask.url_for('google_auth'))



# -------------------------------------------------------------------------------------- #
# 				                     Home	                         					 #
# -------------------------------------------------------------------------------------- #

@app.route('/home')					                # Home Address	
def home():
    if 'user' not in flask.session:
      return redirect('/login')
    arguments = (USER,)
    print (arguments)
    cursor = get_db().execute("SELECT * FROM todos WHERE user=?", arguments)
    todos = cursor.fetchall()
    cursor = get_db().execute("SELECT * FROM deadlines WHERE user=?", arguments)
    deadlines_unformatted = cursor.fetchall()
    cursor.close()

    deadlines = deadline_format(deadlines_unformatted)

    return render_template('home.html', todos=todos, deadline=deadlines)


# -------------------------------------------------------------------------------------- #
# 				                     Forums	                         					 #
# -------------------------------------------------------------------------------------- #

@app.route('/forums')					                # Home Address	
def forums():
    if 'user' not in flask.session:
      return redirect('/login')
    return render_template('forums.html')


# -------------------------------------------------------------------------------------- #
# 				                  Note Taking                       					 #
# -------------------------------------------------------------------------------------- #

@app.route('/note_taking')					                # Home Address	
def note_taking():
    if 'user' not in flask.session:
      return redirect('/login')
    return render_template('note_taking.html')

# -------------------------------------------------------------------------------------- #
# 				                       Tasks                          					 #
# -------------------------------------------------------------------------------------- #

@app.route('/tasks', methods=['GET'])
def tasks():
    if 'user' not in flask.session:
      return redirect('/login')
    # Extract data from database and store todos in list
    arguments = (USER,)
    cursor = get_db().execute("SELECT * FROM todos WHERE user=?", arguments)
    todos = cursor.fetchall()
    cursor = get_db().execute("SELECT * FROM deadlines WHERE user=?", arguments)
    deadlines_unformatted = cursor.fetchall()
    cursor.close()

    deadlines = deadline_format(deadlines_unformatted)

    return render_template('to_do.html', todos=todos, deadlines=deadlines)

# -------------------------------------------------------- #
# 	              Request to add new task   	           #
# -------------------------------------------------------- #
@app.route('/tasks/api/create_task', methods=['POST'])
def create_task():
    if 'user' not in flask.session:
      return redirect('/login')
    # Abort if request doesn't exist
    if not request.form or not 'title' in request.form:
        abort(400)

    arguments = (request.form.get("title", None), request.form.get("description", None), USER)
    cursor = get_db().execute("INSERT INTO todos (title, desc, user) VALUES (?, ?, ?)", arguments)
    get_db().commit()
    cursor.close()

    return redirect("/tasks")

# -------------------------------------------------------- #
# 	            Request to add new deadline   	           #
# -------------------------------------------------------- #
@app.route('/tasks/api/create_deadline', methods=['POST'])
def create_deadline():
    if 'user' not in flask.session:
      return redirect('/login')
    # Abort if request doesn't exist
    if not request.form or not 'title' in request.form:
        abort(400)

    arguments = (request.form.get("title", None), request.form.get("date", None), USER)
    cursor = get_db().execute("INSERT INTO deadlines (title, date, user) VALUES (?, ?, ?)", arguments)
    get_db().commit()
    cursor.close()

    return redirect("/tasks")


# -------------------------------------------------------- #
# 	       Toggle a task checkbox   	           #
# -------------------------------------------------------- #
@app.route('/tasks/api/toggle_task/<int:task_id>', methods=['GET'])
def toggle_task(task_id):
    if 'user' not in flask.session:
      return redirect('/login')
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

    return redirect("/tasks")

# -------------------------------------------------------- #
# 	       Request to delete a task   	           #
# -------------------------------------------------------- #
@app.route('/tasks/api/delete_deadline/<int:deadline_id>', methods=['GET'])
def delete_deadline(deadline_id):
    if 'user' not in flask.session:
      return redirect('/login')
    print("Deadline_id = ", deadline_id)
    arguments = (USER, deadline_id)
    cursor = get_db().execute("DELETE FROM deadlines WHERE user=? AND id=?", arguments)
    get_db().commit()
    cursor.close()

    return redirect("/tasks")

# -------------------------------------------------------- #
# 	       Request to delete a _todo   	                    #
# -------------------------------------------------------- #
@app.route('/tasks/api/delete_todo/<int:todo_id>', methods=['GET'])
def delete_todo(todo_id):

    print("todo_id = ", todo_id)
    arguments = (USER, todo_id)
    cursor = get_db().execute("DELETE FROM todos WHERE user=? AND id=?", arguments)
    get_db().commit()
    cursor.close()

    return redirect("/tasks")

# -------------------------------------------------------- #
# 	       Error handler for error 404                 #
# -------------------------------------------------------- #
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

# -------------------------------------------------------- #
# 	       Determine width of deadline bars                #
# -------------------------------------------------------- #
def deadline_format(deadlines):
        # Determining number of days left until deadline
    date_today = datetime.date.today()
    for deadline in deadlines:
        date_elems = deadline['date'].strip().split("/")
        due_date = datetime.date(int(date_elems[2]), int(date_elems[1]), int(date_elems[0]))
        time_left = due_date - date_today
        days_left = time_left.days
        if days_left > 30:
            deadline['date'] = str(days_left)
            deadline['width'] = int(100)
        else:
            deadline['date'] = str(days_left)
            deadline['width'] = int((float(days_left)/float(30))*100)

    return(deadlines)


# -------------------------------------------------------------------------------------- #
# 				                  Drive                      					 #
# -------------------------------------------------------------------------------------- #

@app.route('/drive')					                # Home Address	
def drive():
    if 'user' not in flask.session:
      return redirect('/login')
    return render_template('drive.html')

# -------------------------------------------------------------------------------------- #
# 					                  main      					                	 #
# -------------------------------------------------------------------------------------- #

if __name__ == '__main__':			# If this script it ran, start the web app
    import uuid
    app.secret_key = str(uuid.uuid4())
    app.debug = True
    app.run()
