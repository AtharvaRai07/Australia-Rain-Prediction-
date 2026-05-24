/**
 * AUSTRALIA RAIN PREDICTION - JAVASCRIPT
 * Handles form submission, API calls, and UI updates
 */

// ============================================
// DOM ELEMENTS
// ============================================
const predictionForm = document.getElementById('predictionForm');
const predictBtn = document.getElementById('predictBtn');
const resultCard = document.getElementById('resultCard');
const loadingCard = document.getElementById('loadingCard');
const errorCard = document.getElementById('errorCard');
const infoCard = document.getElementById('infoCard');
const resultContent = document.getElementById('resultContent');
const errorMessage = document.getElementById('errorMessage');
const rainStatus = document.getElementById('rainStatus');
const predictionText = document.getElementById('predictionText');
const confidenceValue = document.getElementById('confidenceValue');
const confidenceBar = document.getElementById('confidenceBar');

// ============================================
// UTILITY FUNCTIONS
// ============================================

/**
 * Show/hide result cards
 */
function showCard(card, show = true) {
    if (show) {
        card.classList.remove('hidden');
        card.classList.add('show');
    } else {
        card.classList.add('hidden');
        card.classList.remove('show');
    }
}

/**
 * Display error message
 */
function displayError(message) {
    errorMessage.textContent = message;
    showCard(loadingCard, false);
    showCard(resultCard, false);
    showCard(errorCard, true);
    predictBtn.disabled = false;
    predictBtn.textContent = 'Predict Now';
}

/**
 * Display success result
 */
function displayResult(prediction, confidence) {
    // Set emoji and text based on prediction
    const isRaining = prediction === 'Yes';
    rainStatus.textContent = isRaining ? '🌧️' : '☀️';
    predictionText.textContent = isRaining ? 'Rain Tomorrow' : 'No Rain Tomorrow';
    predictionText.className = isRaining ? 'text-3xl font-bold text-red-600' : 'text-3xl font-bold text-green-600';

    // Update confidence
    confidenceValue.textContent = `${confidence}%`;
    confidenceBar.style.width = `${confidence}%`;

    // Show result card
    showCard(loadingCard, false);
    showCard(errorCard, false);
    showCard(resultCard, true);

    // Re-enable button
    predictBtn.disabled = false;
    predictBtn.textContent = 'Predict Now';

    // Scroll to results
    resultCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

/**
 * Validate form inputs
 */
function validateForm() {
    const formData = new FormData(predictionForm);
    const errors = [];

    for (let [key, value] of formData.entries()) {
        if (value === '' || value === null) {
            errors.push(`${key} is required`);
        }

        // Validate numeric fields (exclude categorical fields)
        const categoricalFields = ['Location', 'WindGustDir', 'WindDir9am', 'WindDir3pm', 'RainToday'];
        if (!categoricalFields.includes(key)) {
            if (isNaN(value)) {
                errors.push(`${key} must be a number`);
            }
        }
    }

    return errors;
}

/**
 * Prepare form data for API
 */
function prepareFormData() {
    const formData = new FormData(predictionForm);
    const data = {};

    for (let [key, value] of formData.entries()) {
        data[key] = value;
    }

    return data;
}

// ============================================
// FORM SUBMISSION HANDLER
// ============================================

predictionForm.addEventListener('submit', async function (e) {
    e.preventDefault();

    // Validate form
    const errors = validateForm();
    if (errors.length > 0) {
        displayError(`Please fix these errors:\n${errors.join('\n')}`);
        return;
    }

    // Show loading state
    predictBtn.disabled = true;
    predictBtn.innerHTML = `
        <svg class="w-5 h-5 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        <span>Predicting...</span>
    `;
    showCard(loadingCard, true);
    showCard(resultCard, false);
    showCard(errorCard, false);

    try {
        // Prepare data
        const formData = prepareFormData();
        console.log('Form Data:', formData);

        // Make API call
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });

        const result = await response.json();
        console.log('API Response:', result);

        if (result.success) {
            displayResult(result.prediction, result.confidence);
            logPrediction(formData, result);
        } else {
            displayError(result.error || 'An error occurred during prediction');
        }
    } catch (error) {
        console.error('Prediction error:', error);
        displayError(`Error: ${error.message}`);
    }
});

// ============================================
// FORM RESET HANDLER
// ============================================

predictionForm.addEventListener('reset', function () {
    showCard(resultCard, false);
    showCard(loadingCard, false);
    showCard(errorCard, false);
    showCard(infoCard, true);
});

// ============================================
// INPUT FIELD ENHANCEMENTS
// ============================================

// Add number formatting to numeric inputs
document.querySelectorAll('input[type="number"]').forEach(input => {
    input.addEventListener('blur', function () {
        if (this.value && !isNaN(this.value)) {
            this.value = parseFloat(this.value).toFixed(2);
        }
    });
});

// Add focus animations
document.querySelectorAll('input, select').forEach(field => {
    field.addEventListener('focus', function () {
        this.parentElement.classList.add('fade-in');
    });
});

// ============================================
// LOGGING & TRACKING
// ============================================

/**
 * Log predictions for analytics (optional)
 */
function logPrediction(inputs, result) {
    const prediction = {
        timestamp: new Date().toISOString(),
        inputs: inputs,
        prediction: result.prediction,
        confidence: result.confidence
    };

    // Log to console (for debugging)
    console.log('Prediction logged:', prediction);

    // Optional: Send to analytics endpoint
    // fetch('/log-prediction', {
    //     method: 'POST',
    //     headers: { 'Content-Type': 'application/json' },
    //     body: JSON.stringify(prediction)
    // }).catch(err => console.error('Logging error:', err));
}

// ============================================
// KEYBOARD SHORTCUTS
// ============================================

/**
 * Keyboard shortcuts for accessibility
 */
document.addEventListener('keydown', function (e) {
    // Ctrl/Cmd + Enter to submit
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        if (document.activeElement !== predictBtn) {
            predictionForm.dispatchEvent(new Event('submit'));
        }
    }

    // Escape to reset
    if (e.key === 'Escape') {
        predictionForm.reset();
    }
});

// ============================================
// PAGE LOAD ANIMATIONS
// ============================================

/**
 * Animate form fields on page load
 */
window.addEventListener('load', function () {
    const formGroups = document.querySelectorAll('.form-group');
    formGroups.forEach((group, index) => {
        group.style.animationDelay = `${index * 0.05}s`;
    });
});

// ============================================
// LOCAL STORAGE FOR FORM DATA
// ============================================

/**
 * Auto-save form data to localStorage
 */
predictionForm.addEventListener('change', function () {
    const formData = new FormData(predictionForm);
    const data = {};

    for (let [key, value] of formData.entries()) {
        data[key] = value;
    }

    localStorage.setItem('predictionFormData', JSON.stringify(data));
});

/**
 * Restore form data from localStorage on page load
 */
window.addEventListener('load', function () {
    const savedData = localStorage.getItem('predictionFormData');
    if (savedData) {
        try {
            const data = JSON.parse(savedData);

            // Show restore message
            const restoreBtn = document.createElement('div');
            restoreBtn.className = 'bg-blue-100 border border-blue-400 text-blue-700 px-4 py-3 rounded mb-4';
            restoreBtn.innerHTML = `
                <span>Previous data found. <button type="button" id="restoreBtn" class="font-bold underline ml-2">Restore</button></span>
            `;

            predictionForm.insertBefore(restoreBtn, predictionForm.firstChild);

            document.getElementById('restoreBtn').addEventListener('click', function (e) {
                e.preventDefault();
                Object.keys(data).forEach(key => {
                    const field = document.querySelector(`[name="${key}"]`);
                    if (field) {
                        field.value = data[key];
                    }
                });
                restoreBtn.remove();
            });
        } catch (err) {
            console.error('Error restoring form data:', err);
        }
    }
});

// ============================================
// PERFORMANCE OPTIMIZATION
// ============================================

/**
 * Debounce function for input events
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Lazy loading for images (if any)
 */
if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.add('fade-in');
                imageObserver.unobserve(img);
            }
        });
    });

    document.querySelectorAll('img[data-src]').forEach(img => imageObserver.observe(img));
}

// ============================================
// ERROR HANDLING & FALLBACKS
// ============================================

/**
 * Global error handler
 */
window.addEventListener('error', function (event) {
    console.error('Global error:', event.error);
    // Don't display scary error messages to users
});

/**
 * Unhandled promise rejection handler
 */
window.addEventListener('unhandledrejection', function (event) {
    console.error('Unhandled promise rejection:', event.reason);
    // Handle gracefully
});

// ============================================
// INITIALIZATION
// ============================================

console.log('🌦️ Australia Rain Prediction App Initialized');
console.log('Ready to make predictions!');
