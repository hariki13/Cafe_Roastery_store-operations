// Custom JavaScript for Coffee Roasting Operations

document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Confirm delete actions
    const deleteButtons = document.querySelectorAll('[data-confirm-delete]');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this item? This action cannot be undone.')) {
                e.preventDefault();
            }
        });
    });

    // Form validation feedback
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // Initialize tooltips
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));

    // Initialize popovers
    const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]');
    const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl));
});

// Helper function to format currency
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

// Helper function to format dates
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('en-US', options);
}

// Weight loss calculator
function calculateWeightLoss(greenWeight, roastedWeight) {
    if (!greenWeight || !roastedWeight) return 0;
    return ((greenWeight - roastedWeight) / greenWeight * 100).toFixed(2);
}

// Auto-calculate weight loss on batch forms
const greenWeightInput = document.getElementById('green_weight');
const roastedWeightInput = document.getElementById('roasted_weight');
const weightLossDisplay = document.getElementById('weight_loss_display');

if (greenWeightInput && roastedWeightInput && weightLossDisplay) {
    function updateWeightLoss() {
        const green = parseFloat(greenWeightInput.value) || 0;
        const roasted = parseFloat(roastedWeightInput.value) || 0;
        const loss = calculateWeightLoss(green, roasted);
        weightLossDisplay.textContent = `${loss}%`;
    }

    greenWeightInput.addEventListener('input', updateWeightLoss);
    roastedWeightInput.addEventListener('input', updateWeightLoss);
}

// Cupping score calculator
function calculateCuppingTotal() {
    const scoreInputs = document.querySelectorAll('.cupping-score');
    let total = 0;
    
    scoreInputs.forEach(input => {
        total += parseFloat(input.value) || 0;
    });
    
    const totalDisplay = document.getElementById('total_score_display');
    if (totalDisplay) {
        totalDisplay.textContent = total.toFixed(2);
    }
    
    return total;
}

// Initialize cupping score calculator
const cuppingScoreInputs = document.querySelectorAll('.cupping-score');
if (cuppingScoreInputs.length > 0) {
    cuppingScoreInputs.forEach(input => {
        input.addEventListener('input', calculateCuppingTotal);
    });
}

// Chart color scheme
const chartColors = {
    primary: '#6F4E37',
    success: '#28a745',
    info: '#17a2b8',
    warning: '#ffc107',
    danger: '#dc3545',
    light: '#A67C52',
    dark: '#3E2723'
};

// Export chart configuration helper
function getChartConfig(type, labels, data, label) {
    return {
        type: type,
        data: {
            labels: labels,
            datasets: [{
                label: label,
                data: data,
                backgroundColor: chartColors.primary,
                borderColor: chartColors.dark,
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    };
}
