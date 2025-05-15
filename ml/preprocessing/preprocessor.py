import pandas as pd
from pathlib import Path
from typing import Union, Dict, Any

class TransactionPreprocessor:
    def preprocess(self, data: Union[pd.DataFrame, Dict[str, Any], str, Path]) -> pd.DataFrame: #Preprocess transaction data.
        if isinstance(data, (str, Path)):
            df = pd.read_csv(data)
        elif isinstance(data, dict):
            df = pd.DataFrame([data])
        else:
            df = data.copy()
            
        required_columns = ['transaction_id', 'amount', 'description', 'merchant', 'date', 'user_id', 'payment_method']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
            
        df['date'] = pd.to_datetime(df['date'])
        
        text_columns = ['description', 'merchant', 'payment_method']
        for col in text_columns:
            df[col] = df[col].str.lower().str.strip()
            
        df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
        if (df['amount'] <= 0).any():
            raise ValueError("All amounts must be positive")
            
        return df 