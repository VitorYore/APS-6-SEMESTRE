# utils/config.py
import os

# Diretórios
PHOTOS_DIR = "fotos"
USERS_FILE = "users.json"
LOG_FILE = "access_log.json"

# Configurações de Reconhecimento Facial
THRESHOLD = 0.7  # Threshold de similaridade (0-1)
MODEL_NAME = "Facenet512"  # Modelo DeepFace
DETECTOR_BACKEND = "mtcnn"  # Detector de faces
CHECK_INTERVAL = 30  # Verifica face a cada N frames

# Configurações de Câmera
CAMERA_INDEX = 0  # 0 = webcam padrão, 1 = segunda câmera
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
CAMERA_FPS = 30

# Configurações de Logs
MAX_LOGS = 40  # Máximo de logs armazenados

# Níveis de Acesso
ACCESS_LEVELS = {
    1: {"name": "Básico", "color": "#10b981"},
    2: {"name": "Intermediário", "color": "#f59e0b"},
    3: {"name": "Total", "color": "#ef4444"}
}