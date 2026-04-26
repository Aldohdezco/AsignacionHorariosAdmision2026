from __future__ import annotations
import json
from pathlib import Path
from typing import List
from .models import ClassRecord

BASE_DIR = Path(__file__).resolve().parents[2]
DEFAULT_DATASET = BASE_DIR / "data" / "tabla1.json"

def load_records(path: Path | None = None) -> List[ClassRecord]:
    dataset_path = path or DEFAULT_DATASET
    with dataset_path.open("r", encoding="utf-8") as handle:
        raw_records = json.load(handle)

    return [ClassRecord(**item) for item in raw_records]
