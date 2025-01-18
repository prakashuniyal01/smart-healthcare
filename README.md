 Smart Healthcare Appointment System
Overview: A healthcare appointment booking system where patients can find and book appointments with doctors based on availability and health requirements. The system should use AI/ML to predict optimal time slots for booking and display analytics for administrators.

Key Tasks for Trainees:
AI/ML:
Train a machine learning model to predict the best time slots for appointments based on historical data.
Implement a feature to predict high-demand days for doctors.

Django:
Develop the backend to manage doctors, patients, appointments, and feedback.
Include user authentication and role-based access (e.g., patient, doctor, admin).

DRF:
Create REST APIs for booking appointments, retrieving doctor details, and managing schedules.
Ensure API documentation is available using Swagger or Postman.

Data Visualization:
Design dashboards showing doctor workload, appointment trends, and cancellation rates.

Deployment:
Deploy the application to a cloud platform (e.g., AWS, Heroku).

Deliverables:
A functioning web application for booking appointments.
Machine learning models integrated with the backend.
APIs with proper authentication and error handling.
Visual dashboards for administrators.


# Smart Healthcare Appointment System

## **Overview**
A healthcare appointment booking system where patients can find and book appointments with doctors based on availability and health requirements. The system uses AI/ML for predicting optimal booking slots and includes administrative analytics dashboards.

---

## **Database Schema**
Below is the detailed SQL schema for the system:

### **1. Users Table**
This table stores shared attributes of all user roles (patients, doctors, and admins).

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(150) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    profile_photo image
    email_verified BOOLEAN DEFAULT FALSE,
    role ENUM('patient', 'doctor') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

---

### **2. Doctors Table**
This table extends the `users` table to include doctor-specific details.

```sql
CREATE TABLE doctors (
    user_id UUID PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    specialization_id INT NOT NULL,
    degree VARCHAR(50)
    license_number VARCHAR(100) UNIQUE NOT NULL,
    years_of_experience INT NOT NULL,
    rating DECIMAL(3, 2) DEFAULT 0,
    consultation_fee DECIMAL(10, 2),
    profile_description TEXT,
    max_patients_per_day INT DEFAULT 10,
    is_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (specialization_id) REFERENCES specializations(id)
);
```

---

### **3. Patients Table**
This table extends the `users` table to include patient-specific details.

```sql
CREATE TABLE patients (
    user_id UUID PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    date_of_birth DATE NOT NULL,
    gender ENUM('male', 'female', 'other'),
    contact_number VARCHAR(15) UNIQUE,
    symptoms TEXT,
    reports 
    relative_contect number(15) UNIQUE,
);
```
---
### **4. Specializations Table**
This table stores predefined doctor specializations.

```sql
CREATE TABLE specializations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    category VARCHAR(50)
);

```

---

### **5. Appointments Table**
This table tracks doctor-patient appointments.

```sql
CREATE TABLE appointments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_id UUID NOT NULL REFERENCES patients(user_id) ON DELETE CASCADE,
    doctor_id UUID NOT NULL REFERENCES doctors(user_id) ON DELETE CASCADE,
    scheduled_at TIMESTAMP NOT NULL,
    reason TEXT,
    duration INTERVAL,
    status ENUM('pending', 'confirmed', 'completed', 'cancelled') DEFAULT 'pending',
    reminder_sent BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

```

---

### **6. Feedback Table**
This table stores feedback and ratings provided by patients for doctors.

```sql
CREATE TABLE feedback (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_id UUID NOT NULL REFERENCES patients(user_id) ON DELETE CASCADE,
    doctor_id UUID NOT NULL REFERENCES doctors(user_id) ON DELETE CASCADE,
    rating INT CHECK (rating BETWEEN 1 AND 5) NOT NULL,
    comments TEXT,
    anonymous BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

### **7. Availability Table**
This table tracks the availability of doctors.

```sql
CREATE TABLE availability (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    doctor_id UUID NOT NULL REFERENCES doctors(user_id) ON DELETE CASCADE,
    available_date DATE NOT NULL, -- This field represents the date of availability
    start_time TIME NOT NULL, -- Start time of availability on the given date
    end_time TIME NOT NULL, -- End time of availability on the given date
    shift_id INT, -- Reference to the shift if using multiple shifts per day (optional)
    time_zone VARCHAR(50), -- Time zone for handling different time zones of the doctor
    CONSTRAINT valid_future_availability CHECK (available_date >= CURRENT_DATE) -- Ensures only future dates are allowed
);

```

---

### **8. Audit Logs Table**
This table logs sensitive actions for traceability.

```sql
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    action_by UUID NOT NULL REFERENCES users(id) ON DELETE SET NULL,
    action_type VARCHAR(255) NOT NULL,
    action_detail TEXT,
    session_id UUID,
    ip_address VARCHAR(50),
    device_info TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

--- 
### **9. Reports Table**
Create a reports table where doctors can upload reports for patients. This table stores metadata like the report file's URL and details about the report.
```sql  
CREATE TABLE reports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_id UUID NOT NULL REFERENCES patients(user_id) ON DELETE CASCADE,
    doctor_id UUID NOT NULL REFERENCES doctors(user_id) ON DELETE CASCADE,
    report_url VARCHAR(255) NOT NULL, -- Path/URL where the report is stored (file path or cloud URL)
    report_type VARCHAR(100), -- Type of report (e.g., X-ray, Blood Test, Prescription)
    description TEXT, -- Optional description for the report
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

---

## **Key Points**

### **1. Security**
- **UUIDs**: Used as primary keys for all main tables to prevent predictable IDs.
- **Encrypted Passwords**: Store passwords in a hashed format (e.g., `bcrypt`).
- **Data Integrity**: Enforced through `FOREIGN KEYS` and constraints.

### **2. DRY Principle**
- Shared attributes are stored in the `users` table.
- Relationships are maintained using foreign keys.

### **3. Scalability**
- Frequently queried fields (e.g., `username`, `email`, `contact_number`) are indexed for performance.
- Schema is designed to handle large data volumes.

### **4. Analytics Support**
- Use `created_at` fields to track appointment trends and user activity.
- Design supports queries for ratings, workload, and high-demand time slots.

---

## **How to Use**
1. **Database Setup**: Execute the SQL script in a PostgreSQL environment.
2. **Integrate with Backend**: Use Django models to map the schema and enforce validations.
3. **Data Population**: Prepopulate the `specializations` table with common doctor specialties.
4. **Indexes and Optimization**: Ensure indexes are applied for optimal query performance.

---
For further assistance, feel free to reach out! 🚀

---
## **@ Folder Structure** 
``` textarea 
.
├── apps
│   ├── analytics
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── __init__.py
│   │   ├── management
│   │   │   ├── commands
│   │   │   │   └── train_model.py
│   │   │   └── test.py
│   │   ├── migrations
│   │   │   └── __init__.py
│   │   ├── ml
│   │   │   ├── data
│   │   │   │   └── preprocessing.py
│   │   │   ├── models
│   │   │   │   └── time_slot_predictor.py
│   │   │   ├── pipeline.py
│   │   │   └── utils
│   │   │       └── evaluation.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── appointments
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── __init__.py
│   │   ├── migrations
│   │   │   └── __init__.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── doctors
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── __init__.py
│   │   ├── migrations
│   │   │   └── __init__.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── feedback
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── __init__.py
│   │   ├── migrations
│   │   │   └── __init__.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── patients
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── __init__.py
│   │   ├── migrations
│   │   │   └── __init__.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   └── users
│       ├── admin.py
│       ├── apps.py
│       ├── __init__.py
│       ├── migrations
│       │   ├── __init__.py
│       │   └── __pycache__
│       │       └── __init__.cpython-312.pyc
│       ├── models.py
│       ├── __pycache__
│       │   ├── admin.cpython-312.pyc
│       │   ├── apps.cpython-312.pyc
│       │   ├── __init__.cpython-312.pyc
│       │   └── models.cpython-312.pyc
│       ├── serializers.py
│       ├── tests.py
│       ├── urls.py
│       └── views.py
├── config
│   ├── asgi.py
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-312.pyc
│   │   ├── settings.cpython-312.pyc
│   │   ├── urls.cpython-312.pyc
│   │   └── wsgi.cpython-312.pyc
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── DATABASE.md
├── db.sqlite3
├── docker-compose.yml
├── Dockerfile
├── frontend
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   │   ├── __init__.py
│   │   └── __pycache__
│   │       └── __init__.cpython-312.pyc
│   ├── models.py
│   ├── __pycache__
│   │   ├── admin.cpython-312.pyc
│   │   ├── apps.cpython-312.pyc
│   │   ├── __init__.cpython-312.pyc
│   │   └── models.cpython-312.pyc
│   ├── tests.py
│   └── views.py
├── logs
├── Makefile
├── manage.py
├── media
├── README.md
├── requirements.txt
├── static
└── templates
```