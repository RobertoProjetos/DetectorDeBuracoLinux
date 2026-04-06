from ultralytics import YOLO
import torch
model = YOLO("yolov8s.pt")
model.train(
    data="/home/ccomt/desenv/DetectorDeBuraco/data.yaml",
    epochs=150,
    imgsz=640,
    batch=8,
    patience=30,
    name="olha_buraco",
    device=0 if torch.cuda.is_available() else 'cpu',
)