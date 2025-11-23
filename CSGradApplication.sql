CREATE DATABASE CSGradApplication;
USE CSGradApplication;

SHOW TABLES;

-- 1. University
CREATE TABLE University (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    UniversityName VARCHAR(255) NOT NULL,
    Country VARCHAR(255) NOT NULL,
    City VARCHAR(255)				-- could be NULL
);

-- 2. Program
CREATE TABLE Program (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    UniversityID INT,
    ProgramName VARCHAR(255) NOT NULL,
    Website VARCHAR(255),			-- could be NULL
    Degree ENUM('Master', 'PhD') NOT NULL,
    FOREIGN KEY (UniversityID) REFERENCES University(ID)
);

-- 3. ApplicantAccount
CREATE TABLE ApplicantAccount (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    Email VARCHAR(255) NOT NULL UNIQUE,
    PasswordHash VARCHAR(255) NOT NULL,
    Name VARCHAR(255),				-- could be NULL
    FinalDecisionProgramID INT,		-- could be NULL
    FOREIGN KEY (FinalDecisionProgramID) REFERENCES Program(ID)
);

-- 4. Education
CREATE TABLE Education (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    ApplicantID INT NOT NULL,
    UniversityID INT NOT NULL,
    GraduationYear INT NOT NULL,
    Major VARCHAR(255) NOT NULL,
    Degree ENUM('Undergraduate', 'Master') NOT NULL,
    GPAScale ENUM('4.0', '100') NOT NULL,
    GPA DECIMAL(5, 2) NOT NULL,		-- input 100 is valid
    FOREIGN KEY (ApplicantID) REFERENCES ApplicantAccount(ID),
    FOREIGN KEY (UniversityID) REFERENCES University(ID)
);

-- 5. Scores
CREATE TABLE Scores (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    ApplicantID INT NOT NULL,
    Type ENUM('GRE', 'TOEFL', 'IELTS') NOT NULL,
    Scores DECIMAL(5, 2) NOT NULL, -- input 322.5 for GRE is valid
    FOREIGN KEY (ApplicantID) REFERENCES ApplicantAccount(ID)
);

-- 6. Experience
CREATE TABLE Experience (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    ApplicantID INT NOT NULL,
    ExperienceType ENUM('Work', 'Research') NOT NULL,
    ExperienceLengthByMonth INT NOT NULL,
    FOREIGN KEY (ApplicantID) REFERENCES ApplicantAccount(ID)
);

-- 7. RecommendationLetter
CREATE TABLE RecommendationLetter (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    ApplicantID INT NOT NULL,
    Relationship ENUM('Research Advisor', 'Course Instructor', 'Employer') NOT NULL,
    Rating ENUM('Strongly Recommend', 'Recommend') NOT NULL,
    FOREIGN KEY (ApplicantID) REFERENCES ApplicantAccount(ID)
);

-- 8. Publication -- it should be M-N relation, but we only care how many pubs an applicant has
CREATE TABLE Publication (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    ApplicantID INT NOT NULL,
    AuthorType ENUM('First Author', 'co-author') NOT NULL,
    JournalType ENUM('Q1', 'Q2', 'Q3', 'Q4') NOT NULL,
    FOREIGN KEY (ApplicantID) REFERENCES ApplicantAccount(ID)
);

-- 9. Application
CREATE TABLE Application (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    ApplicantID INT NOT NULL,
    Status ENUM('Accept', 'Reject', 'Waitlisted') NOT NULL,
    Semester VARCHAR(255) NOT NULL,
    FOREIGN KEY (ApplicantID) REFERENCES ApplicantAccount(ID)
);