from flask import Flask 
from flask import render_template
from flask import request
from flask import redirect
from flask import g 	    # Global Variable
import sqlite3		    # SQL Lite

app = Flask(__name__)

# -------------------------------------------------------------------------------------- #
#				Opening & Closing the Database				 #		
# -------------------------------------------------------------------------------------- #

@app.before_request
def before_request():
    g.db = sqlite3.connect("emails.db")

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

# -------------------------------------------------------------------------------------- #
# 					Login Page					 #
# -------------------------------------------------------------------------------------- #

@app.route('/login', methods = ['POST'])                             		
def login():
    email_entry     =  request.form['email']							# Taking the email entry 
    password_entry  =  request.form['password']		                             		# Taking the password entry 
    print("The email address is '" + email + "'")
    #email           =  g.db.execute("SELECT email FROM email_addresses").fetchall()		# 
    #password        =  g.db.execute("SELECT password_entry FROM passwords").fetchall()		# 

    #if password_entry == password:
    #    return redirect('/home')
    #else:
    #    return render_template('login.html')

# -------------------------------------------------------------------------------------- #
# 					Home Page					 #
# -------------------------------------------------------------------------------------- #

@app.route('/home')					
def home():
    return render_template('home.html')
    
    
    
    

# -------------------------------------------------------------------------------------- #	

@app.route('/signup', methods = ['POST'])		# Signup Page
def signup():
    email = request.form['email']			# Taking the email entry 
    g.db.execute("INSERT INTO email_addresses VALUES (?)", [email])
    g.db.commit()					# Saves the email address
    return redirect('/')
    
@app.route('/unregister', methods = ['POST'])
def unregister():
    if 'email' not in session:				# Make sure they've already registered an email address
        return "You haven't submitted an email!"
    email = session['email']
    if email not in email_addresses:			# Make sure it was already in our address list
        return "That address isn't on our list"
    email_addresses.remove(email)			# Remove th email from the list
    del session['email'] 				# Make sure to remove it from the session
    return 'We have removed ' + email + ' from the list!'   
   
@app.route('/emails.html')
def emails():
    email_addresses = g.db.execute("SELECT email FROM email_addresses").fetchall()
    return render_template('emails.html', email_addresses=email_addresses)   

	
if __name__ == '__main__':
     app.run()
