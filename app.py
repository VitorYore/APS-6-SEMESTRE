import os
# Silenciar logs do TensorFlow
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # 0=all, 1=info, 2=warning, 3=error

# Opcional: desativar otimizações oneDNN se quiser consistência
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

from flask import Flask
from routes.main import main_bp
from routes.api import api_bp
from routes.camera import camera_bp
from utils.face_recognition import preparar_usuarios


app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'

# Cria diretórios necessários
os.makedirs('fotos', exist_ok=True)
os.makedirs('static/css', exist_ok=True)
os.makedirs('static/js', exist_ok=True)

# Registra blueprints (rotas)
app.register_blueprint(main_bp)
app.register_blueprint(api_bp, url_prefix='/api')
app.register_blueprint(camera_bp)

# Inicializa sistema
print("="*60)
print("🔐 SISTEMA DE CONTROLE DE ACESSO FACIAL")
print("="*60)

# Carrega usuários ao iniciar
usuarios = preparar_usuarios()
print(f"✓ Usuários carregados: {len(usuarios)}")
print(f"✓ Servidor rodando em: http://localhost:5000")
print("="*60)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)