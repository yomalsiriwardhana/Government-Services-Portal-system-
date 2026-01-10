// ====================================
// Authentication JavaScript
// Handles registration and login
// ====================================

const { apiRequest, showAlert, showLoading, hideLoading, setAuthToken, setUserData, validateEmail, validatePhone } = window.GovernmentPortal;

// ===== REGISTRATION =====
document.addEventListener('DOMContentLoaded', () => {
    console.log('🔍 Auth.js: DOM loaded, checking for forms...');
    
    const registerForm = document.getElementById('registerForm');
    
    if (registerForm) {
        console.log('✅ Registration form found!');
        initializeRegistrationForm();
    }
    
    const loginForm = document.getElementById('loginForm');
    
    if (loginForm) {
        console.log('✅ Login form found!');
        initializeLoginForm();
    }
});

// Initialize Registration Form
function initializeRegistrationForm() {
    const registerForm = document.getElementById('registerForm');
    const hasChildrenCheckbox = document.getElementById('hasChildren');
    const childrenSection = document.getElementById('childrenSection');
    const addChildBtn = document.getElementById('addChildBtn');
    const submitBtn = document.getElementById('submitBtn');
    
    console.log('🎯 Initializing registration form...');
    
    // Toggle children section
    if (hasChildrenCheckbox) {
        hasChildrenCheckbox.addEventListener('change', (e) => {
            if (e.target.checked) {
                childrenSection.classList.remove('hidden');
                addChildField(); // Add first child field
            } else {
                childrenSection.classList.add('hidden');
                document.getElementById('childrenContainer').innerHTML = '';
            }
        });
    }
    
    // Add child button
    if (addChildBtn) {
        addChildBtn.addEventListener('click', (e) => {
            e.preventDefault();
            addChildField();
        });
    }
    
    // Form submission - Method 1: Form submit event
    registerForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        e.stopPropagation();
        console.log('📝 Form submit event triggered!');
        
        if (!validateRegistrationForm()) {
            console.log('❌ Form validation failed');
            return false;
        }
        
        await handleRegistration();
        return false;
    });
    
    // Form submission - Method 2: Button click event (backup)
    if (submitBtn) {
        submitBtn.addEventListener('click', async (e) => {
            e.preventDefault();
            e.stopPropagation();
            console.log('🖱️ Submit button clicked!');
            
            if (!validateRegistrationForm()) {
                console.log('❌ Form validation failed');
                return false;
            }
            
            await handleRegistration();
            return false;
        });
    }
    
    console.log('✅ Registration form initialized successfully');
}

// Add Child Field
let childCount = 0;
function addChildField() {
    childCount++;
    const childrenContainer = document.getElementById('childrenContainer');
    
    const childHTML = `
        <div class="child-item" id="child-${childCount}">
            <div class="row">
                <div class="col col-md-5">
                    <div class="form-group">
                        <input type="number" name="child_age_${childCount}" 
                               placeholder="Age" class="form-control" min="0" max="25">
                    </div>
                </div>
                <div class="col col-md-5">
                    <div class="form-group">
                        <select name="child_education_${childCount}" class="form-select">
                            <option value="">Education Level</option>
                            <option value="Preschool">Preschool</option>
                            <option value="Primary">Primary School</option>
                            <option value="Secondary">Secondary School</option>
                            <option value="A/L">A/L</option>
                            <option value="University">University</option>
                        </select>
                    </div>
                </div>
                <div class="col col-md-2">
                    <button type="button" class="btn btn-danger btn-sm" onclick="removeChild(${childCount})">×</button>
                </div>
            </div>
        </div>
    `;
    
    childrenContainer.insertAdjacentHTML('beforeend', childHTML);
}

// Remove Child Field
function removeChild(id) {
    const childItem = document.getElementById(`child-${id}`);
    if (childItem) {
        childItem.remove();
    }
}
window.removeChild = removeChild; // Make it globally accessible

// Validate Registration Form
function validateRegistrationForm() {
    const form = document.getElementById('registerForm');
    let isValid = true;
    
    // Clear previous errors
    document.querySelectorAll('.form-error').forEach(el => el.classList.remove('show'));
    document.querySelectorAll('.form-control').forEach(el => el.classList.remove('error'));
    
    // Name
    const name = form.querySelector('[name="name"]').value.trim();
    if (!name || name.length < 3) {
        showFieldError('name', 'Please enter your full name (at least 3 characters)');
        isValid = false;
    }
    
    // Email
    const email = form.querySelector('[name="email"]').value.trim();
    if (!email || !validateEmail(email)) {
        showFieldError('email', 'Please enter a valid email address');
        isValid = false;
    }
    
    // Phone
    const phone = form.querySelector('[name="phone"]').value.trim();
    if (!phone || !validatePhone(phone)) {
        showFieldError('phone', 'Please enter a valid phone number (0XXXXXXXXX)');
        isValid = false;
    }
    
    // Password
    const password = form.querySelector('[name="password"]').value;
    if (!password || password.length < 6) {
        showFieldError('password', 'Password must be at least 6 characters');
        isValid = false;
    }
    
    // Confirm Password
    const confirmPassword = form.querySelector('[name="confirmPassword"]').value;
    if (password !== confirmPassword) {
        showFieldError('confirmPassword', 'Passwords do not match');
        isValid = false;
    }
    
    // Age
    const age = parseInt(form.querySelector('[name="age"]').value);
    if (!age || age < 18 || age > 100) {
        showFieldError('age', 'Age must be between 18 and 100');
        isValid = false;
    }
    
    // Location
    const location = form.querySelector('[name="location"]').value;
    if (!location) {
        showFieldError('location', 'Please select your district');
        isValid = false;
    }
    
    // Education
    const education = form.querySelector('[name="education"]').value;
    if (!education) {
        showAlert('Please select your education level', 'error');
        isValid = false;
    }
    
    // Job
    const job = form.querySelector('[name="job"]').value.trim();
    if (!job) {
        showAlert('Please enter your occupation', 'error');
        isValid = false;
    }
    
    // Marital Status
    const maritalStatus = form.querySelector('[name="maritalStatus"]').value;
    if (!maritalStatus) {
        showAlert('Please select your marital status', 'error');
        isValid = false;
    }
    
    // Terms
    const termsAccepted = form.querySelector('[name="termsAccepted"]').checked;
    if (!termsAccepted) {
        showAlert('You must accept the Terms & Conditions', 'error');
        isValid = false;
    }
    
    return isValid;
}

// Show Field Error
function showFieldError(fieldName, message) {
    const field = document.querySelector(`[name="${fieldName}"]`);
    const errorElement = document.getElementById(`${fieldName}Error`);
    
    if (field) {
        field.classList.add('error');
    }
    
    if (errorElement) {
        errorElement.textContent = message;
        errorElement.classList.add('show');
    }
}

// Handle Registration
async function handleRegistration() {
    console.log('🚀 Starting registration process...');
    showLoading();
    
    const form = document.getElementById('registerForm');
    
    // Get form data
    const formData = {
        name: form.querySelector('[name="name"]').value.trim(),
        email: form.querySelector('[name="email"]').value.trim(),
        phone: form.querySelector('[name="phone"]').value.trim(),
        password: form.querySelector('[name="password"]').value,
        age: parseInt(form.querySelector('[name="age"]').value),
        location: form.querySelector('[name="location"]').value,
        education: form.querySelector('[name="education"]').value,
        job: form.querySelector('[name="job"]').value.trim(),
        experience_years: parseInt(form.querySelector('[name="experienceYears"]').value) || 0,
        marital_status: form.querySelector('[name="maritalStatus"]').value,
        interests: getSelectedInterests(),
        children: getChildrenData(),
        marketing_emails: form.querySelector('[name="marketingEmails"]').checked,
        personalized_ads: form.querySelector('[name="personalizedAds"]').checked,
        data_analytics: form.querySelector('[name="dataAnalytics"]').checked,
        terms_accepted: form.querySelector('[name="termsAccepted"]').checked,
    };
    
    console.log('📦 Form data collected:', {
        ...formData,
        password: '***hidden***'
    });
    
    try {
        console.log('📡 Sending request to:', `${window.GovernmentPortal.API_BASE_URL}/auth/register`);
        
        const result = await apiRequest('/auth/register', {
            method: 'POST',
            body: JSON.stringify(formData),
        });
        
        console.log('📥 Response received:', result);
        
        hideLoading();
        
        if (result.success) {
            console.log('✅ Registration successful!');
            // Save token and user data
            setAuthToken(result.data.token);
            setUserData({
                user_id: result.data.user_id,
                email: formData.email,
                name: formData.name,
                ai_categories: result.data.ai_categories,
            });
            
            // Show success message
            showSuccessMessage(result.data.ai_categories);
        } else {
            console.error('❌ Registration failed:', result.data);
            showAlert(result.data.error || 'Registration failed. Please try again.', 'error');
        }
    } catch (error) {
        hideLoading();
        console.error('💥 Registration error:', error);
        showAlert('An error occurred. Please try again.', 'error');
    }
}

// Get Selected Interests
function getSelectedInterests() {
    const interests = [];
    document.querySelectorAll('[name="interests"]:checked').forEach(checkbox => {
        interests.push(checkbox.value);
    });
    return interests;
}

// Get Children Data
function getChildrenData() {
    const children = [];
    const hasChildren = document.getElementById('hasChildren').checked;
    
    if (!hasChildren) {
        return children;
    }
    
    for (let i = 1; i <= childCount; i++) {
        const ageInput = document.querySelector(`[name="child_age_${i}"]`);
        const educationSelect = document.querySelector(`[name="child_education_${i}"]`);
        
        if (ageInput && ageInput.value) {
            children.push({
                age: parseInt(ageInput.value),
                education: educationSelect ? educationSelect.value : '',
            });
        }
    }
    
    return children;
}

// Show Success Message
function showSuccessMessage(aiCategories) {
    const registerForm = document.getElementById('registerForm');
    const successMessage = document.getElementById('successMessage');
    const categoriesList = document.getElementById('categoriesList');
    
    // Hide form
    registerForm.style.display = 'none';
    
    // Show AI categories
    categoriesList.innerHTML = '';
    aiCategories.forEach(category => {
        const badge = document.createElement('span');
        badge.className = 'badge badge-primary';
        badge.textContent = category.replace(/_/g, ' ');
        categoriesList.appendChild(badge);
    });
    
    // Show success message
    successMessage.classList.remove('hidden');
    
    // Redirect after 5 seconds
    setTimeout(() => {
        window.location.href = 'dashboard.html';
    }, 5000);
}

// ===== LOGIN =====

// Initialize Login Form
function initializeLoginForm() {
    const loginForm = document.getElementById('loginForm');
    
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        if (!validateLoginForm()) {
            return;
        }
        
        await handleLogin();
    });
}

// Validate Login Form
function validateLoginForm() {
    const form = document.getElementById('loginForm');
    let isValid = true;
    
    // Clear previous errors
    document.querySelectorAll('.form-error').forEach(el => el.classList.remove('show'));
    document.querySelectorAll('.form-control').forEach(el => el.classList.remove('error'));
    
    // Email
    const email = form.querySelector('[name="email"]').value.trim();
    if (!email || !validateEmail(email)) {
        showFieldError('email', 'Please enter a valid email address');
        isValid = false;
    }
    
    // Password
    const password = form.querySelector('[name="password"]').value;
    if (!password) {
        showFieldError('password', 'Please enter your password');
        isValid = false;
    }
    
    return isValid;
}

// Handle Login
async function handleLogin() {
    showLoading();
    
    const form = document.getElementById('loginForm');
    
    const formData = {
        email: form.querySelector('[name="email"]').value.trim(),
        password: form.querySelector('[name="password"]').value,
    };
    
    try {
        const result = await apiRequest('/auth/login', {
            method: 'POST',
            body: JSON.stringify(formData),
        });
        
        hideLoading();
        
        if (result.success) {
            // Save token and user data
            setAuthToken(result.data.token);
            setUserData(result.data.user);
            
            showAlert('Login successful! Redirecting...', 'success');
            
            // Redirect to dashboard
            setTimeout(() => {
                window.location.href = 'dashboard.html';
            }, 1000);
        } else {
            showAlert(result.data.error || 'Invalid email or password', 'error');
        }
    } catch (error) {
        hideLoading();
        showAlert('An error occurred. Please try again.', 'error');
        console.error('Login error:', error);
    }
}

console.log('✅ Auth JS Loaded');