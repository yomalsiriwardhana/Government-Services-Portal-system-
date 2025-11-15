// Authentication JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Check if user is already logged in
    const token = localStorage.getItem('access_token');
    if (token && (window.location.pathname === '/login' || window.location.pathname === '/register')) {
        window.location.href = '/dashboard';
        return;
    }
    
    // Registration form handler
    const registerForm = document.getElementById('register-form');
    if (registerForm) {
        registerForm.addEventListener('submit', handleRegister);
    }
    
    // Login form handler
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }
});

async function handleRegister(e) {
    e.preventDefault();
    
    const btn = document.getElementById('register-btn');
    const messageDiv = document.getElementById('message');
    const formData = new FormData(e.target);
    
    // Get selected interests
    const interests = Array.from(document.querySelectorAll('input[name="interests"]:checked'))
        .map(checkbox => checkbox.value);
    
    // Prepare registration data
    const data = {
        name: formData.get('name'),
        email: formData.get('email'),
        password: formData.get('password'),
        phone: formData.get('phone'),
        age: formData.get('age') ? parseInt(formData.get('age')) : null,
        location: formData.get('location'),
        interests: interests
    };
    
    // Show loading state
    btn.disabled = true;
    btn.textContent = 'Creating Account...';
    messageDiv.className = 'message';
    messageDiv.style.display = 'none';
    
    try {
        const response = await fetch('/api/auth/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
            messageDiv.className = 'message success';
            messageDiv.textContent = 'Account created successfully! Redirecting to login...';
            messageDiv.style.display = 'block';
            
            // Redirect to login after 2 seconds
            setTimeout(() => {
                window.location.href = '/login';
            }, 2000);
        } else {
            messageDiv.className = 'message error';
            messageDiv.textContent = result.message || 'Registration failed';
            messageDiv.style.display = 'block';
        }
    } catch (error) {
        messageDiv.className = 'message error';
        messageDiv.textContent = 'Network error. Please try again.';
        messageDiv.style.display = 'block';
    } finally {
        btn.disabled = false;
        btn.textContent = 'Create Account';
    }
}

async function handleLogin(e) {
    e.preventDefault();
    
    const btn = document.getElementById('login-btn');
    const messageDiv = document.getElementById('message');
    const formData = new FormData(e.target);
    
    const data = {
        email: formData.get('email'),
        password: formData.get('password')
    };
    
    // Show loading state
    btn.disabled = true;
    btn.textContent = 'Signing In...';
    messageDiv.className = 'message';
    messageDiv.style.display = 'none';
    
    try {
        const response = await fetch('/api/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
            // Store token and user info
            localStorage.setItem('access_token', result.access_token);
            localStorage.setItem('user_info', JSON.stringify(result.user));
            
            messageDiv.className = 'message success';
            messageDiv.textContent = 'Login successful! Redirecting...';
            messageDiv.style.display = 'block';
            
            // Redirect to dashboard
            setTimeout(() => {
                window.location.href = '/dashboard';
            }, 1000);
        } else {
            messageDiv.className = 'message error';
            messageDiv.textContent = result.message || 'Login failed';
            messageDiv.style.display = 'block';
        }
    } catch (error) {
        messageDiv.className = 'message error';
        messageDiv.textContent = 'Network error. Please try again.';
        messageDiv.style.display = 'block';
    } finally {
        btn.disabled = false;
        btn.textContent = 'Sign In';
    }
}

// Utility functions for authentication state
function isAuthenticated() {
    return localStorage.getItem('access_token') !== null;
}

function getAuthToken() {
    return localStorage.getItem('access_token');
}

function getUserInfo() {
    const userInfo = localStorage.getItem('user_info');
    return userInfo ? JSON.parse(userInfo) : null;
}

function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user_info');
    window.location.href = '/';
}

// Add authentication headers to API requests
function makeAuthenticatedRequest(url, options = {}) {
    const token = getAuthToken();
    
    if (!token) {
        throw new Error('No authentication token found');
    }
    
    const headers = {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
        ...options.headers
    };
    
    return fetch(url, {
        ...options,
        headers
    });
}