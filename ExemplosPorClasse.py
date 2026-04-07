import os
import cv2

LABELS_DIR  = os.environ.get("LABELS_DIR",  "train/labels")
IMAGES_DIR  = os.environ.get("IMAGES_DIR",  "train/images")
OUTPUT_DIR  = os.environ.get("EXEMPLOS_DIR", "exemplos_classes")

CLASSES = {
    0: "buraco",
    1: "remendo",
    2: "rachadura_crocodilo",
    3: "rachadura_longitudinal",
    4: "rachadura_obliqua",
    5: "rachadura_transversal",
}

os.makedirs(OUTPUT_DIR, exist_ok=True)
encontrados = {}  # classe_id -> True quando já salvou

for label_file in sorted(os.listdir(LABELS_DIR)):
    if not label_file.endswith(".txt"):
        continue
    if len(encontrados) == len(CLASSES):
        break  # já encontrou uma de cada

    img_file = label_file.replace(".txt", ".jpg")
    img_path = os.path.join(IMAGES_DIR, img_file)
    label_path = os.path.join(LABELS_DIR, label_file)

    if not os.path.exists(img_path):
        img_file = label_file.replace(".txt", ".png")
        img_path = os.path.join(IMAGES_DIR, img_file)
    if not os.path.exists(img_path):
        continue

    img = cv2.imread(img_path)
    if img is None:
        continue

    h, w = img.shape[:2]

    with open(label_path) as f:
        for linha in f:
            partes = linha.strip().split()
            if not partes:
                continue
            cls_id = int(partes[0])
            if cls_id in encontrados or cls_id not in CLASSES:
                continue

            # Coordenadas YOLO (cx, cy, bw, bh) normalizadas → pixel
            cx, cy, bw, bh = map(float, partes[1:5])
            x1 = int((cx - bw / 2) * w)
            y1 = int((cy - bh / 2) * h)
            x2 = int((cx + bw / 2) * w)
            y2 = int((cy + bh / 2) * h)

            # Garante dentro dos limites
            x1, y1 = max(0, x1), max(0, y1)
            x2, y2 = min(w, x2), min(h, y2)

            crop = img[y1:y2, x1:x2]
            if crop.size == 0:
                continue

            nome_saida = os.path.join(OUTPUT_DIR, f"{cls_id:02d}_{CLASSES[cls_id]}.jpg")
            cv2.imwrite(nome_saida, crop)
            print(f"Salvo exemplo: {nome_saida}")
            encontrados[cls_id] = True

print(f"\nTotal de classes com exemplo: {len(encontrados)}/{len(CLASSES)}")
classes_faltando = [CLASSES[i] for i in CLASSES if i not in encontrados]
if classes_faltando:
    print(f"Sem exemplo para: {classes_faltando}")