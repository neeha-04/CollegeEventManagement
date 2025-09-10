# College Event Management System

## Overview

The College Event Management System is a Flask-based web application designed to streamline the management of college events with blockchain-secured ticketing. The system provides two main user interfaces: a student portal for event registration and an admin portal for event management and attendance tracking. 

Key features include student registration with USN validation, secure ticket generation with blockchain simulation, event management capabilities, and attendance tracking using unique ticket codes. The system uses mock SMS notifications for ticket delivery and implements basic blockchain concepts through cryptographic hashing for ticket verification.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
The application uses a traditional server-side rendered architecture with Flask's Jinja2 templating engine. The frontend is built using Bootstrap 5 with a dark theme for responsive design and modern UI components. Feather icons are integrated for consistent iconography throughout the application. The template system includes a base layout with navigation that adapts based on user authentication status.

### Backend Architecture
The system follows a monolithic Flask architecture with the following key components:

- **Flask Application**: Central app.py file handles all routing, business logic, and request processing
- **Model Layer**: SQLAlchemy ORM models define the database schema and relationships
- **Session Management**: Flask sessions handle admin authentication and user state
- **Blockchain Simulation**: Mock blockchain functionality using SHA-256 hashing for ticket verification
- **SMS Simulation**: Console logging replaces actual SMS sending for ticket notifications

### Data Storage Solutions
The application uses SQLite as the primary database, which is suitable for development and small-scale deployments. The database schema includes:

- **Students Table**: Stores student information with USN validation requirements
- **Events Table**: Contains event details including scheduling and contact information  
- **Registrations Table**: Links students to events with unique ticket codes and blockchain hashes
- **Attendance Table**: Tracks attendance status for registered students
- **Admin Table**: Stores admin credentials with hashed passwords

SQLAlchemy ORM provides database abstraction with automatic table creation and relationship management.

### Authentication and Authorization
The system implements a simple session-based authentication mechanism for admin users. Admin passwords are hashed using Werkzeug's security utilities. Student access does not require authentication - they register directly for events using their USN (University Serial Number) which must start with "1KS" for validation.

### Core Business Logic
- **USN Validation**: Ensures student registration numbers follow the required "1KS" prefix format
- **Ticket Generation**: Creates unique ticket codes using UUID for each registration
- **Blockchain Integration**: Simulates blockchain storage by generating SHA-256 hashes of ticket data
- **Attendance Verification**: Validates ticket codes against stored blockchain hashes before marking attendance

## External Dependencies

### Python Packages
- **Flask**: Core web framework for routing and request handling
- **Flask-SQLAlchemy**: Database ORM integration and management
- **Werkzeug**: Security utilities for password hashing and WSGI middleware

### Frontend Libraries
- **Bootstrap 5**: CSS framework for responsive design and UI components
- **Feather Icons**: Icon library for consistent visual elements throughout the application

### Development Tools
- **SQLite**: Embedded database engine for data persistence
- **ProxyFix**: WSGI middleware for handling proxy headers in deployment environments

The system is designed to be self-contained with minimal external service dependencies, making it suitable for educational environments and rapid prototyping. The mock blockchain and SMS implementations allow for testing without requiring actual blockchain infrastructure or SMS service integration.