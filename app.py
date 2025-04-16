from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('HomePage.html')

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
    return render_template('login_verification.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # process signup form data here
        return redirect('/verification')  # move to verification step
    return render_template('signup.html')


@app.route('/lender')
def lender():
    return render_template('Lender.html')

@app.route('/borrower')
def borrower():
    return render_template('Borrower.html')

@app.route('/email_verification')
def email_verification():
    return render_template('EmailVerification.html')

@app.route('/dashboard')
def dashboard():
    return render_template('DashBoard.html')



if __name__ == '__main__':
    app.run(debug=True)
