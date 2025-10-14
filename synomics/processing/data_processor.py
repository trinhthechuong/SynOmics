"""
Data Processor Module
=====================

This module provides the DataPreprocessor class for preparing omics data
for synthetic data generation. It includes comprehensive data cleaning,
normalization, transformation, and feature engineering capabilities.
"""

import pandas as pd
import numpy as np
from typing import Union, List, Tuple, Optional, Dict, Any
from sklearn.preprocessing import (
    MinMaxScaler, StandardScaler, LabelEncoder, OneHotEncoder
)
from sklearn.impute import SimpleImputer
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split


class DataPreprocessor:
    """
    A comprehensive data preprocessing class for omics data preparation.
    
    The DataPreprocessor handles various preprocessing tasks including:
    - Data loading and validation
    - Missing value handling
    - Outlier detection and removal
    - Data normalization and scaling
    - Categorical encoding
    - Feature engineering
    - Data splitting
    
    Attributes
    ----------
    data : pd.DataFrame
        The current data being processed
    scaler : object
        The fitted scaler object (if normalization has been applied)
    encoders : dict
        Dictionary of fitted encoders for categorical variables
    """
    
    def __init__(self):
        """Initialize the DataPreprocessor."""
        self.data = None
        self.scaler = None
        self.encoders = {}
        self.imputer = None
        self.pca = None
        
    def load_data(self, filepath: str, **kwargs) -> pd.DataFrame:
        """
        Load omics data from a file.
        
        Parameters
        ----------
        filepath : str
            Path to the data file (CSV, TSV, Excel, etc.)
        **kwargs : dict
            Additional arguments passed to pandas read function
            
        Returns
        -------
        pd.DataFrame
            Loaded data
            
        Examples
        --------
        >>> preprocessor = DataPreprocessor()
        >>> data = preprocessor.load_data('path/to/data.csv')
        >>> data = preprocessor.load_data('path/to/data.xlsx', sheet_name='Sheet1')
        """
        if filepath.endswith('.csv'):
            self.data = pd.read_csv(filepath, **kwargs)
        elif filepath.endswith('.tsv'):
            self.data = pd.read_csv(filepath, sep='\t', **kwargs)
        elif filepath.endswith(('.xlsx', '.xls')):
            self.data = pd.read_excel(filepath, **kwargs)
        else:
            raise ValueError(f"Unsupported file format: {filepath}")
            
        print(f"Loaded data with shape: {self.data.shape}")
        return self.data
    
    def handle_missing(
        self, 
        data: Optional[pd.DataFrame] = None,
        strategy: str = 'mean',
        fill_value: Optional[float] = None
    ) -> pd.DataFrame:
        """
        Handle missing values in the dataset.
        
        Parameters
        ----------
        data : pd.DataFrame, optional
            Input data. If None, uses self.data
        strategy : str, default='mean'
            Strategy for imputation: 'mean', 'median', 'most_frequent', 'constant'
        fill_value : float, optional
            Fill value when strategy='constant'
            
        Returns
        -------
        pd.DataFrame
            Data with missing values handled
            
        Examples
        --------
        >>> data = preprocessor.handle_missing(data, strategy='mean')
        >>> data = preprocessor.handle_missing(data, strategy='constant', fill_value=0)
        """
        if data is None:
            data = self.data
            
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        categorical_cols = data.select_dtypes(exclude=[np.number]).columns
        
        # Handle numeric columns
        if len(numeric_cols) > 0:
            if strategy == 'constant' and fill_value is not None:
                self.imputer = SimpleImputer(strategy=strategy, fill_value=fill_value)
            else:
                self.imputer = SimpleImputer(strategy=strategy)
            data[numeric_cols] = self.imputer.fit_transform(data[numeric_cols])
        
        # Handle categorical columns
        if len(categorical_cols) > 0:
            cat_imputer = SimpleImputer(strategy='most_frequent')
            data[categorical_cols] = cat_imputer.fit_transform(data[categorical_cols])
            
        if data is self.data:
            self.data = data
            
        print(f"Missing values handled using '{strategy}' strategy")
        return data
    
    def remove_outliers(
        self,
        data: Optional[pd.DataFrame] = None,
        threshold: float = 3.0,
        method: str = 'zscore'
    ) -> pd.DataFrame:
        """
        Detect and remove outliers from the dataset.
        
        Parameters
        ----------
        data : pd.DataFrame, optional
            Input data. If None, uses self.data
        threshold : float, default=3.0
            Threshold for outlier detection
        method : str, default='zscore'
            Method for outlier detection: 'zscore' or 'iqr'
            
        Returns
        -------
        pd.DataFrame
            Data with outliers removed
            
        Examples
        --------
        >>> data = preprocessor.remove_outliers(data, threshold=3.0)
        >>> data = preprocessor.remove_outliers(data, method='iqr')
        """
        if data is None:
            data = self.data
            
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        
        if method == 'zscore':
            z_scores = np.abs((data[numeric_cols] - data[numeric_cols].mean()) / data[numeric_cols].std())
            mask = (z_scores < threshold).all(axis=1)
        elif method == 'iqr':
            Q1 = data[numeric_cols].quantile(0.25)
            Q3 = data[numeric_cols].quantile(0.75)
            IQR = Q3 - Q1
            mask = ~((data[numeric_cols] < (Q1 - threshold * IQR)) | 
                    (data[numeric_cols] > (Q3 + threshold * IQR))).any(axis=1)
        else:
            raise ValueError(f"Unknown method: {method}")
            
        data_cleaned = data[mask].reset_index(drop=True)
        removed = len(data) - len(data_cleaned)
        
        if data is self.data:
            self.data = data_cleaned
            
        print(f"Removed {removed} outliers using {method} method")
        return data_cleaned
    
    def normalize(
        self,
        data: Optional[pd.DataFrame] = None,
        method: str = 'min-max',
        feature_range: Tuple[float, float] = (0, 1)
    ) -> pd.DataFrame:
        """
        Normalize numeric features in the dataset.
        
        Parameters
        ----------
        data : pd.DataFrame, optional
            Input data. If None, uses self.data
        method : str, default='min-max'
            Normalization method: 'min-max', 'z-score', 'log'
        feature_range : tuple, default=(0, 1)
            Desired range for min-max scaling
            
        Returns
        -------
        pd.DataFrame
            Normalized data
            
        Examples
        --------
        >>> data = preprocessor.normalize(data, method='min-max')
        >>> data = preprocessor.normalize(data, method='z-score')
        >>> data = preprocessor.normalize(data, method='log')
        """
        if data is None:
            data = self.data
            
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        
        if method == 'min-max':
            self.scaler = MinMaxScaler(feature_range=feature_range)
            data[numeric_cols] = self.scaler.fit_transform(data[numeric_cols])
        elif method == 'z-score':
            self.scaler = StandardScaler()
            data[numeric_cols] = self.scaler.fit_transform(data[numeric_cols])
        elif method == 'log':
            # Add small constant to avoid log(0)
            data[numeric_cols] = np.log1p(data[numeric_cols])
        else:
            raise ValueError(f"Unknown normalization method: {method}")
            
        if data is self.data:
            self.data = data
            
        print(f"Data normalized using '{method}' method")
        return data
    
    def encode_categorical(
        self,
        data: Optional[pd.DataFrame] = None,
        method: str = 'onehot',
        columns: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Encode categorical variables.
        
        Parameters
        ----------
        data : pd.DataFrame, optional
            Input data. If None, uses self.data
        method : str, default='onehot'
            Encoding method: 'onehot', 'label', 'target'
        columns : list, optional
            List of columns to encode. If None, encodes all categorical columns
            
        Returns
        -------
        pd.DataFrame
            Data with encoded categorical variables
            
        Examples
        --------
        >>> data = preprocessor.encode_categorical(data, method='onehot')
        >>> data = preprocessor.encode_categorical(data, method='label', columns=['category'])
        """
        if data is None:
            data = self.data
            
        if columns is None:
            columns = data.select_dtypes(exclude=[np.number]).columns.tolist()
            
        if method == 'onehot':
            data = pd.get_dummies(data, columns=columns, prefix=columns)
        elif method == 'label':
            for col in columns:
                encoder = LabelEncoder()
                data[col] = encoder.fit_transform(data[col].astype(str))
                self.encoders[col] = encoder
        else:
            raise ValueError(f"Unknown encoding method: {method}")
            
        if data is self.data:
            self.data = data
            
        print(f"Categorical variables encoded using '{method}' method")
        return data
    
    def apply_pca(
        self,
        data: Optional[pd.DataFrame] = None,
        n_components: Union[int, float] = 0.95,
        columns: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Apply Principal Component Analysis for dimensionality reduction.
        
        Parameters
        ----------
        data : pd.DataFrame, optional
            Input data. If None, uses self.data
        n_components : int or float, default=0.95
            Number of components or variance ratio to preserve
        columns : list, optional
            Columns to apply PCA on. If None, uses all numeric columns
            
        Returns
        -------
        pd.DataFrame
            Data with PCA applied
            
        Examples
        --------
        >>> data = preprocessor.apply_pca(data, n_components=10)
        >>> data = preprocessor.apply_pca(data, n_components=0.95)
        """
        if data is None:
            data = self.data
            
        if columns is None:
            columns = data.select_dtypes(include=[np.number]).columns.tolist()
            
        self.pca = PCA(n_components=n_components)
        pca_features = self.pca.fit_transform(data[columns])
        
        # Create new DataFrame with PCA components
        pca_cols = [f'PC{i+1}' for i in range(pca_features.shape[1])]
        pca_df = pd.DataFrame(pca_features, columns=pca_cols, index=data.index)
        
        # Keep non-PCA columns
        other_cols = [col for col in data.columns if col not in columns]
        result = pd.concat([data[other_cols], pca_df], axis=1)
        
        if data is self.data:
            self.data = result
            
        print(f"PCA applied: {pca_features.shape[1]} components explaining "
              f"{self.pca.explained_variance_ratio_.sum():.2%} of variance")
        return result
    
    def split_data(
        self,
        data: Optional[pd.DataFrame] = None,
        test_size: float = 0.2,
        random_state: Optional[int] = 42,
        stratify_column: Optional[str] = None
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Split data into training and testing sets.
        
        Parameters
        ----------
        data : pd.DataFrame, optional
            Input data. If None, uses self.data
        test_size : float, default=0.2
            Proportion of data to include in test split
        random_state : int, optional
            Random state for reproducibility
        stratify_column : str, optional
            Column name to use for stratified splitting
            
        Returns
        -------
        tuple of pd.DataFrame
            Training and testing data
            
        Examples
        --------
        >>> train_data, test_data = preprocessor.split_data(data, test_size=0.2)
        >>> train_data, test_data = preprocessor.split_data(data, stratify_column='label')
        """
        if data is None:
            data = self.data
            
        stratify = data[stratify_column] if stratify_column else None
        
        train_data, test_data = train_test_split(
            data,
            test_size=test_size,
            random_state=random_state,
            stratify=stratify
        )
        
        print(f"Data split: {len(train_data)} training samples, {len(test_data)} test samples")
        return train_data, test_data
    
    def get_data_summary(self, data: Optional[pd.DataFrame] = None) -> Dict[str, Any]:
        """
        Get a summary of the dataset.
        
        Parameters
        ----------
        data : pd.DataFrame, optional
            Input data. If None, uses self.data
            
        Returns
        -------
        dict
            Dictionary containing dataset summary statistics
            
        Examples
        --------
        >>> summary = preprocessor.get_data_summary()
        >>> print(summary)
        """
        if data is None:
            data = self.data
            
        if data is None:
            return {"error": "No data loaded"}
            
        summary = {
            "shape": data.shape,
            "n_samples": len(data),
            "n_features": len(data.columns),
            "n_numeric": len(data.select_dtypes(include=[np.number]).columns),
            "n_categorical": len(data.select_dtypes(exclude=[np.number]).columns),
            "missing_values": data.isnull().sum().to_dict(),
            "memory_usage": f"{data.memory_usage(deep=True).sum() / 1024**2:.2f} MB"
        }
        
        return summary
