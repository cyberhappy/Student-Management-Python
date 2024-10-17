# Student Management WebApp

A Python Flask-based web application for managing student data, featuring login functionality, data management
 capabilities, and password reset features. Integrated with MySQL for storing student information and Flask-Mail for
 sending password reset emails.

## Features

- User Authentication: Secure login functionality using hashed passwords.
- Student Data Management: Ability to add, update, and delete student records.
- Password Reset: Users can request a password reset link via email and reset their password
- Flash Messages: User-friendly flash messages to inform users of actions taken
- Responsive Web Pages: Simple and clean UI with Bootstrap forms and minimal design.

### Main Routes

- Login (`/login`): User authentication page
- Home (`/home`): Display list of students (accessible post-login)
- Insert New Student (`/insert`): Add new records to the database
- Update Existing Student (`/update`): Modify existing student records
- Delete Student (`/delete/<id>`): Remove student record by ID
- Request Password Reset (`/reset_password`): Send reset link to user's email
- Reset Password (`/reset/<token>`): Reset password using provided token

## Installation Guide

This guide outlines the steps to set up the Student Management WebApp locally using Flask and MySQL, utilizing XAMPP
 for database and web server management.

### Prerequisites

- Download and Install XAMPP: [Download Link](https://www.apachefriends.org/download.html)
- Launch XAMPP Control Panel
- Start Apache (web server) and MySQL (database server)

### Database Setup

1. Access phpMyAdmin: [Link](http://localhost/phpmyadmin)
2. Create New Database: `student_management`
3. Create Tables:
   ```sql
   CREATE TABLE users (
       id INT AUTO_INCREMENT PRIMARY KEY,
       username VARCHAR(100),
       password VARCHAR(255),
       email VARCHAR(100),
       reset_token VARCHAR(255),
       token_expiration DATETIME
   );

   CREATE TABLE students_info (
       id INT AUTO_INCREMENT PRIMARY KEY,
       name VARCHAR(100),
       email VARCHAR(100),
       phone VARCHAR(20)
   );


### Project Setup

1. Clone Repository:
   ```bash
   https://github.com/cyberhappy/Student-Management-Python.git
   cd Student-Management-Python

2. Install Dependencies:
   ```bash
   pip install flask requests flask-mysqldb flask-mail

3. Configure Environment Variables:
   Open `app.py` and update:
   ```python
   app.config['MYSQL_HOST'] = 'localhost'
   app.config['MYSQL_USER'] = 'flaskuser'
   app.config['MYSQL_PASSWORD'] = 'your_password'
   app.config['MYSQL_DB'] = 'student_management'

4. Run Application:
   ```bash
   python app.py

5. Access Application: http://127.0.0.1:5000

### Usage

- Log in to manage students and user data
- Use password reset feature if forgotten
- Interact with various routes as described above
