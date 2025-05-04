function handlePassword(event) {
    event.preventDefault();
    
    const newPassword = document.getElementById('newPassword').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    const errorMessage = document.getElementById('errorMessage');


    if (newPassword !== confirmPassword) {
        errorMessage.textContent = "Passwords do not match.  Please try again.";
        return;
    } 
    else if (newPassword.length < 8) {
        errorMessage.textContent = "Password must be at least 8 characters long.";
    } else {
        errorMessage.textContent = "";
        alert("Password created successfully!");
        window.location.href = 'dashboard.html'; 
    }
}