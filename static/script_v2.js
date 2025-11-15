let lang = "en";
let services = [];
let categories = [];
let currentServiceName = "";
let currentSub = null;
let profile_id = null;

// ==================== CATEGORIES ====================
async function loadCategories() {
    try {
        const res = await fetch("/api/categories");
        categories = await res.json();
        const el = document.getElementById("category-list");
        el.innerHTML = "";
        
        categories.forEach(c => {
            const btn = document.createElement("div");
            btn.className = "cat-item";
            btn.textContent = c.name?.[lang] || c.name?.en || c.id;
            btn.onclick = () => loadMinistriesInCategory(c);
            el.appendChild(btn);
        });
        
        loadAds();
    } catch (error) {
        console.error("Error loading categories:", error);
    }
}

async function loadMinistriesInCategory(cat) {
    document.getElementById("sub-list").innerHTML = "";
    document.getElementById("sub-title").innerText = cat.name?.[lang] || cat.name?.en || cat.id;
    
    if (cat.ministry_ids && cat.ministry_ids.length) {
        for (let id of cat.ministry_ids) {
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
        }
    } else {
        const svcRes = await fetch("/api/services");
        const all = await svcRes.json();
        all.filter(s => s.category === cat.id).forEach(s => {
            s.subservices.forEach(sub => {
                let li = document.createElement("li");
                li.textContent = sub.name?.[lang] || sub.name?.en || sub.id;
                li.onclick = () => loadQuestions(s, sub);
                document.getElementById("sub-list").appendChild(li);
            });
        });
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
            service: currentServiceName
        })
    });
}

// ==================== AI CHAT ====================
function openChat() {
    document.getElementById("chat-panel").style.display = "flex";
}

function closeChat() {
    document.getElementById("chat-panel").style.display = "none";
}

async function sendChat() {
    const input = document.getElementById("chat-text");
    const text = input.value.trim();
    if (!text) return;
    
    appendChat("user", text);
    input.value = "";
    
    // Show loading
    appendChat("bot", "🔍 Searching...");
    
    try {
        const res = await fetch("/api/ai/search", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({query: text, top_k: 5})
        });
        const data = await res.json();
        
        // Remove loading message
        const chatBody = document.getElementById("chat-body");
        chatBody.removeChild(chatBody.lastChild);
        
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
        });
    } catch (error) {
        // Remove loading message
        const chatBody = document.getElementById("chat-body");
        chatBody.removeChild(chatBody.lastChild);
        appendChat("bot", "Sorry, search failed. Please try again.");
    }
}

function appendChat(sender, text) {
    const body = document.getElementById("chat-body");
    const div = document.createElement("div");
    div.className = "chat-msg " + (sender === "user" ? "user-msg" : "bot-msg");
    div.innerText = text;
    body.appendChild(div);
    body.scrollTop = body.scrollHeight;
}

// ==================== AUTOSUGGEST ====================
let suggestTimer = null;

async function autosuggest(q) {
    clearTimeout(suggestTimer);
    if (!q || q.length < 2) {
        document.getElementById("suggestions").innerHTML = "";
        return;
    }
    
    suggestTimer = setTimeout(async () => {
        const res = await fetch(`/api/search/autosuggest?q=${encodeURIComponent(q)}`);
        const items = await res.json();
        const el = document.getElementById("suggestions");
        el.innerHTML = items.map(it => 
            `<div class="s-item" onclick='pickSuggestion(${JSON.stringify(JSON.stringify(it))})'>${it.name?.en || it.name}</div>`
        ).join("");
    }, 250);
}

function pickSuggestion(serialized) {
    const it = JSON.parse(serialized);
    if (it && it.subservices && it.subservices.length) {
        loadQuestions(it, it.subservices[0]);
    }
    document.getElementById("suggestions").innerHTML = "";
}

// Add event listener to search input
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            autosuggest(this.value);
        });
    }
});

// ==================== PROGRESSIVE PROFILE ====================
function showProfileModal() {
    document.getElementById("profile-modal").style.display = "block";
}

function closeProfileModal() {
    document.getElementById("profile-modal").style.display = "none";
}

function profileNext(step) {
    document.getElementById(`profile-step-${step}`).style.display = "none";
    document.getElementById(`profile-step-${step + 1}`).style.display = "block";
}

function profileBack(step) {
    document.getElementById(`profile-step-${step}`).style.display = "none";
    document.getElementById(`profile-step-${step - 1}`).style.display = "block";
}

async function profileSubmit() {
    const data1 = {
        name: document.getElementById("p_name").value,
        age: document.getElementById("p_age").value
    };
    const data2 = {
        email: document.getElementById("p_email").value,
        phone: document.getElementById("p_phone").value
    };
    const data3 = {
        job: document.getElementById("p_job").value
    };
    
    // Send steps
    let res = await fetch("/api/profile/step", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({email: data2.email, step: "basic", data: data1})
    });
    let j = await res.json();
    profile_id = j.profile_id || null;
    
    await fetch("/api/profile/step", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({profile_id: profile_id, step: "contact", data: data2})
    });
    
    await fetch("/api/profile/step", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({profile_id: profile_id, step: "employment", data: data3})
    });
    
    closeProfileModal();
    alert("Profile saved! Thank you.");
}

// ==================== ADS ====================
async function loadAds() {
    try {
        const res = await fetch("/api/ads");
        const ads = await res.json();
        const el = document.getElementById("ads-area");
        el.innerHTML = ads.map(a => 
            `<div class="ad-card">
                <a href="${a.link || '#'}" target="_blank">
                    <h4>${a.title}</h4>
                    <p>${a.body || ''}</p>
                </a>
            </div>`
        ).join("");
    } catch (error) {
        console.error("Error loading ads:", error);
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
        const user = JSON.parse(userInfo);
        authButtons.style.display = 'none';
        userInfoDiv.style.display = 'flex';
        authMessage.textContent = `Welcome back, ${user.name}!`;
        document.getElementById('user-greeting').textContent = `Hello, ${user.name}`;
    } else {
        authButtons.style.display = 'flex';
        userInfoDiv.style.display = 'none';
        authMessage.textContent = 'Welcome! Sign in for personalized recommendations';
    }
}

// Logout functionality
document.addEventListener('DOMContentLoaded', function() {
    const logoutBtn = document.getElementById('logout-link');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function() {
            localStorage.removeItem('access_token');
            localStorage.removeItem('user_info');
            location.reload();
        });
    }
    checkAuthStatus();
});

// ==================== INITIALIZATION ====================
window.onload = async () => {
    await loadCategories();
    const svcRes = await fetch("/api/services");
    services = await svcRes.json();
};