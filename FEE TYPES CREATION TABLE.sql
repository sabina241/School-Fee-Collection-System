CREATE TABLE FeeTypes (
    FeeTypeID INT IDENTITY(1,1) PRIMARY KEY,
    FeeTypeName VARCHAR(50) NOT NULL
);
INSERT INTO FeeTypes (FeeTypeName)
VALUES ('Annual'), ('Semester'), ('Monthly');
ALTER TABLE FeeTypes
ADD Frequency VARCHAR(20);

UPDATE FeeTypes
SET Frequency = 'Yearly'
WHERE FeeTypeName = 'Annual';

UPDATE FeeTypes
SET Frequency = 'Half-Yearly'
WHERE FeeTypeName = 'Semester';

UPDATE FeeTypes
SET Frequency = 'Monthly'
WHERE FeeTypeName = 'Monthly';

SELECT * FROM FeeTypes;
