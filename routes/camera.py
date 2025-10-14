# routes/camera.py
from flask import Blueprint, Response, jsonify
import cv2
import time
from utils.face_recognition import check_face, detected_user, confidence
from utils.config import CAMERA_INDEX, CHECK_INTERVAL

camera_bp = Blueprint('camera', __name__)

# Variáveis globais
cap = None
camera_active = False
counter = 0
last_check_time = 0

def generate_frames():
    """Gerador de frames para streaming de vídeo"""
    global cap, counter, camera_active, last_check_time
    
    if cap is None or not cap.isOpened():
        cap = cv2.VideoCapture(CAMERA_INDEX)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        cap.set(cv2.CAP_PROP_FPS, 30) # 30 FPS pra fluidez
        
    
    camera_active = True
    
    while camera_active:
        ret, frame = cap.read()
        if not ret:
            break

        current_time = time.time()
        
        # Verifica face a cada CHECK_INTERVAL frames OU a cada 1 segundo (o que acontecer primeiro)
        # =========  AQUSIÇÃO E PRÉ-PROCESSAMENTO ============
        if counter % CHECK_INTERVAL == 0 or (time.time() - last_check_time) > 1.5:
            # Reduz a imagem antes de enviar pro DeepFace
            small_frame = cv2.resize(frame, (160, 120))
            check_face(small_frame)
            last_check_time = time.time()
        
        counter += 1


        # Adiciona texto ao frame
        from utils.face_recognition import detected_user, confidence
        
        if detected_user:
            nome = detected_user["name"]
            nivel = detected_user["access_level"]
            texto = f"ACESSO AUTORIZADO - Nivel {nivel}: {nome} ({confidence:.0%})"
            color = (0, 255, 0)
            
            # Adiciona retângulo de fundo para melhor legibilidade
            cv2.rectangle(frame, (10, 5), (630, 45), (0, 0, 0), -1)
        else:
            texto = "ACESSO NEGADO - Usuario nao reconhecido"
            color = (0, 0, 255)
            
            # Adiciona retângulo de fundo
            cv2.rectangle(frame, (10, 5), (630, 45), (0, 0, 0), -1)

        cv2.putText(frame, texto, (20, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        
        # Adiciona indicador de verificação ativa
        if counter % CHECK_INTERVAL == 0:
            cv2.circle(frame, (620, 460), 10, (0, 255, 0), -1)  # Bolinha verde quando verifica
        
        # Converte para JPEG
        ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
        frame = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@camera_bp.route('/video_feed')
def video_feed():
    """Stream de vídeo"""
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@camera_bp.route('/stop_camera')
def stop_camera():
    """Para a câmera"""
    global camera_active, cap
    camera_active = False
    if cap:
        cap.release()
        cap = None
    return jsonify({'success': True, 'message': 'Câmera liberada'})