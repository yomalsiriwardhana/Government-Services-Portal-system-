# 🏛️ Government Services Portal - Sri Lanka

A modern, AI-powered e-government platform that enables Sri Lankan citizens to discover, access, and manage government services with personalized recommendations and intelligent search capabilities.

![Government Portal](https://img.shields.io/badge/Status-Active-success)
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![MongoDB](https://img.shields.io/badge/MongoDB-4.6+-yellow)

## 📋 Table of Contents

- [Features](#-features)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Running the Application](#-running-the-application)
- [API Endpoints](#-api-endpoints)
- [Database Seeding](#-database-seeding)
- [Configuration](#-configuration)
- [Frontend Pages](#-frontend-pages)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

### 🧠 AI-Powered Capabilities
- **Intelligent Search**: Natural language processing for finding government services
- **Context-Aware Advertisements**: Smart ad recommendations based on user search intent
- **Personalized Recommendations**: Service suggestions based on user profile and activity
- **AI Chatbot**: Interactive assistant for navigating government services

### 🔐 User Management
- Secure user registration and authentication (JWT-based)
- Profile management with demographic categorization
- Activity tracking and search history

### 🏢 Government Services
- Browse and search ministry information
- Access 100+ government services across categories:
  - Education
  - Health
  - Business
  - Immigration
  - Employment
  - Technology
  - Transport
  - Housing
  - Financial

### 🛒 Marketplace
- Product listings with intelligent categorization
- Context-aware product recommendations
- Search-based ad matching

### 👨‍💼 Admin Dashboard
- User management
- Service administration
- Analytics and reporting

---

## 🛠️ Technology Stack

### Backend
| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.10+ | Core language |
| Flask | 3.0.0 | Web framework |
| MongoDB | 4.6+ | Database |
| PyMongo | 4.6.1 | MongoDB driver |
| PyJWT | 2.8.0 | Authentication |
| bcrypt | 4.1.2 | Password hashing |

### AI/ML
| Technology | Version | Purpose |
|------------|---------|---------|
| FAISS | 1.7.4 | Vector similarity search |
| Sentence Transformers | 2.2.2 | Text embeddings |
| scikit-learn | 1.4.0 | ML utilities |
| PyTorch | 2.0.1 | Deep learning framework |
| Transformers | 4.30.0 | NLP models |

### Frontend
| Technology | Purpose |
|------------|---------|
| HTML5 | Structure |
| CSS3 | Styling (Glassmorphism, animations) |
| JavaScript | Interactivity |
| Font Awesome | Icons |

---

## 📁 Project Structure

```
government-portal/
├── backend/
│   ├── app.py                    # Flask application entry point
│   ├── config.py                 # Application configuration
│   ├── requirements.txt          # Python dependencies
│   │
│   ├── models/                   # Database models
│   │   ├── user.py               # User model
│   │   ├── service.py            # Government services model
│   │   ├── product.py            # Marketplace products model
│   │   ├── ministry.py           # Ministry information model
│   │   ├── advertisement.py      # Advertisement model
│   │   ├── user_profile.py       # User profile & preferences
│   │   ├── user_activity.py      # User activity tracking
│   │   ├── search_history.py     # Search history model
│   │   └── ad_click.py           # Ad click tracking
│   │
│   ├── routes/                   # API route handlers
│   │   ├── auth.py               # Authentication endpoints
│   │   ├── services.py           # Government services API
│   │   ├── products.py           # Products/marketplace API
│   │   ├── search.py             # Search functionality
│   │   ├── ai_search.py          # AI-powered search
│   │   ├── chat.py               # Chatbot endpoints
│   │   ├── recommendations.py    # Recommendation engine
│   │   ├── ministries.py         # Ministry information
│   │   ├── announcements.py      # Government announcements
│   │   └── admin.py              # Admin panel APIs
│   │
│   ├── utils/                    # Utility functions
│   │
│   ├── seed_database.py          # Database seeding script
│   ├── seed_ministries.py        # Ministry data seeder
│   ├── seed_ad_data.py           # Advertisement data seeder
│   └── seed_products_enhanced.py # Enhanced product seeder
│
├── frontend/
│   ├── index.html                # Landing page
│   ├── login-simple.html         # Login page
│   ├── register-simple.html      # Registration page
│   ├── dashboard-enhanced.html   # User dashboard
│   ├── services.html             # Services catalog
│   ├── marketplace.html          # Marketplace
│   ├── admin-dashboard-enhanced.html  # Admin panel
│   │
│   ├── css/
│   │   ├── style.css             # Main styles
│   │   ├── dashboard.css         # Dashboard styles
│   │   └── admin.css             # Admin panel styles
│   │
│   └── js/
│       ├── main.js               # Main JavaScript
│       ├── auth.js               # Authentication logic
│       ├── dashboard.js          # Dashboard functionality
│       ├── services.js           # Services page logic
│       └── translations.js       # i18n support
│
└── README.md
```

---

## 📦 Prerequisites

Before running this application, ensure you have the following installed:

1. **Python 3.10 or higher**
   ```bash
   python --version
   ```

2. **MongoDB 4.6 or higher**
   - Download from: https://www.mongodb.com/try/download/community
   - Ensure MongoDB service is running on `localhost:27017`

3. **pip** (Python package manager)
   ```bash
   pip --version
   ```

---

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd government-portal
```

### 2. Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 4. Configure Environment Variables (Optional)
Create a `.env` file in the `backend` directory:
```env
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-here
MONGO_URI=mongodb://localhost:27017/
```

---

## ▶️ Running the Application

### 1. Start MongoDB
Ensure MongoDB is running on your system:
```bash
# Windows (if installed as service, it starts automatically)
net start MongoDB

# macOS/Linux
sudo systemctl start mongod
```

### 2. Seed the Database (First Run)
```bash
cd backend

# Seed core data
python seed_database.py

# Seed ministry information
python seed_ministries.py

# Seed advertisement data
python seed_ad_data.py

# Seed enhanced products
python seed_products_enhanced.py
```

### 3. Start the Flask Server
```bash
cd backend
python app.py
```

### 4. Access the Application
Open your browser and navigate to:

| Page | URL |
|------|-----|
| Landing Page | http://localhost:5000/ |
| Dashboard | http://localhost:5000/dashboard-enhanced.html |
| Services | http://localhost:5000/services.html |
| Marketplace | http://localhost:5000/marketplace.html |
| Admin Panel | http://localhost:5000/admin-dashboard-enhanced.html |

---

## 🔌 API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/register` | Register new user |
| POST | `/api/login` | User login |
| GET | `/api/profile` | Get user profile |
| PUT | `/api/profile` | Update user profile |

### Services
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/services/` | Get all services |
| GET | `/api/services/<id>` | Get service by ID |
| GET | `/api/services/category/<category>` | Get services by category |

### Products
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/products/` | Get all products |
| GET | `/api/products/<id>` | Get product by ID |
| POST | `/api/products/` | Create new product |

### Search
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/search/` | Search services and products |
| POST | `/api/ai-search/ministry` | AI-powered ministry search |

### Recommendations
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/recommendations` | Get personalized recommendations |
| POST | `/api/recommendations/context` | Get context-aware ads |

### Chat
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/chat` | Send message to AI chatbot |

### Ministries
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/ministries/` | Get all ministries |
| GET | `/api/ministries/<id>` | Get ministry details |

### Admin
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/admin/users` | Get all users |
| GET | `/api/admin/stats` | Get dashboard statistics |

---

## 🗃️ Database Seeding

The application includes several seeders to populate initial data:

| Script | Purpose |
|--------|---------|
| `seed_database.py` | Core database setup with users, services |
| `seed_ministries.py` | Sri Lankan ministry information |
| `seed_ad_data.py` | Advertisement and product data |
| `seed_products_enhanced.py` | Enhanced product catalog |
| `seed_search_mappings.py` | Search keyword mappings |
| `seed_announcements.py` | Government announcements |

---

## ⚙️ Configuration

Configuration is managed through `backend/config.py`:

| Setting | Default | Description |
|---------|---------|-------------|
| `SECRET_KEY` | Auto-generated | Flask secret key |
| `MONGO_URI` | `mongodb://localhost:27017/` | MongoDB connection |
| `MONGO_DB_NAME` | `government_portal` | Database name |
| `JWT_ACCESS_TOKEN_EXPIRES` | 24 hours | Token expiration |
| `MAX_CONTENT_LENGTH` | 16MB | Max upload size |
| `ADS_PER_PAGE` | 5 | Ads shown per page |
| `AD_REFRESH_INTERVAL` | 5 minutes | Ad refresh rate |

### Service Categories
- Education, Health, Business, Immigration, Employment, Technology, Transport, Housing, Financial

### AI User Categories
- Demographics: young_adult, early_career, mid_career_family, established_professional, senior
- Professional: student, government_employee, education_professional, tech_professional
- Behavioral: education_seeker, course_buyer, tech_enthusiast, travel_seeker, and more

---

## 🖼️ Frontend Pages

### Public Pages
| Page | Description |
|------|-------------|
| `index.html` | Modern landing page with hero section and features |
| `login-simple.html` | User login with glassmorphism design |
| `register-simple.html` | User registration form |
| `services.html` | Government services catalog |

### Protected Pages
| Page | Description |
|------|-------------|
| `dashboard-enhanced.html` | User dashboard with AI search, recommendations, and marketplace |
| `marketplace.html` | Product listings and shopping |
| `admin-dashboard-enhanced.html` | Admin control panel |

### Design Features
- 🎨 **Glassmorphism** - Modern frosted glass effect
- ✨ **Micro-animations** - Smooth hover and transition effects
- 📱 **Responsive** - Mobile-first design
- 🌙 **Dark Mode Ready** - Consistent color palette

---

## 🧪 Testing

The project includes several test scripts:

```bash
# Test context-aware ads
python test_context_aware_ads.py

# Test complete user flow
python test_complete_flow.py

# Test ad updates
python test_ad_updates.py

# Debug recommendations
python debug_recommendations.py
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is developed for the Government of Sri Lanka.

---

## 📞 Support

For technical support or questions:
- 📧 Email: support@govportal.lk
- 📞 Hotline: 1919
- 🌐 Website: https://www.gov.lk

---

## 👥 Development Team

**Project Handover Date**: January 2026

For any questions about the codebase, architecture decisions, or implementation details, please refer to:
1. This README documentation
2. Code comments throughout the codebase
3. The development team's contact information above

---

*Last Updated: January 2026*
