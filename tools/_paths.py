"""Find the plugin's single runtime; development tools never copy it."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / 'skills' / 'flow-aidd'
MODEL_ROOT = SKILL_ROOT / 'references'
sys.path.insert(0, str(SKILL_ROOT / 'scripts'))
