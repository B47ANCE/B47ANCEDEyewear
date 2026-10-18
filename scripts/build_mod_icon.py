"""Export the selected transparent authoring master at the existing 64px mod-icon size."""
from pathlib import Path
import hashlib
import json
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / 'assets/branding/Eyewear_Icon_Transparent.png'
TARGET = ROOT / 'src/B47ANCEDEyewear/42/media/ui/B47ANCEDEyewear_icon.png'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    with Image.open(MASTER) as image:
        if image.mode != 'RGBA' or image.getchannel('A').getextrema() != (0, 255):
            raise ValueError('The selected master must have true transparent alpha')
        exported = image.resize((64, 64), Image.Resampling.LANCZOS)
        exported.save(TARGET)
        size = list(image.size)
    manifest = {
        'project_version': (ROOT / 'VERSION').read_text().strip(),
        'selection_date': '2026-10-18',
        'master': MASTER.relative_to(ROOT).as_posix(),
        'master_sha256': sha(MASTER),
        'master_dimensions': size,
        'runtime': TARGET.relative_to(ROOT).as_posix(),
        'runtime_sha256': sha(TARGET),
        'runtime_dimensions': [64, 64],
        'mode': 'RGBA',
        'export': 'Pillow LANCZOS resize; preserve alpha; no fill, crop or redraw',
        'thumbnail_sha256': sha(ROOT / 'thumbnail.png'),
        'poster_sha256': sha(ROOT / 'src/B47ANCEDEyewear/42/poster.png'),
        'provenance': 'User selected a built-in image-generation cutout of the existing thumbnail; original prompt retained beside master.',
    }
    (ROOT / 'assets/branding/mod-icon.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    print('Exported transparent 64x64 RGBA mod icon; thumbnail and poster read only.')


if __name__ == '__main__':
    main()
