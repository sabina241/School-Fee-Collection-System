document.addEventListener("DOMContentLoaded", loadHistory);

function loadHistory() {
    fetch("/student/payment-history/data")
        .then(res => res.json())
        .then(data => {
            const table = document.getElementById("historyTable");
            table.innerHTML = "";

            if (data.length === 0) {
                table.innerHTML = `
                    <tr>
                        <td colspan="5">No completed payments yet</td>
                    </tr>`;
                return;
            }

            data.forEach(fee => {
                table.innerHTML += `
                    <tr>
                        <td>${fee.fee_name}</td>
                        <td>${fee.type}</td>
                        <td>₹ ${fee.amount}</td>
                        <td>${fee.date}</td>
                        <td>
                            <a href="/student/receipt/${fee.fee_id}"
                               class="receipt-btn" target="_blank">
                               Get Receipt
                            </a>
                        </td>
                    </tr>
                `;
            });
        });
}
