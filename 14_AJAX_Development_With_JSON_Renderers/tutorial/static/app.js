// AJAX Development Tutorial JavaScript
document.addEventListener('DOMContentLoaded', function() {
    console.log('AJAX Tutorial loaded successfully!');

    // History management
    let requestHistory = [];

    function addToHistory(method, url, status, data = null) {
        const entry = {
            timestamp: new Date().toLocaleString(),
            method: method,
            url: url,
            status: status,
            data: data
        };
        requestHistory.unshift(entry);

        // Keep only last 10 entries
        if (requestHistory.length > 10) {
            requestHistory = requestHistory.slice(0, 10);
        }

        updateHistoryDisplay();
    }

    function updateHistoryDisplay() {
        const historyEl = document.getElementById('history');
        if (requestHistory.length === 0) {
            historyEl.innerHTML = '<p>API call history will appear here...</p>';
            return;
        }

        const historyHtml = requestHistory.map(entry => `
            <div class="history-entry ${entry.method}">
                <div class="timestamp">${entry.timestamp}</div>
                <div class="method">${entry.method} ${entry.url}</div>
                <div>Status: ${entry.status}</div>
                ${entry.data ? `<div>Data: ${JSON.stringify(entry.data).substring(0, 100)}${JSON.stringify(entry.data).length > 100 ? '...' : ''}</div>` : ''}
            </div>
        `).join('');

        historyEl.innerHTML = historyHtml;
    }

    // Utility function for making AJAX requests
    function makeRequest(url, options = {}) {
        return fetch(url, {
            method: options.method || 'GET',
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            body: options.body ? JSON.stringify(options.body) : undefined
        })
        .then(response => {
            addToHistory(options.method || 'GET', url, response.status);
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            return response.json();
        });
    }

    // GET request demo
    const getDataBtn = document.getElementById('get-data-btn');
    const getResponseEl = document.getElementById('get-response');

    getDataBtn.addEventListener('click', function() {
        // Show loading state
        getResponseEl.className = 'response-area loading';
        getResponseEl.innerHTML = '<div class="loading-spinner"></div>Loading data from API...';
        getDataBtn.disabled = true;

        makeRequest('/api/data')
            .then(data => {
                getResponseEl.className = 'response-area success';
                getResponseEl.textContent = JSON.stringify(data, null, 2);
            })
            .catch(error => {
                getResponseEl.className = 'response-area error';
                getResponseEl.textContent = `Error: ${error.message}`;
            })
            .finally(() => {
                getDataBtn.disabled = false;
            });
    });

    // POST request demo
    const postForm = document.getElementById('post-form');
    const postResponseEl = document.getElementById('post-response');

    postForm.addEventListener('submit', function(e) {
        e.preventDefault();

        const formData = new FormData(postForm);
        const data = Object.fromEntries(formData.entries());

        // Show loading state
        postResponseEl.className = 'response-area loading';
        postResponseEl.innerHTML = '<div class="loading-spinner"></div>Sending data to API...';

        makeRequest('/api/echo', {
            method: 'POST',
            body: data
        })
            .then(response => {
                postResponseEl.className = 'response-area success';
                postResponseEl.textContent = JSON.stringify(response, null, 2);
            })
            .catch(error => {
                postResponseEl.className = 'response-area error';
                postResponseEl.textContent = `Error: ${error.message}`;
            });
    });

    // Clear history button
    const clearHistoryBtn = document.getElementById('clear-history-btn');
    clearHistoryBtn.addEventListener('click', function() {
        requestHistory = [];
        updateHistoryDisplay();
    });

    // Initialize history display
    updateHistoryDisplay();

    // Add some example interactions
    console.log('Available API endpoints:');
    console.log('- GET /api/data - Returns sample JSON data');
    console.log('- POST /api/echo - Echoes back sent data');

    // Performance monitoring
    window.addEventListener('load', function() {
        console.log('AJAX Tutorial: Page loaded successfully');
        console.log('Try clicking the buttons to test AJAX functionality!');
    });
});
