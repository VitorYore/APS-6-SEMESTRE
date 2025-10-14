// static/js/dashboard.js

function loadStats() {
    fetch('/api/stats')
        .then(res => res.json())
        .then(data => {
            document.getElementById('total-users').textContent = data.users_registered;
            document.getElementById('total-authorized').textContent = data.authorized;
            document.getElementById('total-denied').textContent = data.denied;
            document.getElementById('total-attempts').textContent = data.total_attempts;
        })
        .catch(err => console.error('Erro ao carregar estatísticas:', err));
}

function loadRecentLogs() {
    fetch('/api/logs')
        .then(res => res.json())
        .then(logs => {
            const logsDiv = document.getElementById('recent-logs');
            
            if (logs.length === 0) {
                logsDiv.innerHTML = '<p class="empty-state">Nenhum registro ainda</p>';
                return;
            }
            
            logsDiv.innerHTML = logs.slice(-10).reverse().map(log => `
                <div class="log-item">
                    <div class="log-info">
                        <strong>${log.user}</strong>
                        <span class="log-time">${log.timestamp}</span>
                    </div>
                    <div>
                        <span class="level-badge level-${log.access_level}">${log.access_level}</span>
                        <span class="status-badge status-${log.status === 'AUTORIZADO' ? 'authorized' : 'denied'}" 
                              style="margin-left: 1rem;">
                            ${log.status}
                        </span>
                    </div>
                </div>
            `).join('');
        })
        .catch(err => console.error('Erro ao carregar logs:', err));
}

// Carrega dados ao inicializar
loadStats();
loadRecentLogs();

// Atualiza a cada 3 segundos
setInterval(() => {
    loadStats();
    loadRecentLogs();
}, 3000);