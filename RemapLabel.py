import os
import shutil

REMAP = {
    0: 2,  # Alligator crack    → rachadura crocodilo
    1: 3,  # Longitudinal crack → rachadura longitudinal
    2: 4,  # Oblique crack      → rachadura obliqua
    3: 0,  # Pothole            → buraco
    4: 1,  # Repair             → remendo
    5: 5,  # Transverse crack   → rachadura transversal
}

PASTAS = [
   "/home/ccomt/desenv/DetectorDeBuraco/train/labels",
    "/home/ccomt/desenv/DetectorDeBuraco/valid/labels",
    "/home/ccomt/desenv/DetectorDeBuraco/test/labels",
]

# Mapeamento para seus backups existentes
BACKUP_EXISTENTE = {
  "/home/ccomt/desenv/DetectorDeBuraco/train/labels": None,
    "/home/ccomt/desenv/DetectorDeBuraco/valid/labels": None,
    "/home/ccomt/desenv/DetectorDeBuraco/test/labels":  None,
}

# Verificação/criação de backups
for pasta in PASTAS:
    backup_existente = BACKUP_EXISTENTE.get(pasta)

    if backup_existente and os.path.exists(backup_existente):
        print(f" Backup já existe em: {backup_existente} — pulando criação")
    else:
        backup_novo = pasta.replace("/labels", "/labels_backup")
        if os.path.exists(pasta) and not os.path.exists(backup_novo):
            shutil.copytree(pasta, backup_novo)
            print(f" Backup criado em: {backup_novo}")

# Remapeamento
for pasta in PASTAS:
    if not os.path.exists(pasta):
        print(f" Pasta não encontrada: {pasta}")
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
                    print(f"  ID desconhecido {id_antigo} em {arquivo}")

        with open(caminho, "w") as f:
            f.write("\n".join(novas_linhas))

    print(f" Concluído: {pasta}")

print("\n Remapeamento finalizado!")