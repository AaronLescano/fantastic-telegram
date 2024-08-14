let allPlayers = []; // Variable para almacenar todos los jugadores

document.addEventListener('DOMContentLoaded', loadPlayers);

function loadPlayers() {
    fetch('http://127.0.0.1:5000/players')
        .then(response => response.json())
        .then(data => {
            allPlayers = data.players; // Guardar todos los jugadores en la variable allPlayers
            displayPlayers(allPlayers); // Mostrar todos los jugadores
        });
}

function displayPlayers(players) {
    const tableBody = document.querySelector('#playersTable tbody');
    tableBody.innerHTML = ''; // Limpiar la tabla

    const goalsData = [];
    const assistsData = [];

    players.forEach(player => {
        const row = document.createElement('tr');

        row.innerHTML = `
            <td>${player.id}</td>
            <td>${player.name}</td>
            <td>${player.team}</td>
            <td>${player.position}</td>
            <td>${player.games_played}</td>
            <td>${player.goals}</td>
            <td>${player.assists}</td>
            <td>${player.yellow_cards}</td>
            <td>${player.red_cards}</td>
        `;
        tableBody.appendChild(row);

        // Agregar datos para gráficos de barras
        goalsData.push({name: player.name, value: player.goals});
        assistsData.push({name: player.name, value: player.assists});
    });

    // Crear gráficos de barras
    createBarChart('goalsBarChart', 'Goles', goalsData, 'rgba(75, 192, 192, 0.2)');
    createBarChart('assistsBarChart', 'Asistencias', assistsData, 'rgba(153, 102, 255, 0.2)');
}

// Función para obtener y mostrar el promedio de goles por partido
function getAverageGoals() {
    const playerId = document.getElementById('playerId').value;
    fetch(`http://127.0.0.1:5000/average_goals_per_game/${playerId}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('results').textContent = data.interpretation;
        });
}

// Función para obtener y mostrar el promedio de asistencias por partido
function getAverageAssists() {
    const playerId = document.getElementById('playerId').value;
    fetch(`http://127.0.0.1:5000/average_assists_per_game/${playerId}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('results').textContent = data.interpretation;
        });
}

// Función para obtener y mostrar el porcentaje de goles del equipo
function getGoalPercentage() {
    const playerId = document.getElementById('playerId').value;
    fetch(`http://127.0.0.1:5000/goal_percentage/${playerId}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('results').textContent = data.interpretation;
        });
}

// Función para obtener y mostrar el ratio de tarjetas por partido
function getCardRatio() {
    const playerId = document.getElementById('playerId').value;
    fetch(`http://127.0.0.1:5000/card_ratio/${playerId}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('results').textContent = data.interpretation;
        });
}

// Función para crear un gráfico de barras
function createBarChart(chartId, label, data, backgroundColor) {
    const ctx = document.getElementById(chartId).getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.map(player => player.name),
            datasets: [{
                label: label,
                data: data.map(player => player.value),
                backgroundColor: backgroundColor
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

// Función para filtrar jugadores por posición
function filterPlayers() {
    const position = document.getElementById('positionFilter').value;
    const filteredPlayers = position ? allPlayers.filter(player => player.position === position) : allPlayers;
    displayPlayers(filteredPlayers); // Mostrar solo los jugadores filtrados
}

// Función para ordenar jugadores por atributo
function sortPlayers(attribute) {
    const sortedPlayers = [...allPlayers].sort((a, b) => b[attribute] - a[attribute]);
    displayPlayers(sortedPlayers); // Mostrar los jugadores ordenados
}

// Función para alternar el modo oscuro
function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    document.querySelector('table').classList.toggle('dark-mode');
    document.querySelectorAll('button').forEach(button => {
        button.classList.toggle('dark-mode');
    });
}

// Función para buscar jugadores por nombre
function searchPlayers() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const filteredPlayers = allPlayers.filter(player => player.name.toLowerCase().includes(searchTerm));
    displayPlayers(filteredPlayers);
}
function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    document.querySelector('table').classList.toggle('dark-mode');
    document.querySelectorAll('button').forEach(button => {
        button.classList.toggle('dark-mode');
    });
}
