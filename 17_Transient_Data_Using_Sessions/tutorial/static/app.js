// Session Management Demo JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize any interactive elements
    initializeEventListeners();
});

function initializeEventListeners() {
    // Add any dynamic event listeners here
    console.log('Session Management Demo initialized');
}

// Utility functions for session management
function getSessionInfo() {
    // This would typically make an AJAX call to get session info
    // For demo purposes, we'll just log to console
    console.log('Getting session information...');
}

function updateCounterDisplay(newValue) {
    const counterElement = document.getElementById('counter-value');
    if (counterElement) {
        counterElement.textContent = newValue;
        // Add a brief highlight effect
        counterElement.style.transition = 'color 0.3s ease';
        counterElement.style.color = '#28a745';
        setTimeout(() => {
            counterElement.style.color = '#004499';
        }, 300);
    }
}

// Flash message handling
function showFlashMessage(message, category = 'info') {
    const flashContainer = document.querySelector('.container');
    if (flashContainer) {
        const flashDiv = document.createElement('div');
        flashDiv.className = `flash-message flash-${category}`;
        flashDiv.innerHTML = message;

        // Insert after h1
        const h1 = flashContainer.querySelector('h1');
        if (h1) {
            h1.insertAdjacentElement('afterend', flashDiv);

            // Auto-remove after 5 seconds
            setTimeout(() => {
                flashDiv.style.opacity = '0';
                setTimeout(() => flashDiv.remove(), 300);
            }, 5000);
        }
    }
}

// Session data validation
function validateSessionData() {
    // Basic validation for session-related forms
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const inputs = form.querySelectorAll('input[required]');
            let isValid = true;

            inputs.forEach(input => {
                if (!input.value.trim()) {
                    input.style.borderColor = '#dc3545';
                    isValid = false;
                } else {
                    input.style.borderColor = '#ced4da';
                }
            });

            if (!isValid) {
                e.preventDefault();
                showFlashMessage('Please fill in all required fields.', 'error');
            }
        });
    });
}

// Initialize validation on page load
validateSessionData();

// Export functions for global use (if needed)
window.SessionDemo = {
    getSessionInfo,
    updateCounterDisplay,
    showFlashMessage
};
