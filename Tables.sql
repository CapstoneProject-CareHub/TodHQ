CREATE TABLE DaycareProfiles (
    daycare_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address VARCHAR(255),
    city VARCHAR(255),
    state VARCHAR(50),
    zipcode VARCHAR(20),
    phone VARCHAR(20),
    email VARCHAR(255),
    website VARCHAR(255),
    description TEXT,
    rating DECIMAL(3, 2),
    total_reviews INT,
    license_number VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);


INSERT INTO DaycareProfiles (name, address, city, state, zipcode, phone, email, website, description, rating, total_reviews, license_number)
VALUES
    ('Kids Academy', '123 Elm Street', 'Fremont', 'CA', '94536', '123-456-7890', 'info@fremontkidsacademy.com', 'https://www.fremontkidsacademy.com', 'A nurturing daycare in Fremont.', 4.5, 25, 'CA123456'),
    ('Little Explorers Daycare', '456 Oak Avenue', 'Fremont', 'CA', '94538', '408-555-1234', 'info@littleexplorersfremont.com', 'https://www.littleexplorersfremont.com', 'We promote learning through play.', 4.0, 15, 'CA789012'),
    ('Milpitas KinderCare', '789 Maple Drive', 'Milpitas', 'CA', '95035', '408-987-6543', 'info@milpitaskindercare.com', 'https://www.milpitaskindercare.com', 'Quality childcare in Milpitas.', 4.2, 30, 'CA456789'),
    ('Sunshine Daycare', '321 Pine Lane', 'Milpitas', 'CA', '95036', '408-333-2222', 'info@sunshinemilpitas.com', 'https://www.sunshinemilpitas.com', 'A bright start for your child.', 4.7, 18, 'CA987654'),
    ('Little Learners', '789 Oakwood Drive', 'Fremont', 'CA', '94539', '510-789-1234', 'info@fremontlittlelearners.com', 'https://www.fremontlittlelearners.com', 'Nurturing young minds in Fremont.', 4.3, 22, 'CA345678'),
    ('Tiny Tots Childcare', '101 Cedar Avenue', 'Fremont', 'CA', '94537', '510-222-3333', 'info@tinytotsfremont.com', 'https://www.tinytotsfremont.com', 'A safe and fun environment for kids.', 4.8, 27, 'CA567890'),
    ('Early Explorers', '456 Birch Street', 'Milpitas', 'CA', '95037', '408-777-8888', 'info@milpitasexplorers.com', 'https://www.milpitasexplorers.com', 'Discover, learn, and grow with us.', 4.6, 24, 'CA234567'),
    ('Happy Kids Daycare', '222 Redwood Lane', 'Milpitas', 'CA', '95038', '408-666-9999', 'info@happykidsmilpitas.com', 'https://www.happykidsmilpitas.com', 'Where every day is a happy day!', 4.4, 20, 'CA678901');

SELECT
    daycare_id,
    name,
    address,
    city,
    state,
    zipcode,
    phone,
    email,
    website,
    description,
    rating
FROM
    DaycareProfiles
WHERE
    (city = 'Fremont' OR city = 'Milpitas') -- Specify the cities you're interested in
    AND state = 'CA' -- Specify the state you're interested in
    AND rating >= 4.0; -- Specify the minimum average rating you want


-- Caregivers Table

CREATE TABLE Caregivers (
    caregiver_id INT AUTO_INCREMENT PRIMARY KEY,
    daycare_id INT, -- Foreign Key linking to the daycare
    name VARCHAR(255) NOT NULL,
    age INT,
    gender VARCHAR(20),
    bio TEXT,
    experience_years INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (daycare_id) REFERENCES DaycareProfiles (daycare_id)
);


-- Insert caregiver profiles
INSERT INTO Caregivers (daycare_id, name, age, gender, bio, experience_years)
VALUES
    (2, 'Emily Johnson', 32, 'Female', 'Experienced caregiver with a passion for early childhood education.', 8),
    (3, 'Michael Davis', 28, 'Male', 'Committed to providing a safe and nurturing environment for children.', 6),
    (2, 'Sophia Martinez', 35, 'Female', 'Dedicated to fostering creativity and learning in young minds.', 10),
    (4, 'David Lee', 26, 'Male', 'Enthusiastic caregiver with a background in child psychology.', 4),
    (1, 'John Doe', 35, 'Male', 'Experienced caregiver with a background in early childhood education.', 5),
    (1, 'Jane Smith', 28, 'Female', 'Passionate about providing quality care to children.', 4);

SELECT
    caregiver_id,
    daycare_id,
    name,
    age,
    gender,
    bio,
    experience_years,
    created_at,
    updated_at
FROM
    Caregivers;
    
-- Users Table

   CREATE TABLE Users (
    user_id INT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) CHECK (role IN ('Parent', 'Caregiver')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample users
INSERT INTO Users (user_id, username, password, role)
VALUES
    (101, 'parent1@example.com', 'hashed_password_1', 'Parent'),
    (102, 'caregiver1@example.com', 'hashed_password_2', 'Caregiver'),
    (103, 'parent2@example.com', 'hashed_password_3', 'Parent'),
    (104, 'caregiver2@example.com', 'hashed_password_4', 'Caregiver'),
    (105, 'parent3@example.com', 'hashed_password_5', 'Parent');

SELECT
    user_id,
    username,
    role,
    created_at
FROM
    Users;


--  Reviews Table

CREATE TABLE Reviews (
    review_id INT AUTO_INCREMENT PRIMARY KEY,
    daycare_id INT, -- Foreign Key linking to the daycare
    user_id INT, -- Foreign Key linking to the user
    rating INT CHECK (rating >= 1 AND rating <= 5), -- Rating from 1 to 5 stars
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (daycare_id) REFERENCES DaycareProfiles (daycare_id),
    FOREIGN KEY (user_id) REFERENCES Users (user_id)
);

-- Insert sample reviews
INSERT INTO Reviews (daycare_id, user_id, rating, comment)
VALUES
    (1, 101, 5, 'Outstanding daycare with caring staff and great facilities.'),
    (2, 102, 4, 'Very good experience, my child enjoys their time here.'),
    (1, 103, 5, 'Exceptional service, highly recommended!'),
    (3, 104, 3, 'Good daycare, but room for improvement in some areas.'),
    (2, 105, 4, 'Friendly staff, clean environment, overall satisfied.');

SELECT
    R.review_id,
    D.name AS daycare_name,
    U.username AS user_name,
    R.rating,
    R.comment,
    R.created_at
FROM
    Reviews R
JOIN
    DaycareProfiles D ON R.daycare_id = D.daycare_id
JOIN
    Users U ON R.user_id = U.user_id;

-- Images Table

CREATE TABLE Images (
    image_id INT AUTO_INCREMENT PRIMARY KEY,
    daycare_id INT,
    url VARCHAR(255) NOT NULL,
    description TEXT,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (daycare_id) REFERENCES DaycareProfiles (daycare_id)
);

INSERT INTO Images (daycare_id, url, description)
VALUES
    (1, 'https://f.hubspotusercontent40.net/hubfs/3073399/EYRC_June2021/Images/work-18.jpg', 'Daycare facility exterior'),
    (1, 'https://example.com/image2.jpg', 'Children playing area'),
    (2, 'https://example.com/image3.jpg', 'Indoor activity space'),
    (3, 'https://example.com/image4.jpg', 'Outdoor playground'),
    (3, 'https://example.com/image5.jpg', 'Classroom setup');

SELECT
    image_id,
    daycare_id,
    url,
    description,
    uploaded_at
FROM
    Images
WHERE
    daycare_id = 1; -- Specify the daycare ID you want to retrieve images for

COMMIT
