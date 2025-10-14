# utils/face_recognition.py
import cv2
from deepface import DeepFace
import numpy as np
import os
from datetime import datetime
from utils.database import load_users, save_log
from utils.config import (
    PHOTOS_DIR, THRESHOLD, MODEL_NAME, 
    DETECTOR_BACKEND, CHECK_INTERVAL
)

# Variáveis globais
usuarios_registrados = []
detected_user = None
confidence = 0.0
counter = 0


def cosine_distance(a, b):
    """Calcula distância coseno entre dois vetores"""
    a = np.array(a)
    b = np.array(b)
    numerator = np.dot(a, b)
    denominator = np.linalg.norm(a) * np.linalg.norm(b)
    
    if denominator == 0:
        return 1.0
    else:
        return 1 - (numerator / denominator)

def preparar_usuarios():
    """Gera embeddings para usuários registrados"""
    global usuarios_registrados
    
    users = load_users()
    registrados = []
    
    print("\n📥 Carregando usuários...")
    for user in users:
        try:
            img_path = os.path.join(PHOTOS_DIR, user["img_filename"])
            img = cv2.imread(img_path)
            
            if img is None:
                print(f"   ⚠️  Imagem não encontrada: {img_path}")
                continue

            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            embedding = DeepFace.represent(
                img_rgb,
                model_name=MODEL_NAME,
                detector_backend=DETECTOR_BACKEND,
                enforce_detection=False
            )[0]["embedding"] # type: ignore

            user["embedding"] = embedding
            registrados.append(user)
            print(f"   ✓ {user['name']} (Nível {user['access_level']})")
            
        except Exception as e:
            print(f"   ❌ Erro ao carregar {user['name']}: {e}")
    
    usuarios_registrados = registrados
    return registrados

def check_face(frame):
    """Verifica face capturada contra usuários registrados"""
    global detected_user, confidence
    
    try:
        # 🔹 Aquisição e pré-processamento já feitos na câmera
        # 🔹 Segmentação e extração de características (feito pelo DeepFace internamente)
        embedding_obj = DeepFace.represent(
            frame,
            model_name=MODEL_NAME,
            detector_backend=DETECTOR_BACKEND,
            enforce_detection=False
        )

        if not embedding_obj:
            detected_user = None
            confidence = 0.0
            return

        frame_embedding = embedding_obj[0]["embedding"] # type: ignore
        min_dist = float("inf")
        best_match = None
        

        # Compara com todos os usuários registrados
        for user in usuarios_registrados:
            dist = cosine_distance(frame_embedding, user["embedding"])
            if dist < min_dist:
                min_dist = dist
                best_match = user

        # Verifica threshold
        if min_dist <= THRESHOLD and best_match is not None:
            # AUTORIZADO!!!
            detected_user = best_match
            confidence = max(0, min(1, (THRESHOLD - min_dist) / THRESHOLD))
            
            # Log de acesso autorizado
            save_log({
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "user": best_match["name"],
                "access_level": best_match["access_level"],
                "status": "AUTORIZADO",
                "confidence": f"{confidence:.2%}"
            })
        else:
            # Log de acesso negado apenas se detectou um rosto
            if min_dist < 0.9:  # Detectou alguém mas não passou no threshold
                save_log({
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "user": "Desconhecido",
                    "access_level": 0,
                    "status": "NEGADO",
                    "confidence": "N/A"
                })
            
            detected_user = None
            confidence = 0.0

    except Exception as e:
        print(f"❌ Erro ao verificar rosto: {e}")
        detected_user = None
        confidence = 0.0

def get_current_status():
    """Retorna status atual do sistema"""
    return {
        'detected_user': detected_user['name'] if detected_user else None,
        'access_level': detected_user['access_level'] if detected_user else 0,
        'confidence': f"{confidence:.0%}",
        'authorized': detected_user is not None,
        'total_users': len(usuarios_registrados)
    }

def reload_users():
    """Recarrega usuários (útil após adicionar novo usuário para não dar erro na detecção)"""
    return preparar_usuarios()