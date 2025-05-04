from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import random
import string
import os
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
app.secret_key = os.urandom(24)




# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Kingck2020.@localhost/LoanSystem2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Models
class User(db.Model):
    __tablename__ = 'User'
    User_ID = db.Column(db.String(8), primary_key=True)
    First_Name = db.Column(db.String(20), nullable=False)
    Last_Name = db.Column(db.String(20), nullable=False)
    Email = db.Column(db.String(60), nullable=False, unique=True)
    phone_number = db.Column(db.Integer, unique=True)
    user_password = db.Column(db.String(255), nullable=False)  # Hashed password needs more space
    BankName = db.Column(db.String(50))
    BankAccount = db.Column(db.String(12), unique=True)
    code_name = db.Column(db.String(5), unique=True)
    credit_score = db.Column(db.Float)
    
    # Relationships
    loans_as_borrower = db.relationship('Loan', foreign_keys='Loan.borrower_ID', backref='borrower')
    loans_as_lender = db.relationship('Loan', foreign_keys='Loan.lender_ID', backref='lender')
    verifications = db.relationship('Verification', backref='user')

class Loan(db.Model):
    __tablename__ = 'Loan'
    loan_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    borrower_ID = db.Column(db.String(8), db.ForeignKey('User.User_ID'))
    lender_ID = db.Column(db.String(8), db.ForeignKey('User.User_ID'))
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    duration_months = db.Column(db.Integer, nullable=False)
    loan_status = db.Column(db.Enum('pending', 'approved', 'Rejected', 'Disbursed', 'settled'))
    date_requested = db.Column(db.Date, default=datetime.now().date())
    date_disbursed = db.Column(db.Date)
    purpose = db.Column(db.Enum('healthcare', 'transportation', 'recreation', 'charity', 'other'), nullable=False)
    
    # Relationships
    repayments = db.relationship('RepaymentSchedule', backref='loan')
    transactions = db.relationship('Transaction', backref='loan')

class RepaymentSchedule(db.Model):
    __tablename__ = 'RepaymentSchedule'
    repayment_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    loan_ID = db.Column(db.Integer, db.ForeignKey('Loan.loan_ID'), nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    amount_due = db.Column(db.Numeric(10, 2), nullable=False)
    loan_status = db.Column(db.Enum('paid', 'pending', 'late'), nullable=False)

class Transaction(db.Model):
    __tablename__ = 'Transactions'
    transaction_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    transaction_type = db.Column(db.Enum('loan Release', 'Repayment'), nullable=False)
    loan_ID = db.Column(db.Integer, db.ForeignKey('Loan.loan_ID'))
    transaction_date = db.Column(db.Date, nullable=False, default=datetime.now().date())

class Verification(db.Model):
    __tablename__ = 'Verification'
    verification_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    User_ID = db.Column(db.String(8), db.ForeignKey('User.User_ID'))
    email = db.Column(db.String(100), nullable=False)
    verification_code = db.Column(db.String(100))
    expiry_date = db.Column(db.Date)

# Helper functions
def generate_user_id():
    """Generate a unique 8-character user ID"""
    while True:
        user_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        if not User.query.filter_by(User_ID=user_id).first():
            return user_id

def generate_verification_code():
    """Generate a 6-digit verification code"""
    return ''.join(random.choices(string.digits, k=4))

def login_required(f):
    """Decorator to require login for certain routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get form data

        first_name = request.form.get('First_Name')
        last_name = request.form.get('Last_Name')
        email = request.form.get('email')
        phone = request.form.get('Phone_Number')
        student_id = request.form.get('Student_Id')

        print(student_id)
        print(phone)
        
        # Check if user already exists
        if User.query.filter_by(Email=email).first():
            flash('Email already registered', 'error')
            print("email exists")
            return render_template('signup.html')
        
        # Generate user ID and verification code
        user_id = student_id
        verification_code = generate_verification_code()
        
        # Create a temporary password (will be updated later)
        temp_password = "0000000000"
        
        # Create the user first
        user = User(
            User_ID=user_id,
            First_Name=first_name,
            Last_Name=last_name,
            Email=email,
            phone_number=phone,
            user_password=temp_password,
            credit_score=5.0  # Default credit score
        )
        print("user now exists")
        
        # Save the user
        db.session.add(user)
        db.session.commit()
        print("added user")
        
        # Now create the verification
        verification = Verification(
            User_ID=user_id,
            email=email,
            verification_code=verification_code,
            expiry_date=datetime.now().date() + timedelta(days=1)
        )
        
        db.session.add(verification)
        db.session.commit()
        
        # Store user ID in session for later steps
        session['temp_user_id'] = user_id
        session['temp_user_email'] = email
        print(session.get('temp_user_id'))
        
        # In a real application, send verification code via email
        # For demo purposes, we'll just display it
        print(f"Verification code sent to {email}. For testing, the code is: {verification_code}", 'info')
        
        # Redirect to verification page
        return redirect(url_for('verification')) 
    return render_template('signup.html')

@app.route('/email_verification', methods=['GET', 'POST'])
def verification():
    if request.method == 'POST':
        try:
            email = session.get('temp_user_email')
            print(email)
            verification_code = request.form.get('verification_code')
            
            # Verify the code - more flexible checking
            verification = Verification.query.filter_by(
                email=email,
                verification_code=verification_code
            ).first()
            
            if verification and verification.expiry_date >= datetime.now().date():
                # Code is valid, proceed to password setup
                return redirect(url_for('password'))
            else:
                flash('Invalid or expired verification code', 'error')
                
        except Exception as e:
            print(f"Error during email verification: {str(e)}")
            flash('An error occurred. Please try again.', 'error')
    
    return render_template('Verification.html')



@app.route('/password', methods=['GET', 'POST'])
def password():
    if 'temp_user_id' not in session:
        flash('Your session has expired. Please sign up again.', 'error')
        return redirect(url_for('signup'))
    
    if request.method == 'POST':
        try:
            password = request.form.get('password')
            confirm_password = request.form.get('confirmPassword')
            print("Passwords")
            print(password)
            print(confirm_password)
            
            if password != confirm_password:
                print('Passwords do not match', 'error')
                return render_template('Password.html')
            
            if len(password) < 8:
                print('Password must be at least 8 characters', 'error')
                return render_template('Password.html')
            
            # Hash the password
         
            
            # Update the user's password
            user = User.query.get(session.get('temp_user_id'))
            print(user.Email)
            if user:
                user.user_password = password
                db.session.commit()
                
                # Clear the session data
                session.pop('temp_user_id', None)
                session.pop('temp_user_email', None)
                
                print('Account created successfully! Please log in.', 'success')
                return redirect(url_for('login'))
            else:
                print('User not found. Please register again.', 'error')
                return redirect(url_for('signup'))
                
        except Exception as e:
            db.session.rollback()
            print(f"Error setting password: {str(e)}")
            flash('An error occurred. Please try again.', 'error')
            
    return render_template('Password.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(Email=email).first()
        
        if user:
            # Login successful
            session['user_id'] = user.User_ID
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('home'))

@app.route('/dashboard')
@login_required
def dashboard():
    user = User.query.get(session['user_id'])
    
    # Get user's loans as borrower
    borrowed_loans = Loan.query.filter_by(borrower_ID=user.User_ID).all()
    
    # Get user's loans as lender
    lent_loans = Loan.query.filter_by(lender_ID=user.User_ID).all()
    
    return render_template('dashboard.html', 
                          user=user, 
                          borrowed_loans=borrowed_loans,
                          lent_loans=lent_loans)

@app.route('/userprofile', methods=['GET', 'POST'])
@login_required
def userprofile():
    user = User.query.get(session['user_id'])
    
    if request.method == 'POST':
        # Update user profile
        user.First_Name = request.form.get('first_name')
        user.Last_Name = request.form.get('last_name')
        user.BankName = request.form.get('bank_name')
        user.BankAccount = request.form.get('bank_account')
        user.code_name = request.form.get('code_name')
        
        # Save changes
        db.session.commit()
        
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('userprofile.html', user=user)

@app.route('/borrower', methods=['GET', 'POST'])
@login_required
def borrower():
    if request.method == 'POST':
        # Create a new loan request
        amount = request.form.get('amount')
        duration = request.form.get('duration')
        purpose = request.form.get('purpose')
        
        loan = Loan(
            borrower_ID=session['user_id'],
            amount=amount,
            duration_months=duration,
            purpose=purpose,
            loan_status='pending',
            date_requested=datetime.now().date()
        )
        
        db.session.add(loan)
        db.session.commit()
        
        flash('Loan request submitted successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('borrower.html')

@app.route('/lender', methods=['GET', 'POST'])
@login_required
def lender():
    # Get all pending loans
    pending_loans = Loan.query.filter_by(loan_status='pending').all()
    
    if request.method == 'POST':
        loan_id = request.form.get('loan_id')
        action = request.form.get('action')
        
        loan = Loan.query.get(loan_id)
        
        if action == 'approve':
            loan.lender_ID = session['user_id']
            loan.loan_status = 'approved'
            flash('Loan approved!', 'success')
        elif action == 'reject':
            loan.loan_status = 'Rejected'
            flash('Loan rejected', 'info')
        
        db.session.commit()
        return redirect(url_for('lender'))
    
    return render_template('lender.html', pending_loans=pending_loans)

@app.route('/get_suggestions', methods=['POST'])
def get_suggestions():
    amount = float(request.form.get('amount', 0))
    
    # Query the database for users with good credit scores
    potential_lenders = User.query.filter(User.credit_score >= 7.0).all()
    
    suggestions = []
    for lender in potential_lenders:
        # In a real app, you would have more complex logic
        # This is simplified for demonstration
        if lender.User_ID != session.get('user_id'):
            suggestions.append({
                'code_name': lender.code_name,
                'amount': amount,  # Assume they can lend the requested amount
                'return_date': (datetime.now() + timedelta(days=30)).strftime('%m/%d/%Y'),
                'rate': '5%'  # Simplified interest rate
            })
    
    return render_template('partials/getStuff.html', suggestions=suggestions)

@app.route('/loan_details/<int:loan_id>')
@login_required
def loan_details(loan_id):
    loan = Loan.query.get_or_404(loan_id)
    
    # Check if user is authorized to view this loan
    if loan.borrower_ID != session['user_id'] and loan.lender_ID != session['user_id']:
        flash('You are not authorized to view this loan', 'error')
        return redirect(url_for('dashboard'))
    
    repayments = RepaymentSchedule.query.filter_by(loan_ID=loan_id).all()
    
    return render_template('loan_details.html', loan=loan, repayments=repayments)

@app.route('/make_payment/<int:repayment_id>', methods=['POST'])
@login_required
def make_payment(repayment_id):
    repayment = RepaymentSchedule.query.get_or_404(repayment_id)
    loan = Loan.query.get(repayment.loan_ID)
    
    # Check if user is the borrower
    if loan.borrower_ID != session['user_id']:
        flash('You are not authorized to make this payment', 'error')
        return redirect(url_for('dashboard'))
    
    # Update repayment status
    repayment.loan_status = 'paid'
    
    # Create transaction record
    transaction = Transaction(
        transaction_type='Repayment',
        loan_ID=loan.loan_ID,
        transaction_date=datetime.now().date()
    )
    
    db.session.add(transaction)
    db.session.commit()
    
    flash('Payment successful!', 'success')
    return redirect(url_for('loan_details', loan_id=loan.loan_ID))

@app.route('/disburse_loan/<int:loan_id>', methods=['POST'])
@login_required
def disburse_loan(loan_id):
    loan = Loan.query.get_or_404(loan_id)
    
    # Check if user is the lender
    if loan.lender_ID != session['user_id']:
        flash('You are not authorized to disburse this loan', 'error')
        return redirect(url_for('dashboard'))
    
    # Update loan status
    loan.loan_status = 'Disbursed'
    loan.date_disbursed = datetime.now().date()
    
    # Create transaction record
    transaction = Transaction(
        transaction_type='loan Release',
        loan_ID=loan.loan_ID,
        transaction_date=datetime.now().date()
    )
    
    # Create repayment schedule
    monthly_repayment = float(loan.amount) / loan.duration_months
    for i in range(1, loan.duration_months + 1):
        due_date = loan.date_disbursed + timedelta(days=30 * i)
        repayment = RepaymentSchedule(
            loan_ID=loan.loan_ID,
            due_date=due_date,
            amount_due=monthly_repayment,
            loan_status='pending'
        )
        db.session.add(repayment)
    
    db.session.add(transaction)
    db.session.commit()
    
    # Update borrower's credit score (simplified)
    borrower = User.query.get(loan.borrower_ID)
    borrower.credit_score = min(10.0, borrower.credit_score + 0.1)
    db.session.commit()
    
    flash('Loan disbursed successfully!', 'success')
    return redirect(url_for('loan_details', loan_id=loan.loan_ID))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error_code=404, message="Page not found"), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html', error_code=500, message="Internal server error"), 500

def init_db():
    """Initialize database tables if they don't exist"""
    try:
        with app.app_context():
            db.create_all()
            print("Database tables created successfully")
    except Exception as e:
        print(f"Error creating database tables: {e}")
        
if __name__ == '__main__':
    # Initialize database
    init_db()
    app.run(debug=True)