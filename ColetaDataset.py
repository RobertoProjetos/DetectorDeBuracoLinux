import cv2
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Configurar caminhos do video fonte e diretório de saída
VIDEO_PATH = os.path.join(BASE_DIR, "videos", "video_teste.mp4")
OUTPUT_DIR = os.path.join(BASE_DIR, "dataset_novo", "images", "train")
INTERVALO = 10  # coleta 1 imagem a cada 10 frames

# Tratamento caso eu tenha esquecido de colocar o vídeo ou o caminho esteja errado
if not os.path.exists(VIDEO_PATH):
    print(f" Erro: Vídeo não encontrado em: {VIDEO_PATH}")
    print(f"Por favor, coloque o vídeo na pasta 'videos' ou ajuste o caminho.")
    sys.exit(1)

os.makedirs(OUTPUT_DIR, exist_ok=True)

cap = cv2.VideoCapture(VIDEO_PATH)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = cap.get(cv2.CAP_PROP_FPS)

print(f"Total de frames: {total_frames} | FPS: {fps}")

frame_num = 0
salvo = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    if frame_num % INTERVALO == 0:
        nome = os.path.join(OUTPUT_DIR, f"frame_{frame_num:05d}.jpg")
        cv2.imwrite(nome, frame)
        salvo += 1
        print(f"Salvo: {nome}")

    frame_num += 1

cap.release()
print(f"\n Total de frames extraídos: {salvo}")
print(f" Salvos em: {OUTPUT_DIR}")