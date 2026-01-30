from pathlib import Path

BASE_DIRECTORY = Path(__file__).resolve().parent.parent

DATASET_DIR = BASE_DIRECTORY / "datasets"
DOCUMENTS = DATASET_DIR / "documents"
VECTOR_DIR = BASE_DIRECTORY / "qdrant_storage"
