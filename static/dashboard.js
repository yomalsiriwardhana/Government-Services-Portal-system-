// Dashboard JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Check authentication
    const token = localStorage.getItem('access_token');
    if (!token) {
        window.location.href = '/login';
        return;
    }
    
    // Initialize dashboard
    loadDashboard();
    
    // Set up event listeners
    document.getElementById('logout-btn').addEventListener('click', logout);
    
    // Modal functionality
    const modal = document.getElementById('ai-modal');
    const closeBtn = document.querySelector('.close');
    
    closeBtn.onclick = function() {
        modal.style.display = 'none';
    }
    
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    }
    
    // AI search in modal
    document.getElementById('modal-search-btn').addEventListener('click', performModalAISearch);
    document.getElementById('modal-search-input').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            performModalAISearch();
        }
    });
});

async function loadDashboard() {
    try {
        // Get user info from localStorage
        const userInfo = JSON.parse(localStorage.getItem('user_info'));
        if (userInfo) {
            document.getElementById('user-name').textContent = userInfo.name;
        }
        
        // Load dashboard data from API
        const response = await makeAuthenticatedRequest('/api/user/dashboard');
        const data = await response.json();
        
        if (response.ok) {
            populateDashboard(data);
        } else {
            if (response.status === 401) {
                // Token expired, redirect to login
                logout();
            } else {
                console.error('Dashboard load failed:', data);
            }
        }
    } catch (error) {
        console.error('Error loading dashboard:', error);
    }
}

function populateDashboard(data) {
    // Update stats
    document.getElementById('engagement-count').textContent = data.stats.total_engagements;
    document.getElementById('account-age').textContent = data.stats.account_age_days;
    
    const profileStatus = document.getElementById('profile-status');
    profileStatus.textContent = data.stats.profile_completion ? 'Complete' : 'Incomplete';
    profileStatus.style.color = data.stats.profile_completion ? '#28a745' : '#ffc107';
    
    // Update recommendations
    const recommendationsList = document.getElementById('recommendations-list');
    if (data.recommendations && data.recommendations.length > 0) {
        recommendationsList.innerHTML = '';
        data.recommendations.forEach(rec => {
            const div = document.createElement('div');
            div.className = 'recommendation-item';
            
            const serviceName = rec.service.name.en;
            const reasons = rec.reasons.join(', ');
            
            div.innerHTML = `
                <div class="recommendation-title">${serviceName}</div>
                <div class="recommendation-reasons">Recommended because: ${reasons}</div>
                <div style="margin-top: 8px;">
                    <span style="background: #0b3b8c; color: white; padding: 2px 8px; border-radius: 12px; font-size: 0.8em;">
                        Score: ${rec.score}
                    </span>
                </div>
            `;
            recommendationsList.appendChild(div);
        });
    } else {
        recommendationsList.innerHTML = '<p>Start using services to get personalized recommendations!</p>';
    }
    
    // Update recent activity
    const activityDiv = document.getElementById('recent-activity');
    if (data.recent_engagements && data.recent_engagements.length > 0) {
        activityDiv.innerHTML = '';
        data.recent_engagements.forEach(eng => {
            const div = document.createElement('div');
            div.className = 'activity-item';
            
            const date = new Date(eng.timestamp).toLocaleDateString();
            const time = new Date(eng.timestamp).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
            
            div.innerHTML = `
                <div class="activity-question">${eng.question_clicked || 'Service accessed'}</div>
                <div class="activity-service">${eng.service || 'Unknown Service'}</div>
                <div class="activity-time">${date} at ${time}</div>
            `;
            activityDiv.appendChild(div);
        });
    } else {
        activityDiv.innerHTML = '<p>No recent activity. Start exploring services!</p>';
    }
}

function showAISearch() {
    document.getElementById('ai-modal').style.display = 'block';
}

async function performModalAISearch() {
    const input = document.getElementById('modal-search-input');
    const btn = document.getElementById('modal-search-btn');
    const resultsDiv = document.getElementById('modal-search-results');
    
    const query = input.value.trim();
    if (!query) return;
    
    // Show loading state
    btn.disabled = true;
    btn.textContent = 'Searching...';
    resultsDiv.innerHTML = '<div class="loading">AI is searching...</div>';
    resultsDiv.classList.add('show');
    
    try {
        const response = await fetch('/api/ai/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query: query })
        });
        
        const data = await response.json();
        
        if (data.error) {
            throw new Error(data.error);
        }
        
        displayModalSearchResults(data);
        
    } catch (error) {
        resultsDiv.innerHTML = `<div class="error">Search failed: ${error.message}</div>`;
    } finally {
        btn.disabled = false;
        btn.textContent = 'Search';
    }
}

function displayModalSearchResults(data) {
    const resultsDiv = document.getElementById('modal-search-results');
    const confidence = (data.confidence * 100).toFixed(1);
    
    let html = `
        <h4>AI Assistant Answer</h4>
        <div class="answer">
            ${formatAnswer(data.answer)}
        </div>
        <div class="sources">
            <strong>Sources:</strong> ${data.sources.join(', ')}
        </div>
        <div class="confidence">
            <strong>Confidence:</strong> ${confidence}%
        </div>
    `;
    
    resultsDiv.innerHTML = html;
}

function formatAnswer(answer) {
    return answer
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2" target="_blank">$1</a>')
        .replace(/\n\n/g, '</p><p>')
        .replace(/\n/g, '<br>');
}

function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user_info');
    window.location.href = '/';
}

// Utility function for authenticated requests
function makeAuthenticatedRequest(url, options = {}) {
    const token = localStorage.getItem('access_token');
    
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