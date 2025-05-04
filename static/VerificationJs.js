function moveToNext(input, position) {
    if (input.value.length === 1) {
        if (position < 4) {
            document.getElementsByClassName('code-input')[position].focus();
        }
    }
}

function verifyCode(event) {
    event.preventDefault();
    
    // Get the code from all inputs
    const inputs = document.getElementsByClassName('code-input');
    let codeEntered = '';
    
    for (let i = 0; i < inputs.length; i++) {
        codeEntered += inputs[i].value;
    }
    
    const correctCode = "1234"; // For demonstration
    
    if (codeEntered === correctCode) {
        // Clear any error message
        document.getElementById('error-message').textContent = '';
        
        // Show success message
        alert("Verification successful! Your account is now active.");
        window.location.href = "Password.html"; 
    } else {
        document.getElementById('error-message').textContent = "Invalid code. Please try again.";
        
        // Clear all inputs for retry
        for (let i = 0; i < inputs.length; i++) {
            inputs[i].value = '';
        }
        
        // Focus on first input
        inputs[0].focus();
    }
}

function resendCode(event) {
    event.preventDefault();
    alert("A new verification code has been sent to your email.");
}

// Set focus to first input on page load
document.addEventListener('DOMContentLoaded', function() {
    document.getElementsByClassName('code-input')[0].focus();
});