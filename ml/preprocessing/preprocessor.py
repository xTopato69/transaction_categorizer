import pandas as pd
from pathlib import Path
from typing import Union, Dict, Any

class TransactionPreprocessor:
    def preprocess(self, data: Union[pd.DataFrame, Dict[str, Any], str, Path]) -> pd.DataFrame:
        if isinstance(data, (str, Path)):
            df = pd.read_csv(data)
        elif isinstance(data, dict):
            df = pd.DataFrame([data])
        else:
            df = data.copy()
            
        # Map new columns to required format
        df = df.rename(columns={
            'transaction_date': 'date',
            'product_amount': 'amount',
            'product_name': 'description',
            'merchant_name': 'merchant',
            'product_category': 'category'
        })
            
        # Ensure required columns exist
        required_columns = ['transaction_id', 'amount', 'description', 'merchant', 'date', 'user_id', 'payment_method']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
            
        # Convert date to datetime
        df['date'] = pd.to_datetime(df['date'])
        
        # Process text columns
        text_columns = ['description', 'merchant', 'payment_method']
        for col in text_columns:
            if col in df.columns:
                df[col] = df[col].str.lower().str.strip()
            
        # Process numerical columns
        df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
        if (df['amount'] <= 0).any():
            raise ValueError("All amounts must be positive")
            
        # Add additional features from new data
        if 'transaction_fee' in df.columns:
            df['transaction_fee'] = pd.to_numeric(df['transaction_fee'], errors='coerce')
            df['total_amount'] = df['amount'] + df['transaction_fee']
            
        if 'cashback' in df.columns:
            df['cashback'] = pd.to_numeric(df['cashback'], errors='coerce')
            
        if 'loyalty_points' in df.columns:
            df['loyalty_points'] = pd.to_numeric(df['loyalty_points'], errors='coerce')
            
        # Add device type as a feature if available
        if 'device_type' in df.columns:
            df['device_type'] = df['device_type'].str.lower().str.strip()
            
        # Add location as a feature if available
        if 'location' in df.columns:
            df['location'] = df['location'].str.lower().str.strip()
            
        return df 