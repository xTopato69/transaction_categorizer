from pathlib import Path
import os


def get_project_root() -> Path: #Get the project root directory.
    return Path(__file__).parent.parent


def get_data_dir() -> Path:
    data_dir = get_project_root() / "data"
    data_dir.mkdir(exist_ok=True)
    return data_dir


def get_models_dir() -> Path:
    models_dir = get_project_root() / "models"
    models_dir.mkdir(exist_ok=True)
    return models_dir


def get_processed_data_path() -> Path:
    return get_data_dir() / "processed" / "cleaned_transactions.csv"


def get_raw_data_path() -> Path:
    cleaned_path = get_processed_data_path()# Use cleaned data if available, otherwise fall back to raw data
    if cleaned_path.exists():
        return cleaned_path
    return get_data_dir() / "raw" / "digital_wallet_transactions.csv"


def get_model_path() -> Path:
    return get_models_dir() / "transaction_classifier.joblib"


def get_vectorizer_path() -> Path:
    return get_models_dir() / "vectorizer.joblib"


def ensure_dir_exists(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True) 