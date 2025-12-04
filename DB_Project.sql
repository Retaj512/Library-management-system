-- Drop existing tables if they exist
DROP TABLE IF EXISTS Loans;
DROP TABLE IF EXISTS Book_Copies;
DROP TABLE IF EXISTS Book_Authors;
DROP TABLE IF EXISTS Books;
DROP TABLE IF EXISTS Library_Branches;
DROP TABLE IF EXISTS Authors;
DROP TABLE IF EXISTS Publishers;
DROP TABLE IF EXISTS Members;

-- Create database
CREATE DATABASE IF NOT EXISTS Library;
USE Library;

-- Publishers Table
CREATE TABLE Publishers (
    publisher_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    address VARCHAR(100),
    phone VARCHAR(20)
);

-- Authors Table
CREATE TABLE Authors (
    author_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL
);

-- Books Table
CREATE TABLE Books (
    isbn INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(100) NOT NULL,
    publisher_id INT,
    publication_year INT,
    genre VARCHAR(50),
    FOREIGN KEY (publisher_id) REFERENCES Publishers(publisher_id)
);

-- Library Branches Table
CREATE TABLE Library_Branches (
    branch_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    location VARCHAR(100) NOT NULL
);

-- Book Authors Table
CREATE TABLE Book_Authors (
    isbn INT,
    author_id INT,
    FOREIGN KEY (isbn) REFERENCES Books(isbn),
    FOREIGN KEY (author_id) REFERENCES Authors(author_id),
    PRIMARY KEY (isbn, author_id)
);

-- Book Copies Table
CREATE TABLE Book_Copies (
    copy_id INT PRIMARY KEY AUTO_INCREMENT,
    isbn INT,
    branch_id INT,
    status ENUM('Available', 'On Loan', 'Reserved') DEFAULT 'Available',
    FOREIGN KEY (isbn) REFERENCES Books(isbn),
    FOREIGN KEY (branch_id) REFERENCES Library_Branches(branch_id)
);

-- Members Table
CREATE TABLE Members (
    member_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE,
    address VARCHAR(100),
    phone VARCHAR(20),
    date_registered DATE DEFAULT CURDATE()
);

-- Loans Table
CREATE TABLE Loans (
    loan_id INT PRIMARY KEY AUTO_INCREMENT,
    copy_id INT,
    member_id INT,
    issue_date DATE NOT NULL,
    due_date DATE NOT NULL,
    return_date DATE,
    fine_amount DECIMAL(10, 2),
    FOREIGN KEY (copy_id) REFERENCES Book_Copies(copy_id),
    FOREIGN KEY (member_id) REFERENCES Members(member_id)
);

-- Insert Publishers
INSERT INTO Publishers (publisher_id, name, address, phone) VALUES
(1, 'Penguin Random House', '1745 Broadway, New York, NY', '212-782-9000'),
(2, 'HarperCollins', '195 Broadway, New York, NY', '212-207-7000');

-- Insert Authors
INSERT INTO Authors (author_id, first_name, last_name) VALUES
(1, 'George', 'Orwell'),
(2, 'Jane', 'Austen');

-- Insert Books
INSERT INTO Books (title, isbn, publisher_id, publication_year, genre) VALUES
('1984', 1001, 1, 1949, 'Fiction'),
('Harry Potter and the Sorcerer''s Stone', 1003, 2, 1997, 'Fantasy');

-- Insert Library Branches
INSERT INTO Library_Branches (branch_id, name, location) VALUES
(1, 'Downtown Central Library', '123 Main Street, City Center'),
(2, 'Northside Branch', '456 Oak Avenue, North District');

-- Insert Book Authors
INSERT INTO Book_Authors (isbn, author_id) VALUES
(1001, 1),  -- 1984 by George Orwell
(1003, 2);  -- Harry Potter by J.K. Rowling

-- Insert Book Copies
INSERT INTO Book_Copies (copy_id, isbn, branch_id, status) VALUES
(1, 1001, 1, 'Available'),
(2, 1001, 2, 'On Loan'),
(3, 1003, 1, 'On Loan');

-- Insert Members
INSERT INTO Members (member_id, first_name, last_name, email, address, phone, date_registered) VALUES
(1, 'John', 'Smith', 'john.smith@email.com', '100 Maple Street', '555-0101', '2024-01-15'),
(2, 'Sarah', 'Johnson', 'sarah.j@email.com', '200 Pine Avenue', '555-0102', '2024-02-20');

-- Insert Loans
INSERT INTO Loans (copy_id, member_id, issue_date, due_date, return_date, fine_amount) VALUES
(2, 1, '2024-11-01', '2024-11-15', NULL, NULL),  -- Active loan - 1984
(3, 2, '2024-10-20', '2024-11-03', '2024-11-10', 7.00);  -- Returned late - Harry Potter

-- Show books that can be borrowed right now
SELECT 
    B.title,
    B.isbn,
    B.genre,
    P.name AS publisher,
    BC.status,
    LB.name AS branch_location
FROM Books B
JOIN Book_Copies BC ON B.isbn = BC.isbn
JOIN Publishers P ON B.publisher_id = P.publisher_id
JOIN Library_Branches LB ON BC.branch_id = LB.branch_id
WHERE BC.status = 'Available'
ORDER BY B.title;

-- Track which books are currently checked out
SELECT 
    L.loan_id,
    M.first_name,
    M.last_name,
    M.email,
    B.title,
    L.issue_date,
    L.due_date,
    DATEDIFF(CURDATE(), L.due_date) AS days_overdue
FROM Loans L
JOIN Members M ON L.member_id = M.member_id
JOIN Book_Copies BC ON L.copy_id = BC.copy_id
JOIN Books B ON BC.isbn = B.isbn
WHERE L.return_date IS NULL
ORDER BY L.due_date;

-- Financial tracking and member account management
SELECT 
    M.member_id,
    M.first_name,
    M.last_name,
    COUNT(L.loan_id) AS total_loans,
    COALESCE(SUM(L.fine_amount), 0) AS total_fines
FROM Members M
LEFT JOIN Loans L ON M.member_id = L.member_id
GROUP BY M.member_id, M.first_name, M.last_name
HAVING total_fines > 0
ORDER BY total_fines DESC;


-- Identify popular titles for purchasing decisions
SELECT 
    B.title,
    B.genre,
    A.first_name,
    A.last_name,
    COUNT(L.loan_id) AS times_borrowed
FROM Books B
LEFT JOIN Book_Authors BA ON B.isbn = BA.isbn
LEFT JOIN Authors A ON BA.author_id = A.author_id
LEFT JOIN Book_Copies BC ON B.isbn = BC.isbn
LEFT JOIN Loans L ON BC.copy_id = L.copy_id
GROUP BY B.isbn, B.title, B.genre, A.first_name, A.last_name
ORDER BY times_borrowed DESC
LIMIT 10;

--  Manage collection distribution across branches
SELECT 
    LB.name AS branch_name,
    LB.location,
    COUNT(BC.copy_id) AS total_copies,
    SUM(CASE WHEN BC.status = 'Available' THEN 1 ELSE 0 END) AS available,
    SUM(CASE WHEN BC.status = 'On Loan' THEN 1 ELSE 0 END) AS on_loan,
    SUM(CASE WHEN BC.status = 'Reserved' THEN 1 ELSE 0 END) AS reserved
FROM Library_Branches LB
LEFT JOIN Book_Copies BC ON LB.branch_id = BC.branch_id
GROUP BY LB.branch_id, LB.name, LB.location
ORDER BY total_copies DESC;

-- Send reminders and manage overdue items
SELECT 
    M.member_id,
    M.first_name,
    M.last_name,
    M.email,
    M.phone,
    B.title,
    L.due_date,
    DATEDIFF(CURDATE(), L.due_date) AS days_overdue,
    DATEDIFF(CURDATE(), L.due_date) * 1.00 AS estimated_fine
FROM Loans L
JOIN Members M ON L.member_id = M.member_id
JOIN Book_Copies BC ON L.copy_id = BC.copy_id
JOIN Books B ON BC.isbn = B.isbn
WHERE L.return_date IS NULL 
  AND L.due_date < CURDATE()
ORDER BY days_overdue DESC;

-- Analyze collection composition by publisher
SELECT 
    P.name AS publisher_name,
    COUNT(DISTINCT B.isbn) AS unique_titles,
    COUNT(BC.copy_id) AS total_copies,
    GROUP_CONCAT(DISTINCT B.genre ORDER BY B.genre) AS genres_published
FROM Publishers P
LEFT JOIN Books B ON P.publisher_id = B.publisher_id
LEFT JOIN Book_Copies BC ON B.isbn = BC.isbn
GROUP BY P.publisher_id, P.name
ORDER BY unique_titles DESC;

-- Return a book and calculate fine
UPDATE Loans 
SET return_date = CURDATE(),
    fine_amount = GREATEST(0, DATEDIFF(CURDATE(), due_date) * 1.00)
WHERE loan_id = 1;

--Change book copy status
UPDATE Book_Copies 
SET status = 'Available'
WHERE copy_id = 2;

-- Remove a member
DELETE FROM Loans WHERE member_id = 4;
DELETE FROM Members WHERE member_id = 4;