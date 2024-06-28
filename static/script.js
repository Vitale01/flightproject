document.getElementById('yearForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const startYear = document.getElementById('startYear').value;
    const endYear = document.getElementById('endYear').value;

    fetch(`/api/frequent-flights?start_year=${startYear}&end_year=${endYear}`)
        .then(response => response.json())
        .then(data => {
            const tableBody = document.querySelector('#resultsTable tbody');
            tableBody.innerHTML = '';  // Svuota la tabella
            data.forEach(flight => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${flight.destination}</td>
                    <td>${flight.count}</td>
                `;
                tableBody.appendChild(row);
            });
        });
});
