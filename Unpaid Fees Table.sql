SELECT 
    f.FeeID,
    f.FeeName,
    ft.FeeTypeName AS FeeType,
    f.TotalAmount,
    ISNULL(SUM(p.AmountPaid), 0) AS PaidAmount,
    (f.TotalAmount - ISNULL(SUM(p.AmountPaid), 0)) AS BalanceAmount
FROM Students s
JOIN Fees f 
    ON s.Department = f.Department
JOIN FeeTypes ft 
    ON f.FeeTypeID = ft.FeeTypeID
LEFT JOIN Payments p 
    ON f.FeeID = p.FeeID 
    AND p.StudentID = s.StudentID
WHERE s.StudentID = ?      -- Logged-in student
GROUP BY 
    f.FeeID, 
    f.FeeName, 
    ft.FeeTypeName, 
    f.TotalAmount
HAVING 
    (f.TotalAmount - ISNULL(SUM(p.AmountPaid), 0)) > 0
ORDER BY 
    ft.FeeTypeName;
