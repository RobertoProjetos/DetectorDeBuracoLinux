from ultralytics import YOLO
import torch
import os

if __name__ == '__main__':
    model = YOLO("yolov8s.pt")

    model.train(
        data=os.environ.get("DATA_YAML", "data.yaml"),
        epochs=int(os.environ.get("EPOCHS", 150)),
        imgsz=640,
        batch=8,
        patience=30,
        name="olha_buraco",
        device=0 if torch.cuda.is_available() else 'cpu',
    )