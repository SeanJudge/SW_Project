from flask import Flask, render_template, request, redirect
app = Flask(__name__)

email_addresses = []

@app.route('/login')                             	# Login Page
def login():
    return render_template('login.html')

@app.route('/')						# Homepage
def home():
    return render_template('index.html')
	
@app.route('/signup', methods = ['POST'])		# Signup Page
def signup():
    email = request.form['email']			# Taking the email entry 
    email_addresses.append(email)			# Adding the email onto the list
    session['email'] = email				# Adding the email to the session	
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
    return render_template('emails.html', email_addresses = email_addresses)
	
if __name__ == '__main__':
     app.run()
