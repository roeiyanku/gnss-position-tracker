"""RINEX extraction utilities using gnss-lib-py.

This module intentionally focuses on ingestion only. Positioning/solver logic
will be added in later steps.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

from .config import DEFAULT_INPUT_DIR, DEFAULT_OUTPUT_DIR


RINEX_SUFFIXES = {".o", ".obs", ".26o", ".rnx"}


def _load_rinex_with_gnss_lib_py(rinex_path: Path) -> Any:
    """Load a RINEX observation file via gnss-lib-py.

    The package API can vary slightly by version, so we try both common import
    locations for the `RinexObs` parser.
    """
    try:
        import gnss_lib_py as glp

        rinex_cls = getattr(glp, "RinexObs", None)
        if rinex_cls is not None:
            return rinex_cls(str(rinex_path))
    except ImportError as exc:
        raise RuntimeError(
            "gnss-lib-py is not installed. Install dependencies and retry."
        ) from exc

    try:
        from gnss_lib_py.parsers.rinex_obs import RinexObs

        return RinexObs(str(rinex_path))
    except ImportError as exc:
        raise RuntimeError(
            "Unable to locate RinexObs parser in gnss-lib-py."
        ) from exc


def _navdata_to_dataframe(navdata: Any) -> pd.DataFrame:
    """Convert gnss-lib-py NavData-like object to pandas DataFrame."""
    if isinstance(navdata, pd.DataFrame):
        return navdata

    for method_name in ("pandas_df", "to_pandas", "as_df"):
        method = getattr(navdata, method_name, None)
        if callable(method):
            df = method()
            if isinstance(df, pd.DataFrame):
                return df

    # Last-resort attempt: map-like object
    if isinstance(navdata, dict):
        return pd.DataFrame(navdata)

    raise TypeError(
        "Could not convert parsed RINEX data to DataFrame. "
        "Expected a gnss-lib-py NavData-compatible object."
    )


def extract_single_file(rinex_path: Path, output_dir: Path) -> tuple[Path, Path]:
    """Extract one RINEX file and write CSV + summary JSON."""
    output_dir.mkdir(parents=True, exist_ok=True)

    navdata = _load_rinex_with_gnss_lib_py(rinex_path)
    df = _navdata_to_dataframe(navdata)

    stem = rinex_path.stem
    csv_path = output_dir / f"{stem}_obs.csv"
    summary_path = output_dir / f"{stem}_summary.json"

    df.to_csv(csv_path, index=False)

    summary = {
        "source_file": str(rinex_path),
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "column_names": list(df.columns),
    }
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    return csv_path, summary_path


def extract_directory(
    input_dir: Path = DEFAULT_INPUT_DIR,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
) -> list[tuple[Path, Path]]:
    """Extract all supported RINEX files from a directory."""
    if not input_dir.exists():
        raise FileNotFoundError(f"Input directory not found: {input_dir}")

    rinex_files = sorted(
        f
        for f in input_dir.iterdir()
        if f.is_file() and (f.suffix.lower() in RINEX_SUFFIXES or f.name.lower().endswith(".26o"))
    )

    outputs: list[tuple[Path, Path]] = []
    for rinex_file in rinex_files:
        outputs.append(extract_single_file(rinex_file, output_dir))

    return outputs
