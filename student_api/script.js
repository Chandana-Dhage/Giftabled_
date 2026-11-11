


let students = [];




async function addStudent() {

    let id = Number(document.getElementById("studentId").value);

    let name = document.getElementById("name").value;

    let course = document.getElementById("course").value;



    if (!id || !name || !course) {
        alert("Please enter all student details");
        return;
    }



    let existing = students.find(student => student.id === id);

    if (existing) {
        alert("Student ID already exists");
        return;
    }


    let student = {
        id: id,
        name: name,
        course: course
    };


    students.push(student);

    alert("Student added successfully");

   document.getElementById("studentId").value="";
   document.getElementById("name").value="";
   document.getElementById("course").value="";

//    first create the endpoints than method...left side variable name python and right hand side javascript so passing
//    the variable name from javascript to python

   const response = await fetch("http://127.0.0.1:8000/students", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id: id, name:name, course:course })
    });

    const data = await response.json();
    alert(data.message);
}





async function updateStudent() {
    
    
    const idText = document.getElementById("updateId").value;

    const name = document.getElementById("updateName").value.trim();

    const course = document.getElementById("updateCourse").value.trim();


    if (idText === "" || name === "" || course === "") {
        alert("Enter ID, name, and course.");
        return;
    }


    const id = Number(idText);

    const response = await fetch(
        "http://127.0.0.1:8000/students/" + id,
        {
            method: "PUT",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                id: id,
                name: name,
                course: course
            })
        }
    );


    const data = await response.json();


    if (!response.ok) {
        alert(JSON.stringify(data.detail));
        return;
    }


    document.getElementById("actionMessage").textContent =
        "Student updated successfully";

    document.getElementById("updateId").value = "";
    document.getElementById("updateName").value = "";
    document.getElementById("updateCourse").value = "";


    await viewAllStudents();

}



// DELETE STUDENT

async function deleteStudent() {

    const idText = document.getElementById("deleteId").value;

    if (idText === "") {
        alert("Enter the student ID to delete.");
        return;
    }

    const id = Number(idText);

    if (!confirm("Delete student " + id + "?")) {
        return;
    }

    const response = await fetch(
        "http://127.0.0.1:8000/students/" + id,
        {
            method: "DELETE"
        }
    );

    const data = await response.json();

    if (!response.ok) {
        alert(JSON.stringify(data.detail));
        return;
    }

    document.getElementById("actionMessage").textContent = data.message;

    document.getElementById("deleteId").value = "";

    await viewAllStudents();
}



async function readLibraries() {
    const response = await fetch("http://127.0.0.1:8000/libraries");

    const data = await response.json();

    const list = document.getElementById("libraryList");
    list.textContent = "";

    for (const library of Object.values(data)) {
        const item = document.createElement("li");

        item.textContent =
            library.LibraryName + " - " + library.Place;

        list.appendChild(item);
    }
}

async function viewStudent() {

    let id = Number(document.getElementById("viewId").value);

    const response = await fetch(`http://127.0.0.1:8000/students/${id}`);

    const data = await response.json();

    const result = document.getElementById("result");

    result.textContent = "";

    if (!response.ok) {
        result.textContent = data.detail || "Student not found";
        return;
    }

    const table = document.createElement("table");

    const header = document.createElement("tr");

    header.innerHTML = `
        <th>ID</th>
        <th>Name</th>
        <th>Course</th>
    `;

    table.appendChild(header);

    const row = document.createElement("tr");

    row.innerHTML = `
        <td>${data.id}</td>
        <td>${data.name}</td>
        <td>${data.course}</td>
    `;

    table.appendChild(row);

    result.appendChild(table);
}


// VIEW ALL STUDENTS

async function viewAllStudents() {

    const response = await fetch("http://127.0.0.1:8000/students");

    const data = await response.json();

    const result = document.getElementById("result");

    result.textContent = "";

    if (!response.ok) {
        result.textContent = "Unable to fetch students";
        return;
    }

    const table = document.createElement("table");

    const header = document.createElement("tr");

    header.innerHTML = `
        <th>ID</th>
        <th>Name</th>
        <th>Course</th>
    `;

    table.appendChild(header);


    for (const [id, student] of Object.entries(data)) {

        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${id}</td>
            <td>${student.name}</td>
            <td>${student.course}</td>
        `;

        table.appendChild(row);

    }

    result.appendChild(table);
}