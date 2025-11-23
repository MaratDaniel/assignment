# CSCI 341 Assignment 3 - Online Caregivers Platform

## Project Overview
This project implements a comprehensive database system and web application for an online caregivers platform, allowing families to find and connect with caregivers for various needs (babysitting, elderly care, playmates for children).

## Project Structure
```
assignment/
├── schema.sql                    # Database schema and initial data
├── database_queries.py           # Part 2: SQLAlchemy queries
├── app.py                        # Part 3: Flask web application
├── requirements.txt              # Python dependencies
├── README.md                     # This file
├── executive_summary.txt         # Executive summary document
└── templates/                    # Flask HTML templates
    ├── base.html
    ├── index.html
    ├── users/
    ├── caregivers/
    ├── members/
    ├── addresses/
    ├── jobs/
    ├── job_applications/
    └── appointments/
```

## Setup Instructions

### 1. Database Setup (PostgreSQL)
```bash
# Create database
createdb caregivers_db

# Run schema.sql to create tables and insert data
psql -d caregivers_db -f schema.sql
```

### 2. Python Environment Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Set database URL (optional, defaults to localhost)
export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/caregivers_db"
```

### 3. Run Part 2 Queries
```bash
python database_queries.py
```

### 4. Run Flask Web Application (Part 3)
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Database Schema
- **USER**: Base user information
- **CAREGIVER**: Caregiver-specific information
- **MEMBER**: Family member information
- **ADDRESS**: Member addresses
- **JOB**: Job postings by members
- **JOB_APPLICATION**: Applications by caregivers to jobs
- **APPOINTMENT**: Scheduled appointments between caregivers and members

## Features Implemented

### Part 1: Database Schema
- All tables created with proper primary keys and foreign keys
- Data constraints and check constraints implemented
- At least 10 instances per table inserted

### Part 2: SQL Queries
- Create, Insert, Update, Delete operations
- Simple queries (4 queries)
- Complex queries with joins and aggregations (4 queries)
- Derived attribute calculation
- View creation and querying

### Part 3: Web Application
- Full CRUD operations for all tables
- Modern, responsive web interface
- Flask-based RESTful application
- Ready for deployment

## Notes
- Database connection string can be modified in both `database_queries.py` and `app.py`
- For deployment, update the `DATABASE_URL` environment variable
- The application uses SQLAlchemy for database operations

