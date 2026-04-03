let allData = [];

async function loadData() {
    const res = await fetch("/admin/fees-data");
    allData = await res.json();
    renderTable();
}

function renderTable() {
    const status = document.getElementById("statusFilter").value;
    const dept = document.getElementById("deptFilter").value;

    const table = document.getElementById("feesTable");
    table.innerHTML = "";

    allData.forEach(row => {
        let feeStatus = "Paid";
        if (row.paid_amount == 0) feeStatus = "Unpaid";
        else if (row.balance > 0) feeStatus = "Balance";

        if (
            (status !== "All" && status !== feeStatus) ||
            (dept !== "All" && dept !== row.department)
        ) return;

        table.innerHTML += `
            <tr>
                <td>${row.student_name}</td>
                <td>${row.department}</td>
                <td>${row.fee_name}</td>
                <td>₹${row.total_amount}</td>
                <td>₹${row.paid_amount}</td>
                <td>₹${row.balance}</td>
                <td>${feeStatus}</td>
            </tr>
        `;
    });
}

document.getElementById("statusFilter").addEventListener("change", renderTable);
document.getElementById("deptFilter").addEventListener("change", renderTable);

loadData();