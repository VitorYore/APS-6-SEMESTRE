// static/js/monitor.js

function updateStatus() {
    fetch('/api/status')
        .then(res => res.json())
        .then(data => {
            const statusDisplay = document.getElementById('status-display');
            const statusIcon = document.getElementById('status-icon');
            const statusText = document.getElementById('status-text');
            const statusUser = document.getElementById('status-user');
            const statusConfidence = document.getElementById('status-confidence');
            
            if (data.authorized) {
                // Acesso autorizado
                statusDisplay.style.background = 'linear-gradient(135deg, #d1fae5, #a7f3d0)';
                statusIcon.textContent = '✅';
                statusText.textContent = 'ACESSO AUTORIZADO';
                statusText.style.color = '#065f46';
                statusUser.textContent = data.detected_user;
                statusUser.style.color = '#047857';
                statusConfidence.textContent = `Confiança: ${data.confidence} | Nível ${data.access_level}`;
                statusConfidence.style.color = '#059669';
            } else {
                // Acesso negado
                statusDisplay.style.background = 'linear-gradient(135deg, #fee2e2, #fecaca)';
                statusIcon.textContent = '❌';
                statusText.textContent = 'ACESSO NEGADO';
                statusText.style.color = '#991b1b';
                statusUser.textContent = 'Usuário não reconhecido';
                statusUser.style.color = '#dc2626';
                statusConfidence.textContent = 'Permissão insuficiente';
                statusConfidence.style.color = '#ef4444';
            }
        })
        .catch(err => console.error('Erro ao atualizar status:', err));
}

function loadActiveUsers() {
    fetch('/api/users')
        .then(res => res.json())
        .then(users => {
            const usersDiv = document.getElementById('active-users');
            
            if (users.length === 0) {
                usersDiv.innerHTML = '<p class="empty-state">Nenhum usuário cadastrado</p>';
                return;
            }
            
            usersDiv.innerHTML = users.map(user => `
                <div class="user-item">
                    <div class="user-info">
                        <span class="level-badge level-${user.access_level}">${user.access_level}</span>
                        <span>${user.name}</span>
                    </div>
                </div>
            `).join('');
        })
        .catch(err => console.error('Erro ao carregar usuários:', err));
}

// Para o stream de vídeo e libera a câmera
function stopCameraStream() {
    if (!confirm('⚠️ Isso vai parar o monitoramento. Deseja continuar?')) {
        return;
    }
    
    fetch('/stop_camera')
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                // Remove a imagem do stream
                const videoStream = document.getElementById('video-stream');
                videoStream.style.display = 'none';
                
                // Mostra mensagem
                const container = videoStream.parentElement;
                container.innerHTML = `
                    <div style="background: #f3f4f6; padding: 3rem; border-radius: 10px; text-align: center;">
                        <div style="font-size: 4rem; margin-bottom: 1rem;">📹</div>
                        <h3 style="color: #6b7280; margin-bottom: 1rem;">Câmera Parada</h3>
                        <p style="color: #9ca3af; margin-bottom: 1.5rem;">
                            A câmera foi liberada. Você pode cadastrar novos usuários agora.
                        </p>
                        <button onclick="location.reload()" class="btn-primary">
                            🔄 Reativar Monitor
                        </button>
                    </div>
                `;
                
                alert('✅ Câmera parada! Agora você pode cadastrar novos usuários.');
            }
        })
        .catch(err => console.error('Erro ao parar câmera:', err));
}

// Para a câmera automaticamente ao sair da página
window.addEventListener('beforeunload', () => {
    fetch('/stop_camera');
});

// Inicializa
updateStatus();
loadActiveUsers();

// Atualiza status a cada 1 segundo
setInterval(updateStatus, 1000);

// Atualiza lista de usuários a cada 5 segundos
setInterval(loadActiveUsers, 5000);