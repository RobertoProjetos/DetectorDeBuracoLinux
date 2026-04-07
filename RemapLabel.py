import os
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

REMAP = {
    0: 2,  # Alligator crack    → rachadura crocodilo
    1: 3,  # Longitudinal crack → rachadura longitudinal
    2: 4,  # Oblique crack      → rachadura obliqua
    3: 0,  # Pothole            → buraco
    4: 1,  # Repair             → remendo
    5: 5,  # Transverse crack   → rachadura transversal
}

PASTAS = [
    os.path.join(BASE_DIR, "train", "labels"),
    os.path.join(BASE_DIR, "valid", "labels"),
    os.path.join(BASE_DIR, "test", "labels"),
]

BACKUP_EXISTENTE = {
    os.path.join(BASE_DIR, "train", "labels"): None,
    os.path.join(BASE_DIR, "valid", "labels"): None,
    os.path.join(BASE_DIR, "test", "labels"): None,
}

for pasta in PASTAS:
    backup_existente = BACKUP_EXISTENTE.get(pasta)

    if backup_existente and os.path.exists(backup_existente):
        print(f"Backup já existe em: {backup_existente} — pulando criação")
    else:
        pasta_pai = os.path.dirname(pasta)
        backup_novo = os.path.join(pasta_pai, "labels_backup")
        if os.path.exists(pasta) and not os.path.exists(backup_novo):
            shutil.copytree(pasta, backup_novo)
            print(f"Backup criado em: {backup_novo}")

# Remapeamento
for pasta in PASTAS:
    if not os.path.exists(pasta):
        print(f"Pasta não encontrada: {pasta}")
        continue

    arquivos = [f for f in os.listdir(pasta) if f.endswith(".txt")]
    print(f"\n Processando {len(arquivos)} arquivos em: {pasta}")

    for arquivo in arquivos:
        caminho = os.path.join(pasta, arquivo)
        novas_linhas = []

        with open(caminho, "r") as f:
            for linha in f.readlines():
                partes = linha.strip().split()
                if not partes:
                    continue

                id_antigo = int(partes[0])
                id_novo = REMAP.get(id_antigo)

                if id_novo is not None:
                    partes[0] = str(id_novo)
                    novas_linhas.append(" ".join(partes))
                else:
                    print(f" ID desconhecido {id_antigo} em {arquivo}")

        with open(caminho, "w") as f:
            f.write("\n".join(novas_linhas))

    print(f"Concluído: {pasta}")

print("\n Remapeamento finalizado!")