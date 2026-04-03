CREATE TABLE StudentFees (
    StudentFeeID INT IDENTITY(1,1) PRIMARY KEY,
    StudentID INT,
    FeeID INT,
    Period VARCHAR(50),
    PaidAmount INT DEFAULT 0,
    Status VARCHAR(20) DEFAULT 'Pending',
    FOREIGN KEY (StudentID) REFERENCES Students(student_id),
    FOREIGN KEY (FeeID) REFERENCES Fees(FeeID)
);
SELECT * FROM StudentFees;