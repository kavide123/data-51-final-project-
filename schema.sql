-- ============================================
-- Appointment Tracker Database Schema
-- ============================================

-- Create the database
CREATE DATABASE IF NOT EXISTS appointment_tracker;
USE appointment_tracker;

-- Create the appointments table
CREATE TABLE IF NOT EXISTS appointments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_name VARCHAR(100) NOT NULL,
    doctor_name VARCHAR(100) NOT NULL,
    appointment_date DATE NOT NULL,
    appointment_time TIME NOT NULL,
    reason VARCHAR(255) NOT NULL,
    status ENUM('Scheduled', 'Completed', 'Cancelled') DEFAULT 'Scheduled',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample data
INSERT INTO appointments (patient_name, doctor_name, appointment_date, appointment_time, reason, status) VALUES
('John Smith', 'Dr. Emily Carter', '2026-05-15', '09:00:00', 'Annual checkup', 'Scheduled'),
('Jane Doe', 'Dr. Michael Lee', '2026-05-16', '10:30:00', 'Follow-up visit', 'Scheduled'),
('Robert Johnson', 'Dr. Emily Carter', '2026-05-14', '14:00:00', 'Blood work review', 'Completed'),
('Maria Garcia', 'Dr. Sarah Patel', '2026-05-17', '11:00:00', 'Consultation', 'Scheduled'),
('James Wilson', 'Dr. Michael Lee', '2026-05-13', '08:30:00', 'Vaccination', 'Cancelled');
