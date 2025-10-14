// static/js/users.js

let stream = null;
let capturedPhoto = null;

// Inicia a câmera
async function startCamera() {
    try {
        const video = document.getElementById('camera');
        stream = await navigator.mediaDevices.getUserMedia({ 
            video: { width: 640, height: 480 } 
        });
        video.srcObject = stream;
        video.style.display = 'block';
    } catch (err) {
        alert('Erro ao acessar câmera: ' + err.message);
    }
}

// Captura foto da câmera
function capturePhoto() {
    const video = document.getElementById('camera');
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');
    const preview = document.getElementById('photo-preview');
    const previewImg = document.getElementById('preview-img');
    
    if (!stream) {
        alert('Por favor, ative a câmera primeiro!');
        return;
    }
    
    // Define tamanho do canvas
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    
    // Captura frame
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    
    // Converte para base64
    capturedPhoto = canvas.toDataURL('image/jpeg');
    
    // Mostra preview
    previewImg.src = capturedPhoto;
    preview.style.display = 'block';
    
    // Para a câmera
    stopCamera();
}

// Para a câmera
function stopCamera() {
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
        stream = null;
        document.getElementById('camera').style.display = 'none';
    }
}

// Cadastra usuário
document.getElementById('user-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const name = document.getElementById('user-name').value;
    const level = document.getElementById('user-level').value;
    
    if (!capturedPhoto) {
        alert('Por favor, capture uma foto primeiro!');
        return;
    }
    
    try {
        const response = await fetch('/api/users', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: name,
                access_level: level,
                photo: capturedPhoto
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            alert(result.message);
            
            // Limpa formulário
            document.getElementById('user-form').reset();
            document.getElementById('photo-preview').style.display = 'none';
            capturedPhoto = null;
            
            // Recarrega lista
            loadUsers();
        } else {
            alert('Erro: ' + result.message);
        }
    } catch (err) {
        alert('Erro ao cadastrar usuário: ' + err.message);
    }
});

// Carrega lista de usuários
function loadUsers() {
    fetch('/api/users')
        .then(res => res.json())
        .then(users => {
            const usersList = document.getElementById('users-list');
            
            if (users.length === 0) {
                usersList.innerHTML = '<p class="empty-state">Nenhum usuário cadastrado</p>';
                return;
            }
            
            usersList.innerHTML = users.map(user => `
                <div class="user-item">
                    <div class="user-info">
                        <span class="level-badge level-${user.access_level}">${user.access_level}</span>
                        <div>
                            <strong>${user.name}</strong>
                            <div style="font-size: 0.85rem; color: #6b7280;">
                                Cadastrado em: ${user.created_at}
                            </div>
                        </div>
                    </div>
                    <button class="btn-danger" onclick="deleteUser('${user.name}')">
                        🗑️ Remover
                    </button>
                </div>
            `).join('');
        })
        .catch(err => console.error('Erro ao carregar usuários:', err));
}

// Remove usuário
async function deleteUser(name) {
    if (!confirm(`Tem certeza que deseja remover ${name}?`)) {
        return;
    }
    
    try {
        const response = await fetch(`/api/users?name=${encodeURIComponent(name)}`, {
            method: 'DELETE'
        });
        
        const result = await response.json();
        
        if (result.success) {
            alert(result.message);
            loadUsers();
        } else {
            alert('Erro: ' + result.message);
        }
    } catch (err) {
        alert('Erro ao remover usuário: ' + err.message);
    }
}

// Recarrega embeddings manualmente
async function reloadEmbeddings() {
    if (!confirm('Isso vai recarregar todos os embeddings. Continuar?')) {
        return;
    }
    
    try {
        const button = event.target;
        button.disabled = true;
        button.textContent = '⏳ Recarregando...';
        
        const response = await fetch('/api/reload', {
            method: 'POST'
        });
        
        const result = await response.json();
        
        if (result.success) {
            alert('✅ ' + result.message);
        } else {
            alert('❌ ' + result.message);
        }
        
        button.disabled = false;
        button.textContent = '🔄 Recarregar Sistema';
    } catch (err) {
        alert('Erro ao recarregar: ' + err.message);
        event.target.disabled = false;
        event.target.textContent = '🔄 Recarregar Sistema';
    }
}

// Carrega usuários ao inicializar
loadUsers();