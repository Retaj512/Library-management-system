# 📚 Library Management System

<div align="center">

![Library Logo](https://img.icons8.com/fluency/96/000000/book-shelf.png)

**Complete Library Operations & Analytics Platform**

*Streamlining Book Management, Member Services & Circulation Analytics*

[![Flask](https://img.shields.io/badge/Flask-2.0+-green?logo=flask)](https://flask.palletsprojects.com/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-blue?logo=mysql)](https://www.mysql.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)](https://www.python.org/)
[![Chart.js](https://img.shields.io/badge/Chart.js-3.9-red?logo=chartdotjs)](https://www.chartjs.org/)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Architecture](#%EF%B8%8F-architecture)
- [Features](#-features)
- [Live Demo](#-live-demo)
- [System Components](#-system-components)
- [Technology Stack](#%EF%B8%8F-technology-stack)
- [Getting Started](#-getting-started)
- [Database Schema](#-database-schema)
- [API Documentation](#-api-documentation)
- [Screenshots](#%EF%B8%8F-screenshots)

---

## 🎯 Overview

The **Library Management System** is a full-stack web application designed to modernize library operations. Built with Flask and MySQL, it provides a comprehensive solution for managing books, members, loans, and multiple branch locations with real-time analytics and intuitive interfaces.

### Key Capabilities

- 📖 **Complete Book Cataloging** - Manage books, authors, publishers, and copies
- 👥 **Member Management** - Track registrations, contact info, and borrowing history
- 🔄 **Circulation System** - Handle loans, returns, and automated fine calculations
- 🏢 **Multi-Branch Support** - Manage inventory across multiple library locations
- 📊 **Analytics Dashboard** - Real-time insights into collection and usage patterns
- 🎨 **Modern UI** - Responsive design with gradient themes and interactive charts

---

## 🗃️ Architecture

The system follows a classic three-tier architecture:

```
┌─────────────────────────────────────────────────────────┐
│                    Presentation Layer                    │
│         (HTML/CSS/JavaScript + Chart.js)                │
│              Responsive Frontend UI                      │
└───────────────────┬─────────────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────────────┐
│                  Application Layer                       │
│              Flask REST API Backend                      │
│         (Python + mysql-connector)                      │
└───────────────────┬─────────────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────────────┐
│                     Data Layer                          │
│            MySQL Relational Database                    │
│         (8 Tables + Foreign Key Relations)              │
└─────────────────────────────────────────────────────────┘
```

### Data Flow

1. **User Interaction** → Frontend captures form input/actions
2. **API Request** → AJAX calls to Flask REST endpoints
3. **Business Logic** → Python processes data with validation
4. **Database Operations** → SQL queries via mysql-connector
5. **Response** → JSON data returned to frontend
6. **UI Update** → Dynamic table/chart rendering without page reload

---

## ✨ Features

### 📚 Book Management
- **Comprehensive Cataloging**: Title, ISBN, genre, publication year
- **Publisher Tracking**: Maintain publisher details and relationships
- **Author Management**: Support multiple authors per book
- **Copy Management**: Track individual copies across branches
- **Bulk Operations**: Delete multiple records with cascading cleanup

### 👤 Member Services
- **Registration System**: Capture member details with auto-registration dates
- **Contact Management**: Email, phone, address tracking
- **Borrowing History**: View all loans and fines per member
- **Bulk Member Operations**: Efficient multi-member management

### 🔄 Circulation Management
- **Loan Creation**: Automated due date calculation (configurable period)
- **Return Processing**: One-click returns with automatic fine calculation
- **Fine Management**: $1/day default rate for overdue items
- **Status Tracking**: Available, On Loan, Reserved statuses
- **Smart Updates**: Auto-update copy status on loan/return operations

### 🏢 Branch Operations
- **Multi-Location Support**: Manage multiple library branches
- **Inventory Distribution**: Track which copies are at which branches
- **Location-Based Search**: Filter availability by branch

### 📊 Analytics Dashboard

**Key Metrics**
- Total Books in Collection
- Available Copies Count
- Books Currently on Loan
- Reserved Items
- Active Member Count

**Visualizations**
- **Status Distribution** (Doughnut Chart) - Inventory breakdown
- **Loans Trend** (Line Chart) - Weekly borrowing patterns
- **Genre Analysis** (Bar Chart) - Collection composition by genre

**Advanced Features**
- Real-time data refresh
- Interactive chart tooltips
- Responsive design for mobile/tablet

### 🎨 User Interface
- **Modern Gradient Theme**: Purple-pink gradient header & backgrounds
- **Responsive Tables**: Horizontal scroll for mobile devices
- **Smart Search**: Real-time table filtering across all views
- **Status Badges**: Color-coded visual indicators
- **Action Buttons**: Edit/Delete with hover effects
- **Form Validation**: Client-side + server-side validation

---

## 🌐 Live Demo

**Try the application locally by following the [Getting Started](#-getting-started) guide!**

Default URL after setup: `http://localhost:5000`

---

## 🧩 System Components

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Backend API** | Flask 2.0+ | RESTful web service |
| **Database** | MySQL 8.0 | Relational data storage |
| **Frontend** | HTML5, CSS3, JavaScript | User interface |
| **Charting** | Chart.js 3.9 | Data visualization |
| **Data Export** | CSV Module | Backup functionality |
| **ORM Layer** | mysql-connector-python | Database connectivity |

---

## 🛠️ Technology Stack

### Backend
- **Flask** - Lightweight Python web framework
- **mysql-connector-python** - MySQL database driver
- **Python 3.8+** - Core programming language

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modern styling with gradients, transitions
- **Vanilla JavaScript** - No framework dependencies
- **Chart.js** - Interactive, responsive charts

### Database
- **MySQL 8.0** - ACID-compliant relational database
- **Foreign Keys** - Enforced referential integrity
- **Auto-Increment** - Automatic ID generation

### Development Tools
- **Git** - Version control
- **Postman** - API testing
- **MySQL Workbench** - Database design

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- MySQL 8.0 or higher
- pip (Python package manager)
- Git

### Installation Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/library-management-system.git
   cd library-management-system
   ```

2. **Set Up Virtual Environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate (Windows)
   venv\Scripts\activate
   
   # Activate (Mac/Linux)
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install flask mysql-connector-python
   ```

4. **Configure MySQL Database**
   ```bash
   # Login to MySQL
   mysql -u root -p
   
   # Create database
   CREATE DATABASE library;
   
   # Run schema script
   SOURCE DB_Project.sql;
   
   # Exit MySQL
   exit;
   ```

5. **Configure Database Connection**
   
   Edit `app.py` and update the database configuration:
   ```python
   db_config = {
       'host': 'localhost',
       'user': 'root',
       'password': 'your_password',  # Change this
       'database': 'library'
   }
   ```

6. **Run the Application**
   ```bash
   python app.py
   ```

7. **Access the Application**
   ```
   Open browser and navigate to: http://localhost:5000
   ```

### Initial Setup

**Option 1: Use Seed Data**
- Click "Seed Data" button in the interface
- Automatically populates sample publishers, authors, books, members, branches, and loans

**Option 2: Manual Entry**
- Navigate to each management section
- Add records using the forms provided

---

## 💾 Database Schema

### Entity Relationship Diagram

```
┌─────────────┐         ┌──────────────┐         ┌────────────┐
│  Publishers │◄────────┤    Books     │────────►│  Authors   │
└─────────────┘         └──────┬───────┘         └────────────┘
                               │                         ▲
                               │                         │
                               ▼                         │
                        ┌──────────────┐         ┌──────┴───────┐
                        │ Book_Copies  │         │ Book_Authors │
                        └──────┬───────┘         └──────────────┘
                               │
                               │ ┌─────────────────┐
                               ├─┤ Library_Branches│
                               │ └─────────────────┘
                               ▼
                        ┌──────────┐
                        │  Loans   │
                        └─────┬────┘
                              │
                              ▼
                        ┌──────────┐
                        │ Members  │
                        └──────────┘
```

### Table Structures

**Publishers**
- `publisher_id` (PK, Auto Increment)
- `name` (VARCHAR 100)
- `address` (VARCHAR 100)
- `phone` (VARCHAR 20)

**Authors**
- `author_id` (PK, Auto Increment)
- `first_name` (VARCHAR 50)
- `last_name` (VARCHAR 50)

**Books**
- `isbn` (PK, INT)
- `title` (VARCHAR 100)
- `publisher_id` (FK → Publishers)
- `publication_year` (INT)
- `genre` (VARCHAR 50)

**Book_Authors** (Junction Table)
- `isbn` (FK → Books)
- `author_id` (FK → Authors)
- Composite PK (isbn, author_id)

**Library_Branches**
- `branch_id` (PK, Auto Increment)
- `name` (VARCHAR 100)
- `location` (VARCHAR 100)

**Book_Copies**
- `copy_id` (PK, Auto Increment)
- `isbn` (FK → Books)
- `branch_id` (FK → Library_Branches)
- `status` (ENUM: Available, On Loan, Reserved)

**Members**
- `member_id` (PK, Auto Increment)
- `first_name` (VARCHAR 50)
- `last_name` (VARCHAR 50)
- `email` (VARCHAR 100, UNIQUE)
- `address` (VARCHAR 100)
- `phone` (VARCHAR 20)
- `date_registered` (DATE, Default: CURDATE())

**Loans**
- `loan_id` (PK, Auto Increment)
- `copy_id` (FK → Book_Copies)
- `member_id` (FK → Members)
- `issue_date` (DATE)
- `due_date` (DATE)
- `return_date` (DATE, Nullable)
- `fine_amount` (DECIMAL 10,2, Nullable)

---

## 🔌 API Documentation

### Books Endpoints

**GET /api/books**
- Returns all books in the collection
- Response: JSON array of book objects

**POST /api/books**
- Creates a new book record
- Body: `{title, isbn, genre, publisher_id, publication_year}`
- Response: Success message

**PUT /api/books/{isbn}**
- Updates existing book
- Body: Updated book fields
- Response: Success message

**DELETE /api/books/{isbn}**
- Deletes book and cascades to copies/authors
- Response: Success message

**POST /api/books/bulk_delete**
- Deletes multiple books
- Body: `{ids: [isbn1, isbn2, ...]}`
- Response: Count of deleted records

### Members Endpoints

**GET /api/members**
- Returns all library members
- Response: JSON array with date_registered converted to strings

**POST /api/members**
- Registers new member
- Body: `{first_name, last_name, email, address, phone}`
- Auto-sets date_registered to current date
- Response: Success message

**PUT /api/members/{member_id}**
- Updates member information
- Body: Updated member fields
- Response: Success message

**DELETE /api/members/{member_id}**
- Removes member and associated loans
- Response: Success message

**POST /api/members/bulk_delete**
- Deletes multiple members
- Body: `{ids: [id1, id2, ...]}`
- Response: Count of deleted records

### Loans Endpoints

**GET /api/loans**
- Returns all loan records
- Response: JSON array with dates as strings

**POST /api/loans**
- Creates new loan
- Body: `{copy_id, member_id, issue_date, due_date, fine_amount?}`
- Updates copy status to "On Loan"
- Generates CSV backup
- Response: Success message

**PUT /api/loans/{loan_id}**
- Updates loan details
- Body: Updated loan fields including return_date
- Updates copy status to "Available" if returned
- Response: Success message

**DELETE /api/loans/{loan_id}**
- Deletes loan and restores copy to "Available"
- Response: Success message

**POST /api/loans/bulk_delete**
- Deletes multiple loans
- Body: `{ids: [id1, id2, ...]}`
- Restores all copies to "Available"
- Response: Count of deleted records

### Book Copies Endpoints

**GET /api/copies**
- Returns all book copies
- Response: JSON array with status information

**POST /api/copies**
- Adds new physical copy
- Body: `{isbn, branch_id, status?}`
- Default status: "Available"
- Response: Success message

**PUT /api/copies/{copy_id}**
- Updates copy details
- Body: `{isbn, branch_id, status}`
- Response: Success message

**DELETE /api/copies/{copy_id}**
- Deletes copy and associated loans
- Response: Success message

**POST /api/copies/bulk_delete**
- Deletes multiple copies
- Body: `{ids: [id1, id2, ...]}`
- Response: Count of deleted records

### Branch Endpoints

**GET /api/branches**
- Returns all library branches
- Response: JSON array

**POST /api/branches**
- Creates new branch
- Body: `{branch_name, location}`
- Response: Success message

**POST /api/branches/bulk_delete**
- Deletes branches and cascades to copies/loans
- Body: `{ids: [id1, id2, ...]}`
- Response: Count of deleted records

### Publisher Endpoints

**GET /api/publishers**
- Returns all publishers
- Response: JSON array

**POST /api/publishers**
- Adds new publisher
- Body: `{publisher_name, address, phone}`
- Response: Success message

**POST /api/publishers/bulk_delete**
- Deletes publishers and cascades to books
- Body: `{ids: [id1, id2, ...]}`
- Response: Count of deleted records

### Author Endpoints

**GET /api/authors**
- Returns all authors
- Response: JSON array

**POST /api/authors**
- Adds new author
- Body: `{first_name, last_name}`
- Response: Success message

**POST /api/authors/bulk_delete**
- Deletes authors and Book_Authors links
- Body: `{ids: [id1, id2, ...]}`
- Response: Count of deleted records

### Analytics Endpoint

**GET /api/dashboard**
- Returns comprehensive statistics
- Response:
  ```json
  {
    "counts": {
      "total_books": 100,
      "available_copies": 45,
      "books_on_loan": 35,
      "reserved_copies": 20,
      "active_members": 150
    },
    "status_distribution": {
      "Available": 45,
      "On Loan": 35,
      "Reserved": 20
    },
    "loans_trend": {
      "labels": ["2024-11-01", "2024-11-08", ...],
      "counts": [12, 19, 15, 25, 22, 30]
    },
    "top_genres": {
      "labels": ["Fiction", "Science", ...],
      "counts": [25, 20, 15, 18, 22, 17]
    }
  }
  ```

### Utility Endpoints

**POST /api/seed**
- Generates sample data for testing
- Creates: 3 publishers, 6 authors, 8 books, 6 members, 2 branches, 12 copies, 8 loans
- Uses UUIDs for uniqueness
- Response: Count of inserted records by entity type

---

## 📁 Project Structure

```
library-management-system/
│
├── 📄 app.py                        # Main Flask application
│   ├── Database configuration
│   ├── API route definitions
│   ├── CRUD operations
│   ├── CSV backup functions
│   └── Seed data generator
│
├── 📁 templates/
│   └── library_management_frontend.html  # Single-page application
│       ├── Dashboard view
│       ├── Management tabs (7 entities)
│       ├── Forms for CRUD operations
│       └── Interactive charts
│
├── 📁 data/                         # CSV exports (auto-generated)
│   ├── books.csv
│   ├── members.csv
│   ├── loans.csv
│   └── copies.csv
│
├── 📄 DB_Project.sql                # Database schema + sample data
│   ├── Table definitions
│   ├── Foreign key constraints
│   ├── Initial seed data
│   └── Analytical queries
│
├── 📄 requirements.txt              # Python dependencies
├── 📄 README.md                     # This file
└── 📄 .gitignore                    # Git exclusions
```

### Key Files Explained

**app.py (750+ lines)**
- Flask application setup with CORS support
- 30+ API endpoints for full CRUD operations
- Automated CSV backup on data changes
- Bulk delete with cascade logic
- Dashboard analytics aggregation
- Seed data generator with UUID uniqueness

**library_management_frontend.html (1200+ lines)**
- Responsive single-page application
- Tab-based navigation (Dashboard + 7 management sections)
- Chart.js integration for 3 visualizations
- Real-time table filtering
- Checkbox-based bulk selection
- AJAX-powered CRUD without page reloads

**DB_Project.sql (200+ lines)**
- Complete schema with 8 tables
- Foreign key relationships
- Sample data insertion
- 6 analytical SQL queries for common operations

---

## 🖼️ Screenshots

### Dashboard Overview
![Dashboard](https://github.com/Retaj512/Library-management-system/blob/main/Images/Screenshot%202025-12-03%20205447.png
)
*Real-time metrics and interactive charts showing collection status, loan trends, and genre distribution*

### Book Management
![Books Tab](https://github.com/Retaj512/Library-management-system/blob/main/Images/Screenshot%202025-12-03%20205511.png)
*Comprehensive book cataloging with search, filtering, and bulk operations*

### Loan Processing
![Loans Tab](https://github.com/Retaj512/Library-management-system/blob/main/Images/Screenshot%202025-12-03%20205556.png)
*Streamlined loan creation with automatic status updates and fine calculation*

### Member Registration
![Members Tab](https://github.com/Retaj512/Library-management-system/blob/main/Images/Screenshot%202025-12-03%20205521.png)
*Member registration and tracking with borrowing history*

### Analytics Charts
![Charts](https://github.com/Retaj512/Library-management-system/blob/main/Images/Screenshot%202025-12-03%20205416.png)
![Charts](https://github.com/Retaj512/Library-management-system/blob/main/Images/Screenshot%202025-12-03%20205428.png)
*Doughnut, line, and bar charts powered by Chart.js for data visualization*

---

## 🚀 Advanced Features

### CSV Backup System
- **Auto-Export**: Triggered on data modifications
- **Entities Covered**: Books, Members, Loans, Book_Copies
- **Storage**: Local `data/` directory
- **Format**: UTF-8 encoded CSV with headers

### Smart Deduplication
- **Seed Generator**: Checks existing records before insertion
- **UUID Integration**: Ensures unique names for test data
- **Conflict Handling**: Silently skips duplicates during bulk operations

### Cascade Delete Logic
- **Books**: Removes copies → loans → book_authors → books
- **Members**: Removes loans → members
- **Branches**: Removes copies → loans → branches
- **Publishers**: Removes books (and cascades) → publishers

### Status Automation
- **On Loan Creation**: Copy status → "On Loan"
- **On Return**: Copy status → "Available"
- **On Delete**: Restored to "Available"

---

## 🔐 Security Considerations

**Current Implementation** (Development Mode)
- CORS enabled for all origins (`Access-Control-Allow-Origin: *`)
- No authentication/authorization
- Database credentials in plaintext
- Debug mode enabled

**Production Recommendations**
1. **Authentication**: Implement JWT or session-based auth
2. **Authorization**: Role-based access (Admin, Librarian, Member)
3. **HTTPS**: Use SSL/TLS certificates
4. **Environment Variables**: Store credentials in `.env` file
5. **Input Sanitization**: Validate all user inputs
6. **SQL Injection Prevention**: Use parameterized queries (already implemented)
7. **CORS**: Restrict to specific domain
8. **Rate Limiting**: Prevent API abuse

---

## 🔮 Future Enhancements

### Planned Features
- [ ] **User Authentication**: Login system for staff and members
- [ ] **Email Notifications**: Automated overdue reminders
- [ ] **Barcode Scanning**: ISBN/Member card scanning
- [ ] **Advanced Search**: Full-text search across all fields
- [ ] **Reservation System**: Hold/reserve books
- [ ] **Fine Payment**: Integrate payment gateway
- [ ] **Mobile App**: Native iOS/Android applications
- [ ] **API Documentation**: Swagger/OpenAPI integration
- [ ] **Export Formats**: PDF reports, Excel exports
- [ ] **Multi-Language**: i18n support for localization

### Architectural Improvements
- [ ] **ORM Migration**: Switch from raw SQL to SQLAlchemy
- [ ] **Caching**: Redis for dashboard queries
- [ ] **Async Processing**: Celery for email/notifications
- [ ] **Containerization**: Docker + Docker Compose
- [ ] **CI/CD Pipeline**: Automated testing and deployment
- [ ] **Microservices**: Separate services for loans, members, etc.

---

## 🐛 Known Issues

1. **Fine Calculation**: Fixed at $1/day, no customization
2. **Date Validation**: No check for invalid date ranges
3. **Duplicate ISBNs**: Manual ISBN entry allows duplicates
4. **No Soft Deletes**: Records are permanently removed
5. **Limited Search**: Case-sensitive, exact match only
6. **No Pagination**: All records loaded at once

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Coding Standards
- Python: Follow PEP 8
- JavaScript: Use ES6+ features
- SQL: Use uppercase for keywords
- Comments: Document complex logic

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Flask Community** - For the excellent web framework
- **Chart.js** - For beautiful, responsive charts
- **MySQL** - For reliable database management
- **Stack Overflow** - For endless troubleshooting help
- **Open Source Community** - For inspiration and tools

---

## 📞 Support

For questions, issues, or suggestions:

- **Email**: retajashraf512@gmail.com
- **GitHub Issues**: [Create an issue](https://github.com/Retaj512/library-management-system/issues)

---

<div align="center">

**Built with ❤️ for Libraries Everywhere**

⭐ Star this repo if you found it helpful! ⭐

</div>
