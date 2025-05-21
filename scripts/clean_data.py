import pandas as pd
import numpy as np
from pathlib import Path
import logging
from typing import Tuple
import re

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def clean_text(text: str) -> str: #Clean text by removing special characters and extra spaces.
    if pd.isna(text):
        return ""
    text = str(text).lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def clean_amount(amount: float) -> float: #Clean amount values.
    if pd.isna(amount):
        return 0.0
    try:
        amount = float(amount)
        return max(0.0, amount) 
    except (ValueError, TypeError):
        return 0.0


def clean_dates(df: pd.DataFrame) -> pd.DataFrame: #Clean and standardize date formats.
    df['transaction_date'] = pd.to_datetime(df['transaction_date'], errors='coerce')
    # Remove rows with invalid dates
    df = df.dropna(subset=['transaction_date'])
    return df


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame: #Remove duplicate transactions.
    initial_len = len(df)
    df = df.drop_duplicates(subset=['transaction_id'], keep='first')
    removed = initial_len - len(df)
    if removed > 0:
        logger.info(f"Removed {removed} duplicate transactions")
    return df


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame: #Handle missing values in the dataset.
    text_columns = ['product_name', 'merchant_name', 'payment_method', 'device_type', 'location']
    for col in text_columns:
        if col in df.columns:
            df[col] = df[col].fillna('')
    
    # Fill missing numerical fields with 0
    numerical_columns = ['product_amount', 'transaction_fee', 'cashback', 'loyalty_points']
    for col in numerical_columns:
        if col in df.columns:
            df[col] = df[col].fillna(0)
    
    return df


def validate_categories(df: pd.DataFrame) -> pd.DataFrame:#Validate and clean product categories.
    if 'product_category' in df.columns:
        # Remove categories with very few occurrences
        category_counts = df['product_category'].value_counts()
        valid_categories = category_counts[category_counts >= 5].index
        df = df[df['product_category'].isin(valid_categories)]
        
        # Clean category names
        df['product_category'] = df['product_category'].apply(clean_text)
    
    return df


def clean_data(input_path: Path, output_path: Path) -> Tuple[pd.DataFrame, dict]:#Main function to clean the transaction data.
    logger.info(f"Loading data from {input_path}")
    df = pd.read_csv(input_path)
    initial_rows = len(df)
    
    stats = {
        'initial_rows': initial_rows,
        'missing_values': {},
        'invalid_amounts': 0,
        'invalid_dates': 0,
        'duplicates': 0
    }
    
    for col in df.columns:
        missing = df[col].isna().sum()
        if missing > 0:
            stats['missing_values'][col] = missing
    
    logger.info("Cleaning text fields...") # Clean the data
    text_columns = ['product_name', 'merchant_name', 'payment_method', 'device_type', 'location']
    for col in text_columns:
        if col in df.columns:
            df[col] = df[col].apply(clean_text)
    
    logger.info("Cleaning numerical fields...")
    if 'product_amount' in df.columns:
        df['product_amount'] = df['product_amount'].apply(clean_amount)
        stats['invalid_amounts'] = (df['product_amount'] == 0).sum()
    
    logger.info("Cleaning dates...")
    df = clean_dates(df)
    stats['invalid_dates'] = initial_rows - len(df)
    
    logger.info("Removing duplicates...")
    df = remove_duplicates(df)
    stats['duplicates'] = initial_rows - len(df)
    
    logger.info("Handling missing values...")
    df = handle_missing_values(df)
    
    logger.info("Validating categories...")
    df = validate_categories(df)
    
    logger.info(f"Saving cleaned data to {output_path}")
    df.to_csv(output_path, index=False)
    
    stats['final_rows'] = len(df)
    stats['rows_removed'] = initial_rows - len(df)
    
    return df, stats


def main():
    project_root = Path(__file__).parent.parent
    input_path = project_root / "data" / "raw" / "digital_wallet_transactions.csv"
    output_path = project_root / "data" / "processed" / "cleaned_transactions.csv"
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    df, stats = clean_data(input_path, output_path)
    
    
    logger.info("\nCleaning Statistics:") # Print cleaning statistics
    logger.info(f"Initial rows: {stats['initial_rows']}")
    logger.info(f"Final rows: {stats['final_rows']}")
    logger.info(f"Rows removed: {stats['rows_removed']}")
    
    if stats['missing_values']:
        logger.info("\nMissing values:")
        for col, count in stats['missing_values'].items():
            logger.info(f"  {col}: {count}")
    
    logger.info(f"\nInvalid amounts: {stats['invalid_amounts']}")
    logger.info(f"Invalid dates: {stats['invalid_dates']}")
    logger.info(f"Duplicates removed: {stats['duplicates']}")

if __name__ == "__main__":
    main() 