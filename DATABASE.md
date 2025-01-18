Entities and Relationships
The system requires the following main entities:

User (Base entity for all types of users: patients, doctors, admins)
Doctor (Extends User for additional doctor-specific details)
Patient (Extends User for additional patient-specific details)
Appointment (Links doctors and patients)
Feedback (Submitted by patients for doctors)
Specialization (Defines doctor specialties)
Availability (Tracks doctor schedules)
Audit Logs (Logs changes for security and traceability)
Database Schema
1. Users Table
Stores shared attributes of all users.
Supports role-based access (Patient, Doctor, Admin).
Field	Type	Constraints
id	UUID (Primary Key)	Unique, Primary Key
username	VARCHAR(150)	Unique, Indexed
email	VARCHAR(255)	Unique, Indexed
password	VARCHAR(255)	Encrypted
role	ENUM('patient', 'doctor', 'admin')	Role-Based Access
created_at	TIMESTAMP	Default: CURRENT_TIMESTAMP
updated_at	TIMESTAMP	Default: CURRENT_TIMESTAMP, On Update
2. Doctors Table
Extends the users table with doctor-specific details.
Field	Type	Constraints
user_id	UUID (FK: users.id)	Unique, References users
specialization_id	INT (FK: specialization.id)	Links to Specialization
license_number	VARCHAR(100)	Unique, Verified
years_of_experience	INT	Not Null
rating	DECIMAL(3,2)	Default: 0
3. Patients Table
Extends the users table with patient-specific details.
Field	Type	Constraints
user_id	UUID (FK: users.id)	Unique, References users
date_of_birth	DATE	Not Null
gender	ENUM('male', 'female', 'other')	Optional
contact_number	VARCHAR(15)	Indexed
4. Specializations Table
Stores predefined doctor specializations.
Field	Type	Constraints
id	INT (Primary Key)	Unique, Auto-Increment
name	VARCHAR(100)	Unique, Not Null
5. Appointments Table
Tracks doctor-patient appointments.
Field	Type	Constraints
id	UUID (Primary Key)	Unique, Primary Key
patient_id	UUID (FK: patients.user_id)	Not Null
doctor_id	UUID (FK: doctors.user_id)	Not Null
scheduled_at	TIMESTAMP	Not Null
status	ENUM('pending', 'confirmed', 'completed', 'cancelled')	Default: 'pending'
created_at	TIMESTAMP	Default: CURRENT_TIMESTAMP
6. Feedback Table
Stores feedback and ratings provided by patients for doctors.
Field	Type	Constraints
id	UUID (Primary Key)	Unique, Primary Key
patient_id	UUID (FK: patients.user_id)	Not Null
doctor_id	UUID (FK: doctors.user_id)	Not Null
rating	INT (1-5)	Not Null
comments	TEXT	Optional
created_at	TIMESTAMP	Default: CURRENT_TIMESTAMP
7. Availability Table
Tracks the availability of doctors.
Field	Type	Constraints
id	UUID (Primary Key)	Unique, Primary Key
doctor_id	UUID (FK: doctors.user_id)	Not Null
day_of_week	ENUM('Monday', 'Tuesday', ..., 'Sunday')	Not Null
start_time	TIME	Not Null
end_time	TIME	Not Null
8. Audit Logs Table
Logs sensitive actions for traceability.
Field	Type	Constraints
id	UUID (Primary Key)	Unique, Primary Key
action_by	UUID (FK: users.id)	Not Null
action_type	VARCHAR(255)	e.g., 'CREATE', 'UPDATE', 'DELETE'
action_detail	TEXT	Detailed Description
created_at	TIMESTAMP	Default: CURRENT_TIMESTAMP
Key Points
Security:

Use UUID for primary keys to avoid predictable IDs.
Encrypt sensitive data like passwords (e.g., use bcrypt or Django’s make_password).
Implement database-level constraints for data integrity.
DRY Principle:

Separate shared attributes into a single users table.
Use foreign keys to avoid duplication of data.
Scalability:

Index frequently queried fields (e.g., username, email, contact_number).
Use partitioning or sharding if the data volume grows significantly.
Analytics Support:

Use created_at fields for tracking trends.
Design the schema to support queries like "average rating per doctor" or "appointment trends per day."
Let me know if you want to refine or implement any specific part! 🚀







-- 1. Users Table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(150) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('patient', 'doctor', 'admin') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 2. Doctors Table
CREATE TABLE doctors (
    user_id UUID PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    specialization_id INT NOT NULL,
    license_number VARCHAR(100) UNIQUE NOT NULL,
    years_of_experience INT NOT NULL,
    rating DECIMAL(3, 2) DEFAULT 0,
    FOREIGN KEY (specialization_id) REFERENCES specializations(id)
);

-- 3. Patients Table
CREATE TABLE patients (
    user_id UUID PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    date_of_birth DATE NOT NULL,
    gender ENUM('male', 'female', 'other'),
    contact_number VARCHAR(15) UNIQUE
);

-- 4. Specializations Table
CREATE TABLE specializations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

-- 5. Appointments Table
CREATE TABLE appointments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_id UUID NOT NULL REFERENCES patients(user_id) ON DELETE CASCADE,
    doctor_id UUID NOT NULL REFERENCES doctors(user_id) ON DELETE CASCADE,
    scheduled_at TIMESTAMP NOT NULL,
    status ENUM('pending', 'confirmed', 'completed', 'cancelled') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 6. Feedback Table
CREATE TABLE feedback (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_id UUID NOT NULL REFERENCES patients(user_id) ON DELETE CASCADE,
    doctor_id UUID NOT NULL REFERENCES doctors(user_id) ON DELETE CASCADE,
    rating INT CHECK (rating BETWEEN 1 AND 5) NOT NULL,
    comments TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 7. Availability Table
CREATE TABLE availability (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    doctor_id UUID NOT NULL REFERENCES doctors(user_id) ON DELETE CASCADE,
    day_of_week ENUM('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday') NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL
);

-- 8. Audit Logs Table
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    action_by UUID NOT NULL REFERENCES users(id) ON DELETE SET NULL,
    action_type VARCHAR(255) NOT NULL,
    action_detail TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for optimization
CREATE INDEX idx_users_email ON users (email);
CREATE INDEX idx_users_username ON users (username);
CREATE INDEX idx_patients_contact_number ON patients (contact_number);
CREATE INDEX idx_appointments_scheduled_at ON appointments (scheduled_at);
