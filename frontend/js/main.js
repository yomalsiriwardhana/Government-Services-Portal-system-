// ====================================
// Government Services Portal - Main JavaScript
// Common functions and utilities
// ====================================

// API Configuration
const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
    ? 'http://localhost:5000/api' 
    : 'http://127.0.0.1:5000/api';

// Get auth token from localStorage
const getAuthToken = () => {
    return localStorage.getItem('authToken');
};

// Set auth token in localStorage
const setAuthToken = (token) => {
    localStorage.setItem('authToken', token);
};

// Remove auth token
const removeAuthToken = () => {
    localStorage.removeItem('authToken');
};

// Get user data from localStorage
const getUserData = () => {
    const userData = localStorage.getItem('userData');
    return userData ? JSON.parse(userData) : null;
};

// Set user data in localStorage
const setUserData = (data) => {
    localStorage.setItem('userData', JSON.stringify(data));
};

// Remove user data
const removeUserData = () => {
    localStorage.removeItem('userData');
};

// Check if user is logged in
const isLoggedIn = () => {
    return !!getAuthToken();
};

// Logout function
const logout = () => {
    removeAuthToken();
    removeUserData();
    window.location.href = 'login.html';
};

// API Request Helper
const apiRequest = async (endpoint, options = {}) => {
    const url = `${API_BASE_URL}${endpoint}`;
    const token = getAuthToken();
    
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
        },
    };
    
    // Add authorization header if token exists
    if (token) {
        defaultOptions.headers['Authorization'] = `Bearer ${token}`;
    }
    
    const finalOptions = {
        ...defaultOptions,
        ...options,
        headers: {
            ...defaultOptions.headers,
            ...options.headers,
        },
    };
    
    try {
        const response = await fetch(url, finalOptions);
        const data = await response.json();
        
        // Handle token expiration
        if (response.status === 401 && data.error === 'Token has expired') {
            showAlert('Your session has expired. Please login again.', 'error');
            logout();
            return null;
        }
        
        return {
            success: response.ok,
            status: response.status,
            data: data,
        };
    } catch (error) {
        console.error('API Request Error:', error);
        return {
            success: false,
            error: error.message,
        };
    }
};

// Show Alert Message
const showAlert = (message, type = 'info') => {
    const alertContainer = document.getElementById('alertContainer');
    if (!alertContainer) return;
    
    const alertClass = {
        'success': 'alert-success',
        'error': 'alert-error',
        'warning': 'alert-warning',
        'info': 'alert-info',
    }[type] || 'alert-info';
    
    const alertIcon = {
        'success': '✅',
        'error': '❌',
        'warning': '⚠️',
        'info': 'ℹ️',
    }[type] || 'ℹ️';
    
    const alertHTML = `
        <div class="alert ${alertClass}">
            <span>${alertIcon}</span>
            <span>${message}</span>
        </div>
    `;
    
    alertContainer.innerHTML = alertHTML;
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        alertContainer.innerHTML = '';
    }, 5000);
};

// Show Loading Spinner
const showLoading = () => {
    const loadingHTML = `
        <div class="loading-overlay" id="loadingOverlay">
            <div class="spinner"></div>
        </div>
    `;
    document.body.insertAdjacentHTML('beforeend', loadingHTML);
};

// Hide Loading Spinner
const hideLoading = () => {
    const loadingOverlay = document.getElementById('loadingOverlay');
    if (loadingOverlay) {
        loadingOverlay.remove();
    }
};

// Format Date
const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
    });
};

// Format Time Ago
const timeAgo = (dateString) => {
    const date = new Date(dateString);
    const now = new Date();
    const seconds = Math.floor((now - date) / 1000);
    
    let interval = Math.floor(seconds / 31536000);
    if (interval > 1) return interval + ' years ago';
    if (interval === 1) return '1 year ago';
    
    interval = Math.floor(seconds / 2592000);
    if (interval > 1) return interval + ' months ago';
    if (interval === 1) return '1 month ago';
    
    interval = Math.floor(seconds / 86400);
    if (interval > 1) return interval + ' days ago';
    if (interval === 1) return '1 day ago';
    
    interval = Math.floor(seconds / 3600);
    if (interval > 1) return interval + ' hours ago';
    if (interval === 1) return '1 hour ago';
    
    interval = Math.floor(seconds / 60);
    if (interval > 1) return interval + ' minutes ago';
    if (interval === 1) return '1 minute ago';
    
    return 'just now';
};

// Format Currency (LKR)
const formatCurrency = (amount) => {
    return `Rs. ${parseFloat(amount).toLocaleString('en-LK', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
    })}`;
};

// Truncate Text
const truncateText = (text, maxLength) => {
    if (text.length <= maxLength) return text;
    return text.substr(0, maxLength) + '...';
};

// Validate Email
const validateEmail = (email) => {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
};

// Validate Phone (Sri Lanka)
const validatePhone = (phone) => {
    const re = /^0[0-9]{9}$/;
    return re.test(phone);
};

// Mobile Menu Toggle
document.addEventListener('DOMContentLoaded', () => {
    const navbarToggle = document.getElementById('navbarToggle');
    const navbarMenu = document.getElementById('navbarMenu');
    
    if (navbarToggle && navbarMenu) {
        navbarToggle.addEventListener('click', () => {
            navbarMenu.classList.toggle('active');
        });
    }
    
    // Update navbar based on login status
    updateNavbar();
});

// Update Navbar Based on Login Status
const updateNavbar = () => {
    const navbarMenu = document.getElementById('navbarMenu');
    if (!navbarMenu) return;
    
    const loggedIn = isLoggedIn();
    const userData = getUserData();
    
    if (loggedIn && userData) {
        // User is logged in - show dashboard and logout
        const loginLink = navbarMenu.querySelector('a[href="login.html"]');
        const registerBtn = navbarMenu.querySelector('a[href="register.html"]');
        
        if (loginLink) {
            loginLink.textContent = 'Dashboard';
            loginLink.href = 'dashboard.html';
        }
        
        if (registerBtn) {
            registerBtn.textContent = 'Logout';
            registerBtn.href = '#';
            registerBtn.onclick = (e) => {
                e.preventDefault();
                if (confirm('Are you sure you want to logout?')) {
                    logout();
                }
            };
        }
    }
};

// Protect Page (Redirect to login if not authenticated)
const protectPage = () => {
    if (!isLoggedIn()) {
        window.location.href = 'login.html';
    }
};

// Redirect if Already Logged In
const redirectIfLoggedIn = () => {
    if (isLoggedIn()) {
        window.location.href = 'dashboard.html';
    }
};

// Form Validation Helper
const validateForm = (formId, rules) => {
    const form = document.getElementById(formId);
    if (!form) return false;
    
    let isValid = true;
    
    Object.keys(rules).forEach(fieldName => {
        const field = form.querySelector(`[name="${fieldName}"]`);
        const errorElement = document.getElementById(`${fieldName}Error`);
        
        if (!field) return;
        
        const value = field.value.trim();
        const rule = rules[fieldName];
        
        // Reset error state
        field.classList.remove('error');
        if (errorElement) errorElement.classList.remove('show');
        
        // Required validation
        if (rule.required && !value) {
            isValid = false;
            field.classList.add('error');
            if (errorElement) {
                errorElement.textContent = rule.message || 'This field is required';
                errorElement.classList.add('show');
            }
            return;
        }
        
        // Custom validation
        if (rule.validate && !rule.validate(value)) {
            isValid = false;
            field.classList.add('error');
            if (errorElement) {
                errorElement.textContent = rule.message || 'Invalid value';
                errorElement.classList.add('show');
            }
        }
    });
    
    return isValid;
};

// Debounce Function
const debounce = (func, wait) => {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
};

// Scroll to Top
const scrollToTop = () => {
    window.scrollTo({
        top: 0,
        behavior: 'smooth',
    });
};

// Copy to Clipboard
const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text).then(() => {
        showAlert('Copied to clipboard!', 'success');
    }).catch(() => {
        showAlert('Failed to copy', 'error');
    });
};

// Export functions for use in other files
window.GovernmentPortal = {
    API_BASE_URL,
    getAuthToken,
    setAuthToken,
    removeAuthToken,
    getUserData,
    setUserData,
    removeUserData,
    isLoggedIn,
    logout,
    apiRequest,
    showAlert,
    showLoading,
    hideLoading,
    formatDate,
    timeAgo,
    formatCurrency,
    truncateText,
    validateEmail,
    validatePhone,
    protectPage,
    redirectIfLoggedIn,
    validateForm,
    debounce,
    scrollToTop,
    copyToClipboard,
};

console.log('✅ Government Portal - Main JS Loaded');