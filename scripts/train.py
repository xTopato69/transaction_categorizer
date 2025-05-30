import os
import sys
import logging
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from ml.features.feature_engineering import FeatureEngineer
from ml.preprocessing.preprocessor import TransactionPreprocessor
from ml.models.model_trainer import ModelTrainer
from utils.paths import get_raw_data_path, get_model_path, get_vectorizer_path, ensure_dir_exists, get_models_dir
from utils.logging import setup_logging


def train_model():#Train the transaction categorization model.
    try:
        setup_logging()
        logger = logging.getLogger(__name__)
        
        logger.info("Loading transaction data")
        data_path = get_raw_data_path()
        
        preprocessor = TransactionPreprocessor()        # Preprocess data
        processed_data = preprocessor.preprocess(data_path)
        
        feature_engineer = FeatureEngineer()        # Create and fit features
        x, y = feature_engineer.create_features(processed_data, is_training=True)
        
        trainer = ModelTrainer()        # Train model
        results = trainer.train(x, y)
        
        model_path = get_model_path()        # Save model and vectorizer
        vectorizer_path = get_vectorizer_path()
        
        ensure_dir_exists(model_path)
        ensure_dir_exists(vectorizer_path)
        
        trainer.save_model(model_path)
        feature_engineer.save_vectorizer(vectorizer_path)
        
        label_encoder_path = get_models_dir() / "label_encoder.joblib"
        feature_engineer.save_label_encoder(label_encoder_path)
        
        logger.info("Training completed successfully")
        print("\nTraining Summary:")
        print("----------------")
        for model_name, metrics in results.items():
            print(f"Model: {model_name}")
            print(f"  Training accuracy: {metrics['train_score']:.2%}")
            print(f"  Testing accuracy: {metrics['test_score']:.2%}")
            print(f"  Cross-validation accuracy: {metrics['cv_mean']:.2%} ± {metrics['cv_std']:.2%}")
            print("----------------")
        return results
    except Exception as e:
        logger.error(f"Error in training: {str(e)}")
        raise


if __name__ == "__main__":
    train_model() 