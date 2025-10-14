// static/js/logs.js

let allLogs = [];
let filteredLogs = [];

// Carrega logs
function loadLogs() {
    fetch('/api/logs')
        .then(res => res.json())
        .then(logs => {
            allLogs = logs.reverse(); // Mais recentes primeiro
            filteredLogs = allLogs;
            renderLogs();
        })
        .catch(err => console.error('Erro ao carregar logs:', err));
}

// Renderiza logs na tabela
function renderLogs() {
    const logsTable = document.getElementById('logs-table');
    
    if (filteredLogs.length === 0) {
        logsTable.innerHTML = '<tr><td colspan="5" class="empty-state">Nenhum log encontrado</td></tr>';
        return;
    }
    
    logsTable.innerHTML = filteredLogs.map(log => `
        <tr>
            <td>${log.timestamp}</td>
            <td>
                <strong>${log.user}</strong>
            </td>
            <td>
                <span class="level-badge level-${log.access_level}">${log.access_level}</span>
            </td>
            <td>
                <span class="status-badge status-${log.status === 'AUTORIZADO' ? 'authorized' : 'denied'}">
                    ${log.status}
                </span>
            </td>
            <td>${log.confidence}</td>
        </tr>
    `).join('');
}

// Filtra logs por status
function filterByStatus(status) {
    if (status === 'all') {
        filteredLogs = allLogs;
    } else {
        filteredLogs = allLogs.filter(log => log.status === status);
    }
    renderLogs();
}

// Busca logs por nome
function searchLogs(query) {
    if (!query) {
        filteredLogs = allLogs;
    } else {
        filteredLogs = allLogs.filter(log => 
            log.user.toLowerCase().includes(query.toLowerCase())
        );
    }
    renderLogs();
}

// Event listeners
document.getElementById('filter-status').addEventListener('change', (e) => {
    filterByStatus(e.target.value);
});

document.getElementById('search-logs').addEventListener('input', (e) => {
    searchLogs(e.target.value);
});

document.getElementById("clearLogsBtn").addEventListener("click", async () => {
    if(!confirm("Tem certeza que deseja apagar todos os logs?")) return;

    const response = await fetch("/api/logs", { method: "DELETE" });
    const data = await response.json();

    alert(data.message);

    // Atualiza tabela de logs após apagar
    if(data.success) {
        loadLogs(); // sua função que recarrega os logs
    }
});


// Carrega logs ao inicializar
loadLogs();

// Atualiza a cada 5 segundos
setInterval(loadLogs, 5000);