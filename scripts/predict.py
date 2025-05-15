import os
import sys
import logging
import pandas as pd
from pathlib import Path
from typing import Dict, Any, List, Union

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from services.transaction_service import TransactionService
from utils.logging import setup_logging
from utils.paths import get_raw_data_path


def predict_single(transaction: Dict[str, Any]) -> str:#    Predict category for a single transaction.
    try:
        service = TransactionService()
        return service.categorize(transaction)
    except Exception as e:
        logger.error(f"Error predicting single transaction: {str(e)}")
        raise


def predict_batch(transactions: List[Dict[str, Any]]) -> List[str]: #    Predict categories for a batch of transactions.
    try:
        service = TransactionService()
        return [service.categorize(tx) for tx in transactions]
    except Exception as e:
        logger.error(f"Error predicting batch transactions: {str(e)}")
        raise


def predict_from_file(file_path: Union[str, Path]) -> pd.DataFrame: # Predict categories for transactions from a CSV file.
    try:
        # Read transactions
        df = pd.read_csv(file_path)
        
        # Convert DataFrame rows to dictionaries
        transactions = df.to_dict('records')
        
        # Get predictions
        predictions = predict_batch(transactions)
        
        # Add predictions to DataFrame
        df['predicted_category'] = predictions
        
        return df
    except Exception as e:
        logger.error(f"Error predicting from file: {str(e)}")
        raise


if __name__ == "__main__":
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # Example usage
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        try:
            results = predict_from_file(file_path)
            output_path = Path(file_path).parent / "predictions.csv"
            results.to_csv(output_path, index=False)
            logger.info(f"Predictions saved to {output_path}")
        except Exception as e:
            logger.error(f"Failed to process file: {str(e)}")
            sys.exit(1)
    else:
        logger.info("Please provide a file path as argument")
        sys.exit(1) 