from flask import Flask				# Import the Flask library
from flask import render_template		# Importing from templates
from flask import request
from flask import redirect
from flask import g 	    			# Global Object Variable
import sqlite3		    			# SQL Lite

app = Flask(__name__)				# Creates a new website in a variable

# -------------------------------------------------------------------------------------- #
#				Opening & Closing the Database				 #		
# -------------------------------------------------------------------------------------- #

@app.before_request				# Connecting with the database before every request 
def before_request():				# from the browser
    g.db = sqlite3.connect("emails.db")

@app.teardown_request				# Closing the database after every request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

#	+-----------------------------------------------------------------------+
#	| For database use in the terminal:					|
#	| 	run: sqlite3	  						|
# 	| in the sqlite mode, 							|
#	|  	run: ATTACH DATABASE 'emails.db' as 'email';			|
#	| 	run: .database							|
# 	| and the database should be listed there				|
#	| 	run: .table							|
#	| and it should list the tables						|
#	| 	run: SELECT * from email.email_addresses;			|
#	| and this will display the contents of the table			|
#	|									|
#	| You can send the database contents to a file. In the terminal:	|
#	| 	run: sqlite3 emails.db .dump > emails.sql			|
#	|									|
#	| To create a new database, in the terminal:				|
#	|	run: sqlite3 user_details.db					|
#	+-----------------------------------------------------------------------+
				




# Do the entire webpage tutorial instead
		

# -------------------------------------------------------------------------------------- #
# 					Login						 #
# -------------------------------------------------------------------------------------- #

@app.route('/login')					# Default Address	
def login():
    return render_template('login.html')


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/signin', methods = ['POST'])
def signin():
    email = request.form['email']
    password = request.form['password']
    print("The email address is '" + email + "'")
    print("The password address is '" + password + "'")

    #g.db.execute("INSERT INTO details VALUES (?,?)", [email, password])
    #g.db.commit()
    
    #for row in g.db.execute("SELECT * FROM details"):    
	#line = g.db.fetchone()
	#print line
        #print line[0]
        #print line[1]
        #if line[0] == email:
         #   if line[1] == password:
          #      return redirect('/')

    row = cur.fetchone()
    print row



    #pswrd = g.db.execute("SELECT password FROM details WHERE email=?", email)
    #print("The email address is '" + email + "'")
    #print("The password address is '" + password + "'")
    
    return redirect('/login')



# -------------------------------------------------------------------------------------- #
# 					main						 #
# -------------------------------------------------------------------------------------- #

if __name__ == '__main__':			# If this script it ran, start the web app 
    app.run()
