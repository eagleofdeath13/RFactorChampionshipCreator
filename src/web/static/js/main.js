// Main JavaScript for rFactor Championship Creator
// Racing-themed animations and interactions

// ========== TOAST NOTIFICATION SYSTEM ==========
class ToastNotification {
    static show(message, type = 'info') {
        const toastContainer = document.getElementById('toast-container') || this.createToastContainer();

        const toast = document.createElement('div');
        toast.className = `toast align-items-center text-white bg-${type} border-0`;
        toast.setAttribute('role', 'alert');
        toast.setAttribute('aria-live', 'assertive');
        toast.setAttribute('aria-atomic', 'true');

        // Racing-themed icon based on type
        const icons = {
            success: '<i class="bi bi-check-circle-fill me-2"></i>',
            danger: '<i class="bi bi-x-circle-fill me-2"></i>',
            warning: '<i class="bi bi-exclamation-triangle-fill me-2"></i>',
            info: '<i class="bi bi-info-circle-fill me-2"></i>'
        };

        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">
                    ${icons[type] || icons.info}
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        `;

        toastContainer.appendChild(toast);

        // Add entrance animation
        toast.style.transform = 'translateX(400px)';
        toast.style.opacity = '0';

        setTimeout(() => {
            toast.style.transition = 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)';
            toast.style.transform = 'translateX(0)';
            toast.style.opacity = '1';
        }, 10);

        const bsToast = new bootstrap.Toast(toast, { delay: 5000 });
        bsToast.show();

        toast.addEventListener('hidden.bs.toast', () => {
            toast.style.transform = 'translateX(400px)';
            toast.style.opacity = '0';
            setTimeout(() => toast.remove(), 300);
        });
    }

    static createToastContainer() {
        const container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'toast-container position-fixed top-0 end-0 p-3';
        container.style.zIndex = '1050';
        document.body.appendChild(container);
        return container;
    }

    static success(message) {
        this.show(message, 'success');
    }

    static error(message) {
        this.show(message, 'danger');
    }

    static warning(message) {
        this.show(message, 'warning');
    }

    static info(message) {
        this.show(message, 'info');
    }
}

// ========== LOADING OVERLAY ==========
class LoadingOverlay {
    static show(message = 'Chargement...') {
        let overlay = document.getElementById('loading-overlay');

        if (!overlay) {
            overlay = document.createElement('div');
            overlay.id = 'loading-overlay';
            overlay.className = 'spinner-overlay';
            overlay.innerHTML = `
                <div class="text-center text-white">
                    <div class="spinner-border mb-3" role="status" style="width: 3rem; height: 3rem;">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                    <div id="loading-message" style="font-family: 'Orbitron', monospace; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; font-size: 1.2rem;">
                        ${message}
                    </div>
                </div>
            `;
            document.body.appendChild(overlay);
        } else {
            document.getElementById('loading-message').textContent = message;
        }

        overlay.classList.add('active');
    }

    static hide() {
        const overlay = document.getElementById('loading-overlay');
        if (overlay) {
            overlay.classList.remove('active');
        }
    }
}

// ========== API CLIENT ==========
class APIClient {
    static async request(url, options = {}) {
        try {
            const response = await fetch(url, {
                ...options,
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers,
                },
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Request failed');
            }

            return await response.json();
        } catch (error) {
            console.error('API request failed:', error);
            throw error;
        }
    }

    static async get(url) {
        return this.request(url, { method: 'GET' });
    }

    static async post(url, data) {
        return this.request(url, {
            method: 'POST',
            body: JSON.stringify(data),
        });
    }

    static async put(url, data) {
        return this.request(url, {
            method: 'PUT',
            body: JSON.stringify(data),
        });
    }

    static async delete(url) {
        return this.request(url, { method: 'DELETE' });
    }
}

// ========== RACING ANIMATIONS ==========
class RacingAnimations {
    // Speedometer-style counter animation
    static animateCounter(element, targetValue, duration = 1200, suffix = '') {
        if (!element) return;

        const startValue = 0;
        const startTime = performance.now();

        function updateCounter(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);

            // Racing-style easing (faster start, smooth end)
            const easeOut = 1 - Math.pow(1 - progress, 4);
            const currentValue = Math.floor(startValue + (targetValue - startValue) * easeOut);

            element.textContent = currentValue + suffix;

            if (progress < 1) {
                requestAnimationFrame(updateCounter);
            } else {
                element.textContent = targetValue + suffix;
            }
        }

        requestAnimationFrame(updateCounter);
    }

    // Rev counter effect (visual pulse)
    static revEffect(element) {
        if (!element) return;

        element.style.transition = 'all 0.3s ease';
        element.style.transform = 'scale(1.1)';
        element.style.filter = 'brightness(1.3)';

        setTimeout(() => {
            element.style.transform = 'scale(1)';
            element.style.filter = 'brightness(1)';
        }, 300);
    }

    // Turbo boost effect (card entrance)
    static turboBoost(elements, delayIncrement = 100) {
        elements.forEach((element, index) => {
            element.style.opacity = '0';
            element.style.transform = 'translateX(-50px)';

            setTimeout(() => {
                element.style.transition = 'all 0.6s cubic-bezier(0.34, 1.56, 0.64, 1)';
                element.style.opacity = '1';
                element.style.transform = 'translateX(0)';
            }, index * delayIncrement);
        });
    }

    // Racing flag wave effect
    static flagWave(element) {
        if (!element) return;

        element.style.animation = 'none';
        setTimeout(() => {
            element.style.animation = 'flagWave 0.6s ease-in-out';
        }, 10);
    }
}

// Add racing flag wave keyframes dynamically
const racingKeyframes = `
    @keyframes flagWave {
        0% { transform: rotate(0deg) translateY(0); }
        25% { transform: rotate(5deg) translateY(-3px); }
        50% { transform: rotate(-5deg) translateY(0); }
        75% { transform: rotate(3deg) translateY(-2px); }
        100% { transform: rotate(0deg) translateY(0); }
    }
`;

// ========== UTILITY FUNCTIONS ==========
function confirmDelete(itemName, itemType = 'élément') {
    return confirm(`🏁 ATTENTION DANGER 🏁\n\nÊtes-vous sûr de vouloir supprimer ${itemType} "${itemName}" ?\n\nCette action est IRRÉVERSIBLE.\n\n[APPUYEZ SUR OK POUR CONFIRMER]`);
}

function formatDate(dateString) {
    const parts = dateString.split('-');
    if (parts.length === 3) {
        const [day, month, year] = parts;
        return `${day}/${month}/${year}`;
    }
    return dateString;
}

function sanitizeFileName(name) {
    return name.replace(/[^a-zA-Z0-9_-]/g, '');
}

function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return false;

    if (!form.checkValidity()) {
        form.classList.add('was-validated');
        return false;
    }

    return true;
}

// ========== PAGE INITIALIZATION ==========
document.addEventListener('DOMContentLoaded', function() {
    // Inject racing keyframes
    const styleSheet = document.createElement('style');
    styleSheet.textContent = racingKeyframes;
    document.head.appendChild(styleSheet);

    // Auto-update active nav link with racing effect
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');

    navLinks.forEach(link => {
        const linkPath = link.getAttribute('href');

        if (linkPath === currentPath || (linkPath !== '/' && currentPath.startsWith(linkPath))) {
            link.classList.add('active');

            // Add racing pulse effect to active link
            setInterval(() => {
                link.style.transition = 'all 0.3s ease';
                link.style.textShadow = '0 0 10px var(--racing-red-glow)';
                setTimeout(() => {
                    link.style.textShadow = 'none';
                }, 300);
            }, 3000);
        } else {
            link.classList.remove('active');
        }
    });

    // Card hover racing effects
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            const icon = this.querySelector('.card-title i');
            if (icon) {
                RacingAnimations.flagWave(icon);
            }
        });
    });

    // Button click effects
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            // Racing ripple effect
            const ripple = document.createElement('span');
            ripple.style.position = 'absolute';
            ripple.style.borderRadius = '50%';
            ripple.style.background = 'rgba(255, 255, 255, 0.6)';
            ripple.style.width = '10px';
            ripple.style.height = '10px';
            ripple.style.animation = 'ripple 0.6s ease-out';
            ripple.style.pointerEvents = 'none';

            const rect = this.getBoundingClientRect();
            ripple.style.left = (e.clientX - rect.left - 5) + 'px';
            ripple.style.top = (e.clientY - rect.top - 5) + 'px';

            this.appendChild(ripple);

            setTimeout(() => ripple.remove(), 600);
        });
    });

    // List group item racing hover
    const listItems = document.querySelectorAll('.list-group-item');
    listItems.forEach(item => {
        item.addEventListener('mouseenter', function() {
            this.style.transition = 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)';
        });
    });

    // Add racing pulse to spinners
    const spinners = document.querySelectorAll('.spinner-border');
    spinners.forEach(spinner => {
        spinner.style.boxShadow = '0 0 20px var(--racing-red-glow)';
    });

    console.log('%c🏁 rFactor Championship Creator 🏁', 'font-family: Orbitron, monospace; font-size: 20px; font-weight: 900; color: #E31E24; text-shadow: 0 0 10px rgba(227, 30, 36, 0.5);');
    console.log('%cRacing Dashboard Loaded Successfully', 'font-family: Rajdhani, sans-serif; font-size: 14px; color: #00FF41;');
});

// Add ripple animation keyframes
const rippleKeyframes = `
    @keyframes ripple {
        to {
            width: 100px;
            height: 100px;
            opacity: 0;
        }
    }
`;

// ========== EXPORT GLOBALLY ==========
window.ToastNotification = ToastNotification;
window.LoadingOverlay = LoadingOverlay;
window.APIClient = APIClient;
window.RacingAnimations = RacingAnimations;
window.confirmDelete = confirmDelete;
window.formatDate = formatDate;
window.sanitizeFileName = sanitizeFileName;
window.validateForm = validateForm;
