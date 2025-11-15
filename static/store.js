let cart = JSON.parse(localStorage.getItem('cart')) || [];
let currentProducts = [];
let currentFilters = {};

// Initialize store
async function initStore() {
    await loadCategories();
    await loadProducts();
    updateCartCount();
    setupPriceRangeListener();
}

// Setup price range slider
function setupPriceRangeListener() {
    const priceRange = document.getElementById('price-range');
    priceRange.addEventListener('input', updatePriceDisplay);
    updatePriceDisplay();
}

function updatePriceDisplay() {
    const range = document.getElementById('price-range');
    const maxPrice = document.getElementById('max-price');
    maxPrice.textContent = parseInt(range.value).toLocaleString();
}

// Load product categories
async function loadCategories() {
    try {
        const res = await fetch('/api/store/categories');
        const data = await res.json();
        
        if (data.success) {
            const container = document.getElementById('category-filters');
            container.innerHTML = '';
            
            data.categories.forEach(category => {
                const label = document.createElement('label');
                label.innerHTML = `
                    <input type="checkbox" name="category" value="${category}">
                    ${category.charAt(0).toUpperCase() + category.slice(1).replace('_', ' ')}
                `;
                container.appendChild(label);
            });
        }
    } catch (error) {
        console.error('Error loading categories:', error);
    }
}

// Load products with filters
async function loadProducts() {
    const loading = document.getElementById('loading');
    loading.style.display = 'block';
    
    const params = new URLSearchParams();
    
    // Add filters
    if (currentFilters.category) {
        params.append('category', currentFilters.category);
    }
    if (currentFilters.minPrice) {
        params.append('min_price', currentFilters.minPrice);
    }
    if (currentFilters.maxPrice) {
        params.append('max_price', currentFilters.maxPrice);
    }
    if (currentFilters.tags) {
        params.append('tags', currentFilters.tags.join(','));
    }
    
    // Add sorting
    const sortBy = document.getElementById('sort-by').value;
    params.append('sort', sortBy);
    
    try {
        const res = await fetch(`/api/store/products?${params}`);
        const data = await res.json();
        
        if (data.success) {
            currentProducts = data.products;
            displayProducts(currentProducts);
        }
    } catch (error) {
        console.error('Error loading products:', error);
        showNotification('Failed to load products. Please try again.', 'error');
    } finally {
        loading.style.display = 'none';
    }
}

// Display products in grid
function displayProducts(products) {
    const container = document.getElementById('products-container');
    
    if (products.length === 0) {
        container.innerHTML = '<div class="no-products">No products found matching your criteria.</div>';
        return;
    }
    
    container.innerHTML = products.map(product => `
        <div class="product-card" onclick="openProductModal('${product.id}')">
            <div class="product-image">
                <img src="${product.images[0] || '/static/store/placeholder.jpg'}" 
                     alt="${product.name}" 
                     onerror="this.src='/static/store/placeholder.jpg'">
                ${product.original_price ? `<div class="discount-badge">-${Math.round((1 - product.price/product.original_price) * 100)}%</div>` : ''}
            </div>
            <div class="product-info">
                <h3 class="product-name">${product.name}</h3>
                <div class="product-price">
                    ${product.original_price ? 
                        `<span class="original-price">LKR ${product.original_price.toLocaleString()}</span>` : ''}
                    <span class="current-price">LKR ${product.price.toLocaleString()}</span>
                </div>
                <div class="product-rating">
                    ${'★'.repeat(Math.floor(product.rating))}${'☆'.repeat(5-Math.floor(product.rating))}
                    <span class="rating-count">(${product.reviews_count})</span>
                </div>
                <button class="add-to-cart-btn" onclick="event.stopPropagation(); addToCart('${product.id}')">
                    Add to Cart
                </button>
            </div>
        </div>
    `).join('');
}

// Cart management
function addToCart(productId) {
    const product = currentProducts.find(p => p.id === productId);
    if (!product) return;
    
    const existingItem = cart.find(item => item.id === productId);
    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({
            id: productId,
            name: product.name,
            price: product.price,
            image: product.images[0],
            quantity: 1
        });
    }
    
    updateCart();
    showNotification(`${product.name} added to cart!`, 'success');
}

function updateCart() {
    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartCount();
    updateCartModal();
}

function updateCartCount() {
    const count = cart.reduce((total, item) => total + item.quantity, 0);
    document.getElementById('cart-count').textContent = count;
}

function viewCart() {
    document.getElementById('cart-modal').style.display = 'block';
    updateCartModal();
}

function closeCart() {
    document.getElementById('cart-modal').style.display = 'none';
}

function updateCartModal() {
    const container = document.getElementById('cart-items');
    const total = document.getElementById('cart-total');
    
    if (cart.length === 0) {
        container.innerHTML = '<p class="empty-cart">Your cart is empty</p>';
        total.textContent = '0';
        return;
    }
    
    container.innerHTML = cart.map(item => `
        <div class="cart-item">
            <img src="${item.image}" alt="${item.name}" onerror="this.src='/static/store/placeholder.jpg'">
            <div class="cart-item-info">
                <h4>${item.name}</h4>
                <div class="cart-item-price">LKR ${item.price.toLocaleString()}</div>
            </div>
            <div class="cart-item-controls">
                <button onclick="updateQuantity('${item.id}', -1)">-</button>
                <span>${item.quantity}</span>
                <button onclick="updateQuantity('${item.id}', 1)">+</button>
                <button onclick="removeFromCart('${item.id}')" class="remove-btn">Remove</button>
            </div>
        </div>
    `).join('');
    
    const cartTotal = cart.reduce((total, item) => total + (item.price * item.quantity), 0);
    total.textContent = cartTotal.toLocaleString();
}

function updateQuantity(productId, change) {
    const item = cart.find(item => item.id === productId);
    if (item) {
        item.quantity += change;
        if (item.quantity <= 0) {
            removeFromCart(productId);
        } else {
            updateCart();
        }
    }
}

function removeFromCart(productId) {
    cart = cart.filter(item => item.id !== productId);
    updateCart();
}

// Product modal with enhanced view
async function openProductModal(productId) {
    const product = currentProducts.find(p => p.id === productId);
    if (!product) return;
    
    const modal = document.getElementById('product-modal');
    const content = document.getElementById('modal-content');
    
    content.innerHTML = `
        <div class="product-modal-content">
            <div class="product-modal-images">
                <img src="${product.images[0]}" alt="${product.name}" class="main-image" onerror="this.src='/static/store/placeholder.jpg'">
            </div>
            <div class="product-modal-details">
                <h2>${product.name}</h2>
                <div class="product-price-large">
                    ${product.original_price ? 
                        `<span class="original-price">LKR ${product.original_price.toLocaleString()}</span>` : ''}
                    <span class="current-price">LKR ${product.price.toLocaleString()}</span>
                </div>
                <div class="product-rating-large">
                    ${'★'.repeat(Math.floor(product.rating))}${'☆'.repeat(5-Math.floor(product.rating))}
                    <span>${product.rating} (${product.reviews_count} reviews)</span>
                </div>
                <p class="product-description">${product.description}</p>
                
                <div class="product-features">
                    <h4>Features:</h4>
                    <ul>
                        ${product.features.map(feature => `<li>✓ ${feature}</li>`).join('')}
                    </ul>
                </div>
                
                <div class="delivery-options">
                    <h4>Delivery Options:</h4>
                    ${product.delivery_options.map(option => 
                        `<span class="delivery-badge">${option}</span>`
                    ).join('')}
                </div>
                
                <div class="product-actions">
                    <button class="buy-now-btn" onclick="buyNow('${product.id}')">Buy Now</button>
                    <button class="add-to-cart-large" onclick="addToCart('${product.id}'); closeModal();">Add to Cart</button>
                </div>
            </div>
        </div>
    `;
    
    modal.style.display = 'block';
}

function closeModal() {
    document.getElementById('product-modal').style.display = 'none';
}

// Filter functions
function toggleFilters() {
    const sidebar = document.getElementById('filters-sidebar');
    sidebar.classList.toggle('active');
}

function applyFilters() {
    const categoryCheckboxes = document.querySelectorAll('input[name="category"]:checked');
    const deliveryCheckboxes = document.querySelectorAll('input[name="delivery"]:checked');
    const priceRange = document.getElementById('price-range');
    
    currentFilters = {
        category: Array.from(categoryCheckboxes).map(cb => cb.value).join(','),
        delivery: Array.from(deliveryCheckboxes).map(cb => cb.value),
        minPrice: 0,
        maxPrice: parseInt(priceRange.value)
    };
    
    loadProducts();
}

function clearFilters() {
    document.querySelectorAll('input[type="checkbox"]').forEach(cb => cb.checked = false);
    document.getElementById('price-range').value = 500000;
    updatePriceDisplay();
    currentFilters = {};
    loadProducts();
}

// Checkout process
async function checkout() {
    if (cart.length === 0) {
        showNotification('Your cart is empty!', 'error');
        return;
    }
    
    // For now, just simulate checkout
    showNotification('Checkout feature coming soon! Your cart has been saved.', 'info');
}

async function buyNow(productId) {
    addToCart(productId);
    closeModal();
    viewCart();
}

// Utility functions
function showNotification(message, type = 'success') {
    const notification = document.getElementById('notification-toast');
    notification.textContent = message;
    notification.className = `notification-toast ${type} show`;
    
    setTimeout(() => {
        notification.classList.remove('show');
    }, 3000);
}

// Close modals when clicking outside
window.onclick = function(event) {
    const productModal = document.getElementById('product-modal');
    const cartModal = document.getElementById('cart-modal');
    
    if (event.target == productModal) {
        closeModal();
    }
    if (event.target == cartModal) {
        closeCart();
    }
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', initStore);