from ultralytics import YOLO
import os
import cv2

if __name__ == '__main__':
    model_path = os.environ.get("MODEL_PATH", "runs/detect/olha_buraco/weights/best.pt")
    video_path = os.environ.get("VIDEO_PATH", "videos/video_teste.mp4")
    crops_dir  = os.environ.get("CROPS_DIR", "deteccoes")

    os.makedirs(crops_dir, exist_ok=True)
    contadores = {}  # classe -> quantidade já salva

    model = YOLO(model_path)

    results = model.predict(
        source=video_path,
        conf=float(os.environ.get("CONFIANCA", 0.3)),
        save=True,
        stream=True,
    )

    for result in results:
        img = result.orig_img
        for box in result.boxes:
            classe = result.names[int(box.cls[0])]
            confianca = round(float(box.conf[0]), 2)
            print(f"{classe}: {confianca}")

            # Salva crop com nome incremental por classe
            contadores[classe] = contadores.get(classe, 0) + 1
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            crop = img[y1:y2, x1:x2]
            if crop.size > 0:
                nome = os.path.join(crops_dir, f"{classe}{contadores[classe]}.png")
                cv2.imwrite(nome, crop)
                print(f"  → Salvo: {nome}")
