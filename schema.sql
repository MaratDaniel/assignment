-- CSCI 341 Assignment 3 - Database Schema
-- Online Caregivers Platform

-- Drop tables if they exist (for clean setup)
DROP TABLE IF EXISTS appointment CASCADE;
DROP TABLE IF EXISTS job_application CASCADE;
DROP TABLE IF EXISTS job CASCADE;
DROP TABLE IF EXISTS address CASCADE;
DROP TABLE IF EXISTS member CASCADE;
DROP TABLE IF EXISTS caregiver CASCADE;
DROP TABLE IF EXISTS "user" CASCADE;

-- Create USER table
CREATE TABLE "user" (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    given_name VARCHAR(100) NOT NULL,
    surname VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    profile_description TEXT,
    password VARCHAR(255) NOT NULL
);

-- Create CAREGIVER table
CREATE TABLE caregiver (
    caregiver_user_id INTEGER PRIMARY KEY,
    photo VARCHAR(255),
    gender VARCHAR(20) NOT NULL,
    caregiving_type VARCHAR(50) NOT NULL CHECK (caregiving_type IN ('babysitter', 'elderly care', 'playmate for children')),
    hourly_rate DECIMAL(10, 2) NOT NULL CHECK (hourly_rate > 0),
    FOREIGN KEY (caregiver_user_id) REFERENCES "user"(user_id) ON DELETE CASCADE
);

-- Create MEMBER table
CREATE TABLE member (
    member_user_id INTEGER PRIMARY KEY,
    house_rules TEXT,
    dependent_description TEXT,
    FOREIGN KEY (member_user_id) REFERENCES "user"(user_id) ON DELETE CASCADE
);

-- Create ADDRESS table
CREATE TABLE address (
    member_user_id INTEGER PRIMARY KEY,
    house_number VARCHAR(20) NOT NULL,
    street VARCHAR(255) NOT NULL,
    town VARCHAR(100) NOT NULL,
    FOREIGN KEY (member_user_id) REFERENCES member(member_user_id) ON DELETE CASCADE
);

-- Create JOB table
CREATE TABLE job (
    job_id SERIAL PRIMARY KEY,
    member_user_id INTEGER NOT NULL,
    required_caregiving_type VARCHAR(50) NOT NULL CHECK (required_caregiving_type IN ('babysitter', 'elderly care', 'playmate for children')),
    other_requirements TEXT,
    date_posted DATE NOT NULL,
    FOREIGN KEY (member_user_id) REFERENCES member(member_user_id) ON DELETE CASCADE
);

-- Create JOB_APPLICATION table
CREATE TABLE job_application (
    caregiver_user_id INTEGER NOT NULL,
    job_id INTEGER NOT NULL,
    date_applied DATE NOT NULL,
    PRIMARY KEY (caregiver_user_id, job_id),
    FOREIGN KEY (caregiver_user_id) REFERENCES caregiver(caregiver_user_id) ON DELETE CASCADE,
    FOREIGN KEY (job_id) REFERENCES job(job_id) ON DELETE CASCADE
);

-- Create APPOINTMENT table
CREATE TABLE appointment (
    appointment_id SERIAL PRIMARY KEY,
    caregiver_user_id INTEGER NOT NULL,
    member_user_id INTEGER NOT NULL,
    appointment_date DATE NOT NULL,
    appointment_time TIME NOT NULL,
    work_hours DECIMAL(4, 2) NOT NULL CHECK (work_hours > 0),
    status VARCHAR(20) NOT NULL CHECK (status IN ('pending', 'confirmed', 'declined', 'completed')),
    FOREIGN KEY (caregiver_user_id) REFERENCES caregiver(caregiver_user_id) ON DELETE CASCADE,
    FOREIGN KEY (member_user_id) REFERENCES member(member_user_id) ON DELETE CASCADE
);

-- Insert data into USER table (at least 10 instances)
INSERT INTO "user" (email, given_name, surname, city, phone_number, profile_description, password) VALUES
('sarah.johnson@email.com', 'Sarah', 'Johnson', 'Astana', '+77012345678', 'Experienced caregiver with 5 years of experience', 'pass123'),
('michael.chen@email.com', 'Michael', 'Chen', 'Almaty', '+77012345679', 'Professional babysitter specializing in early childhood development', 'pass124'),
('emily.davis@email.com', 'Emily', 'Davis', 'Astana', '+77012345680', 'Certified elderly care specialist', 'pass125'),
('david.wilson@email.com', 'David', 'Wilson', 'Shymkent', '+77012345681', 'Fun and energetic playmate for children', 'pass126'),
('lisa.anderson@email.com', 'Lisa', 'Anderson', 'Astana', '+77012345682', 'Nursing background with CPR certification', 'pass127'),
('james.martinez@email.com', 'James', 'Martinez', 'Almaty', '+77012345683', 'Patient and caring elderly caregiver', 'pass128'),
('anna.kim@email.com', 'Anna', 'Kim', 'Astana', '+77012345684', 'Creative activities coordinator for children', 'pass129'),
('robert.taylor@email.com', 'Robert', 'Taylor', 'Aktobe', '+77012345685', 'Experienced with special needs children', 'pass130'),
('maria.garcia@email.com', 'Maria', 'Garcia', 'Astana', '+77012345686', 'Bilingual caregiver (English and Russian)', 'pass131'),
('john.brown@email.com', 'John', 'Brown', 'Almaty', '+77012345687', 'Retired teacher now providing elderly care', 'pass132'),
('arman.armanov@email.com', 'Arman', 'Armanov', 'Astana', '+77012345688', 'Professional caregiver with medical training', 'pass133'),
('amina.aminova@email.com', 'Amina', 'Aminova', 'Almaty', '+77012345689', 'Family member seeking reliable caregiver', 'pass134'),
('alex.smith@email.com', 'Alex', 'Smith', 'Astana', '+77012345690', 'Looking for experienced babysitter', 'pass135'),
('olga.petrova@email.com', 'Olga', 'Petrova', 'Shymkent', '+77012345691', 'Mother of two seeking weekend caregiver', 'pass136'),
('nurbol.nurbolov@email.com', 'Nurbol', 'Nurbolov', 'Astana', '+77012345692', 'Seeking elderly care for my father', 'pass137'),
('zhanar.zhumagulova@email.com', 'Zhanar', 'Zhumagulova', 'Almaty', '+77012345693', 'Need playmate for my 6-year-old daughter', 'pass138'),
('dmitry.ivanov@email.com', 'Dmitry', 'Ivanov', 'Astana', '+77012345694', 'Working parent seeking after-school care', 'pass139'),
('ayzhan.kazakhova@email.com', 'Ayzhan', 'Kazakhova', 'Aktobe', '+77012345695', 'Looking for elderly care with medical knowledge', 'pass140'),
('sergey.volkov@email.com', 'Sergey', 'Volkov', 'Astana', '+77012345696', 'Father seeking reliable babysitter', 'pass141'),
('madina.abdullayeva@email.com', 'Madina', 'Abdullayeva', 'Almaty', '+77012345697', 'Need caregiver for my elderly mother', 'pass142'),
('nazira.suleimenova@email.com', 'Nazira', 'Suleimenova', 'Astana', '+77012345698', 'Seeking gentle care for elderly family member', 'pass143');

-- Insert data into CAREGIVER table (at least 10 instances)
INSERT INTO caregiver (caregiver_user_id, photo, gender, caregiving_type, hourly_rate) VALUES
(1, 'sarah_photo.jpg', 'Female', 'babysitter', 15.50),
(2, 'michael_photo.jpg', 'Male', 'babysitter', 12.00),
(3, 'emily_photo.jpg', 'Female', 'elderly care', 18.75),
(4, 'david_photo.jpg', 'Male', 'playmate for children', 10.00),
(5, 'lisa_photo.jpg', 'Female', 'elderly care', 20.00),
(6, 'james_photo.jpg', 'Male', 'elderly care', 16.50),
(7, 'anna_photo.jpg', 'Female', 'playmate for children', 11.25),
(8, 'robert_photo.jpg', 'Male', 'babysitter', 14.00),
(9, 'maria_photo.jpg', 'Female', 'babysitter', 13.50),
(10, 'john_photo.jpg', 'Male', 'elderly care', 17.00),
(11, 'arman_photo.jpg', 'Male', 'babysitter', 9.50);

-- Insert data into MEMBER table (at least 10 instances)
INSERT INTO member (member_user_id, house_rules, dependent_description) VALUES
(12, 'No pets. Please maintain hygiene standards.', 'I have a 5-year-old son who likes painting and needs supervision'),
(13, 'Smoke-free environment. Quiet hours after 8 PM.', 'Looking for caregiver for my 3-year-old daughter'),
(14, 'No pets. Strict hygiene protocols required.', 'Elderly father (78 years old) with mobility issues'),
(15, 'Pet-friendly home. Flexible schedule.', 'Two children: 7-year-old boy and 5-year-old girl'),
(16, 'No pets. Medical equipment in the house.', 'Elderly mother (82 years old) with dementia'),
(17, 'No pets. Creative activities encouraged.', '6-year-old daughter who loves arts and crafts'),
(18, 'No pets. Homework help required.', '8-year-old son who needs after-school supervision'),
(19, 'No pets. Medication management needed.', 'Elderly grandmother (85 years old) with diabetes'),
(20, 'No pets. Outdoor activities preferred.', '5-year-old son who is very active'),
(21, 'No pets. Gentle care required.', 'Elderly mother (80 years old) with arthritis');

-- Insert data into ADDRESS table (at least 10 instances)
INSERT INTO address (member_user_id, house_number, street, town) VALUES
(12, '45', 'Kabanbay Batyr', 'Astana'),
(13, '12', 'Abay Avenue', 'Almaty'),
(14, '78', 'Nazarbayev Street', 'Shymkent'),
(15, '23', 'Kabanbay Batyr', 'Astana'),
(16, '56', 'Dostyk Avenue', 'Almaty'),
(17, '34', 'Turan Avenue', 'Astana'),
(18, '89', 'Sain Street', 'Aktobe'),
(19, '67', 'Kabanbay Batyr', 'Astana'),
(20, '91', 'Al-Farabi Avenue', 'Almaty'),
(21, '44', 'Kabanbay Batyr', 'Astana');

-- Insert data into JOB table (at least 10 instances)
INSERT INTO job (member_user_id, required_caregiving_type, other_requirements, date_posted) VALUES
(12, 'babysitter', 'Must be soft-spoken and patient. Experience with children preferred.', '2025-01-15'),
(13, 'babysitter', 'Creative activities, soft-spoken caregiver needed', '2025-01-20'),
(14, 'elderly care', 'Medical knowledge preferred. No pets in house.', '2025-01-25'),
(15, 'playmate for children', 'Energetic and fun. Must love outdoor activities.', '2025-02-01'),
(16, 'elderly care', 'Experience with dementia patients. Soft-spoken and gentle.', '2025-02-05'),
(17, 'playmate for children', 'Arts and crafts skills. Creative and soft-spoken.', '2025-02-10'),
(18, 'babysitter', 'Homework help required. Educational background preferred.', '2025-02-15'),
(19, 'elderly care', 'Medication management. Medical training required.', '2025-02-20'),
(20, 'playmate for children', 'Active and energetic. Sports activities preferred.', '2025-02-25'),
(21, 'elderly care', 'Gentle care for arthritis patient. Soft-spoken caregiver.', '2025-03-01'),
(12, 'playmate for children', 'Painting and art activities. Soft-spoken preferred.', '2025-03-05'),
(13, 'babysitter', 'Weekend care. Flexible schedule.', '2025-03-10');

-- Insert data into JOB_APPLICATION table (at least 10 instances)
INSERT INTO job_application (caregiver_user_id, job_id, date_applied) VALUES
(1, 1, '2025-01-16'),
(2, 1, '2025-01-17'),
(4, 4, '2025-02-02'),
(7, 4, '2025-02-03'),
(3, 3, '2025-01-26'),
(5, 3, '2025-01-27'),
(6, 5, '2025-02-06'),
(10, 5, '2025-02-07'),
(7, 6, '2025-02-11'),
(9, 7, '2025-02-16'),
(8, 7, '2025-02-17'),
(3, 8, '2025-02-21'),
(5, 8, '2025-02-22'),
(4, 9, '2025-02-26'),
(6, 10, '2025-03-02'),
(1, 11, '2025-03-06'),
(4, 11, '2025-03-07'),
(2, 12, '2025-03-11');

-- Insert data into APPOINTMENT table (at least 10 instances)
INSERT INTO appointment (caregiver_user_id, member_user_id, appointment_date, appointment_time, work_hours, status) VALUES
(1, 12, '2025-03-15', '09:00:00', 3.0, 'confirmed'),
(2, 13, '2025-03-16', '10:00:00', 4.0, 'confirmed'),
(3, 14, '2025-03-17', '14:00:00', 5.0, 'confirmed'),
(4, 15, '2025-03-18', '09:00:00', 3.5, 'confirmed'),
(5, 16, '2025-03-19', '15:00:00', 6.0, 'confirmed'),
(6, 19, '2025-03-20', '10:00:00', 4.5, 'confirmed'),
(7, 17, '2025-03-21', '11:00:00', 3.0, 'confirmed'),
(8, 18, '2025-03-22', '13:00:00', 4.0, 'confirmed'),
(9, 20, '2025-03-23', '09:00:00', 5.0, 'confirmed'),
(10, 21, '2025-03-24', '14:00:00', 4.0, 'confirmed'),
(1, 12, '2025-03-25', '12:00:00', 3.0, 'pending'),
(2, 13, '2025-03-26', '15:00:00', 2.5, 'declined'),
(3, 14, '2025-03-27', '16:00:00', 4.0, 'pending'),
(4, 15, '2025-03-28', '10:00:00', 3.0, 'declined'),
(11, 12, '2025-03-29', '11:00:00', 4.5, 'confirmed');

