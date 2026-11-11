
// API URL

const API_URL = "http://127.0.0.1:8000/expenses";


// ADD EXPENSE - POST

async function addExpense() {

    const idText = document.getElementById("expenseId").value;

    const description = document.getElementById("description").value.trim();

    const amountText = document.getElementById("amount").value;

    const category = document.getElementById("category").value.trim();


    if (idText === "" || description === "" || amountText === "" || category === "") {
        alert("Please enter all expense details.");
        return;
    }

    const amount = Number(amountText);

    if (amount <= 0 || !Number.isFinite(amount)) {
        alert("Amount must be greater than zero.");
        return;
    }

    const id = Number(idText);

    if (!Number.isInteger(id)) {
        alert("Expense ID must be an integer.");
        return;
    }


    const response = await fetch(API_URL, {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            id: id,
            description: description,
            amount: amount,
            category: category
        })

    });


    const data = await response.json();


    if (!response.ok) {
        alert(JSON.stringify(data.detail));
        return;
    }


    document.getElementById("actionMessage").textContent = data.message;

    document.getElementById("expenseId").value = "";
    document.getElementById("description").value = "";
    document.getElementById("amount").value = "";
    document.getElementById("category").value = "";

    await viewAllExpenses();

}



// VIEW ONE EXPENSE - GET

async function viewExpense() {

    const idText = document.getElementById("viewId").value;

    if (idText === "") {
        alert("Enter Expense ID.");
        return;
    }

    const id = Number(idText);

    const response = await fetch(API_URL + "/" + id);

    const data = await response.json();

    const result = document.getElementById("result");

    result.textContent = "";

    if (!response.ok) {
        result.textContent = data.detail || "Expense not found";
        return;
    }


    const table = document.createElement("table");

    const header = document.createElement("tr");

    header.innerHTML = `
        <th>ID</th>
        <th>Description</th>
        <th>Amount</th>
        <th>Category</th>
    `;

    table.appendChild(header);


    const row = document.createElement("tr");

    const values = [
        data.id,
        data.description,
        data.amount,
        data.category
    ];

    for (const value of values) {
        const cell = document.createElement("td");
        cell.textContent = value;
        row.appendChild(cell);
    }

    table.appendChild(row);

    result.appendChild(table);

}





async function viewAllExpenses() {

    const response = await fetch(API_URL);

    const data = await response.json();

    const result = document.getElementById("result");

    result.textContent = "";

    if (!response.ok) {
        result.textContent = "Unable to fetch expenses";
        return;
    }


    const table = document.createElement("table");

    const header = document.createElement("tr");

    let totalAmount=0;

    header.innerHTML = `
        <th>ID</th>
        <th>Description</th>
        <th>Amount</th>
        <th>Category</th>
    `;

    table.appendChild(header);


    for (const [id, expense] of Object.entries(data)) {

        const row = document.createElement("tr");

        totalAmount+=expense.amount;
        const values = [
            id,
            expense.description,
            expense.amount,
            expense.category
        ];

        for (const value of values) {
            const cell = document.createElement("td");
            cell.textContent = value;
            row.appendChild(cell);
        }

        table.appendChild(row);

    }

    result.appendChild(table);

    const total = document.createElement("h3");

    total.textContent = "Total Expenses: ₹" + totalAmount;

    result.appendChild(total);

}



// UPDATE EXPENSE - PUT

async function updateExpense() {

    const idText = document.getElementById("updateId").value;

    const description = document.getElementById("updateDescription").value.trim();

    const amountText = document.getElementById("updateAmount").value;

    const category = document.getElementById("updateCategory").value.trim();


    if (idText === "" ||
        description === "" || amountText === "" || category === "") {

        alert("Please enter all expense details.");
        return;
    }


    const id = Number(idText);

    const amount = Number(amountText);


    if (!Number.isInteger(id)) {
        alert("Expense IDs must be integers.");
        return;
    }

    if (!Number.isFinite(amount) || amount <= 0) {
        alert("Amount must be greater than zero.");
        return;
    }


    const response = await fetch(API_URL + "/" + id, {

        method: "PUT",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({

            id: id,
            description: description,
            amount: amount,
            category: category

        })

    });


    const data = await response.json();


    if (!response.ok) {
        alert(JSON.stringify(data.detail));
        return;
    }


    document.getElementById("actionMessage").textContent = data.message;

    document.getElementById("updateId").value = "";
    document.getElementById("updateDescription").value = "";
    document.getElementById("updateAmount").value = "";
    document.getElementById("updateCategory").value = "";


    await viewAllExpenses();

}



async function deleteExpense() {

    const idText = document.getElementById("deleteId").value;


    if (idText === "") {
        alert("Enter Expense ID to delete.");
        return;
    }


    const id = Number(idText);


    if (!confirm("Delete expense " + id + "?")) {
        return;
    }


    const response = await fetch(API_URL + "/" + id, {
        method: "DELETE"
    });


    const data = await response.json();


    if (!response.ok) {
        alert(JSON.stringify(data.detail));
        return;
    }


    document.getElementById("actionMessage").textContent = data.message;

    document.getElementById("deleteId").value = "";


    await viewAllExpenses();

}
