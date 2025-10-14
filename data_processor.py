"""
Data Processor Module for SynOmics

This module provides the DataProcessor class for comprehensive data preprocessing
and preparation tasks for synthetic omics data generation.
"""

import pandas as pd
import numpy as np
from typing import Optional, Union, List, Tuple, Any
from sklearn.preprocessing import (
    MinMaxScaler, StandardScaler, LabelEncoder, 
    OneHotEncoder, QuantileTransformer
)
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.model_selection import train_test_split, KFold, StratifiedKFold


class DataProcessor:
    """
    Comprehensive data preprocessing and preparation for synthetic data generation.
    
    The DataProcessor class provides essential data cleaning, normalization,
    transformation, and feature engineering capabilities for omics data.
    
    Attributes
    ----------
    data : pd.DataFrame
        The current dataset being processed
    scalers : dict
        Dictionary storing fitted scalers for each normalization method
    encoders : dict
        Dictionary storing fitted encoders for categorical variables
        
    Examples
    --------
    >>> from synomics.preprocessing import DataProcessor
    >>> processor = DataProcessor()
    >>> data = processor.load_data('path/to/data.csv')
    >>> data = processor.handle_missing(data, strategy='mean')
    >>> data = processor.normalize(data, method='min-max')
    """
    
    def __init__(self):
        """Initialize the DataProcessor."""
        self.data = None
        self.scalers = {}
        self.encoders = {}
        
    def load_data(self, filepath: str, **kwargs) -> pd.DataFrame:
        """
        Load data from a file.
        
        Parameters
        ----------
        filepath : str
            Path to the data file (CSV, Excel, etc.)
        **kwargs : dict
            Additional arguments passed to pandas read function
            
        Returns
        -------
        pd.DataFrame
            Loaded dataset
            
        Examples
        --------
        >>> processor = DataProcessor()
        >>> data = processor.load_data('data.csv')
        >>> data = processor.load_data('data.xlsx', sheet_name='Sheet1')
        """
        if filepath.endswith('.csv'):
            self.data = pd.read_csv(filepath, **kwargs)
        elif filepath.endswith(('.xlsx', '.xls')):
            self.data = pd.read_excel(filepath, **kwargs)
        elif filepath.endswith('.parquet'):
            self.data = pd.read_parquet(filepath, **kwargs)
        else:
            raise ValueError(f"Unsupported file format: {filepath}")
        return self.data
    
    def handle_missing(
        self, 
        data: pd.DataFrame, 
        strategy: str = 'mean',
        columns: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Handle missing values in the dataset.
        
        Parameters
        ----------
        data : pd.DataFrame
            Input dataset
        strategy : str, default='mean'
            Strategy for handling missing values:
            - 'mean': Replace with column mean
            - 'median': Replace with column median
            - 'mode': Replace with column mode
            - 'drop': Drop rows with missing values
            - 'forward_fill': Forward fill missing values
            - 'backward_fill': Backward fill missing values
        columns : list of str, optional
            Specific columns to apply the strategy to. If None, applies to all columns
            
        Returns
        -------
        pd.DataFrame
            Dataset with missing values handled
            
        Examples
        --------
        >>> data = processor.handle_missing(data, strategy='mean')
        >>> data = processor.handle_missing(data, strategy='median', columns=['age', 'score'])
        """
        data = data.copy()
        target_cols = columns if columns else data.columns
        
        if strategy == 'mean':
            data[target_cols] = data[target_cols].fillna(data[target_cols].mean())
        elif strategy == 'median':
            data[target_cols] = data[target_cols].fillna(data[target_cols].median())
        elif strategy == 'mode':
            for col in target_cols:
                data[col] = data[col].fillna(data[col].mode()[0] if not data[col].mode().empty else data[col])
        elif strategy == 'drop':
            data = data.dropna(subset=target_cols)
        elif strategy == 'forward_fill':
            data[target_cols] = data[target_cols].fillna(method='ffill')
        elif strategy == 'backward_fill':
            data[target_cols] = data[target_cols].fillna(method='bfill')
        else:
            raise ValueError(f"Unknown strategy: {strategy}")
            
        return data
    
    def remove_outliers(
        self,
        data: pd.DataFrame,
        threshold: float = 3.0,
        method: str = 'zscore',
        columns: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Identify and remove statistical outliers.
        
        Parameters
        ----------
        data : pd.DataFrame
            Input dataset
        threshold : float, default=3.0
            Threshold for outlier detection
        method : str, default='zscore'
            Method for outlier detection:
            - 'zscore': Z-score based detection
            - 'iqr': Interquartile range based detection
        columns : list of str, optional
            Specific columns to check for outliers. If None, checks all numeric columns
            
        Returns
        -------
        pd.DataFrame
            Dataset with outliers removed
            
        Examples
        --------
        >>> data = processor.remove_outliers(data, threshold=3.0)
        >>> data = processor.remove_outliers(data, method='iqr', columns=['expression_1'])
        """
        data = data.copy()
        numeric_cols = columns if columns else data.select_dtypes(include=[np.number]).columns
        
        if method == 'zscore':
            z_scores = np.abs((data[numeric_cols] - data[numeric_cols].mean()) / data[numeric_cols].std())
            mask = (z_scores < threshold).all(axis=1)
            data = data[mask]
        elif method == 'iqr':
            for col in numeric_cols:
                Q1 = data[col].quantile(0.25)
                Q3 = data[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - threshold * IQR
                upper_bound = Q3 + threshold * IQR
                data = data[(data[col] >= lower_bound) & (data[col] <= upper_bound)]
        else:
            raise ValueError(f"Unknown method: {method}")
            
        return data
    
    def normalize(
        self,
        data: pd.DataFrame,
        method: str = 'min-max',
        columns: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Normalize features in the dataset.
        
        Parameters
        ----------
        data : pd.DataFrame
            Input dataset
        method : str, default='min-max'
            Normalization method:
            - 'min-max': Scale features to [0, 1] range
            - 'z-score': Standardize to zero mean and unit variance
            - 'log': Apply logarithmic transformation
            - 'quantile': Transform to uniform or normal distribution
        columns : list of str, optional
            Specific columns to normalize. If None, normalizes all numeric columns
            
        Returns
        -------
        pd.DataFrame
            Normalized dataset
            
        Examples
        --------
        >>> data = processor.normalize(data, method='min-max')
        >>> data = processor.normalize(data, method='z-score', columns=['gene_1', 'gene_2'])
        """
        data = data.copy()
        numeric_cols = columns if columns else data.select_dtypes(include=[np.number]).columns
        
        if method == 'min-max':
            scaler = MinMaxScaler()
            data[numeric_cols] = scaler.fit_transform(data[numeric_cols])
            self.scalers['min-max'] = scaler
        elif method == 'z-score':
            scaler = StandardScaler()
            data[numeric_cols] = scaler.fit_transform(data[numeric_cols])
            self.scalers['z-score'] = scaler
        elif method == 'log':
            # Add small constant to avoid log(0)
            data[numeric_cols] = np.log1p(data[numeric_cols])
        elif method == 'quantile':
            scaler = QuantileTransformer()
            data[numeric_cols] = scaler.fit_transform(data[numeric_cols])
            self.scalers['quantile'] = scaler
        else:
            raise ValueError(f"Unknown method: {method}")
            
        return data
    
    def encode_categorical(
        self,
        data: pd.DataFrame,
        method: str = 'onehot',
        columns: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Encode categorical variables.
        
        Parameters
        ----------
        data : pd.DataFrame
            Input dataset
        method : str, default='onehot'
            Encoding method:
            - 'onehot': One-hot encoding
            - 'label': Label encoding
            - 'target': Target encoding (requires target variable)
        columns : list of str, optional
            Specific columns to encode. If None, encodes all object/category columns
            
        Returns
        -------
        pd.DataFrame
            Dataset with encoded categorical variables
            
        Examples
        --------
        >>> data = processor.encode_categorical(data, method='onehot')
        >>> data = processor.encode_categorical(data, method='label', columns=['category'])
        """
        data = data.copy()
        cat_cols = columns if columns else data.select_dtypes(include=['object', 'category']).columns
        
        if method == 'onehot':
            data = pd.get_dummies(data, columns=cat_cols, prefix=cat_cols)
        elif method == 'label':
            for col in cat_cols:
                encoder = LabelEncoder()
                data[col] = encoder.fit_transform(data[col].astype(str))
                self.encoders[col] = encoder
        elif method == 'target':
            # Target encoding requires target variable - placeholder implementation
            raise NotImplementedError("Target encoding requires a target variable")
        else:
            raise ValueError(f"Unknown method: {method}")
            
        return data
    
    def reduce_dimensions(
        self,
        data: pd.DataFrame,
        method: str = 'pca',
        n_components: int = 2,
        columns: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Perform dimensionality reduction.
        
        Parameters
        ----------
        data : pd.DataFrame
            Input dataset
        method : str, default='pca'
            Dimensionality reduction method:
            - 'pca': Principal Component Analysis
            - 'tsne': t-SNE
            - 'umap': UMAP (requires umap-learn package)
        n_components : int, default=2
            Number of components to reduce to
        columns : list of str, optional
            Specific columns to use. If None, uses all numeric columns
            
        Returns
        -------
        pd.DataFrame
            Dataset with reduced dimensions
            
        Examples
        --------
        >>> data_reduced = processor.reduce_dimensions(data, method='pca', n_components=10)
        >>> data_reduced = processor.reduce_dimensions(data, method='tsne', n_components=2)
        """
        numeric_cols = columns if columns else data.select_dtypes(include=[np.number]).columns
        X = data[numeric_cols].values
        
        if method == 'pca':
            reducer = PCA(n_components=n_components)
            X_reduced = reducer.fit_transform(X)
        elif method == 'tsne':
            reducer = TSNE(n_components=n_components)
            X_reduced = reducer.fit_transform(X)
        elif method == 'umap':
            try:
                from umap import UMAP
                reducer = UMAP(n_components=n_components)
                X_reduced = reducer.fit_transform(X)
            except ImportError:
                raise ImportError("UMAP requires the umap-learn package")
        else:
            raise ValueError(f"Unknown method: {method}")
        
        # Create new dataframe with reduced dimensions
        col_names = [f'{method}_component_{i+1}' for i in range(n_components)]
        result = pd.DataFrame(X_reduced, columns=col_names, index=data.index)
        
        # Add back non-numeric columns
        for col in data.columns:
            if col not in numeric_cols:
                result[col] = data[col]
                
        return result
    
    def split_data(
        self,
        data: pd.DataFrame,
        test_size: float = 0.2,
        random_state: Optional[int] = None,
        stratify_column: Optional[str] = None
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Split data into training and testing sets.
        
        Parameters
        ----------
        data : pd.DataFrame
            Input dataset
        test_size : float, default=0.2
            Proportion of data for testing (0.0 to 1.0)
        random_state : int, optional
            Random seed for reproducibility
        stratify_column : str, optional
            Column name to use for stratified splitting
            
        Returns
        -------
        tuple of pd.DataFrame
            Training and testing datasets (train_data, test_data)
            
        Examples
        --------
        >>> train_data, test_data = processor.split_data(data, test_size=0.2)
        >>> train_data, test_data = processor.split_data(data, test_size=0.3, stratify_column='class')
        """
        stratify = data[stratify_column] if stratify_column else None
        train_data, test_data = train_test_split(
            data, 
            test_size=test_size, 
            random_state=random_state,
            stratify=stratify
        )
        return train_data, test_data
    
    def create_folds(
        self,
        data: pd.DataFrame,
        n_splits: int = 5,
        shuffle: bool = True,
        random_state: Optional[int] = None,
        stratify_column: Optional[str] = None
    ) -> List[Tuple[pd.DataFrame, pd.DataFrame]]:
        """
        Create K-fold cross-validation splits.
        
        Parameters
        ----------
        data : pd.DataFrame
            Input dataset
        n_splits : int, default=5
            Number of folds
        shuffle : bool, default=True
            Whether to shuffle data before splitting
        random_state : int, optional
            Random seed for reproducibility
        stratify_column : str, optional
            Column name to use for stratified K-fold
            
        Returns
        -------
        list of tuple of pd.DataFrame
            List of (train_data, val_data) tuples for each fold
            
        Examples
        --------
        >>> folds = processor.create_folds(data, n_splits=5)
        >>> for train_fold, val_fold in folds:
        ...     # Train and validate on each fold
        ...     pass
        """
        if stratify_column:
            kfold = StratifiedKFold(n_splits=n_splits, shuffle=shuffle, random_state=random_state)
            splits = kfold.split(data, data[stratify_column])
        else:
            kfold = KFold(n_splits=n_splits, shuffle=shuffle, random_state=random_state)
            splits = kfold.split(data)
        
        folds = []
        for train_idx, val_idx in splits:
            train_fold = data.iloc[train_idx]
            val_fold = data.iloc[val_idx]
            folds.append((train_fold, val_fold))
        
        return folds
    
    def remove_duplicates(
        self,
        data: pd.DataFrame,
        subset: Optional[List[str]] = None,
        keep: str = 'first'
    ) -> pd.DataFrame:
        """
        Remove duplicate records from the dataset.
        
        Parameters
        ----------
        data : pd.DataFrame
            Input dataset
        subset : list of str, optional
            Columns to consider for identifying duplicates. If None, uses all columns
        keep : str, default='first'
            Which duplicate to keep: 'first', 'last', or False (drop all duplicates)
            
        Returns
        -------
        pd.DataFrame
            Dataset with duplicates removed
            
        Examples
        --------
        >>> data = processor.remove_duplicates(data)
        >>> data = processor.remove_duplicates(data, subset=['id', 'timestamp'])
        """
        return data.drop_duplicates(subset=subset, keep=keep)
    
    def validate_data_types(
        self,
        data: pd.DataFrame,
        column_types: dict
    ) -> pd.DataFrame:
        """
        Validate and convert data types for specified columns.
        
        Parameters
        ----------
        data : pd.DataFrame
            Input dataset
        column_types : dict
            Dictionary mapping column names to desired data types
            Example: {'age': 'int', 'score': 'float', 'category': 'str'}
            
        Returns
        -------
        pd.DataFrame
            Dataset with validated/converted data types
            
        Examples
        --------
        >>> types = {'age': 'int', 'weight': 'float', 'name': 'str'}
        >>> data = processor.validate_data_types(data, types)
        """
        data = data.copy()
        for col, dtype in column_types.items():
            if col in data.columns:
                if dtype == 'int':
                    data[col] = pd.to_numeric(data[col], errors='coerce').astype('Int64')
                elif dtype == 'float':
                    data[col] = pd.to_numeric(data[col], errors='coerce')
                elif dtype == 'str':
                    data[col] = data[col].astype(str)
                elif dtype == 'datetime':
                    data[col] = pd.to_datetime(data[col], errors='coerce')
                elif dtype == 'category':
                    data[col] = data[col].astype('category')
        return data
    
    def bin_continuous_variables(
        self,
        data: pd.DataFrame,
        column: str,
        bins: Union[int, List[float]],
        labels: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Discretize continuous variables into bins.
        
        Parameters
        ----------
        data : pd.DataFrame
            Input dataset
        column : str
            Column name to bin
        bins : int or list of float
            Number of equal-width bins or list of bin edges
        labels : list of str, optional
            Labels for the bins
            
        Returns
        -------
        pd.DataFrame
            Dataset with binned variable
            
        Examples
        --------
        >>> data = processor.bin_continuous_variables(data, 'age', bins=5)
        >>> data = processor.bin_continuous_variables(data, 'score', bins=[0, 50, 75, 100], 
        ...                                           labels=['low', 'medium', 'high'])
        """
        data = data.copy()
        data[f'{column}_binned'] = pd.cut(data[column], bins=bins, labels=labels)
        return data
    
    def get_summary_statistics(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Generate summary statistics for the dataset.
        
        Parameters
        ----------
        data : pd.DataFrame
            Input dataset
            
        Returns
        -------
        pd.DataFrame
            Summary statistics including count, mean, std, min, max, quartiles
            
        Examples
        --------
        >>> summary = processor.get_summary_statistics(data)
        >>> print(summary)
        """
        return data.describe(include='all')
