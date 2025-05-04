from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import text



app = Flask(__name__)

@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/verification', methods=['GET', 'POST'])
def verification():
    if request.method == 'POST':
        return redirect('/password')
    return render_template('Verification.html')

@app.route('/password', methods=['GET', 'POST'])
def password():
    if request.method == 'POST':
        # check passwords match and length
        return redirect('/login')
    return render_template('Password.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        #process of checking the password in database
        return redirect('/dashboard')  
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # process signup form data here
        return redirect('/verification')  # move to verification step
    return render_template('signup.html')


@app.route('/lender', methods=['GET', 'POST'])
def lender():
    if request.method == 'POST':
        #handle logging the infor into the database
        return redirect('dashboard')
    return render_template('lender.html')

@app.route('/borrower')
def borrower():
    return render_template('borrower.html')

@app.route('/email_verification',methods=['GET','POST'])
def email_verification():
    if request.method == 'POST':
        #logic of verifying email
        return redirect('password')
    return render_template('Verification.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/userprofile')
def userprofile():
    return render_template('userprofile.html')



if __name__ == '__main__':
    app.run(debug=True)
