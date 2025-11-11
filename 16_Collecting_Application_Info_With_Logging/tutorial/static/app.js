// Advanced View Classes Tutorial JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all interactive elements
    initializeAPIStatus();
    initializePostForm();
    initializeCompanyOperations();
    initializeJSONFetch();
});

// API Status functionality
function initializeAPIStatus() {
    const statusBtn = document.getElementById('get-status-btn');
    if (!statusBtn) return;

    statusBtn.addEventListener('click', async function() {
        const responseArea = document.getElementById('api-response');
        responseArea.textContent = 'Loading...';

        try {
            const response = await fetch('/api/status');
            const data = await response.json();

            responseArea.textContent = JSON.stringify(data, null, 2);
            responseArea.style.borderColor = response.ok ? '#28a745' : '#dc3545';
        } catch (error) {
            responseArea.textContent = `Error: ${error.message}`;
            responseArea.style.borderColor = '#dc3545';
        }
    });
}

// POST form functionality
function initializePostForm() {
    const form = document.getElementById('post-form');
    if (!form) return;

    form.addEventListener('submit', async function(e) {
        e.preventDefault();

        const formData = new FormData(form);
        const message = formData.get('message');
        const responseArea = document.getElementById('post-response');

        responseArea.textContent = 'Sending POST request...';

        try {
            const response = await fetch(window.location.pathname, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    timestamp: new Date().toISOString()
                })
            });

            const data = await response.json();
            responseArea.textContent = JSON.stringify(data, null, 2);
            responseArea.style.borderColor = response.ok ? '#28a745' : '#dc3545';
        } catch (error) {
            responseArea.textContent = `Error: ${error.message}`;
            responseArea.style.borderColor = '#dc3545';
        }
    });
}

// Company operations (PUT/DELETE)
function initializeCompanyOperations() {
    const putBtn = document.getElementById('put-btn');
    const deleteBtn = document.getElementById('delete-btn');

    if (putBtn) {
        putBtn.addEventListener('click', async function() {
            const company = this.dataset.company;
            const responseArea = document.getElementById('operation-response');

            responseArea.textContent = 'Sending PUT request...';

            try {
                const response = await fetch(`/company/${company}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        revenue: 30000000,
                        employees: 200
                    })
                });

                const data = await response.json();
                responseArea.textContent = JSON.stringify(data, null, 2);
                responseArea.style.borderColor = response.ok ? '#28a745' : '#dc3545';
            } catch (error) {
                responseArea.textContent = `Error: ${error.message}`;
                responseArea.style.borderColor = '#dc3545';
            }
        });
    }

    if (deleteBtn) {
        deleteBtn.addEventListener('click', async function() {
            const company = this.dataset.company;
            const responseArea = document.getElementById('operation-response');

            if (!confirm(`Are you sure you want to delete ${company}?`)) {
                return;
            }

            responseArea.textContent = 'Sending DELETE request...';

            try {
                const response = await fetch(`/company/${company}`, {
                    method: 'DELETE'
                });

                const data = await response.json();
                responseArea.textContent = JSON.stringify(data, null, 2);
                responseArea.style.borderColor = response.ok ? '#28a745' : '#dc3545';
            } catch (error) {
                responseArea.textContent = `Error: ${error.message}`;
                responseArea.style.borderColor = '#dc3545';
            }
        });
    }
}

// JSON fetch functionality
function initializeJSONFetch() {
    const fetchBtn = document.getElementById('fetch-json-btn');
    if (!fetchBtn) return;

    fetchBtn.addEventListener('click', async function() {
        const company = this.dataset.company;
        const responseArea = document.getElementById('json-response');

        responseArea.textContent = 'Fetching JSON data...';

        try {
            const response = await fetch(`/company/${company}/json`);
            const data = await response.json();

            responseArea.textContent = JSON.stringify(data, null, 2);
            responseArea.style.borderColor = response.ok ? '#28a745' : '#dc3545';
        } catch (error) {
            responseArea.textContent = `Error: ${error.message}`;
            responseArea.style.borderColor = '#dc3545';
        }
    });
}

// Utility functions
function showLoading(element, text = 'Loading...') {
    element.textContent = text;
    element.style.borderColor = '#ffc107';
}

function showSuccess(element, data) {
    element.textContent = JSON.stringify(data, null, 2);
    element.style.borderColor = '#28a745';
}

function showError(element, error) {
    element.textContent = `Error: ${error.message}`;
    element.style.borderColor = '#dc3545';
}

// Add some visual feedback for button clicks
document.addEventListener('click', function(e) {
    if (e.target.classList.contains('btn')) {
        e.target.style.transform = 'scale(0.95)';
        setTimeout(() => {
            e.target.style.transform = '';
        }, 100);
    }
});

// Handle browser back/forward navigation
window.addEventListener('popstate', function(event) {
    // Could implement navigation handling here
    console.log('Navigation event:', event.state);
});

// Add keyboard shortcuts for development
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + Shift + D for debug mode
    if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === 'D') {
        e.preventDefault();
        const currentUrl = new URL(window.location);
        if (currentUrl.searchParams.get('debug') === 'true') {
            currentUrl.searchParams.delete('debug');
        } else {
            currentUrl.searchParams.set('debug', 'true');
        }
        window.location.href = currentUrl.toString();
    }
});

// Console logging for debugging
console.log('Advanced View Classes Tutorial loaded');
console.log('Available keyboard shortcuts:');
console.log('Ctrl/Cmd + Shift + D: Toggle debug mode');
