import cv2
from deepface import DeepFace 
import numpy as np
import os


def cosine_distance(a, b):
    a = np.array(a)
    b = np.array(b)
    numerator = np.dot(a, b)
    denominator = np.linalg.norm(a) * np.linalg.norm(b)
    if denominator == 0:
        return 1.0  # máxima distância se um vetor for zero
    else:
        return 1 - (numerator / denominator)  # distância coseno

# Inicializa a captura de vídeo da webcam
cap = cv2.VideoCapture(1)

# Lista de usuários registrados com caminho da imagem e nível de acesso
users = [
    {
        "name": "Vitor",
        "img_path": "C:/Users/User/APS-6-SEMESTRE/fotos/Vitor.jpg",
        "access_level": 1
    }
]

# Gera embeddings para cada usuário da lista
def preparar_usuarios():
    registrados = []
    print("Carregando usuários...")
    for user in users:
        try:
            img = cv2.imread(user["img_path"])
            if img is None:
                print(f"Imagem não encontrada: {user['img_path']}")
                continue

            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            embedding = DeepFace.represent(
                img_rgb,
                model_name="Facenet512",
                detector_backend="mtcnn",
                enforce_detection=False
            )[0]["embedding"]

            user["embedding"] = embedding
            registrados.append(user)
            print(f" - {user['name']} (Nivel {user['access_level']}) carregado.")
        except Exception as e:
            print(f"Erro ao carregar {user['name']}: {e}")
    return registrados

# Carregar os usuários na memória
usuarios_registrados = preparar_usuarios()

if not usuarios_registrados:
    print("Nenhum usuário carregado. Encerrando.")
    exit()

# Variáveis globais
detected_user = None
confidence = 0.0
counter = 0

# Verificação da face capturada
def check_face(frame):
    global detected_user, confidence
    try:
        # Gera embedding da imagem ao vivo
        embedding_obj = DeepFace.represent(
            frame,
            model_name="Facenet512",
            detector_backend="mtcnn",
            enforce_detection=False
        )

        if not embedding_obj:
            detected_user = None
            confidence = 0.0
            return

        frame_embedding = embedding_obj[0]["embedding"]

        # Inicializa distância mínima
        min_dist = float("inf")
        best_match = None

        for user in usuarios_registrados:
            dist = cosine_distance(frame_embedding, user["embedding"])
            if dist < min_dist:
                min_dist = dist
                best_match = user


        # Threshold
        threshold = 0.7
        if min_dist <= threshold:
            detected_user = best_match
            confidence = max(0, min(1, (threshold - min_dist) / threshold))
        else:
            detected_user = None
            confidence = 0.0

    except Exception as e:
        print("Erro ao verificar rosto:", e)
        detected_user = None
        confidence = 0.0

# Loop principal da câmera
while True:
    ret, frame = cap.read()
    if not ret:
        print("Erro ao capturar a webcam.")
        break

    if counter % 15 == 0:
        check_face(frame.copy())
    counter += 1

    # Texto a exibir
    if detected_user:
        nome = detected_user["name"]
        nivel = detected_user["access_level"]
        texto = f"Acesso Nivel {nivel}: {nome} ({confidence:.2%})"
        color = (0, 255, 0)
    else:
        texto = f"Acesso Negado ({confidence:.2%})"
        color = (0, 0, 255)

    cv2.putText(frame, texto, (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
    cv2.imshow("Reconhecimento Facial", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
