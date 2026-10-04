-- Create Students table
CREATE TABLE Students (
    StudentID INT PRIMARY KEY IDENTITY(1,1),
    Name NVARCHAR(100) NOT NULL,
    Email NVARCHAR(100) NOT NULL,
    Course NVARCHAR(100) NOT NULL,
    TotalFee DECIMAL(10,2) NOT NULL,
    PaidAmount DECIMAL(10,2) NOT NULL DEFAULT 0,
    DueDate DATE NOT NULL
);

-- Create Administrators table
CREATE TABLE Administrators (
    AdminID INT PRIMARY KEY IDENTITY(1,1),
    Name NVARCHAR(100) NOT NULL,
    Email NVARCHAR(100) NOT NULL,
    Role NVARCHAR(50) NOT NULL
);

-- Insert 20 sample students
INSERT INTO Students (Name, Email, Course, TotalFee, PaidAmount, DueDate) VALUES
('Aarav Sharma',     'aarav@college.edu',    'B.Tech CSE',    85000, 85000, '2025-06-30'),
('Priya Patel',      'priya@college.edu',    'MBA',          120000, 60000, '2025-05-15'),
('Rohit Verma',      'rohit@college.edu',    'B.Com',         45000,     0, '2025-04-01'),
('Sneha Iyer',       'sneha@college.edu',    'B.Tech ECE',    85000, 42500, '2025-06-30'),
('Arjun Nair',       'arjun@college.edu',    'BCA',           55000, 55000, '2025-06-30'),
('Kavya Reddy',      'kavya@college.edu',    'MCA',           70000, 35000, '2025-05-01'),
('Tuba Ansari',     'tuba.ansari4321@gmail.com',   'AI/ML',   85000,     0, '2025-03-31'),
('Ananya Joshi',     'ananya@college.edu',   'BA Economics',  40000, 40000, '2025-06-30'),
('Rahul Gupta',      'rahul@college.edu',    'MBA Finance',  120000, 80000, '2025-05-15'),
('Pooja Mehta',      'pooja@college.edu',    'B.Sc IT',       50000, 25000, '2025-04-30'),
('Karan Malhotra',   'karan@college.edu',    'B.Tech CSE',    85000,     0, '2025-03-01'),
('Divya Pillai',     'divya@college.edu',    'BBA',           60000, 60000, '2025-06-30'),
('Siddharth Rao',    'siddharth@college.edu','B.Tech Civil',  85000, 20000, '2025-05-31'),
('Meera Kulkarni',   'meera@college.edu',    'MCA',           70000,     0, '2025-04-15'),
('Aditya Bose',      'aditya@college.edu',   'B.Com Honors',  45000, 45000, '2025-06-30'),
('Nisha Tiwari',     'nisha@college.edu',    'MBA HR',       120000, 90000, '2025-05-15'),
('Suresh Kumar',     'suresh@college.edu',   'B.Tech EEE',    85000, 10000, '2025-04-01'),
('Ritu Agarwal',     'ritu@college.edu',     'BA English',    40000, 20000, '2025-05-30'),
('Manish Choudhary', 'manish@college.edu',   'BCA',           55000,     0, '2025-03-15'),
('Anjali Desai',     'anjali@college.edu',   'B.Sc Physics',  48000, 48000, '2025-06-30');

-- Insert admin
INSERT INTO Administrators (Name, Email, Role) VALUES
('Admin User', 'admin@college.edu', 'SuperAdmin');

-- Verify data
SELECT * FROM Students;
SELECT * FROM Administrators;

