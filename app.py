from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import text



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Kingck2020.@localhost/LoanSystem'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
#Database models
# Models mapped to your existing database tables
class User(db.Model):
    __tablename__ = 'User'
    
    User_ID = db.Column(db.String(8), primary_key=True)
    First_Name = db.Column(db.String(20), nullable=False)
    Last_Name = db.Column(db.String(20), nullable=False)
    Email = db.Column(db.String(60), nullable=False, unique=True)
    phone_number = db.Column(db.Integer, unique=True)
    user_password = db.Column(db.String(10), nullable=False)
    BankName = db.Column(db.String(50))
    BankAccount = db.Column(db.String(12), unique=True)
    code_name = db.Column(db.String(5), unique=True)
    credit_score = db.Column(db.Float)
    
    # Relationships
    loans_as_borrower = db.relationship('Loan', backref='borrower', foreign_keys='Loan.borrower_ID')
    loans_as_lender = db.relationship('Loan', backref='lender', foreign_keys='Loan.lender_ID')
    verifications = db.relationship('Verification', backref='user')
    
    def __repr__(self):
        return f'<User {self.User_ID}: {self.First_Name} {self.Last_Name}>'


class Loan(db.Model):
    __tablename__ = 'Loan'
    
    loan_ID = db.Column(db.Integer, primary_key=True)
    borrower_ID = db.Column(db.String(8), db.ForeignKey('User.User_ID'))
    lender_ID = db.Column(db.String(8), db.ForeignKey('User.User_ID'))
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    duration_months = db.Column(db.Integer, nullable=False)
    loan_status = db.Column(db.Enum('pending', 'approved', 'Rejected', 'Disbursed', 'settled'))
    date_requested = db.Column(db.Date)
    date_disbursed = db.Column(db.Date)
    purpose = db.Column(db.Enum('healthcare', 'transportation', 'recreation', 'charity', 'other'), nullable=False)
    
    # Relationships
    repayments = db.relationship('RepaymentSchedule', backref='loan')
    transactions = db.relationship('Transactions', backref='loan')
    
    def __repr__(self):
        return f'<Loan {self.loan_ID}: {self.amount} - {self.loan_status}>'


class RepaymentSchedule(db.Model):
    __tablename__ = 'RepaymentSchedule'
    
    repayment_ID = db.Column(db.Integer, primary_key=True)
    loan_ID = db.Column(db.Integer, db.ForeignKey('Loan.loan_ID'), nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    amount_due = db.Column(db.Numeric(10, 2), nullable=False)
    loan_status = db.Column(db.Enum('paid', 'pending', 'late'), nullable=False)
    
    def __repr__(self):
        return f'<Repayment {self.repayment_ID} for Loan {self.loan_ID}: {self.amount_due}>'


class Transactions(db.Model):
    __tablename__ = 'Transactions'
    
    transaction_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    transaction_type = db.Column(db.Enum('loan Release', 'Repayment'), nullable=False)
    loan_ID = db.Column(db.Integer, db.ForeignKey('Loan.loan_ID'))
    transaction_date = db.Column(db.Date, nullable=False)
    
    def __repr__(self):
        return f'<Transaction {self.transaction_ID}: {self.transaction_type}>'


class Verification(db.Model):
    __tablename__ = 'Verification'
    
    verification_ID = db.Column(db.Integer, primary_key=True)
    User_ID = db.Column(db.String(8), db.ForeignKey('User.User_ID'))
    email = db.Column(db.String(100), nullable=False)
    verification_code = db.Column(db.String(100))
    expiry_date = db.Column(db.Date)
    
    def __repr__(self):
        return f'<Verification {self.verification_ID} for User {self.User_ID}>'



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


@app.route('/lender', methods=['GET', 'POST'])
def lender():
    if request.method == 'POST':
        #handle logging the infor into the database
        return redirect('dashboard')
    return render_template('Lender_page.html')

@app.route('/borrower')
def borrower():
    return render_template('Borrower.html')

@app.route('/email_verification',methods=['GET','POST'])
def email_verification():
    if request.method == 'POST':
        #logic of verifying email
        return redirect('password')
    return render_template('EmailVerification.html')

@app.route('/dashboard')
def dashboard():
    return render_template('DashBoard.html')



if __name__ == '__main__':
    app.run(debug=True)
