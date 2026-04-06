from ultralytics import YOLO

if __name__ == '__main__':
    model = YOLO("runs/detect/olha_buraco3/weights/best.pt")

    results = model.predict(
        source="/home/ccomt/desenv/DetectorDeBuraco/videos/video_teste.mp4",
        conf=0.3,
        save=True,
        stream=True,
    )

    for result in results:
        for box in result.boxes:
            classe = result.names[int(box.cls[0])]
            confianca = round(float(box.conf[0]), 2)
            print(f"{classe}: {confianca}")
