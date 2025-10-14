"""
Data Integration Pipeline Module
=================================

This module provides the IntegrationPipeline class for orchestrating
the complete data preprocessing workflow. It integrates multiple preprocessing
steps into a configurable pipeline for reproducible data preparation.
"""

import pandas as pd
import numpy as np
from typing import Optional, List, Dict, Any, Union
import json
import pickle
from pathlib import Path
from .data_processor import DataPreprocessor


class IntegrationPipeline:
    """
    A pipeline orchestrator for integrating multiple preprocessing steps.
    
    The IntegrationPipeline provides a convenient way to chain multiple
    preprocessing operations together and apply them consistently across
    datasets. It supports:
    - Sequential application of preprocessing steps
    - Configuration management
    - Pipeline serialization and loading
    - Reproducible preprocessing workflows
    
    Attributes
    ----------
    preprocessor : DataPreprocessor
        The underlying data preprocessor
    pipeline_config : dict
        Configuration of the pipeline steps
    steps : list
        List of preprocessing steps to execute
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the Integration Pipeline.
        
        Parameters
        ----------
        config : dict, optional
            Configuration dictionary specifying preprocessing steps and parameters
            
        Examples
        --------
        >>> pipeline = IntegrationPipeline()
        >>> config = {
        ...     'steps': [
        ...         {'name': 'handle_missing', 'params': {'strategy': 'mean'}},
        ...         {'name': 'normalize', 'params': {'method': 'min-max'}},
        ...         {'name': 'remove_outliers', 'params': {'threshold': 3.0}}
        ...     ]
        ... }
        >>> pipeline = IntegrationPipeline(config=config)
        """
        self.preprocessor = DataPreprocessor()
        self.pipeline_config = config or {'steps': []}
        self.steps = []
        self.fitted = False
        
        if config:
            self._parse_config(config)
    
    def _parse_config(self, config: Dict[str, Any]) -> None:
        """
        Parse the configuration dictionary and build the pipeline steps.
        
        Parameters
        ----------
        config : dict
            Configuration dictionary
        """
        if 'steps' in config:
            self.steps = config['steps']
        else:
            raise ValueError("Configuration must contain 'steps' key")
    
    def add_step(self, step_name: str, params: Optional[Dict[str, Any]] = None) -> 'IntegrationPipeline':
        """
        Add a preprocessing step to the pipeline.
        
        Parameters
        ----------
        step_name : str
            Name of the preprocessing method (e.g., 'handle_missing', 'normalize')
        params : dict, optional
            Parameters to pass to the preprocessing method
            
        Returns
        -------
        IntegrationPipeline
            Self for method chaining
            
        Examples
        --------
        >>> pipeline = IntegrationPipeline()
        >>> pipeline.add_step('handle_missing', {'strategy': 'mean'})
        >>> pipeline.add_step('normalize', {'method': 'z-score'})
        >>> pipeline.add_step('remove_outliers', {'threshold': 3.0})
        """
        step = {
            'name': step_name,
            'params': params or {}
        }
        self.steps.append(step)
        self.pipeline_config['steps'] = self.steps
        return self
    
    def load_data(self, filepath: str, **kwargs) -> pd.DataFrame:
        """
        Load data through the pipeline.
        
        Parameters
        ----------
        filepath : str
            Path to the data file
        **kwargs : dict
            Additional arguments passed to load_data
            
        Returns
        -------
        pd.DataFrame
            Loaded data
            
        Examples
        --------
        >>> pipeline = IntegrationPipeline()
        >>> data = pipeline.load_data('path/to/data.csv')
        """
        data = self.preprocessor.load_data(filepath, **kwargs)
        return data
    
    def fit(self, data: pd.DataFrame) -> 'IntegrationPipeline':
        """
        Fit the pipeline on the training data.
        
        This method applies all configured preprocessing steps to the data
        and stores the fitted transformers for later use.
        
        Parameters
        ----------
        data : pd.DataFrame
            Training data to fit the pipeline on
            
        Returns
        -------
        IntegrationPipeline
            Self for method chaining
            
        Examples
        --------
        >>> pipeline = IntegrationPipeline(config)
        >>> pipeline.fit(train_data)
        """
        self.preprocessor.data = data.copy()
        
        print("=" * 60)
        print("Starting Pipeline Execution")
        print("=" * 60)
        
        for i, step in enumerate(self.steps, 1):
            step_name = step['name']
            params = step['params']
            
            print(f"\nStep {i}/{len(self.steps)}: {step_name}")
            print("-" * 40)
            
            if not hasattr(self.preprocessor, step_name):
                raise ValueError(f"Unknown preprocessing step: {step_name}")
            
            method = getattr(self.preprocessor, step_name)
            self.preprocessor.data = method(self.preprocessor.data, **params)
        
        self.fitted = True
        print("\n" + "=" * 60)
        print("Pipeline Execution Completed")
        print("=" * 60)
        
        return self
    
    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Transform new data using the fitted pipeline.
        
        Parameters
        ----------
        data : pd.DataFrame
            Data to transform
            
        Returns
        -------
        pd.DataFrame
            Transformed data
            
        Examples
        --------
        >>> pipeline.fit(train_data)
        >>> test_data_transformed = pipeline.transform(test_data)
        """
        if not self.fitted:
            raise RuntimeError("Pipeline must be fitted before transform. Call fit() first.")
        
        transformed_data = data.copy()
        
        for step in self.steps:
            step_name = step['name']
            params = step['params']
            
            method = getattr(self.preprocessor, step_name)
            transformed_data = method(transformed_data, **params)
        
        return transformed_data
    
    def fit_transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Fit the pipeline and transform the data in one step.
        
        Parameters
        ----------
        data : pd.DataFrame
            Data to fit and transform
            
        Returns
        -------
        pd.DataFrame
            Transformed data
            
        Examples
        --------
        >>> pipeline = IntegrationPipeline(config)
        >>> processed_data = pipeline.fit_transform(data)
        """
        self.fit(data)
        return self.preprocessor.data
    
    def get_processed_data(self) -> pd.DataFrame:
        """
        Get the processed data from the pipeline.
        
        Returns
        -------
        pd.DataFrame
            Processed data
            
        Examples
        --------
        >>> pipeline.fit(data)
        >>> processed_data = pipeline.get_processed_data()
        """
        if self.preprocessor.data is None:
            raise ValueError("No data has been processed yet. Call fit() first.")
        return self.preprocessor.data
    
    def save_pipeline(self, filepath: str) -> None:
        """
        Save the pipeline configuration and fitted transformers.
        
        Parameters
        ----------
        filepath : str
            Path to save the pipeline (without extension)
            
        Examples
        --------
        >>> pipeline.save_pipeline('my_pipeline')
        # This creates my_pipeline_config.json and my_pipeline_transformers.pkl
        """
        # Save configuration
        config_path = f"{filepath}_config.json"
        with open(config_path, 'w') as f:
            json.dump(self.pipeline_config, f, indent=2)
        
        # Save fitted transformers
        transformers = {
            'scaler': self.preprocessor.scaler,
            'encoders': self.preprocessor.encoders,
            'imputer': self.preprocessor.imputer,
            'pca': self.preprocessor.pca
        }
        
        transformers_path = f"{filepath}_transformers.pkl"
        with open(transformers_path, 'wb') as f:
            pickle.dump(transformers, f)
        
        print(f"Pipeline saved to {filepath}_config.json and {filepath}_transformers.pkl")
    
    def load_pipeline(self, filepath: str) -> 'IntegrationPipeline':
        """
        Load a saved pipeline configuration and transformers.
        
        Parameters
        ----------
        filepath : str
            Path to the saved pipeline (without extension)
            
        Returns
        -------
        IntegrationPipeline
            Self with loaded configuration
            
        Examples
        --------
        >>> pipeline = IntegrationPipeline()
        >>> pipeline.load_pipeline('my_pipeline')
        """
        # Load configuration
        config_path = f"{filepath}_config.json"
        with open(config_path, 'r') as f:
            self.pipeline_config = json.load(f)
        
        self._parse_config(self.pipeline_config)
        
        # Load transformers
        transformers_path = f"{filepath}_transformers.pkl"
        with open(transformers_path, 'rb') as f:
            transformers = pickle.load(f)
        
        self.preprocessor.scaler = transformers['scaler']
        self.preprocessor.encoders = transformers['encoders']
        self.preprocessor.imputer = transformers['imputer']
        self.preprocessor.pca = transformers['pca']
        
        self.fitted = True
        print(f"Pipeline loaded from {filepath}")
        
        return self
    
    def get_pipeline_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the pipeline configuration.
        
        Returns
        -------
        dict
            Summary of pipeline steps and status
            
        Examples
        --------
        >>> summary = pipeline.get_pipeline_summary()
        >>> print(summary)
        """
        summary = {
            'n_steps': len(self.steps),
            'steps': [
                {
                    'step_number': i + 1,
                    'name': step['name'],
                    'params': step['params']
                }
                for i, step in enumerate(self.steps)
            ],
            'fitted': self.fitted,
            'data_shape': self.preprocessor.data.shape if self.preprocessor.data is not None else None
        }
        
        return summary
    
    def print_pipeline_summary(self) -> None:
        """
        Print a formatted summary of the pipeline.
        
        Examples
        --------
        >>> pipeline.print_pipeline_summary()
        """
        summary = self.get_pipeline_summary()
        
        print("=" * 60)
        print("PIPELINE SUMMARY")
        print("=" * 60)
        print(f"Number of Steps: {summary['n_steps']}")
        print(f"Pipeline Status: {'Fitted' if summary['fitted'] else 'Not Fitted'}")
        
        if summary['data_shape']:
            print(f"Data Shape: {summary['data_shape']}")
        
        print("\nPipeline Steps:")
        print("-" * 60)
        
        for step_info in summary['steps']:
            print(f"{step_info['step_number']}. {step_info['name']}")
            if step_info['params']:
                for key, value in step_info['params'].items():
                    print(f"   - {key}: {value}")
        
        print("=" * 60)
    
    @staticmethod
    def create_default_pipeline() -> 'IntegrationPipeline':
        """
        Create a pipeline with default preprocessing steps.
        
        Returns
        -------
        IntegrationPipeline
            Pipeline with standard preprocessing steps
            
        Examples
        --------
        >>> pipeline = IntegrationPipeline.create_default_pipeline()
        >>> pipeline.fit_transform(data)
        """
        config = {
            'steps': [
                {'name': 'handle_missing', 'params': {'strategy': 'mean'}},
                {'name': 'remove_outliers', 'params': {'threshold': 3.0, 'method': 'zscore'}},
                {'name': 'normalize', 'params': {'method': 'min-max'}},
                {'name': 'encode_categorical', 'params': {'method': 'onehot'}}
            ]
        }
        
        return IntegrationPipeline(config=config)
    
    @staticmethod
    def create_genomics_pipeline() -> 'IntegrationPipeline':
        """
        Create a pipeline optimized for genomics data.
        
        Returns
        -------
        IntegrationPipeline
            Pipeline optimized for genomics preprocessing
            
        Examples
        --------
        >>> pipeline = IntegrationPipeline.create_genomics_pipeline()
        >>> pipeline.fit_transform(genomics_data)
        """
        config = {
            'steps': [
                {'name': 'handle_missing', 'params': {'strategy': 'median'}},
                {'name': 'normalize', 'params': {'method': 'log'}},
                {'name': 'remove_outliers', 'params': {'threshold': 4.0, 'method': 'zscore'}},
                {'name': 'normalize', 'params': {'method': 'z-score'}},
                {'name': 'apply_pca', 'params': {'n_components': 0.95}}
            ]
        }
        
        return IntegrationPipeline(config=config)
