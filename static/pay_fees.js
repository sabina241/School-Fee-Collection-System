let selectedFeeId = null;

/* LOAD FEES WHEN PAGE OPENS */
document.addEventListener("DOMContentLoaded", () => {
    loadFees("All");
});

/* FETCH FEES */
function loadFees(filter) {
    fetch(`/student/pay-fees/data?filter=${filter}`)
        .then(res => res.json())
        .then(data => {
            const table = document.getElementById("feesTable");
            table.innerHTML = "";

            if (data.length === 0) {
                table.innerHTML = `<tr><td colspan="6">No unpaid fees</td></tr>`;
                return;
            }

            data.forEach(fee => {
                table.innerHTML += `
                    <tr>
                        <td>${fee.fee_name}</td>
                        <td>${fee.fee_type}</td>
                        <td>₹${fee.total}</td>
                        <td>₹${fee.paid}</td>
                        <td>₹${fee.balance}</td>
                        <td>
                            <button onclick="openModal(${fee.fee_id})">
                                Pay
                            </button>
                        </td>
                    </tr>
                `;
            });
        });
}

/* FILTER LOGIC */
function applyFilter(type) {
    loadFees(type);
    document.getElementById("filterDropdown").style.display = "none";
}

/* FILTER TOGGLE */
function toggleFilter() {
    const drop = document.getElementById("filterDropdown");
    drop.style.display = drop.style.display === "block" ? "none" : "block";
}

/* MODAL */
function openModal(feeId) {
    selectedFeeId = feeId;
    document.getElementById("paymentModal").style.display = "flex";
}

function closeModal() {
    document.getElementById("paymentModal").style.display = "none";
    document.getElementById("payAmount").value = "";
}

/* PAYMENT */
function confirmPayment() {
    let amount = document.getElementById("payAmount").value;

    fetch("/student/pay-fees/pay", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            fee_id: selectedFeeId,
            amount: amount
        })
    })
    .then(res => res.json())
    .then(() => {
        closeModal();
        loadFees("All");
    });
}