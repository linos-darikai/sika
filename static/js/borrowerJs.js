
function showPage(pageId) {
            
    document.querySelectorAll('.dashboard-card').forEach(page => {
        page.style.display = 'none';
    });
    
    
    document.getElementById(pageId).style.display = 'block';
}

function selectSuggestion(codeName, amount, returnDate, rate) {
    
    document.getElementById('codeName').value = codeName;
    document.getElementById('amount').value = amount;
    document.getElementById('returnDate').value = returnDate;
    document.getElementById('rate').value = rate;
    
    
    showPage('confirm');
}

function applyFilter() {
    // In a real application, this would filter the suggestions based on the selected criteria
    const filterType = document.getElementById('filterType').value;
    alert(`Filtering by ${filterType}`);
    
    // A real implementation would hide/show suggestion items based on the filter
}

function showAllSuggestions() {
    // In a real application, this would clear filters and show all suggestions
    alert("Showing all suggestions");
    
    // A real implementation would reset filters and show all suggestion items
}

// Initialize with the first page visible
document.addEventListener('DOMContentLoaded', function() {
    showPage('lender');
});