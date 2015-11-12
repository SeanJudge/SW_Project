from flask import Flask				                # Import the Flask library
from flask import render_template		            # Importing from templates
from flask import request
from flask import redirect
from flask import g 	    			            # Global Object Variable
import sqlite3		    			                # SQL Lite

app = Flask(__name__)				                # Creates a new website in a variable

# -------------------------------------------------------------------------------------- #
#				            Opening & Closing the Database				                 #		
# -------------------------------------------------------------------------------------- #

@app.before_request				                    # Connecting with the database before every request 
def before_request():				                # from the browser
    #g.db = sqlite3.connect("emails.db")
    db = sqlite3.connect("emails.db")
    
@app.teardown_request				                # Closing the database after every request
def teardown_request(exception):
    if hasattr(g, 'db'):
        #g.db.close()
        db.close()

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
def hello_world():
    return 'Hello World!'

@app.route('/login')					                # Default Address	
def login():
    return render_template('login.html')

@app.route('/signin', methods = ['POST'])
def signin():
    email = request.form['email']
    password = request.form['password']
    print("The email address is '" + email + "'")
    print("The password address is '" + password + "'")

    db = sqlite3.connect("emails.db")
    db.row_factory = sqlite3.Row

    def query_db(query, args=(), one=False):
       	cur = db.execute(query, args)
       	rv = cur.fetchall()
       	cur.close()
       	return (rv[0] if rv else None) if one else rv
    
    user = query_db('select * from details where email = ? and password = ?',[email, password], one=True)

    if user is None:
        print ('No such user')
        return redirect('/login')
    else:
        print ('Has a user')
        return redirect('/home')


		# Only user is: sean@hotmail.com  with a passoword of: jeep

# -------------------------------------------------------------------------------------- #
# 				                     Home	                         					 #
# -------------------------------------------------------------------------------------- #

@app.route('/home')					                # Home Address	
def home():
    return render_template('home.html')



# -------------------------------------------------------------------------------------- #
# 				                  Note Taking                       					 #
# -------------------------------------------------------------------------------------- #

@app.route('/note_taking')					                # Home Address	
def note_taking():
    return render_template('note_taking.html')


# -------------------------------------------------------------------------------------- #
# 					                  main      					                	 #
# -------------------------------------------------------------------------------------- #

if __name__ == '__main__':			# If this script it ran, start the web app 
    app.run()
