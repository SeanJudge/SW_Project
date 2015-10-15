from flask import Flask, render_template, request, redirect
app = Flask(__name__)

email_addresses = []

@app.route('/')
def home():
    author = "Sean Judge"
    name   = "Brian Waters"
    return render_template('index.html', author = author, name = name)
	
@app.route('/signup', methods = ['POST'])
def signup():
    email = request.form['email']
    email_addresses.append(email)
    session['email'] = email
    print(email_addresses)
    return redirect('/')
    
@app.route('/unregister', methods = ['POST'])
def unregister():
    if 'email' not in session:				# Make sure they've already registered an email address
        return "You haven't submitted an email!"
    email = session['email']
    if email not in email_addresses:			# Make sure it was already in our address list
        return "That address isn't on our list"
    email_addresses.remove(email)
    del session['email'] 				# Make sure to remove it from the session
    return 'We have removed ' + email + ' from the list!'   
   
   
@app.route('/emails.html')
def emails():
    return render_template('emails.html', email_addresses = email_addresses)
	
if __name__ == '__main__':
     app.run()
