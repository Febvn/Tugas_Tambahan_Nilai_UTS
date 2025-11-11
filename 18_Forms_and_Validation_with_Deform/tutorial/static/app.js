// Forms and Validation Demo JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize form enhancements
    initializeFormEnhancements();
    initializeValidationFeedback();
});

function initializeFormEnhancements() {
    // Add dynamic form field highlighting
    const formInputs = document.querySelectorAll('input, select, textarea');

    formInputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });

        input.addEventListener('blur', function() {
            this.parentElement.classList.remove('focused');
        });

        input.addEventListener('input', function() {
            if (this.value.trim()) {
                this.parentElement.classList.add('has-content');
            } else {
                this.parentElement.classList.remove('has-content');
            }
        });
    });

    console.log('Form enhancements initialized');
}

function initializeValidationFeedback() {
    // Add real-time validation feedback
    const emailInputs = document.querySelectorAll('input[type="email"]');
    const passwordInputs = document.querySelectorAll('input[type="password"]');

    emailInputs.forEach(input => {
        input.addEventListener('blur', function() {
            validateEmail(this);
        });
    });

    passwordInputs.forEach(input => {
        input.addEventListener('input', function() {
            validatePasswordStrength(this);
        });
    });
}

function validateEmail(input) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const isValid = emailRegex.test(input.value);

    input.parentElement.classList.remove('has-success', 'has-error');

    if (input.value && !isValid) {
        input.parentElement.classList.add('has-error');
        showFieldError(input, 'Please enter a valid email address');
    } else if (input.value && isValid) {
        input.parentElement.classList.add('has-success');
        clearFieldError(input);
    }
}

function validatePasswordStrength(input) {
    const password = input.value;
    let strength = 0;

    if (password.length >= 8) strength++;
    if (/[a-z]/.test(password)) strength++;
    if (/[A-Z]/.test(password)) strength++;
    if (/[0-9]/.test(password)) strength++;
    if (/[^A-Za-z0-9]/.test(password)) strength++;

    // Visual feedback for password strength
    const strengthIndicator = input.parentElement.querySelector('.password-strength');
    if (!strengthIndicator) {
        const indicator = document.createElement('div');
        indicator.className = 'password-strength';
        input.parentElement.appendChild(indicator);
    }

    const indicator = input.parentElement.querySelector('.password-strength');
    indicator.className = 'password-strength strength-' + strength;

    const strengthTexts = ['', 'Very Weak', 'Weak', 'Fair', 'Good', 'Strong'];
    indicator.textContent = strengthTexts[strength] || '';
}

function showFieldError(input, message) {
    clearFieldError(input);

    const errorDiv = document.createElement('div');
    errorDiv.className = 'error';
    errorDiv.textContent = message;

    input.parentElement.appendChild(errorDiv);
}

function clearFieldError(input) {
    const existingError = input.parentElement.querySelector('.error');
    if (existingError) {
        existingError.remove();
    }
}

// Password confirmation validation
function validatePasswordConfirmation() {
    const passwordInputs = document.querySelectorAll('input[type="password"]');
    if (passwordInputs.length >= 2) {
        const [password, confirm] = passwordInputs;

        confirm.addEventListener('input', function() {
            if (this.value && password.value !== this.value) {
                showFieldError(this, 'Passwords do not match');
                this.parentElement.classList.add('has-error');
            } else {
                clearFieldError(this);
                this.parentElement.classList.remove('has-error');
                if (this.value && password.value === this.value) {
                    this.parentElement.classList.add('has-success');
                }
            }
        });
    }
}

// Sequence form helpers
function initializeSequenceForm() {
    // Add event listeners for sequence form buttons
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('deform-seq-add')) {
            setTimeout(() => {
                initializeFormEnhancements();
            }, 100);
        }
    });
}

// Form submission enhancement
function enhanceFormSubmission() {
    const forms = document.querySelectorAll('form');

    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = form.querySelector('input[type="submit"], button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.value = submitBtn.value + ' (Processing...)';
            }
        });
    });
}

// Initialize all enhancements
validatePasswordConfirmation();
initializeSequenceForm();
enhanceFormSubmission();

// Export functions for global use
window.FormsDemo = {
    validateEmail,
    validatePasswordStrength,
    showFieldError,
    clearFieldError
};
