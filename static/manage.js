// Service Management JavaScript
let services = [];
let currentEditingService = null;

document.addEventListener('DOMContentLoaded', function() {
    loadServices();
    initializeEventListeners();
});

function initializeEventListeners() {
    // Modal controls
    const modal = document.getElementById('service-modal');
    const deleteModal = document.getElementById('delete-modal');
    const closeBtn = document.querySelector('.close');
    
    document.getElementById('add-service-btn').addEventListener('click', () => openServiceModal());
    closeBtn.addEventListener('click', () => closeModal());
    document.getElementById('cancel-btn').addEventListener('click', () => closeModal());
    document.getElementById('cancel-delete-btn').addEventListener('click', () => closeDeleteModal());
    
    // Form submission
    document.getElementById('service-form').addEventListener('submit', saveService);
    
    // Dynamic form controls
    document.getElementById('add-subservice-btn').addEventListener('click', addSubservice);
    
    // Search and filter
    document.getElementById('search-input').addEventListener('input', filterServices);
    document.getElementById('filter-select').addEventListener('change', filterServices);
    
    // Delete confirmation
    document.getElementById('confirm-delete-btn').addEventListener('click', confirmDelete);
    
    // Close modal when clicking outside
    window.addEventListener('click', function(event) {
        if (event.target === modal) closeModal();
        if (event.target === deleteModal) closeDeleteModal();
    });
}

async function loadServices() {
    try {
        const response = await fetch('/api/admin/services', {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('admin_token') || ''}`
            }
        });
        
        if (response.ok) {
            services = await response.json();
            displayServices(services);
        } else {
            console.error('Failed to load services');
        }
    } catch (error) {
        console.error('Error loading services:', error);
    }
}

function displayServices(servicesToShow = services) {
    const grid = document.getElementById('services-grid');
    
    if (servicesToShow.length === 0) {
        grid.innerHTML = '<div class="loading">No services found</div>';
        return;
    }
    
    grid.innerHTML = servicesToShow.map(service => {
        const subserviceCount = service.subservices ? service.subservices.length : 0;
        const questionCount = service.subservices ? 
            service.subservices.reduce((total, sub) => total + (sub.questions ? sub.questions.length : 0), 0) : 0;
        
        return `
            <div class="service-card">
                <div class="service-title">${service.name.en}</div>
                <div class="service-id">${service.id}</div>
                
                <div class="service-stats">
                    <span>${subserviceCount} subservices</span>
                    <span>${questionCount} questions</span>
                </div>
                
                <div class="service-actions">
                    <button class="btn btn-primary btn-small" onclick="editService('${service.id}')">
                        Edit
                    </button>
                    <button class="btn btn-danger btn-small" onclick="deleteService('${service.id}')">
                        Delete
                    </button>
                </div>
            </div>
        `;
    }).join('');
}

function filterServices() {
    const searchTerm = document.getElementById('search-input').value.toLowerCase();
    const filterValue = document.getElementById('filter-select').value;
    
    let filtered = services.filter(service => {
        const matchesSearch = !searchTerm || 
            service.name.en.toLowerCase().includes(searchTerm) ||
            service.id.toLowerCase().includes(searchTerm);
        
        const matchesFilter = !filterValue || service.id === filterValue;
        
        return matchesSearch && matchesFilter;
    });
    
    displayServices(filtered);
}

function openServiceModal(serviceId = null) {
    const modal = document.getElementById('service-modal');
    const form = document.getElementById('service-form');
    
    if (serviceId) {
        // Edit mode
        currentEditingService = services.find(s => s.id === serviceId);
        document.getElementById('modal-title').textContent = 'Edit Service';
        populateForm(currentEditingService);
        document.getElementById('service-id-input').disabled = true;
    } else {
        // Add mode
        currentEditingService = null;
        document.getElementById('modal-title').textContent = 'Add New Service';
        form.reset();
        document.getElementById('service-id').value = '';
        document.getElementById('service-id-input').disabled = false;
        document.getElementById('subservices-container').innerHTML = '';
    }
    
    modal.style.display = 'block';
}

function populateForm(service) {
    document.getElementById('service-id').value = service.id;
    document.getElementById('service-id-input').value = service.id;
    document.getElementById('name-en').value = service.name.en || '';
    document.getElementById('name-si').value = service.name.si || '';
    document.getElementById('name-ta').value = service.name.ta || '';
    
    // Populate subservices
    const container = document.getElementById('subservices-container');
    container.innerHTML = '';
    
    if (service.subservices) {
        service.subservices.forEach((subservice, index) => {
            addSubservice(subservice, index);
        });
    }
}

function addSubservice(subserviceData = null, index = null) {
    const container = document.getElementById('subservices-container');
    const subserviceIndex = index !== null ? index : container.children.length;
    
    const subserviceHtml = `
        <div class="subservice-item" data-index="${subserviceIndex}">
            <div class="subservice-header">
                <span class="subservice-title">Subservice ${subserviceIndex + 1}</span>
                <button type="button" class="btn-remove" onclick="removeSubservice(${subserviceIndex})">Remove</button>
            </div>
            
            <div class="form-row">
                <div class="form-group">
                    <label>Subservice ID</label>
                    <input type="text" name="subservice_id_${subserviceIndex}" 
                           value="${subserviceData ? subserviceData.id : ''}" 
                           placeholder="e.g., general_services" required>
                </div>
            </div>
            
            <div class="form-row">
                <div class="form-group">
                    <label>Name (English)</label>
                    <input type="text" name="subservice_name_en_${subserviceIndex}" 
                           value="${subserviceData ? subserviceData.name.en : ''}" 
                           placeholder="General Services" required>
                </div>
            </div>
            
            <div class="form-row">
                <div class="form-group">
                    <label>Name (Sinhala)</label>
                    <input type="text" name="subservice_name_si_${subserviceIndex}" 
                           value="${subserviceData ? subserviceData.name.si || '' : ''}" 
                           placeholder="සාමාන්‍ය සේවා">
                </div>
            </div>
            
            <div class="form-row">
                <div class="form-group">
                    <label>Name (Tamil)</label>
                    <input type="text" name="subservice_name_ta_${subserviceIndex}" 
                           value="${subserviceData ? subserviceData.name.ta || '' : ''}" 
                           placeholder="பொதுச் சேவைகள்">
                </div>
            </div>
            
            <div class="questions-section">
                <div class="section-header">
                    <h5>Questions</h5>
                    <button type="button" class="btn btn-small" onclick="addQuestion(${subserviceIndex})">+ Add Question</button>
                </div>
                <div class="questions-container" id="questions-${subserviceIndex}">
                    <!-- Questions will be added here -->
                </div>
            </div>
        </div>
    `;
    
    container.insertAdjacentHTML('beforeend', subserviceHtml);
    
    // Add existing questions if any
    if (subserviceData && subserviceData.questions) {
        subserviceData.questions.forEach((question, qIndex) => {
            addQuestion(subserviceIndex, question, qIndex);
        });
    }
}

function addQuestion(subserviceIndex, questionData = null, questionIndex = null) {
    const container = document.getElementById(`questions-${subserviceIndex}`);
    const qIndex = questionIndex !== null ? questionIndex : container.children.length;
    
    const questionHtml = `
        <div class="question-item" data-question-index="${qIndex}">
            <div class="question-header">
                <span>Question ${qIndex + 1}</span>
                <button type="button" class="btn-remove" onclick="removeQuestion(${subserviceIndex}, ${qIndex})">Remove</button>
            </div>
            
            <div class="form-row">
                <div class="form-group textarea-group">
                    <label>Question (English)</label>
                    <textarea name="question_en_${subserviceIndex}_${qIndex}" 
                              placeholder="What services are offered?">${questionData ? questionData.q.en || '' : ''}</textarea>
                </div>
            </div>
            
            <div class="form-row">
                <div class="form-group textarea-group">
                    <label>Answer (English)</label>
                    <textarea name="answer_en_${subserviceIndex}_${qIndex}" 
                              placeholder="Please check our service list...">${questionData ? questionData.answer.en || '' : ''}</textarea>
                </div>
            </div>
            
            <div class="form-row">
                <div class="form-group">
                    <label>Instructions</label>
                    <input type="text" name="instructions_${subserviceIndex}_${qIndex}" 
                           value="${questionData ? questionData.instructions || '' : ''}" 
                           placeholder="Additional instructions...">
                </div>
            </div>
            
            <div class="form-row">
                <div class="form-group">
                    <label>Location URL</label>
                    <input type="url" name="location_${subserviceIndex}_${qIndex}" 
                           value="${questionData ? questionData.location || '' : ''}" 
                           placeholder="https://maps.google.com/?q=Location">
                </div>
            </div>
        </div>
    `;
    
    container.insertAdjacentHTML('beforeend', questionHtml);
}

function removeSubservice(index) {
    const item = document.querySelector(`[data-index="${index}"]`);
    if (item) {
        item.remove();
    }
}

function removeQuestion(subserviceIndex, questionIndex) {
    const item = document.querySelector(`[data-question-index="${questionIndex}"]`);
    if (item) {
        item.remove();
    }
}

async function saveService(e) {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const serviceData = buildServiceObject(formData);
    
    const saveBtn = document.getElementById('save-btn');
    saveBtn.disabled = true;
    saveBtn.textContent = 'Saving...';
    
    try {
        const response = await fetch('/api/admin/services', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(serviceData)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            closeModal();
            loadServices(); // Refresh the list
            alert('Service saved successfully!');
        } else {
            alert('Error saving service: ' + (result.error || 'Unknown error'));
        }
    } catch (error) {
        console.error('Error saving service:', error);
        alert('Network error. Please try again.');
    } finally {
        saveBtn.disabled = false;
        saveBtn.textContent = 'Save Service';
    }
}

function buildServiceObject(formData) {
    const serviceId = formData.get('service_id') || formData.get('id');
    
    const service = {
        id: serviceId,
        name: {
            en: formData.get('name_en'),
            si: formData.get('name_si') || formData.get('name_en'),
            ta: formData.get('name_ta') || formData.get('name_en')
        },
        subservices: []
    };
    
    // Build subservices
    const subserviceElements = document.querySelectorAll('.subservice-item');
    subserviceElements.forEach((element, index) => {
        const subservice = {
            id: formData.get(`subservice_id_${index}`),
            name: {
                en: formData.get(`subservice_name_en_${index}`),
                si: formData.get(`subservice_name_si_${index}`) || formData.get(`subservice_name_en_${index}`),
                ta: formData.get(`subservice_name_ta_${index}`) || formData.get(`subservice_name_en_${index}`)
            },
            questions: []
        };
        
        // Build questions for this subservice
        const questionElements = element.querySelectorAll('.question-item');
        questionElements.forEach((qElement, qIndex) => {
            const question = {
                q: {
                    en: formData.get(`question_en_${index}_${qIndex}`),
                    si: formData.get(`question_en_${index}_${qIndex}`), // Default to English
                    ta: formData.get(`question_en_${index}_${qIndex}`)  // Default to English
                },
                answer: {
                    en: formData.get(`answer_en_${index}_${qIndex}`),
                    si: formData.get(`answer_en_${index}_${qIndex}`), // Default to English
                    ta: formData.get(`answer_en_${index}_${qIndex}`)  // Default to English
                },
                instructions: formData.get(`instructions_${index}_${qIndex}`) || '',
                location: formData.get(`location_${index}_${qIndex}`) || '',
                downloads: [] // Can be extended later
            };
            
            subservice.questions.push(question);
        });
        
        service.subservices.push(subservice);
    });
    
    return service;
}

function editService(serviceId) {
    openServiceModal(serviceId);
}

function deleteService(serviceId) {
    currentEditingService = services.find(s => s.id === serviceId);
    document.getElementById('delete-modal').style.display = 'block';
}

async function confirmDelete() {
    if (!currentEditingService) return;
    
    const confirmBtn = document.getElementById('confirm-delete-btn');
    confirmBtn.disabled = true;
    confirmBtn.textContent = 'Deleting...';
    
    try {
        const response = await fetch(`/api/admin/services/${currentEditingService.id}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            closeDeleteModal();
            loadServices(); // Refresh the list
            alert('Service deleted successfully!');
        } else {
            alert('Error deleting service');
        }
    } catch (error) {
        console.error('Error deleting service:', error);
        alert('Network error. Please try again.');
    } finally {
        confirmBtn.disabled = false;
        confirmBtn.textContent = 'Delete';
    }
}

function closeModal() {
    document.getElementById('service-modal').style.display = 'none';
    currentEditingService = null;
}

function closeDeleteModal() {
    document.getElementById('delete-modal').style.display = 'none';
    currentEditingService = null;
}