document.addEventListener('DOMContentLoaded', function() {
    // Select all alert messages
    const alerts = document.querySelectorAll('.alert');
    
    alerts.forEach(alert => {
        // Set timeout to fade out after 3 seconds
        setTimeout(() => {
            alert.classList.add('fade-out');
            
            // Remove element after fade completes
            setTimeout(() => {
                alert.remove();
            }, 500); // Match this with the CSS transition time
        }, 2000);
    });
});