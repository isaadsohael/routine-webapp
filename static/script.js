function logout() {
    window.location.href = "/logout";
}

function addRow() {
    const table = document.getElementById('routineTable').getElementsByTagName('tbody')[0];
    const colCount = document.getElementById('routineTable').rows[0].cells.length;
    const newRow = table.insertRow();
    for (let i = 0; i < colCount; i++) {
        const cell = newRow.insertCell();
        cell.contentEditable = "true";
        cell.innerText = "";
    }
}

function deleteRow() {
    const table = document.getElementById('routineTable').getElementsByTagName('tbody')[0];
    if (table.rows.length > 0) {
        table.deleteRow(table.rows.length - 1);
    }
}

function addColumn() {
    const table = document.getElementById('routineTable');
    const headerRow = table.rows[0];
    const newHeader = headerRow.insertCell();
    newHeader.contentEditable = "true";
    newHeader.innerText = "New Column";

    for (let i = 1; i < table.rows.length; i++) {
        const newCell = table.rows[i].insertCell();
        newCell.contentEditable = "true";
        newCell.innerText = "";
    }
}

function deleteColumn() {
    const table = document.getElementById('routineTable');
    const colCount = table.rows[0].cells.length;
    if (colCount > 1) {
        for (let row of table.rows) {
            row.deleteCell(colCount - 1);
        }
    }
}

function saveChanges() {
    const table = document.getElementById('routineTable');
    const tbody = table.getElementsByTagName('tbody')[0];
    const data = [];

    const headers = Array.from(table.querySelector('thead tr').cells).map(cell => cell.innerText.trim());

    for (let row of tbody.rows) {
        const rowData = {};
        for (let i = 0; i < row.cells.length; i++) {
            rowData[headers[i] || `column_${i+1}`] = row.cells[i].innerText.trim();
        }

        if (Object.values(rowData).some(value => value !== '')) {
            data.push(rowData);
        }
    }

    const title = document.getElementById('routineTitle')?.innerText.trim() || 'CLASS TESTS & LABS';

    fetch('/save_routine', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({routine: data,title:title})
    }).then(res => res.json())
      .then(response => {
        alert('Routine saved successfully!');
        location.reload();
    }).catch(error => {
        alert('Failed to save!');
        console.error(error);
    });
}
