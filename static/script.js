let lang = "en";
let services = [];
let categories = [];
let currentServiceName = "";
let currentSub = null;
let profile_id = null;

// ==================== LOAD CATEGORIES ====================
async function loadCategories() {
    try {
        console.log("Loading categories...");
        const res = await fetch("/api/categories");
        
        if (!res.ok) {
            throw new Error(`HTTP ${res.status}: ${res.statusText}`);
        }
        
        categories = await res.json();
        console.log("✅ Categories loaded:", categories);
        
        const el = document.getElementById("category-list");
        if (!el) {
            console.error("❌ category-list element not found!");
            return;
        }
        
        el.innerHTML = "";
        
        if (categories.length === 0) {
            el.innerHTML = '<p style="color: white; padding: 10px; font-size: 14px;">No categories available</p>';
            return;
        }
        
        categories.forEach(c => {
            const btn = document.createElement("div");
            btn.className = "cat-item";
            btn.textContent = c.name?.[lang] || c.name?.en || c.id;
            btn.onclick = () => loadMinistriesInCategory(c);
            el.appendChild(btn);
        });
        
        // Load ads after categories
        loadAds();
    } catch (error) {
        console.error("❌ Error loading categories:", error);
        const el = document.getElementById("category-list");
        if (el) {
            el.innerHTML = '<p style="color: #ff6b6b; padding: 10px; font-size: 12px;">Failed to load categories. Please refresh.</p>';
        }
    }
}

async function loadMinistriesInCategory(cat) {
    console.log("Loading ministries for category:", cat);
    document.getElementById("sub-list").innerHTML = "";
    document.getElementById("sub-title").innerText = cat.name?.[lang] || cat.name?.en || cat.id;
    
    if (cat.ministry_ids && cat.ministry_ids.length) {
        for (let id of cat.ministry_ids) {
            try {
                const r = await fetch(`/api/service/${id}`);
                const s = await r.json();
                if (s && s.subservices) {
                    s.subservices.forEach(sub => {
                        let li = document.createElement("li");
                        li.textContent = sub.name?.[lang] || sub.name?.en || sub.id;
                        li.onclick = () => loadQuestions(s, sub);
                        document.getElementById("sub-list").appendChild(li);
                    });
                }
            } catch (error) {
                console.error(`Error loading service ${id}:`, error);
            }
        }
    } else {
        // Fallback: filter services by category
        try {
            const svcRes = await fetch("/api/services");
            const all = await svcRes.json();
            all.filter(s => s.category === cat.id).forEach(s => {
                (s.subservices || []).forEach(sub => {
                    let li = document.createElement("li");
                    li.textContent = sub.name?.[lang] || sub.name?.en || sub.id;
                    li.onclick = () => loadQuestions(s, sub);
                    document.getElementById("sub-list").appendChild(li);
                });
            });
        } catch (error) {
            console.error("Error loading services:", error);
        }
    }
}

// ==================== QUESTIONS & ANSWERS ====================
async function loadQuestions(service, sub) {
    currentServiceName = service.name?.[lang] || service.name?.en;
    currentSub = sub;
    const qList = document.getElementById("question-list");
    qList.innerHTML = "";
    document.getElementById("q-title").innerText = sub.name?.[lang] || sub.name?.en || sub.id;
    
    (sub.questions || []).forEach(q => {
        let li = document.createElement("li");
        li.textContent = q.q?.[lang] || q.q?.en;
        li.onclick = () => showAnswer(service, sub, q);
        qList.appendChild(li);
    });
}

function showAnswer(service, sub, q) {
    let html = `<h3>${q.q?.[lang] || q.q?.en}</h3>`;
    html += `<p>${q.answer?.[lang] || q.answer?.en}</p>`;
    
    if (q.downloads && q.downloads.length) {
        html += `<p><b>Downloads:</b> ${q.downloads.map(d => `<a href="${d}" target="_blank">${d.split("/").pop()}</a>`).join(", ")}</p>`;
    }
    if (q.location) {
        html += `<p><b>Location:</b> <a href="${q.location}" target="_blank">View Map</a></p>`;
    }
    if (q.instructions) {
        html += `<p><b>Instructions:</b> ${q.instructions}</p>`;
    }
    
    document.getElementById("answer-box").innerHTML = html;
    
    // Log engagement
    fetch("/api/engagement", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            user_id: profile_id,
            question_clicked: q.q?.[lang] || q.q?.en,
            service: currentServiceName,
            source: "question_click"
        })
    }).catch(err => console.error("Engagement log failed:", err));
}

// ==================== AI CHAT ====================
function openChat() {
    document.getElementById("chat-panel").style.display = "flex";
    console.log("Chat panel opened");
}

function closeChat() {
    document.getElementById("chat-panel").style.display = "none";
    console.log("Chat panel closed");
}

async function sendChat() {
    const input = document.getElementById("chat-text");
    const text = input.value.trim();
    if (!text) return;
    
    appendChat("user", text);
    input.value = "";
    
    // Show loading
    const loadingMsg = appendChat("bot", "🔍 Searching...");
    
    try {
        console.log("Sending AI search:", text);
        const res = await fetch("/api/ai/search", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({query: text, top_k: 5})
        });
        
        if (!res.ok) {
            throw new Error(`HTTP ${res.status}`);
        }
        
        const data = await res.json();
        console.log("AI response:", data);
        
        // Remove loading message
        loadingMsg.remove();
        
        let reply = data.answer || "No answer found.";
        appendChat("bot", reply);
        
        // Log engagement
        fetch("/api/engagement", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                user_id: profile_id,
                question_clicked: text,
                service: null,
                source: "ai_chat"
            })
        }).catch(err => console.error("Engagement log failed:", err));
    } catch (error) {
        console.error("AI search error:", error);
        loadingMsg.remove();
        appendChat("bot", "❌ Sorry, search failed. Please try again.");
    }
}

function appendChat(sender, text) {
    const body = document.getElementById("chat-body");
    const div = document.createElement("div");
    div.className = "chat-msg " + (sender === "user" ? "user-msg" : "bot-msg");
    div.innerText = text;
    body.appendChild(div);
    body.scrollTop = body.scrollHeight;
    return div; // Return element so we can remove loading messages
}

// ==================== AUTOSUGGEST ====================
let suggestTimer = null;

async function autosuggest(q) {
    clearTimeout(suggestTimer);
    const suggestEl = document.getElementById("suggestions");
    
    if (!q || q.length < 2) {
        suggestEl.innerHTML = "";
        return;
    }
    
    suggestTimer = setTimeout(async () => {
        try {
            const res = await fetch(`/api/search/autosuggest?q=${encodeURIComponent(q)}`);
            const items = await res.json();
            
            if (items.length === 0) {
                suggestEl.innerHTML = "";
                return;
            }
            
            suggestEl.innerHTML = items.map(it => 
                `<div class="s-item" onclick='pickSuggestion(${JSON.stringify(JSON.stringify(it))})'>${it.name?.en || it.name}</div>`
            ).join("");
        } catch (error) {
            console.error("Autosuggest error:", error);
            suggestEl.innerHTML = "";
        }
    }, 250);
}

function pickSuggestion(serialized) {
    const it = JSON.parse(serialized);
    if (it && it.subservices && it.subservices.length) {
        loadQuestions(it, it.subservices[0]);
    }
    document.getElementById("suggestions").innerHTML = "";
    document.getElementById("search-input").value = "";
}

// ==================== ADS ====================
async function loadAds() {
    try {
        console.log("Loading ads...");
        const res = await fetch("/api/ads");
        
        if (!res.ok) {
            throw new Error(`HTTP ${res.status}`);
        }
        
        const ads = await res.json();
        console.log("✅ Ads loaded:", ads);
        
        const el = document.getElementById("ads-area");
        if (!el) {
            console.error("❌ ads-area element not found!");
            return;
        }
        
        if (ads.length === 0) {
            el.innerHTML = '<p style="color: rgba(255,255,255,0.7); padding: 10px; font-size: 12px;">No announcements</p>';
            return;
        }
        
        el.innerHTML = ads.map(a => 
            `<div class="ad-card">
                <a href="${a.link || '#'}" target="_blank">
                    <h4>${a.title}</h4>
                    <p>${a.body || ''}</p>
                </a>
            </div>`
        ).join("");
    } catch (error) {
        console.error("❌ Error loading ads:", error);
        const el = document.getElementById("ads-area");
        if (el) {
            el.innerHTML = '<p style="color: #ff6b6b; padding: 10px; font-size: 11px;">Failed to load</p>';
        }
    }
}

// ==================== LANGUAGE ====================
function setLang(l) {
    lang = l;
    loadCategories();
    document.getElementById("sub-list").innerHTML = "";
    document.getElementById("question-list").innerHTML = "";
    document.getElementById("answer-box").innerHTML = "";
}

// ==================== AUTH CHECK ====================
function checkAuthStatus() {
    const token = localStorage.getItem('access_token');
    const userInfo = localStorage.getItem('user_info');
    const authButtons = document.getElementById('auth-buttons');
    const userInfoDiv = document.getElementById('user-info');
    const authMessage = document.getElementById('auth-message');
    
    if (token && userInfo) {
        try {
            const user = JSON.parse(userInfo);
            authButtons.style.display = 'none';
            userInfoDiv.style.display = 'flex';
            authMessage.textContent = `Welcome back, ${user.name}!`;
            document.getElementById('user-greeting').textContent = `Hello, ${user.name}`;
        } catch (e) {
            console.error("Error parsing user info:", e);
            localStorage.removeItem('access_token');
            localStorage.removeItem('user_info');
        }
    } else {
        authButtons.style.display = 'flex';
        userInfoDiv.style.display = 'none';
        authMessage.textContent = 'Welcome! Sign in for personalized recommendations';
    }
}

// ==================== EVENT LISTENERS ====================
document.addEventListener('DOMContentLoaded', function() {
    console.log("✅ DOM loaded, initializing...");
    
    // Search input listener
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            autosuggest(this.value);
        });
    } else {
        console.error("❌ search-input not found");
    }
    
    // Logout button
    const logoutBtn = document.getElementById('logout-link');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function() {
            localStorage.removeItem('access_token');
            localStorage.removeItem('user_info');
            location.reload();
        });
    }
    
    // Check auth
    checkAuthStatus();
});

// ==================== INITIALIZATION ====================
window.onload = async () => {
    console.log("✅ Window loaded, loading data...");
    
    // Load categories (this will also load ads)
    await loadCategories();
    
    // Load all services as fallback
    try {
        const svcRes = await fetch("/api/services");
        if (svcRes.ok) {
            services = await svcRes.json();
            console.log("✅ Services loaded:", services.length);
        }
    } catch (error) {
        console.error("❌ Error loading services:", error);
    }
};