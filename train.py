from ultralytics import YOLO
import torch
import os

# Caminho relativo ao diretório do script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_YAML = os.path.join(BASE_DIR, "data.yaml")

model = YOLO("yolov8s.pt")
model.train(
    data=DATA_YAML,
    epochs=150,
    imgsz=640,
    batch=8,
    patience=30,
    name="olha_buraco",
    device=0 if torch.cuda.is_available() else 'cpu',
)