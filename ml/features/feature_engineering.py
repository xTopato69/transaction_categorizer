import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
import joblib
from pathlib import Path
from typing import Tuple, Optional, Union

class FeatureEngineer:
    def __init__(self, vectorizer_path: Optional[Union[str, Path]] = None, label_encoder_path: Optional[Union[str, Path]] = None):
        self.vectorizer = TfidfVectorizer( # Initialize the feature engineer.
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        
        if vectorizer_path and Path(vectorizer_path).exists():
            self.vectorizer = joblib.load(vectorizer_path)
        self.label_encoder = LabelEncoder()
        self.label_encoder_fitted = False
        if label_encoder_path and Path(label_encoder_path).exists():
            self.label_encoder = joblib.load(label_encoder_path)
            self.label_encoder_fitted = True
    
    def create_features(self, data: pd.DataFrame, is_training: bool = False) -> Tuple[np.ndarray, Optional[np.ndarray]]: #Create features from transaction data.
        text_features = data['description'] + ' ' + data['merchant']
        
        if is_training:
            X = self.vectorizer.fit_transform(text_features)
            if 'category' in data.columns:
                y = self.label_encoder.fit_transform(data['category'])
                self.label_encoder_fitted = True
            else:
                y = None
        else:
            X = self.vectorizer.transform(text_features)
            y = None
            
        numerical_features = pd.DataFrame({
            'amount': data['amount'],
            'hour': pd.to_datetime(data['date']).dt.hour,
            'day_of_week': pd.to_datetime(data['date']).dt.dayofweek
        })
        
        X_combined = np.hstack([X.toarray(), numerical_features.values])
        
        return X_combined, y
    
    def transform(self, data: pd.DataFrame) -> Tuple[np.ndarray, None]: #Transform data for prediction.
        return self.create_features(data, is_training=False) # Returns:Tuple of (features, None)
    
    def save_vectorizer(self, path: Union[str, Path]):
        joblib.dump(self.vectorizer, path)

    def save_label_encoder(self, path: Union[str, Path]):
        if self.label_encoder_fitted:
            joblib.dump(self.label_encoder, path) 