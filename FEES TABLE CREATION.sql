CREATE TABLE Fees (
    FeeID INT IDENTITY(1,1) PRIMARY KEY,
    FeeName VARCHAR(100) NOT NULL,
    FeeTypeID INT,
    Department VARCHAR(50),
    YearRange VARCHAR(20),
    Amount INT,
    FOREIGN KEY (FeeTypeID) REFERENCES FeeTypes(FeeTypeID)
);
INSERT INTO Fees (FeeName, FeeTypeID, Department, YearRange, Amount)
VALUES
('Tuition Fee', 1, 'AI&DS', '2024-28', 60000),
('Exam Fee', 2, 'AI&DS', '2024-28', 5000),
('Transport Fee', 3, 'AI&DS', '2024-28', 2000);

INSERT INTO Fees (FeeName, FeeTypeID, Department, YearRange, Amount)
VALUES
('Tuition Fee', 1, 'Computer', '2024-28', 65000),
('Exam Fee', 2, 'Computer', '2024-28', 5500),
('Transport Fee', 3, 'Computer', '2024-28', 2500),

('Tuition Fee', 1, 'IT', '2024-28', 62000),
('Exam Fee', 2, 'IT', '2024-28', 5200),
('Transport Fee', 3, 'IT', '2024-28', 2200),

('Tuition Fee', 1, 'Mechanical', '2024-28', 58000),
('Exam Fee', 2, 'Mechanical', '2024-28', 4800),
('Transport Fee', 3, 'Mechanical', '2024-28', 2000),

('Tuition Fee', 1, 'Civil', '2024-28', 57000),
('Exam Fee', 2, 'Civil', '2024-28', 4700),
('Transport Fee', 3, 'Civil', '2024-28', 2100),

('Tuition Fee', 1, 'Electronics', '2024-28', 63000),
('Exam Fee', 2, 'Electronics', '2024-28', 5300),
('Transport Fee', 3, 'Electronics', '2024-28', 2400);


TRUNCATE TABLE Fees;
SELECT * FROM Fees;
SELECT DISTINCT Department FROM Fees;
