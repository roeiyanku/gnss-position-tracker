from pathlib import Path

from gnss_position_tracker.config import DEFAULT_INPUT_DIR


def test_raw_data_directory_exists() -> None:
    assert Path(DEFAULT_INPUT_DIR).exists()
