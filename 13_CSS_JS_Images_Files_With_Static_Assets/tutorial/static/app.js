// Static Assets Demo JavaScript
document.addEventListener('DOMContentLoaded', function() {
    console.log('Static assets tutorial loaded successfully!');

    // Demo button functionality
    const demoButton = document.getElementById('demo-button');
    const demoOutput = document.getElementById('demo-output');

    if (demoButton && demoOutput) {
        demoButton.addEventListener('click', function() {
            // Show loading state
            demoButton.textContent = 'Processing...';
            demoButton.disabled = true;

            // Simulate async operation
            setTimeout(function() {
                // Update output
                demoOutput.textContent = 'Hello from JavaScript! Static assets are working correctly. Current time: ' + new Date().toLocaleTimeString();
                demoOutput.classList.add('show');

                // Reset button
                demoButton.textContent = 'Click for Demo';
                demoButton.disabled = false;

                // Add some animation
                demoOutput.style.animation = 'fadeIn 0.5s ease-in';
            }, 500);
        });
    }

    // Add some interactive features
    const features = document.querySelectorAll('.feature');

    features.forEach(function(feature, index) {
        feature.addEventListener('mouseenter', function() {
            console.log(`Hovered over feature ${index + 1}`);
        });

        feature.addEventListener('click', function() {
            // Toggle a class for visual feedback
            this.classList.toggle('clicked');

            // Show a message
            if (this.classList.contains('clicked')) {
                showMessage(`Feature ${index + 1} clicked!`, 'info');
            }
        });
    });

    // Utility function to show messages
    function showMessage(message, type) {
        // Remove existing messages
        const existingMessages = document.querySelectorAll('.message');
        existingMessages.forEach(function(msg) {
            msg.remove();
        });

        // Create new message element
        const messageEl = document.createElement('div');
        messageEl.className = `message ${type}`;
        messageEl.textContent = message;
        messageEl.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${type === 'info' ? '#d1ecf1' : '#f8d7da'};
            color: ${type === 'info' ? '#0c5460' : '#721c24'};
            padding: 10px 15px;
            border-radius: 4px;
            border-left: 4px solid ${type === 'info' ? '#17a2b8' : '#dc3545'};
            z-index: 1000;
            animation: slideIn 0.3s ease-out;
        `;

        document.body.appendChild(messageEl);

        // Auto-remove after 3 seconds
        setTimeout(function() {
            messageEl.style.animation = 'slideOut 0.3s ease-in';
            setTimeout(function() {
                if (messageEl.parentNode) {
                    messageEl.parentNode.removeChild(messageEl);
                }
            }, 300);
        }, 3000);
    }

    // Add CSS animations for messages
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        @keyframes slideOut {
            from { transform: translateX(0); opacity: 1; }
            to { transform: translateX(100%); opacity: 0; }
        }
        .feature.clicked {
            background: linear-gradient(135deg, #28a745 0%, #20c997 100%) !important;
            color: white;
        }
        .feature.clicked h3 {
            color: white;
        }
    `;
    document.head.appendChild(style);

    // Performance monitoring
    let pageLoadTime = performance.now();
    console.log(`Page loaded in ${pageLoadTime.toFixed(2)} milliseconds`);

    // Add some performance metrics
    window.addEventListener('load', function() {
        setTimeout(function() {
            const perfData = performance.getEntriesByType('navigation')[0];
            console.log('Performance metrics:', {
                'DNS lookup': (perfData.domainLookupEnd - perfData.domainLookupStart).toFixed(2) + 'ms',
                'TCP connection': (perfData.connectEnd - perfData.connectStart).toFixed(2) + 'ms',
                'Server response': (perfData.responseStart - perfData.requestStart).toFixed(2) + 'ms',
                'Page load': (perfData.loadEventEnd - perfData.navigationStart).toFixed(2) + 'ms'
            });
        }, 0);
    });
});
