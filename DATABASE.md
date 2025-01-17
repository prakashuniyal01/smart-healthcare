# Smart Healthcare Appointment System

## Overview
A healthcare appointment booking system where patients can find and book appointments with doctors based on availability and health requirements. The system uses AI/ML to predict optimal time slots for booking and provides analytics dashboards for administrators.

---

## Key Tables and Relationships

### 1. Users Table (Abstracting Patients, Doctors, and Admins)
This table stores basic user information and leverages Django's `AbstractUser` for role-based management.

```sql
User
-----
id (Primary Key)
username (Unique)
email (Unique)
password
first_name
last_name
phone
role (Choices: PATIENT, DOCTOR, ADMIN)
date_joined
last_login
is_active
is_staff (For admin)
```

### 2. Doctor Table
Stores additional information specific to doctors. This table has a one-to-one relationship with the `User` table.

```plaintext
Doctor
-----
id (Primary Key)
user_id (Foreign Key to User)
specialization (e.g., Cardiologist, Dentist)
experience_years
bio
clinic_address
consultation_fee
available_days (e.g., Mon, Tue, Wed - ArrayField)
available_slots (e.g., ["10:00", "11:00"] - JSONField)
profile_image
```

### 3. Patient Table
Stores additional information for patients. This table has a one-to-one relationship with the `User` table.

```plaintext
Patient
-----
id (Primary Key)
user_id (Foreign Key to User)
date_of_birth
gender (Choices: Male, Female, Other)
address
medical_history (TextField or JSONField for conditions like diabetes, allergies, etc.)
profile_image
```

### 4. Appointment Table
Tracks all appointments. This table has many-to-one relationships with both `Doctor` and `Patient`.

```plaintext
Appointment
-----
id (Primary Key)
doctor_id (Foreign Key to Doctor)
patient_id (Foreign Key to Patient)
appointment_date (Date)
appointment_time (Time)
status (Choices: PENDING, CONFIRMED, CANCELED, COMPLETED)
symptoms (TextField)
created_at (Timestamp)
updated_at (Timestamp)
```

### 5. Feedback Table
Stores feedback for doctors from patients. This table has many-to-one relationships with both `Doctor` and `Patient`.

```plaintext
Feedback
-----
id (Primary Key)
doctor_id (Foreign Key to Doctor)
patient_id (Foreign Key to Patient)
rating (IntegerField: 1-5)
comment (TextField)
created_at (Timestamp)
```

### 6. Analytics Table
Stores aggregated data for analytics purposes.

```plaintext
Analytics
-----
id (Primary Key)
doctor_id (Foreign Key to Doctor)
total_appointments
completed_appointments
canceled_appointments
average_rating
last_updated (Timestamp)
```

---

## ER Diagram Relationships

- **User ↔ Doctor (1-to-1):** Each doctor is a user with additional attributes.
- **User ↔ Patient (1-to-1):** Each patient is a user with additional attributes.
- **Doctor ↔ Appointment (1-to-Many):** A doctor can have many appointments.
- **Patient ↔ Appointment (1-to-Many):** A patient can book multiple appointments.
- **Doctor ↔ Feedback (1-to-Many):** A doctor can receive feedback from multiple patients.
- **Patient ↔ Feedback (1-to-Many):** A patient can give feedback to multiple doctors.

---

## Scalability and Best Practices

1. **Abstract Models:** Use Django’s abstract base models for shared fields (e.g., timestamps for `created_at` and `updated_at`).
2. **Indexes:** Add database indexes on frequently queried fields (e.g., `appointment_date`, `status`).
3. **JSONFields:** Use `JSONField` for flexible fields like `medical_history` or `available_slots`.
4. **Audit Logs:** Optionally, add a `Log` table to track changes for debugging or reporting.
5. **Soft Deletes:** Use a `deleted` boolean flag for tables to implement soft delete instead of permanently deleting rows.

---

## Getting Started

1. **Install Dependencies:**
   ```bash
   pip install django djangorestframework
   ```

2. **Migrate Database:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Run the Development Server:**
   ```bash
   python manage.py runserver
   ```

4. **Access the Admin Panel:**
   Create a superuser and log in to the admin interface to manage users, doctors, and appointments.

---

## Additional Notes

- Use Django’s `admin` panel for easy management of data.
- Add unit tests to ensure code quality and functionality.
- Deploy the application to a cloud platform like AWS, Heroku, or Azure for production.
