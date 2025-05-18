# Notification Service using Flask and MySQL

## Overview
This project implements a notification service with a REST API for:

- POST /notifications: Accepts a JSON payload with userId, type (EMAIL, SMS, INAPP), an optional subject, and a message. The notification is saved with a "PENDING" status in a MySQL database, processed immediately, and its status is updated.
- GET /users/{id}/notifications: Returns all notifications for the specified user.

## Setup Instructions

1. Clone the Repository:
   ```bash
   git clone <https://github.com/Piyush-Ver/notification_service.git
   >
   cd notification_service
    
   b: Create a Virtual Environment and Install Dependencies:(in bash)
     python -m venv venv
     source venv/bin/activate  # On Windows: venv\Scripts\activate
     pip install -r requirements.txt
   c:Configure the Database: (in sql)
   Update config.py with your MySQL connection string or set the DATABASE_URI environment variable. Create the MySQL database if it doesn’t exist:
       CREATE DATABASE notification_service_db;
d:Run the Flask Application:(in bash)
      python app.py

  Application will be available at http://localhost:5000.


