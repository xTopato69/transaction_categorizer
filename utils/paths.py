from pathlib import Path
import os

def get_project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.parent

def get_data_dir() -> Path:
    """Get the data directory path."""
    data_dir = get_project_root() / "data"
    data_dir.mkdir(exist_ok=True)
    return data_dir

def get_models_dir() -> Path:
    """Get the models directory path."""
    models_dir = get_project_root() / "models"
    models_dir.mkdir(exist_ok=True)
    return models_dir

def get_raw_data_path() -> Path:
    """Get the path to the raw transaction data."""
    return get_data_dir() / "transactions.csv"

def get_model_path() -> Path:
    """Get the path to the trained model."""
    return get_models_dir() / "transaction_classifier.joblib"

def get_vectorizer_path() -> Path:
    """Get the path to the trained vectorizer."""
    return get_models_dir() / "vectorizer.joblib"

def ensure_dir_exists(path: Path):
    """Ensure the directory for a file exists."""
    path.parent.mkdir(parents=True, exist_ok=True) 