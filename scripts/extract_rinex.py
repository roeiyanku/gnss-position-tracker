#!/usr/bin/env python3
"""CLI for extracting RINEX observations with gnss-lib-py."""

from __future__ import annotations

import argparse
from pathlib import Path

from gnss_position_tracker.config import DEFAULT_INPUT_DIR, DEFAULT_OUTPUT_DIR
from gnss_position_tracker.rinex_extractor import extract_directory


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Extract RINEX observation files to tabular CSV outputs."
    )
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=DEFAULT_INPUT_DIR,
        help=f"Directory containing RINEX files (default: {DEFAULT_INPUT_DIR})",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Directory for extracted outputs (default: {DEFAULT_OUTPUT_DIR})",
    )

    args = parser.parse_args()
    results = extract_directory(args.input_dir, args.output_dir)

    if not results:
        print(f"No RINEX files found in {args.input_dir}")
        return 0

    print("Extraction complete:")
    for csv_path, summary_path in results:
        print(f" - {csv_path}")
        print(f" - {summary_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
