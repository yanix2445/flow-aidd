"""Build a distributable plugin ZIP outside its source repository, without installing."""
import argparse
import io
import json
from pathlib import Path
import zipfile

from _paths import ROOT

SOURCES = ['.codex-plugin/plugin.json', '.agents/plugins/marketplace.json', 'skills', 'hooks', 'README.md', 'docs']


def package(output):
    output = Path(output).expanduser().resolve()
    if output.is_relative_to(ROOT):
        raise ValueError('Choisir une archive hors du dépôt, sans nouvelle copie de distribution interne.')
    manifest = json.loads((ROOT / '.codex-plugin/plugin.json').read_text())
    references = [manifest['extensions']['com.openai']['onboardingSkill'], manifest['hooks'],
                  manifest['interface']['composerIcon'], manifest['interface']['logo']]
    for reference in references:
        path = (ROOT / reference).resolve()
        if not path.is_relative_to(ROOT) or not path.is_file():
            raise ValueError('Ressource du manifeste absente ou hors paquet : ' + reference)
    files = []
    for name in SOURCES:
        source = ROOT / name
        for file in sorted(source.rglob('*')) if source.is_dir() else [source]:
            if file.is_symlink():
                raise ValueError('Ressource symbolique à résoudre avant distribution : ' + str(file))
            if file.is_file() and '__pycache__' not in file.parts and file.suffix != '.pyc':
                files.append(file)
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as archive:
        for file in files:
            archive.write(file, file.relative_to(ROOT))
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('xb') as stream:
        stream.write(buffer.getvalue())
    return {'archive': str(output), 'version': manifest['version'], 'files': len(files), 'installed': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    try:
        print(json.dumps(package(args.output), ensure_ascii=False, indent=2))
    except (OSError, ValueError) as error:
        parser.exit(1, str(error) + '\n')


if __name__ == '__main__':
    main()
