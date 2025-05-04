// Global variables
let currentPage = 'lender';
let allSuggestions = [];
let selectedLoan = {};

// DOM elements
document.addEventListener('DOMContentLoaded', function() {
    // Initialize the page
    showPage('lender');
    
    // Set up request amount input event
    const requestAmountInput = document.getElementById('requestAmount');
    if (requestAmountInput) {
        requestAmountInput.addEventListener('change', function() {
            fetchSuggestions(this.value);
        });
    }
    
    // Set up form submission for the memo page
    setupMemoFormSubmission();
    
    // Set up thank you page form submission (connects to borrower route)
    setupThankYouPageSubmission();
});

// Page navigation
function showPage(pageId) {
    // Hide all pages
    document.querySelectorAll('.dashboard-card').forEach(card => {
        card.style.display = 'none';
    });
    
    // Show the requested page
    document.getElementById(pageId).style.display = 'block';
    
    // Update current page
    currentPage = pageId;
}

// Fetch suggestions from the backend
function fetchSuggestions(amount) {
    // Show loading state
    const suggestionList = document.querySelector('.suggestion-list');
    suggestionList.innerHTML = '<div class="suggestion-item">Loading suggestions...</div>';
    
    // Create form data
    const formData = new FormData();
    formData.append('amount', amount);
    
    // Fetch suggestions from the backend
    fetch('/get_suggestions', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        // Store all suggestions
        allSuggestions = data.suggestions;
        
        // Display suggestions
        displaySuggestions(allSuggestions);
    })
    .catch(error => {
        console.error('Error fetching suggestions:', error);
        suggestionList.innerHTML = '<div class="suggestion-item">Error loading suggestions. Please try again.</div>';
    });
}

// Display suggestions in the UI
function displaySuggestions(suggestions) {
    const suggestionList = document.querySelector('.suggestion-list');
    suggestionList.innerHTML = '';
    
    if (suggestions.length === 0) {
        suggestionList.innerHTML = '<div class="suggestion-item">No suggestions available for this amount.</div>';
        return;
    }
    
    suggestions.forEach(suggestion => {
        const suggestionItem = document.createElement('div');
        suggestionItem.className = 'suggestion-item';
        suggestionItem.onclick = function() {
            selectSuggestion(
                suggestion.code_name,
                suggestion.amount,
                suggestion.return_date,
                suggestion.rate,
                suggestion.loan_id  // Adding loan_id if available
            );
        };
        
        suggestionItem.innerHTML = `
            <div><strong>Code Name:</strong> ${suggestion.code_name}</div>
            <div><strong>Amount:</strong> ${suggestion.amount}</div>
            <div><strong>Return Date:</strong> ${suggestion.return_date}</div>
            <div><strong>Rate:</strong> ${suggestion.rate}</div>
        `;
        
        suggestionList.appendChild(suggestionItem);
    });
}

// Select a suggestion and move to confirmation page
function selectSuggestion(codeName, amount, returnDate, rate, loanId) {
    // Store the selected loan data
    selectedLoan = {
        code_name: codeName,
        amount: amount,
        return_date: returnDate,
        rate: rate,
        loan_id: loanId
    };
    
    // Fill in the confirmation form
    document.getElementById('codeName').value = codeName;
    document.getElementById('amount').value = amount;
    document.getElementById('returnDate').value = returnDate;
    document.getElementById('rate').value = rate;
    
    // Show the confirmation page
    showPage('confirm');
}

// Apply filters to suggestions
function applyFilter() {
    const filterType = document.getElementById('filterType').value;
    let filteredSuggestions = [...allSuggestions];
    
    switch (filterType) {
        case 'rate':
            filteredSuggestions.sort((a, b) => {
                return parseFloat(a.rate) - parseFloat(b.rate);
            });
            break;
        case 'amount':
            filteredSuggestions.sort((a, b) => {
                return a.amount - b.amount;
            });
            break;
        case 'date':
            filteredSuggestions.sort((a, b) => {
                return new Date(a.return_date) - new Date(b.return_date);
            });
            break;
    }
    
    displaySuggestions(filteredSuggestions);
}

// Show all suggestions without filtering
function showAllSuggestions() {
    displaySuggestions(allSuggestions);
}

// Set up the form submission for the memo page
function setupMemoFormSubmission() {
    const memoPage = document.getElementById('memo');
    if (memoPage) {
        const submitButton = memoPage.querySelector('.btn-primary');
        submitButton.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Validate input
            const momoNumber = document.getElementById('momoNumber').value;
            const bankAccount = document.getElementById('bankAccount').value;
            
            if (!momoNumber && !bankAccount) {
                alert('Please enter either Mobile Money number or Bank Account details');
                return;
            }
            
            // Add payment details to selected loan
            selectedLoan.payment_method = momoNumber ? 'momo' : 'bank';
            selectedLoan.payment_details = momoNumber || bankAccount;
            
            // Show thank you page
            showPage('thank-you');
            
            // Add hidden fields to the thank you form with loan data
            addLoanDataToThankYouForm();
        });
    }
}

// Add loan data to the thank you form as hidden fields
function addLoanDataToThankYouForm() {
    const thankYouForm = document.getElementById('thank-you');
    
    // Clear any existing hidden fields
    const existingHiddenFields = thankYouForm.querySelectorAll('input[type="hidden"]');
    existingHiddenFields.forEach(field => field.remove());
    
    // Add hidden fields for each loan detail
    for (const [key, value] of Object.entries(selectedLoan)) {
        const hiddenInput = document.createElement('input');
        hiddenInput.type = 'hidden';
        hiddenInput.name = key;
        hiddenInput.value = value;
        thankYouForm.appendChild(hiddenInput);
    }
}

// Set up the thank you page form submission
function setupThankYouPageSubmission() {
    const thankYouForm = document.getElementById('thank-you');
    if (thankYouForm) {
        thankYouForm.addEventListener('submit', function(e) {
            // Let the form submit naturally to the 'borrower' route
            // We don't need to prevent default since we want the form to submit
            
            // You could add additional logic here if needed
            console.log('Submitting loan data to backend:', selectedLoan);
        });
        
        // Update the "Done" button to submit the form
        const doneButton = thankYouForm.querySelector('.done-button');
        if (doneButton) {
            doneButton.addEventListener('click', function(e) {
                e.preventDefault();
                thankYouForm.submit();
            });
        }
    }
}