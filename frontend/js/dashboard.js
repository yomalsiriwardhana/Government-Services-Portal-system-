// ====================================
// Dashboard JavaScript
// Handles dashboard functionality
// ====================================


const { 
    apiRequest, 
    showAlert, 
    showLoading, 
    hideLoading, 
    getUserData, 
    logout, 
    protectPage,
    timeAgo,
    formatCurrency,
    debounce
} = window.GovernmentPortal;


// Protect this page - redirect to login if not authenticated
protectPage();


// Dashboard State
let searchTimeout;


// Initialize Dashboard
document.addEventListener('DOMContentLoaded', async () => {
    await initializeDashboard();
    setupEventListeners();
});


// Initialize Dashboard
async function initializeDashboard() {
    showLoading();
    
    try {
        const userData = getUserData();
        
        if (!userData) {
            logout();
            return;
        }
        
        // Load all dashboard data
        await Promise.all([
            loadUserProfile(),
            loadPersonalizedAds(),
            loadRecentActivity()
        ]);
        
        hideLoading();
    } catch (error) {
        hideLoading();
        console.error('Dashboard initialization error:', error);
        showAlert('Failed to load dashboard data', 'error');
    }
}


// Load User Profile
async function loadUserProfile() {
    const result = await apiRequest('/auth/profile');
    
    if (result.success) {
        const user = result.data.user;
        
        // Update welcome message
        document.getElementById('userName').textContent = user.name;
        
        // Update stats
        document.getElementById('totalSearches').textContent = user.total_searches || 0;
        document.getElementById('totalCategories').textContent = (user.ai_categories || []).length;
        document.getElementById('totalClicks').textContent = user.total_ad_clicks || 0;
        
        // Load AI categories
        loadAICategories(user.ai_categories || []);
        
        // Get search stats for activity level
        await loadSearchStats();
    }
}


// Load AI Categories
function loadAICategories(categories) {
    const categoriesList = document.getElementById('aiCategoriesList');
    
    if (!categories || categories.length === 0) {
        categoriesList.innerHTML = '<p class="text-gray">No categories assigned yet</p>';
        return;
    }
    
    categoriesList.innerHTML = '';
    categories.forEach(category => {
        const badge = document.createElement('span');
        badge.className = 'category-badge';
        badge.textContent = category.replace(/_/g, ' ');
        categoriesList.appendChild(badge);
    });
}


// Load Search Stats
async function loadSearchStats() {
    const result = await apiRequest('/search/stats?days=30');
    
    if (result.success) {
        const activityLevel = result.data.activity_level || 'INACTIVE';
        document.getElementById('activityLevel').textContent = activityLevel;
    }
}


// Load Personalized Ads
async function loadPersonalizedAds() {
    const adsContainer = document.getElementById('personalizedAds');
    adsContainer.innerHTML = '<div class="ads-loading">Loading personalized ads...</div>';
    
    const result = await apiRequest('/products/personalized?limit=5');
    
    if (result.success) {
        const ads = result.data.ads || [];
        
        if (ads.length === 0) {
            adsContainer.innerHTML = '<div class="ads-empty">No ads available at the moment</div>';
            return;
        }
        
        adsContainer.innerHTML = '';
        ads.forEach(ad => {
            const adCard = createAdCard(ad);
            adsContainer.appendChild(adCard);
        });
    } else {
        adsContainer.innerHTML = '<div class="ads-empty">Failed to load ads</div>';
    }
}


// Create Ad Card
function createAdCard(ad) {
    const card = document.createElement('div');
    card.className = 'ad-card';
    card.onclick = () => handleAdClick(ad);
    
    // Create emoji based on category
    const categoryEmojis = {
        'Education': '📚',
        'Electronics': '💻',
        'Vehicles': '🚗',
        'Property': '🏠',
        'Courses': '🎓',
        'Services': '🛠️'
    };
    
    const emoji = categoryEmojis[ad.category] || '🎯';
    
    card.innerHTML = `
        <div class="ad-image">${emoji}</div>
        <div class="ad-content">
            <h4>${ad.title}</h4>
            <p>${ad.description.substring(0, 80)}...</p>
            <div class="ad-price">${formatCurrency(ad.price)}</div>
            <div class="ad-meta">
                <span class="ad-category">${ad.category}</span>
                <span class="ad-match">✨ ${Math.round(ad.relevance_score || 0)}% match</span>
            </div>
        </div>
    `;
    
    return card;
}


// Handle Ad Click
async function handleAdClick(ad) {
    // Track the click
    await apiRequest(`/products/${ad._id}/click`, {
        method: 'POST'
    });
    
    // Open product link in new tab
    if (ad.product_link) {
        window.open(ad.product_link, '_blank');
    } else {
        showAlert('Product link not available', 'info');
    }
}


// Load Recent Activity
async function loadRecentActivity() {
    const activityContainer = document.getElementById('recentActivity');
    activityContainer.innerHTML = '<div class="ads-loading">Loading activity...</div>';
    
    const result = await apiRequest('/search/history?limit=5');
    
    if (result.success) {
        const searches = result.data.searches || [];
        
        if (searches.length === 0) {
            activityContainer.innerHTML = `
                <div class="activity-empty">
                    <p>No recent activity</p>
                    <small>Start searching for services to see your activity here</small>
                </div>
            `;
            return;
        }
        
        activityContainer.innerHTML = '';
        searches.forEach(search => {
            const activityItem = document.createElement('div');
            activityItem.className = 'activity-item';
            activityItem.innerHTML = `
                <div class="activity-content">
                    <strong>🔍 Searched for "${search.query}"</strong>
                    <p>${search.category || 'General'} • ${search.results_count || 0} results</p>
                </div>
                <div class="activity-time">${timeAgo(search.timestamp)}</div>
            `;
            activityContainer.appendChild(activityItem);
        });
    } else {
        activityContainer.innerHTML = '<div class="activity-empty">Failed to load activity</div>';
    }
}


// Setup Event Listeners
function setupEventListeners() {
    // Logout button
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', (e) => {
            e.preventDefault();
            if (confirm('Are you sure you want to logout?')) {
                logout();
            }
        });
    }
    
    // Search functionality
    const searchInput = document.getElementById('searchInput');
    const searchBtn = document.getElementById('searchBtn');
    
    if (searchInput) {
        // Auto-suggest on typing
        searchInput.addEventListener('input', debounce((e) => {
            const query = e.target.value.trim();
            if (query.length >= 2) {
                showSearchSuggestions(query);
            } else {
                hideSearchSuggestions();
            }
        }, 300));
        
        // Search on Enter key
        searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                performSearch();
            }
        });
    }
    
    if (searchBtn) {
        searchBtn.addEventListener('click', performSearch);
    }
    
    // Refresh ads every 5 minutes
    setInterval(() => {
        loadPersonalizedAds();
    }, 5 * 60 * 1000);
}


// Show Search Suggestions
async function showSearchSuggestions(query) {
    const suggestionsContainer = document.getElementById('searchSuggestions');
    
    const result = await apiRequest(`/search/autosuggest?q=${encodeURIComponent(query)}`);
    
    if (result.success && result.data.suggestions.length > 0) {
        suggestionsContainer.innerHTML = '';
        suggestionsContainer.classList.remove('hidden');
        
        result.data.suggestions.forEach(suggestion => {
            const item = document.createElement('div');
            item.className = 'suggestion-item';
            item.innerHTML = `
                <strong>${suggestion.text}</strong>
                <small>${suggestion.category || ''}</small>
            `;
            item.onclick = () => {
                document.getElementById('searchInput').value = suggestion.text;
                hideSearchSuggestions();
                performSearch();
            };
            suggestionsContainer.appendChild(item);
        });
    } else {
        hideSearchSuggestions();
    }
}


// Hide Search Suggestions
function hideSearchSuggestions() {
    const suggestionsContainer = document.getElementById('searchSuggestions');
    suggestionsContainer.classList.add('hidden');
    suggestionsContainer.innerHTML = '';
}


// Perform Search
// Perform Search
async function performSearch() {
    const searchInput = document.getElementById('searchInput');
    const query = searchInput.value.trim();
    
    if (!query || query.length < 2) {
        showAlert('Please enter at least 2 characters', 'warning');
        return;
    }
    
    hideSearchSuggestions();
    showLoading();
    
    try {
        // Track the search for advertisement personalization
        const trackResult = await apiRequest('/search/track', {
            method: 'POST',
            body: JSON.stringify({
                query: query,
                timestamp: new Date().toISOString()
            })
        });
        
        console.log('✅ Search tracked:', trackResult);
        
        // Wait a moment to ensure tracking is saved
        await new Promise(resolve => setTimeout(resolve, 300));
        
        hideLoading();
        
        // Redirect to services page with search query
        window.location.href = `http://localhost:5000/services.html?search=${encodeURIComponent(query)}`;
        
    } catch (error) {
        console.error('Error tracking search:', error);
        hideLoading();
        
        // Still redirect even if tracking fails
        window.location.href = `http://localhost:5000/services.html?search=${encodeURIComponent(query)}`;
    }
}



// View Service Details
function viewServiceDetails(service) {
    // Track service view
    apiRequest(`/services/${service._id}/click`, {
        method: 'POST'
    });
    
    // Show service details in modal or redirect
    alert(`Service: ${service.name}\n\nDescription: ${service.description}\n\nDepartment: ${service.department}\n\nHow to Apply: ${service.how_to_apply}\n\nOfficial Link: ${service.official_link || 'Not available'}`);
    
    // In a real app, you would open a modal or redirect to service details page
}


console.log('✅ Dashboard JS Loaded');
