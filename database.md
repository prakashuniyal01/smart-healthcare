## Database Schema

- **1. Users Table**: Stores information about all users (patients, doctors, and administrators).

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    full_name VARCHAR(50),
    number NUMBER(15),
    profile_photo BLOB,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('patient', 'doctor', 'admin')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

- **2. Doctors Table**: This table extends the users table to include doctor-specific details.

```sql
CREATE TABLE doctors (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,,  -- Foreign key to users(id)
    specialization_id UUID NOT NULL REFERENCES specializations(id) ON DELETE CASCADE,,  -- Foreign key to specializations(id)
    degree VARCHAR(50),
    license_number VARCHAR(100) UNIQUE NOT NULL,
    years_of_experience INT NOT NULL,
    rating DECIMAL(3, 2) DEFAULT 0,
    consultation_fee DECIMAL(10, 2),
    profile_description TEXT,
    max_patients_per_day INT DEFAULT 10,
    is_active BOOLEAN DEFAULT TRUE,
);
```

- **3. Specializations Table**: This table stores predefined doctor specializations.
```sql 
CREATE TABLE specializations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) UNIQUE NOT NULL,
    category VARCHAR(50)
);
```

- **4. Patients Table**: This table extends the users table to include patient-specific details.

```sql
CREATE TABLE patients (
    user_id UUID PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    date_of_birth DATE NOT NULL,
    gender ENUM('male', 'female', 'other'),
    contact_number VARCHAR(15) UNIQUE,
    reports BLOB,  -- To store report files (PDF, DOC, etc.)
    relative_contact NUMBER(15) UNIQUE
);
```

- **5. Appointments Table**: This table tracks doctor-patient appointments.

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

- **6. Feedback Table**: This table stores feedback and ratings provided by patients for doctors.

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

- **7. Availability Table**: This table tracks the availability of doctors.
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
- **9. Reports Table**: Create a reports table where doctors can upload reports for patients. This table stores metadata like the report file's URL and details about the report.
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



-- Users Table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    full_name VARCHAR(50),
    number VARCHAR(15),
    profile_photo BLOB, -- Storing the image directly
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('patient', 'doctor', 'admin')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Doctors Table
CREATE TABLE doctors (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    specialization_id UUID NOT NULL REFERENCES specializations(id) ON DELETE CASCADE,
    degree VARCHAR(50),
    license_number VARCHAR(100) UNIQUE NOT NULL,
    years_of_experience INT NOT NULL,
    rating DECIMAL(3, 2) DEFAULT 0,
    consultation_fee DECIMAL(10, 2),
    profile_description TEXT,
    max_patients_per_day INT DEFAULT 10,
    availability_status ENUM('active', 'on_leave', 'unavailable') DEFAULT 'active',
    is_active BOOLEAN DEFAULT TRUE
);

-- Specializations Table
CREATE TABLE specializations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) UNIQUE NOT NULL,
    category VARCHAR(50)
);

-- Patients Table
CREATE TABLE patients (
    user_id UUID PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    date_of_birth DATE NOT NULL,
    gender ENUM('male', 'female', 'other'),
    contact_number VARCHAR(15) UNIQUE,
    relative_contact VARCHAR(15) UNIQUE
);

-- Appointments Table
CREATE TABLE appointments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_id UUID NOT NULL REFERENCES patients(user_id) ON DELETE CASCADE,
    doctor_id UUID NOT NULL REFERENCES doctors(user_id) ON DELETE CASCADE,
    scheduled_at TIMESTAMP NOT NULL,
    reason TEXT,
    duration INTERVAL,
    status ENUM('pending', 'confirmed', 'completed', 'cancelled') DEFAULT 'pending',
    payment_status ENUM('pending', 'completed', 'refunded') DEFAULT 'pending',
    reminder_sent BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Feedback Table
CREATE TABLE feedback (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_id UUID NOT NULL REFERENCES patients(user_id) ON DELETE CASCADE,
    doctor_id UUID NOT NULL REFERENCES doctors(user_id) ON DELETE CASCADE,
    rating INT CHECK (rating BETWEEN 1 AND 5) NOT NULL,
    comments TEXT,
    anonymous BOOLEAN DEFAULT FALSE,
    response TEXT DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Availability Table
CREATE TABLE availability (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    doctor_id UUID NOT NULL REFERENCES doctors(user_id) ON DELETE CASCADE,
    available_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    is_available BOOLEAN DEFAULT TRUE,
    CONSTRAINT valid_future_availability CHECK (available_date >= CURRENT_DATE)
);

-- Reports Table
CREATE TABLE reports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_id UUID NOT NULL REFERENCES patients(user_id) ON DELETE CASCADE,
    doctor_id UUID NOT NULL REFERENCES doctors(user_id) ON DELETE CASCADE,
    report_url VARCHAR(255) NOT NULL,
    report_title VARCHAR(100) NOT NULL,
    report_type VARCHAR(100),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
thik h is database or project ke senario jo Project Structure Readme me h sabko save karke readme code me bana do i mean ki 
# Smart Healthcare Appointment System

## **Overview**
A healthcare appointment booking system enabling patients to find and book appointments with doctors based on availability and health requirements. AI/ML will be used to predict optimal time slots and display analytics for administrators.

---

## **Key Features**
1. **Patients** can:
   - Search for doctors based on specialty, location, and availability.
   - Book, reschedule, or cancel appointments.
   - Provide feedback after appointments.

2. **Doctors** can:
   - Manage availability and appointments.
   - View feedback and patient details.

3. **Administrators** can:
   - View analytics like doctor workload, appointment trends, and cancellation rates.
   - Manage users and system settings.

4. **AI/ML Integration**:
   - Predict optimal time slots for appointments based on historical data.
   - Identify high-demand days for doctors.

5. **APIs**:
   - REST APIs for patient-doctor interactions.
   - API documentation via Swagger/Postman.

6. **Dashboards**:
   - Visualize trends and analytics for administrators.

7. **Deployment**:
   - Cloud deployment (e.g., AWS, Heroku).

---

## **Folder Structure**
```plaintext
smart_healthcare/
├── backend/                     # Django backend
│   ├── core/                    # Core app for settings and configurations
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   ├── apps/                    # All Django apps
│   │   ├── __init__.py
│   │   ├── users/               # User management app
│   │   │   ├── migrations/
│   │   │   ├── models.py
│   │   │   ├── serializers.py
│   │   │   ├── urls.py
│   │   │   ├── views.py
│   │   │   └── admin.py
│   │   ├── doctors/             # Doctor management app
│   │   │   ├── migrations/
│   │   │   ├── models.py
│   │   │   ├── serializers.py
│   │   │   ├── urls.py
│   │   │   ├── views.py
│   │   │   └── admin.py
│   │   ├── appointments/        # Appointment booking app
│   │   │   ├── migrations/
│   │   │   ├── models.py
│   │   │   ├── serializers.py
│   │   │   ├── urls.py
│   │   │   ├── views.py
│   │   │   └── admin.py
│   │   └── feedback/            # Feedback app
│   │       ├── migrations/
│   │       ├── models.py
│   │       ├── serializers.py
│   │       ├── urls.py
│   │       ├── views.py
│   │       └── admin.py
│   ├── ml/                      # ML Pipelines
│   │   ├── models/              # Pretrained models
│   │   │   ├── time_slot_model.pkl
│   │   │   └── demand_prediction_model.pkl
│   │   ├── pipelines/           # Pipeline scripts
│   │   │   ├── train_time_slot_model.py
│   │   │   ├── train_demand_model.py
│   │   │   └── preprocess.py
│   │   └── services.py          # ML integration with APIs
│   ├── api/                     # API folder for DRF
│   │   ├── __init__.py
│   │   ├── urls.py              # DRF URL routing
│   │   └── views.py             # General API views
│   ├── static/                  # Static files
│   ├── media/                   # Uploaded files
│   ├── manage.py
│   └── requirements.txt         # Dependencies
├── frontend/                    # React frontend (if hosted here)
│   ├── public/
│   └── src/
│       ├── components/
│       ├── pages/
│       ├── App.js
│       └── index.js
└── deployment/                  # Deployment configurations
    ├── Dockerfile               # For containerization
    ├── docker-compose.yml
    ├── nginx.conf               # Nginx configuration
    └── README.md
```

---

## **Setup Instructions**

### **Backend (Django + DRF)**
1. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```

3. Apply migrations:
   ```bash
   python backend/manage.py migrate
   ```

4. Run the server:
   ```bash
   python backend/manage.py runserver
   ```

---

### **Frontend (React)**
1. Navigate to the `frontend/` folder.
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Run the React development server:
   ```bash
   npm start
   ```

---

### **ML Pipelines**
1. Train models using the scripts in `backend/ml/pipelines/`.
   ```bash
   python backend/ml/pipelines/train_time_slot_model.py
   python backend/ml/pipelines/train_demand_model.py
   ```

2. Save the trained models in `backend/ml/models/`.

---

### **Deployment**
1. Build Docker images and start the containers:
   ```bash
   docker-compose up --build
   ```

2. Access the application at `http://localhost:8000`.

---

## **Key Deliverables**
- A functioning web application for booking appointments.
- Integrated ML models for predictions.
- Secure REST APIs with documentation.
- Interactive dashboards for administrators.

---

is information ko save kar lena ab 
isee releted hi quaryis honge or isko ek readme pe update kar do ache se 
