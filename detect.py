from ultralytics import YOLO
import os

if __name__ == '__main__':
    model_path = os.environ.get("MODEL_PATH", "runs/detect/olha_buraco/weights/best.pt")
    video_path = os.environ.get("VIDEO_PATH", "videos/video_teste.mp4")

    model = YOLO(model_path)

    results = model.predict(
        source=video_path,
        conf=float(os.environ.get("CONFIANCA", 0.3)),
        save=True,
        stream=True,
    )

    for result in results:
        for box in result.boxes:
            classe = result.names[int(box.cls[0])]
            confianca = round(float(box.conf[0]), 2)
            print(f"{classe}: {confianca}")
