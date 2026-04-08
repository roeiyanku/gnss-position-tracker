"""Project-level configuration values."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
DEFAULT_INPUT_DIR = DATA_DIR / "raw"
DEFAULT_OUTPUT_DIR = DATA_DIR / "interim"
