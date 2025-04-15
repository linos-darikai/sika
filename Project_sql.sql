CREATE database LoanSystem;
USE LoanSystem;

CREATE table User(
	User_ID varchar(8) PRIMARY KEY,
    First_Name varchar(20) not null,
    Last_Name varchar(20) not null,
    Email varchar(60) not null,
    phone_number int,
    user_password varchar(10) not null,
    BankName varchar(50),
    -- bank account numbers in ghana have an average of 10-12 characters 
    BankAccount varchar(12),
    code_name varchar(5),
    credit_score float check(credit_score between 0 and 10),
	UNIQUE(code_name),
    UNIQUE(Email),
    UNIQUE(BankAccount),
    UNIQUE(Phone_number)
    );
    
    
	
describe user;

CREATE table Loan(
	loan_ID int PRIMARY KEY,
    borrower_ID int,
    lender_ID int,
    amount decimal(10,2) not null,
    duration_months int not null,
    loan_status enum('pending', 'approved','Rejected','Disbursed', 'settled'),
    date_requested date,
    date_disbursed date,
    purpose enum('healthcare','transportation','recreation', 'charity','other') not null,
    FOREIGN KEY (lender_ID) REFERENCES User(User_ID),
    FOREIGN KEY (borrower_ID) REFERENCES User(User_ID)
    );
CREATE table RepaymentSchedule(
	repayment_ID int PRIMARY KEY,
    loan_ID int not null,
    due_date date not null,
    amount_due decimal(10,2) not null,
    loan_status enum('paid','pending','late') not null,
    FOREIGN KEY (loan_ID) REFERENCES Loan(loan_ID)
    );
CREATE table Transactions(
	transaction_ID int PRIMARY KEY auto_increment,
    transaction_type enum('loan Release', 'Repayment') not null,
    loan_ID int,
    transaction_date date not null,
    FOREIGN KEY (loan_ID) REFERENCES Loan(loan_ID)
    );
CREATE table Verification(
	verification_ID int PRIMARY KEY,
	User_ID int,
    email varchar(100) not null,
    verification_code varchar(100),
    expiry_date date,
    FOREIGN KEY (User_ID) REFERENCES User(User_ID)
    );
    
    
    
    

    
