CREATE TABLE Students (
    student_id INT IDENTITY(1,1) PRIMARY KEY,
    name VARCHAR(100),
    username VARCHAR(50) UNIQUE,
    password VARCHAR(50),
    department VARCHAR(50),
    year_range VARCHAR(20),
    abc_id VARCHAR(50),
    blood_group VARCHAR(10)
);
ALTER TABLE Students
ADD email VARCHAR(100);

ALTER TABLE Students
ADD CONSTRAINT chk_gmail
CHECK (email LIKE '%@tcetmumbai.in');

UPDATE Students
SET email = '1032241368@tcetmumbai.in'
WHERE student_id = 1;

SELECT *FROM Students;