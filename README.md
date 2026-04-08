# GNSS Position Tracker

This repository now contains the **project architecture and data-ingestion stage** for your assignment.

> Scope of this step: ingest and extract RINEX observations with `gnss-lib-py`.
> 
> Not implemented yet: pseudorange-based positioning algorithm and path estimation logic.

## Current architecture

```text
.
├── data/
│   ├── raw/                    # Input .26o/.obs RINEX files (already present)
│   ├── interim/                # Extracted tabular observation data (generated)
│   └── processed/              # Existing processed artifacts (nmea, etc.)
├── scripts/
│   └── extract_rinex.py        # CLI entry point for RINEX extraction
├── src/
│   └── gnss_position_tracker/
│       ├── __init__.py
│       ├── config.py           # Central paths/config constants
│       └── rinex_extractor.py  # gnss-lib-py wrapper + export helpers
├── tests/
│   └── test_structure.py       # Basic architecture test
└── pyproject.toml
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Run extraction

Extract all RINEX files in `data/raw`:

```bash
python scripts/extract_rinex.py
```

Choose custom input/output directories:

```bash
python scripts/extract_rinex.py \
  --input-dir data/raw \
  --output-dir data/interim
```

## Output format

For each RINEX file, the extractor attempts to save:

- `<name>_obs.csv`: flattened observation table
- `<name>_summary.json`: basic metadata (row/column counts and source file)

## Next steps (you can continue from here)

1. Integrate ephemeris download and alignment (`load_ephemeris`) for observation epochs.
2. Build the WLS/GNSS solution stage from extracted observables.
3. Add path generation (KML/CSV) and evaluation against provided NMEA/TXT.
