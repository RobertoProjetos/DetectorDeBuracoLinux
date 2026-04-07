from ultralytics import YOLO
import os

if __name__ == '__main__':
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
    # Caminho para o modelo treinado (ajuste o nome conforme necessário)
    MODEL_PATH = os.path.join(BASE_DIR, "runs", "detect", "olha_buraco3", "weights", "best.pt")
    
    # Caminho para o vídeo de teste (ajuste conforme necessário)
    VIDEO_PATH = os.path.join(BASE_DIR, "videos", "video_teste.mp4")
    
    model = YOLO(MODEL_PATH)

    results = model.predict(
        source=VIDEO_PATH,
        conf=0.3,
        save=True,
        stream=True,
    )

    for result in results:
        for box in result.boxes:
            classe = result.names[int(box.cls[0])]
            confianca = round(float(box.conf[0]), 2)
            print(f"{classe}: {confianca}")
