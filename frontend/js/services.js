// Services page functionality
let allServices = [];
let filteredServices = [];


// Load services on page load
document.addEventListener('DOMContentLoaded', function() {
    loadCategories();
    
    // Check if there's a search parameter in URL
    const urlParams = new URLSearchParams(window.location.search);
    const searchParam = urlParams.get('search');
    
    if (searchParam) {
        // Set the search input value
        const searchInput = document.getElementById('searchInput');
        if (searchInput) {
            searchInput.value = searchParam;
        }
        
        // Trigger search with the parameter and track it
        searchServicesFromURL(searchParam);
    } else {
        // No search parameter, load all services normally
        loadServices();
    }
    
    // Setup event listeners
    const categoryFilter = document.getElementById('categoryFilter');
    if (categoryFilter) {
        categoryFilter.addEventListener('change', filterServices);
    }
    
    const searchBtn = document.getElementById('searchBtn');
    if (searchBtn) {
        searchBtn.addEventListener('click', searchServices);
    }
    
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                searchServices();
            }
        });
    }
});


// Search services from URL parameter (when redirected from dashboard)
async function searchServicesFromURL(query) {
    try {
        const token = localStorage.getItem('token');
        
        if (token) {
            // Call search API with authentication
            const response = await fetch(
                `/api/search/?q=${encodeURIComponent(query)}`,
                {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    }
                }
            );
            
            const data = await response.json();
            
            if (data.services) {
                allServices = data.services;
                filteredServices = data.services;
                displayServices(filteredServices);
                
                // Show success message
                showSuccessMessage(`Found ${data.services.length} services for "${query}"`);
            } else {
                // No results
                displayServices([]);
            }
        } else {
            // Not logged in, load all services and filter locally
            await loadServices();
            filterServicesByQuery(query);
        }
    } catch (error) {
        console.error('Error searching services:', error);
        // Fallback: load all and filter locally
        await loadServices();
        filterServicesByQuery(query);
    }
}


// Filter services by query text (local filtering)
function filterServicesByQuery(query) {
    const searchTerm = query.toLowerCase();
    filteredServices = allServices.filter(service => {
        return service.name.toLowerCase().includes(searchTerm) ||
               (service.description && service.description.toLowerCase().includes(searchTerm)) ||
               (service.category && service.category.toLowerCase().includes(searchTerm));
    });
    displayServices(filteredServices);
}


// Show success message
function showSuccessMessage(message) {
    const container = document.getElementById('servicesGrid');
    if (container && container.parentElement) {
        const alert = document.createElement('div');
        alert.className = 'alert alert-success alert-dismissible fade show';
        alert.innerHTML = `
            <strong>✅ ${message}</strong>
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        container.parentElement.insertBefore(alert, container);
        
        // Auto-dismiss after 3 seconds
        setTimeout(() => {
            alert.remove();
        }, 3000);
    }
}


// Load all categories
async function loadCategories() {
    try {
        const response = await fetch('/api/services/categories');
        const data = await response.json();
        
        if (data.success && data.categories) {
            const select = document.getElementById('categoryFilter');
            if (select) {
                // Clear existing options except "All Categories"
                select.innerHTML = '<option value="">All Categories</option>';
                
                // Add categories
                data.categories.forEach(category => {
                    const option = document.createElement('option');
                    option.value = category;
                    option.textContent = category;
                    select.appendChild(option);
                });
            }
        }
    } catch (error) {
        console.error('Error loading categories:', error);
    }
}


// Load all services
async function loadServices() {
    try {
        const response = await fetch('/api/services/');
        const data = await response.json();
        
        if (data.success && data.services) {
            allServices = data.services;
            filteredServices = allServices;
            displayServices(filteredServices);
        } else {
            showError('Failed to load services');
        }
    } catch (error) {
        console.error('Error loading services:', error);
        showError('Error connecting to server');
    }
}


// Display services in grid
function displayServices(services) {
    const container = document.getElementById('servicesGrid');
    if (!container) return;
    
    if (services.length === 0) {
        container.innerHTML = `
            <div class="col-12 text-center py-5">
                <p class="text-muted">No services found matching your criteria.</p>
            </div>
        `;
        return;
    }
    
    container.innerHTML = services.map(service => `
        <div class="col-md-6 col-lg-4 mb-4">
            <div class="service-card" onclick="showServiceDetails('${service.id}')">
                <div class="service-icon">${service.icon || '📋'}</div>
                <h3 class="service-title">${service.name}</h3>
                <p class="service-description">${service.description || 'No description available'}</p>
                <div class="service-meta">
                    <span class="badge bg-primary">${service.category || 'General'}</span>
                    <span class="badge bg-secondary">${service.ministry || 'Government'}</span>
                </div>
                <button class="btn btn-outline-primary btn-sm mt-3">View Details →</button>
            </div>
        </div>
    `).join('');
}


// Filter services by category
function filterServices() {
    const categoryFilter = document.getElementById('categoryFilter');
    const searchInput = document.getElementById('searchInput');
    
    const selectedCategory = categoryFilter ? categoryFilter.value : '';
    const searchTerm = searchInput ? searchInput.value.toLowerCase() : '';
    
    filteredServices = allServices.filter(service => {
        const matchesCategory = !selectedCategory || service.category === selectedCategory;
        const matchesSearch = !searchTerm || 
            service.name.toLowerCase().includes(searchTerm) ||
            (service.description && service.description.toLowerCase().includes(searchTerm));
        
        return matchesCategory && matchesSearch;
    });
    
    displayServices(filteredServices);
}


// Search services with API call and tracking
async function searchServices() {
    const searchInput = document.getElementById('searchInput');
    const categoryFilter = document.getElementById('categoryFilter');
    
    const query = searchInput ? searchInput.value.trim() : '';
    const category = categoryFilter ? categoryFilter.value : '';
    
    if (!query && !category) {
        // No search query, just filter locally
        filterServices();
        return;
    }
    
    // If there's a search query, call API for tracking
    if (query && query.length >= 2) {
        try {
            const token = localStorage.getItem('authToken');
            if (token) {
                // Call search API with authentication to track the search
                const response = await fetch(
                    `/api/search/?q=${encodeURIComponent(query)}${category ? '&category=' + category : ''}`,
                    {
                        method: 'GET',
                        headers: {
                            'Authorization': `Bearer ${token}`,
                            'Content-Type': 'application/json'
                        }
                    }
                );
                
                const data = await response.json();
                
                if (data.services) {
                    allServices = data.services;
                    filteredServices = data.services;
                    displayServices(filteredServices);
                    
                    showSuccessMessage(`Found ${data.services.length} services`);
                }
                
                // Mark that ads need refresh when user returns to dashboard
                if (data.profile_updated) {
                    localStorage.setItem('adsNeedRefresh', 'true');
                    console.log('✅ Search tracked - ads will refresh on dashboard');
                }
            } else {
                // Not logged in, just filter locally
                filterServices();
            }
        } catch (error) {
            console.error('Error searching services:', error);
            // Fallback to local filtering
            filterServices();
        }
    } else {
        // Short query, just filter locally
        filterServices();
    }
}


// Show service details in modal
async function showServiceDetails(serviceId) {
    try {
        // Track click
        fetch(`/api/services/${serviceId}/click`, { method: 'POST' })
            .catch(err => console.log('Click tracking failed:', err));
        
        // Fetch full service details
        const response = await fetch(`/api/services/${serviceId}`);
        const data = await response.json();
        
        if (data.success && data.service) {
            displayServiceModal(data.service);
        } else {
            showError('Service not found');
        }
    } catch (error) {
        console.error('Error loading service details:', error);
        showError('Error loading service details');
    }
}


// Display service details in modal
function displayServiceModal(service) {
    const modal = document.getElementById('serviceModal');
    if (!modal) {
        console.error('Modal element not found');
        return;
    }
    
    const details = service.details || {};
    
    // Build modal content
    let modalContent = `
        <div class="modal-header">
            <div>
                <h2 class="modal-title">
                    <span class="service-icon-large">${service.icon || '📋'}</span>
                    ${service.name}
                </h2>
                <p class="text-muted mb-0">${service.ministry || 'Government of India'}</p>
            </div>
            <button type="button" class="btn-close" onclick="closeServiceModal()"></button>
        </div>
        <div class="modal-body">
    `;
    
    // Full Description
    if (details.full_description) {
        modalContent += `
            <section class="mb-4">
                <h3>Overview</h3>
                <p>${details.full_description}</p>
            </section>
        `;
    }
    
    // Types (if applicable)
    if (details.types && details.types.length > 0) {
        modalContent += `
            <section class="mb-4">
                <h3>Types</h3>
                <ul>
                    ${details.types.map(type => `<li>${type}</li>`).join('')}
                </ul>
            </section>
        `;
    }
    
    // Eligibility
    if (details.eligibility && details.eligibility.length > 0) {
        modalContent += `
            <section class="mb-4">
                <h3>Eligibility Criteria</h3>
                <ul class="eligibility-list">
                    ${details.eligibility.map(item => `<li>✓ ${item}</li>`).join('')}
                </ul>
            </section>
        `;
    }
    
    // Required Documents
    if (details.required_documents && details.required_documents.length > 0) {
        modalContent += `
            <section class="mb-4">
                <h3>Required Documents</h3>
                <ul class="documents-list">
                    ${details.required_documents.map(doc => `<li>📄 ${doc}</li>`).join('')}
                </ul>
            </section>
        `;
    }
    
    // Application Process
    if (details.application_process && details.application_process.length > 0) {
        modalContent += `
            <section class="mb-4">
                <h3>Application Process</h3>
                <ol class="process-list">
                    ${details.application_process.map(step => `<li>${step}</li>`).join('')}
                </ol>
            </section>
        `;
    }
    
    // Fees
    if (details.fees) {
        modalContent += `
            <section class="mb-4">
                <h3>Fees</h3>
        `;
        
        if (typeof details.fees === 'string') {
            modalContent += `<p class="fee-amount">${details.fees}</p>`;
        } else if (typeof details.fees === 'object') {
            modalContent += `<ul class="fees-list">`;
            for (const [key, value] of Object.entries(details.fees)) {
                const label = key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
                modalContent += `<li><strong>${label}:</strong> ${value}</li>`;
            }
            modalContent += `</ul>`;
        }
        
        modalContent += `</section>`;
    }
    
    // Processing Time
    if (details.processing_time) {
        modalContent += `
            <section class="mb-4">
                <h3>Processing Time</h3>
        `;
        
        if (typeof details.processing_time === 'string') {
            modalContent += `<p class="processing-time">⏱️ ${details.processing_time}</p>`;
        } else if (typeof details.processing_time === 'object') {
            modalContent += `<ul>`;
            for (const [key, value] of Object.entries(details.processing_time)) {
                const label = key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
                modalContent += `<li><strong>${label}:</strong> ${value}</li>`;
            }
            modalContent += `</ul>`;
        }
        
        modalContent += `</section>`;
    }
    
    // Validity
    if (details.validity) {
        modalContent += `
            <section class="mb-4">
                <h3>Validity</h3>
        `;
        
        if (typeof details.validity === 'string') {
            modalContent += `<p>${details.validity}</p>`;
        } else if (typeof details.validity === 'object') {
            modalContent += `<ul>`;
            for (const [key, value] of Object.entries(details.validity)) {
                const label = key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
                modalContent += `<li><strong>${label}:</strong> ${value}</li>`;
            }
            modalContent += `</ul>`;
        }
        
        modalContent += `</section>`;
    }
    
    // Important Notes
    if (details.important_notes && details.important_notes.length > 0) {
        modalContent += `
            <section class="mb-4">
                <h3>Important Notes</h3>
                <div class="alert alert-info">
                    <ul class="mb-0">
                        ${details.important_notes.map(note => `<li>${note}</li>`).join('')}
                    </ul>
                </div>
            </section>
        `;
    }
    
    // Contact Information
    if (details.contact) {
        modalContent += `
            <section class="mb-4">
                <h3>Contact Information</h3>
                <div class="contact-info">
        `;
        
        if (details.contact.website) {
            modalContent += `<p>🌐 <strong>Website:</strong> <a href="${details.contact.website}" target="_blank">${details.contact.website}</a></p>`;
        }
        if (details.contact.helpline) {
            modalContent += `<p>📞 <strong>Helpline:</strong> ${details.contact.helpline}</p>`;
        }
        if (details.contact.email) {
            modalContent += `<p>📧 <strong>Email:</strong> <a href="mailto:${details.contact.email}">${details.contact.email}</a></p>`;
        }
        
        modalContent += `
                </div>
            </section>
        `;
    }
    
    // Online Services Available
    if (details.online_services && details.online_services.length > 0) {
        modalContent += `
            <section class="mb-4">
                <h3>Online Services Available</h3>
                <ul class="online-services-list">
                    ${details.online_services.map(service => `<li>💻 ${service}</li>`).join('')}
                </ul>
            </section>
        `;
    }
    
    modalContent += `
        </div>
        <div class="modal-footer">
            <button type="button" class="btn btn-secondary" onclick="closeServiceModal()">Close</button>
            ${details.contact && details.contact.website ? 
                `<a href="${details.contact.website}" target="_blank" class="btn btn-primary">Visit Official Website →</a>` 
                : ''}
        </div>
    `;
    
    // Set modal content and show
    const modalElement = document.getElementById('serviceModal');
    if (modalElement) {
        modalElement.innerHTML = modalContent;
        modalElement.style.display = 'block';
        document.body.style.overflow = 'hidden'; // Prevent background scroll
    }
}


// Close service modal
function closeServiceModal() {
    const modal = document.getElementById('serviceModal');
    if (modal) {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto'; // Re-enable scroll
    }
}


// Close modal when clicking outside
window.addEventListener('click', function(event) {
    const modal = document.getElementById('serviceModal');
    if (event.target === modal) {
        closeServiceModal();
    }
});


// Show error message
function showError(message) {
    const container = document.getElementById('servicesGrid');
    if (container) {
        container.innerHTML = `
            <div class="col-12">
                <div class="alert alert-danger" role="alert">
                    <strong>Error:</strong> ${message}
                </div>
            </div>
        `;
    }
}
