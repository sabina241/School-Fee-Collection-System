SELECT 
    f.FeeID,
    f.FeeName,
    ft.FeeTypeName,
    f.TotalAmount,
    ISNULL(SUM(p.AmountPaid), 0) AS PaidAmount,
    (f.TotalAmount - ISNULL(SUM(p.AmountPaid), 0)) AS BalanceAmount
FROM Students s
JOIN Fees f ON s.department = f.Department
JOIN FeeTypes ft ON f.FeeTypeID = ft.FeeTypeID
LEFT JOIN Payments p 
    ON f.FeeID = p.FeeID AND p.StudentID = 1
WHERE s.StudentID = 1
GROUP BY f.FeeID, f.FeeName, ft.FeeTypeName, f.TotalAmount;
