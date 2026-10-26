from pathlib import Path
import hashlib
import json
import shutil

root = Path(__file__).resolve().parent
archive = root / 'archive' / 'v1'
if archive.exists():
    raise SystemExit('Archive v1 déjà présente : aucune modification.')
archive.mkdir(parents=True)
copied = ['README.md','FLOW.md','ORCHESTRATION.md','SCHEMA.md','MERMAID.md','workflow.json']
moved = ['schema.json','FLOW-shadow-report.md','mermaid','scripts/build_flow.py','scripts/build_schema.py','scripts/build_mermaid.py','scripts/verify_mermaid.cjs']
manifest = {}
for name in copied + moved:
    source = root / name
    destination = archive / name
    destination.parent.mkdir(parents=True, exist_ok=True)
    if source.is_file():
        manifest[name] = hashlib.sha256(source.read_bytes()).hexdigest()
    if name in copied:
        shutil.copy2(source,destination)
    else:
        shutil.move(str(source),str(destination))
(archive / 'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
(archive / 'ARCHIVE.md').write_text('# Version 1 archivée\n\nInstantané avant la structuration par séquences. Les liens absolus de l’ancien audit désignent les chemins de son époque ; lire les fichiers présents dans cette archive pour retrouver cette version. Le modèle courant et les guides sont à la racine du projet.\n')
shutil.move(str(Path(__file__)), str(archive / 'snapshot.py'))
print('Version 1 conservée dans archive/v1 ; fichiers historiques disponibles avec empreintes SHA-256.')
