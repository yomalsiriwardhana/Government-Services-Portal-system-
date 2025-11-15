document.getElementById("login-form").onsubmit = async (e) => {
    e.preventDefault();
    const form = new FormData(e.target);
    const res = await fetch('/admin/login', { method:'POST', body: form });
    if (res.redirected) window.location = res.url;
    else {
        // Try to fetch insights to check if logged in
        loadDashboard();
    }
};

async function loadDashboard(){
    const dashEl = document.getElementById("dashboard");
    try {
        const r = await fetch('/api/admin/insights');
        if (r.status === 401) {
            document.getElementById("login-box").style.display = "block";
            dashEl.style.display = "none";
            return;
        }
        const data = await r.json();
        document.getElementById("login-box").style.display = "none";
        dashEl.style.display = "block";
        
        // Age Chart
        new Chart(document.getElementById("ageChart"), { 
            type:'bar',
            data:{ 
                labels:Object.keys(data.age_groups), 
                datasets:[{
                    label:"Users by Age Group",
                    data:Object.values(data.age_groups),
                    backgroundColor: 'rgba(59, 130, 246, 0.6)',
                    borderColor: 'rgba(59, 130, 246, 1)',
                    borderWidth: 1
                }] 
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'User Age Distribution'
                    }
                }
            }
        });
        
        // Jobs Chart
        new Chart(document.getElementById("jobChart"), { 
            type:'pie',
            data:{ 
                labels:Object.keys(data.jobs), 
                datasets:[{
                    label:"Jobs", 
                    data:Object.values(data.jobs),
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.6)',
                        'rgba(54, 162, 235, 0.6)',
                        'rgba(255, 205, 86, 0.6)',
                        'rgba(75, 192, 192, 0.6)',
                        'rgba(153, 102, 255, 0.6)',
                        'rgba(255, 159, 64, 0.6)'
                    ]
                }] 
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'User Job Distribution'
                    }
                }
            }
        });
        
        // Services Chart
        new Chart(document.getElementById("serviceChart"), { 
            type:'doughnut',
            data:{ 
                labels:Object.keys(data.services), 
                datasets:[{
                    label:"Services", 
                    data:Object.values(data.services),
                    backgroundColor: [
                        'rgba(34, 197, 94, 0.6)',
                        'rgba(168, 85, 247, 0.6)',
                        'rgba(239, 68, 68, 0.6)',
                        'rgba(245, 158, 11, 0.6)',
                        'rgba(6, 182, 212, 0.6)'
                    ]
                }] 
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Popular Services'
                    }
                }
            }
        });
        
        // Questions Chart
        new Chart(document.getElementById("questionChart"), { 
            type:'bar',
            data:{ 
                labels:Object.keys(data.questions).slice(0,10), 
                datasets:[{
                    label:"Top Questions", 
                    data:Object.values(data.questions).slice(0,10),
                    backgroundColor: 'rgba(168, 85, 247, 0.6)',
                    borderColor: 'rgba(168, 85, 247, 1)',
                    borderWidth: 1
                }] 
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Most Asked Questions'
                    }
                },
                scales: {
                    x: {
                        ticks: {
                            maxRotation: 45,
                            minRotation: 45
                        }
                    }
                }
            }
        });
        
        // Premium list
        const pl = document.getElementById("premiumList");
        pl.innerHTML = data.premium_suggestions.length ? 
            data.premium_suggestions.map(p => `<div style="padding:10px;margin:5px;background:#f0f9ff;border-radius:5px;">User: ${p.user} | Question: ${p.question} | Count: ${p.count}</div>`).join("") : 
            "<div style='padding:10px;background:#f9fafb;border-radius:5px;'>No premium suggestions at this time</div>";
        
        // Engagements list
        const res = await fetch('/api/admin/engagements');
        const items = await res.json();
        const tbody = document.querySelector("#engTable tbody");
        tbody.innerHTML = "";
        
        items.forEach(it=>{
            const row = `<tr>
                <td>${it.age||""}</td>
                <td>${it.job||""}</td>
                <td>${(it.desires||[]).join(", ")}</td>
                <td>${it.question_clicked||""}</td>
                <td>${it.service||""}</td>
                <td>${it.timestamp||""}</td>
            </tr>`;
            tbody.insertAdjacentHTML('beforeend', row);
        });
        
    } catch (err) {
        console.error(err);
        alert('Error loading dashboard data');
    }
}

document.getElementById("logoutBtn")?.addEventListener('click', async ()=>{
    await fetch('/api/admin/logout', {method:'POST'});
    window.location="/admin";
});

document.getElementById("exportCsv")?.addEventListener('click', ()=>{ 
    window.location = '/api/admin/export_csv'; 
});

// Email notification functionality
document.getElementById("sendPremiumBtn")?.addEventListener('click', sendPremiumSuggestions);
document.getElementById("emailReportBtn")?.addEventListener('click', sendEmailReport);
document.getElementById("viewCandidatesBtn")?.addEventListener('click', viewPremiumCandidates);

// System monitoring functionality
document.getElementById("systemStatsBtn")?.addEventListener('click', viewSystemStats);
document.getElementById("clearCacheBtn")?.addEventListener('click', clearSystemCache);
document.getElementById("rateLimitStatusBtn")?.addEventListener('click', viewRateLimitStatus);

async function viewSystemStats() {
    try {
        const response = await fetch('/api/admin/system-stats', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        if (response.status === 401 || response.status === 302) {
            alert('Session expired. Please login again.');
            window.location.href = '/admin/login';
            return;
        }
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        const stats = await response.json();
        
        if (stats.error) {
            alert('Error: ' + stats.error);
            return;
        }
        
        let message = 'SYSTEM PERFORMANCE STATS\n\n';
        
        // Cache Stats
        message += 'CACHE PERFORMANCE:\n';
        message += `- Cache Hits: ${stats.cache.hits}\n`;
        message += `- Cache Misses: ${stats.cache.misses}\n`;
        message += `- Hit Rate: ${stats.cache.hit_rate}%\n`;
        message += `- Total Requests: ${stats.cache.total_requests}\n\n`;
        
        // Rate Limiting
        message += 'RATE LIMITING:\n';
        message += `- Blocked IPs: ${stats.rate_limiting.blocked_ips}\n`;
        message += `- Suspicious Activities Tracked: ${stats.rate_limiting.suspicious_activity_tracked}\n\n`;
        
        // Database Stats
        message += 'DATABASE METRICS:\n';
        message += `- Total Users: ${stats.database.total_users}\n`;
        message += `- Total Services: ${stats.database.total_services}\n`;
        message += `- Total Engagements: ${stats.database.total_engagements}\n`;
        message += `- Recent Engagements (24h): ${stats.database.recent_engagements}\n`;
        
        alert(message);
    } catch (error) {
        alert('Error loading system stats: ' + error.message);
    }
}

async function clearSystemCache() {
    if (!confirm('Are you sure you want to clear the system cache? This may temporarily slow down the application.')) {
        return;
    }
    
    const btn = document.getElementById("clearCacheBtn");
    const originalText = btn.textContent;
    
    btn.disabled = true;
    btn.textContent = 'Clearing...';
    
    try {
        const response = await fetch('/api/admin/clear-cache', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        if (response.status === 401 || response.status === 302) {
            alert('Session expired. Please login again.');
            window.location.href = '/admin/login';
            return;
        }
        
        const result = await response.json();
        
        if (result.success) {
            alert(result.message);
        } else {
            alert('Error: ' + result.error);
        }
    } catch (error) {
        alert('Network error: ' + error.message);
    } finally {
        btn.disabled = false;
        btn.textContent = originalText;
    }
}

async function viewPremiumCandidates() {
    try {
        const response = await fetch('/api/admin/premium-candidates', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        if (response.status === 401 || response.status === 302) {
            alert('Session expired. Please login again.');
            window.location.href = '/admin/login';
            return;
        }
        
        const result = await response.json();
        
        if (result.error) {
            alert('Error: ' + result.error);
            return;
        }
        
        if (result.candidates && result.candidates.length > 0) {
            let message = `Found ${result.total} premium candidates:\n\n`;
            result.candidates.forEach((candidate, index) => {
                message += `${index + 1}. ${candidate.user_name} (${candidate.user_email})\n`;
                message += `   Service: ${candidate.service_name}\n`;
                message += `   Engagements: ${candidate.engagement_count}\n`;
                message += `   Questions: ${candidate.questions.length}\n\n`;
            });
            alert(message);
        } else {
            alert('No premium candidates found at this time.');
        }
    } catch (error) {
        alert('Error loading candidates: ' + error.message);
    }
}

async function viewRateLimitStatus() {
    try {
        const response = await fetch('/api/admin/rate-limit-status', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        if (response.status === 401 || response.status === 302) {
            alert('Session expired. Please login again.');
            window.location.href = '/admin/login';
            return;
        }
        
        const status = await response.json();
        
        if (status.error) {
            alert('Error: ' + status.error);
            return;
        }
        
        let message = 'RATE LIMITING STATUS\n\n';
        
        // Blocked Clients
        message += 'BLOCKED CLIENTS:\n';
        if (status.blocked_clients.length > 0) {
            status.blocked_clients.forEach(client => {
                message += `- ${client}\n`;
            });
        } else {
            message += 'None\n';
        }
        
        message += '\nSUSPICIOUS CLIENTS:\n';
        const suspiciousClients = Object.keys(status.suspicious_clients);
        if (suspiciousClients.length > 0) {
            suspiciousClients.forEach(client => {
                message += `- ${client}: ${status.suspicious_clients[client]} activities\n`;
            });
        } else {
            message += 'None\n';
        }
        
        message += '\nRATE LIMITS:\n';
        Object.keys(status.rate_limits).forEach(endpoint => {
            message += `- ${endpoint}: ${status.rate_limits[endpoint]}\n`;
        });
        
        alert(message);
    } catch (error) {
        alert('Error loading rate limit status: ' + error.message);
    }
}

async function sendPremiumSuggestions() {
    const btn = document.getElementById("sendPremiumBtn");
    const originalText = btn.textContent;
    
    btn.disabled = true;
    btn.textContent = 'Sending...';
    
    try {
        const response = await fetch('/api/admin/send-premium-suggestions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        if (response.status === 401 || response.status === 302) {
            alert('Session expired. Please login again.');
            window.location.href = '/admin/login';
            return;
        }
        
        const result = await response.json();
        
        if (result.success) {
            alert(result.message);
        } else {
            alert('Error: ' + result.message);
        }
    } catch (error) {
        alert('Network error: ' + error.message);
    } finally {
        btn.disabled = false;
        btn.textContent = originalText;
    }
}

async function sendEmailReport() {
    const email = prompt('Enter admin email address for the report:');
    if (!email) return;
    
    const btn = document.getElementById("emailReportBtn");
    const originalText = btn.textContent;
    
    btn.disabled = true;
    btn.textContent = 'Sending...';
    
    try {
        const response = await fetch('/api/admin/email-report', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email: email })
        });
        
        if (response.status === 401 || response.status === 302) {
            alert('Session expired. Please login again.');
            window.location.href = '/admin/login';
            return;
        }
        
        const result = await response.json();
        
        if (result.success) {
            alert(result.message);
        } else {
            alert('Error: ' + result.message);
        }
    } catch (error) {
        alert('Network error: ' + error.message);
    } finally {
        btn.disabled = false;
        btn.textContent = originalText;
    }
}

async function viewPremiumCandidates() {
    try {
        const response = await fetch('/api/admin/premium-candidates');
        const result = await response.json();
        
        if (result.candidates && result.candidates.length > 0) {
            let message = `Found ${result.total} premium candidates:\n\n`;
            result.candidates.forEach((candidate, index) => {
                message += `${index + 1}. ${candidate.user_name} (${candidate.user_email})\n`;
                message += `   Service: ${candidate.service_name}\n`;
                message += `   Engagements: ${candidate.engagement_count}\n`;
                message += `   Questions: ${candidate.questions.length}\n\n`;
            });
            alert(message);
        } else {
            alert('No premium candidates found at this time.');
        }
    } catch (error) {
        alert('Error loading candidates: ' + error.message);
    }
}

window.onload = loadDashboard;