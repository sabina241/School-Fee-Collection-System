CREATE TABLE Payments (
    PaymentID INT IDENTITY PRIMARY KEY,
    StudentID INT,
    FeeID INT,
    AmountPaid INT,
    PaymentDate DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (StudentID) REFERENCES Students(student_id),
    FOREIGN KEY (FeeID) REFERENCES Fees(FeeID)
);
DROP TABLE Payments;

SELECT * FROM Payments;

ALTER TABLE Payments
DROP CONSTRAINT FK__Payments__Studen__2A164134;

ALTER TABLE Payments
ADD CONSTRAINT FK_Payments_Student
FOREIGN KEY (StudentID)
REFERENCES Students(student_id)
ON DELETE CASCADE;

