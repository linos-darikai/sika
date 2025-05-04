document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('passwordForm');

    form.addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent immediate submission

        const newPassword = document.getElementById('newPassword').value;
        const confirmPassword = document.getElementById('confirmPassword').value;
        const errorMessage = document.getElementById('errorMessage');

        if (newPassword !== confirmPassword) {
            errorMessage.textContent = "Passwords do not match. Please try again.";
        } else if (newPassword.length < 8) {
            errorMessage.textContent = "Password must be at least 8 characters long.";
        } else {
            errorMessage.textContent = "";
            // Optionally show success alert
            alert("Password created successfully!");
            // Now allow the form to submit
            form.submit();
        }
    });
});