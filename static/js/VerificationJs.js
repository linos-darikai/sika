


function moveToNext(input, position) {
    if (input.value.length === 1) {
        if (position < 4) {
            document.getElementsByClassName('code-input')[position].focus();
        }
    }
}

document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('verificationForm');

    form.addEventListener('submit', function (event) {
        event.preventDefault();  // Stop automatic form submission

        const inputs = document.getElementsByClassName('code-input');
        let codeEntered = '';

        for (let i = 0; i < inputs.length; i++) {
            codeEntered += inputs[i].value;
        }

        // Set the value of the hidden input
        document.getElementById('verification_code').value = codeEntered;

        // Now manually submit the form
        form.submit();
    });
});

// Set focus to first input on page load
document.addEventListener('DOMContentLoaded', function() {
    document.getElementsByClassName('code-input')[0].focus();
});