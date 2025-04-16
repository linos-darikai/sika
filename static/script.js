
  //borrower`s page handling
  function showPage(pageId) {
    // Hide all pages
    document.querySelectorAll('.page').forEach(page => {
        page.style.display = 'none';
    });

    // Show the selected page
    document.getElementById(pageId).style.display = 'block';
}

function selectSuggestion(codeName, amount, returnDate, rate) {
    // Fill the confirm details form with the selected suggestion
    document.getElementById('codeName').value = codeName;
    document.getElementById('amount').value = amount;
    document.getElementById('returnDate').value = returnDate;
    document.getElementById('rate').value = rate;

    // Navigate to confirm page
    showPage('confirm');
}

function applyFilter() {
    // In a real application, this would filter the suggestions based on the selected criteria
    // For this demo, we'll just show an alert
    const filterType = document.getElementById('filterType').value;
    alert(`Filtering by ${filterType}`);

    // A real implementation would hide/show suggestion items based on the filter
}

function showAllSuggestions() {
    // In a real application, this would clear filters and show all suggestions
    // For this demo, we'll just show an alert
    alert("Showing all suggestions");

    // A real implementation would reset filters and show all suggestion items
}

function goToUserPage() {
    // In a real application, this would navigate to the user page
    alert("Navigating to User Page");
}

// Initialize with the first page visible
document.addEventListener('DOMContentLoaded', function() {
    showPage('lender');
});


//
