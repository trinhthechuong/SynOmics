Preprocessing Module
====================

The Preprocessing module provides essential data preparation and cleaning capabilities for synthetic data generation.

Overview
--------

Before generating synthetic data, real-world omics data often requires preprocessing to ensure quality and consistency. 
This module handles various preprocessing tasks including data cleaning, normalization, transformation, and feature engineering.

Key Features
------------

Data Cleaning
~~~~~~~~~~~~~

* **Missing Value Handling**: Strategies for imputing or removing missing data
* **Outlier Detection**: Identification and treatment of statistical outliers
* **Data Type Validation**: Ensuring correct data types for downstream processing
* **Duplicate Removal**: Identifying and handling duplicate records

Data Normalization
~~~~~~~~~~~~~~~~~~

* **Min-Max Scaling**: Scale features to a specific range (typically 0 to 1)
* **Z-Score Standardization**: Normalize data to have zero mean and unit variance
* **Log Transformation**: Apply logarithmic transformation for skewed distributions
* **Quantile Transformation**: Map features to a uniform or normal distribution

Feature Engineering
~~~~~~~~~~~~~~~~~~~

* **Feature Selection**: Identify and select relevant features for synthesis
* **Dimensionality Reduction**: PCA, t-SNE, and UMAP for high-dimensional data
* **Categorical Encoding**: One-hot encoding, label encoding, and target encoding
* **Binning**: Discretization of continuous variables

Data Splitting
~~~~~~~~~~~~~~

* **Train-Test Split**: Partition data for model training and validation
* **Cross-Validation**: K-fold and stratified splitting strategies
* **Temporal Splitting**: Time-based splitting for sequential data

Usage Example
-------------

.. code-block:: python

   from synomics.preprocessing import DataProcessor
   
   # Initialize processor
   processor = DataProcessor()
   
   # Load your omics data
   data = processor.load_data('path/to/data.csv')
   
   # Handle missing values
   data = processor.handle_missing(data, strategy='mean')
   
   # Normalize features
   data = processor.normalize(data, method='min-max')
   
   # Remove outliers
   data = processor.remove_outliers(data, threshold=3.0)
   
   # Encode categorical variables
   data = processor.encode_categorical(data, method='onehot')
   
   # Split data
   train_data, test_data = processor.split_data(data, test_size=0.2)

API Reference
-------------

DataProcessor Class
~~~~~~~~~~~~~~~~~~~

The ``DataProcessor`` class provides comprehensive data preprocessing capabilities for synthetic data generation.

**Class: DataProcessor()**

Main preprocessing class with the following methods:

Data Loading
^^^^^^^^^^^^

* **load_data(filepath, \*\*kwargs)** - Load data from CSV, Excel, or Parquet files

  - *filepath* (str): Path to the data file
  - *\*\*kwargs*: Additional arguments for pandas read functions
  - *Returns*: pd.DataFrame

Data Cleaning
^^^^^^^^^^^^^

* **handle_missing(data, strategy='mean', columns=None)** - Handle missing values

  - *data* (pd.DataFrame): Input dataset
  - *strategy* (str): 'mean', 'median', 'mode', 'drop', 'forward_fill', 'backward_fill'
  - *columns* (list): Specific columns to process (default: all)
  - *Returns*: pd.DataFrame

* **remove_outliers(data, threshold=3.0, method='zscore', columns=None)** - Remove statistical outliers

  - *data* (pd.DataFrame): Input dataset
  - *threshold* (float): Detection threshold
  - *method* (str): 'zscore' or 'iqr'
  - *columns* (list): Columns to check (default: all numeric)
  - *Returns*: pd.DataFrame

* **remove_duplicates(data, subset=None, keep='first')** - Remove duplicate records

  - *data* (pd.DataFrame): Input dataset
  - *subset* (list): Columns to consider for duplicates
  - *keep* (str): 'first', 'last', or False
  - *Returns*: pd.DataFrame

* **validate_data_types(data, column_types)** - Validate and convert data types

  - *data* (pd.DataFrame): Input dataset
  - *column_types* (dict): Column name to type mappings
  - *Returns*: pd.DataFrame

Data Normalization
^^^^^^^^^^^^^^^^^^

* **normalize(data, method='min-max', columns=None)** - Normalize features

  - *data* (pd.DataFrame): Input dataset
  - *method* (str): 'min-max', 'z-score', 'log', 'quantile'
  - *columns* (list): Columns to normalize (default: all numeric)
  - *Returns*: pd.DataFrame

Feature Engineering
^^^^^^^^^^^^^^^^^^^

* **encode_categorical(data, method='onehot', columns=None)** - Encode categorical variables

  - *data* (pd.DataFrame): Input dataset
  - *method* (str): 'onehot', 'label', 'target'
  - *columns* (list): Columns to encode (default: all categorical)
  - *Returns*: pd.DataFrame

* **reduce_dimensions(data, method='pca', n_components=2, columns=None)** - Dimensionality reduction

  - *data* (pd.DataFrame): Input dataset
  - *method* (str): 'pca', 'tsne', 'umap'
  - *n_components* (int): Number of components
  - *columns* (list): Columns to use (default: all numeric)
  - *Returns*: pd.DataFrame

* **bin_continuous_variables(data, column, bins, labels=None)** - Discretize continuous variables

  - *data* (pd.DataFrame): Input dataset
  - *column* (str): Column name to bin
  - *bins* (int or list): Number of bins or bin edges
  - *labels* (list): Optional bin labels
  - *Returns*: pd.DataFrame

Data Splitting
^^^^^^^^^^^^^^

* **split_data(data, test_size=0.2, random_state=None, stratify_column=None)** - Train-test split

  - *data* (pd.DataFrame): Input dataset
  - *test_size* (float): Proportion for testing (0.0-1.0)
  - *random_state* (int): Random seed
  - *stratify_column* (str): Column for stratified splitting
  - *Returns*: tuple of pd.DataFrame (train_data, test_data)

* **create_folds(data, n_splits=5, shuffle=True, random_state=None, stratify_column=None)** - K-fold cross-validation

  - *data* (pd.DataFrame): Input dataset
  - *n_splits* (int): Number of folds
  - *shuffle* (bool): Whether to shuffle
  - *random_state* (int): Random seed
  - *stratify_column* (str): Column for stratified folding
  - *Returns*: list of tuples (train_fold, val_fold)

Utility Methods
^^^^^^^^^^^^^^^

* **get_summary_statistics(data)** - Generate summary statistics

  - *data* (pd.DataFrame): Input dataset
  - *Returns*: pd.DataFrame with statistics

Best Practices
--------------

1. **Understand Your Data**: Always perform exploratory data analysis before preprocessing
2. **Handle Missing Data Carefully**: Choose imputation strategies appropriate for your data type
3. **Scale Appropriately**: Different synthesis methods may require different scaling approaches
4. **Preserve Data Characteristics**: Ensure preprocessing doesn't remove important data patterns
5. **Document Transformations**: Keep track of all preprocessing steps for reproducibility

Advanced Usage Examples
-----------------------

Complete Preprocessing Pipeline
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from synomics.preprocessing import DataProcessor
   import pandas as pd
   
   # Initialize processor
   processor = DataProcessor()
   
   # Load data
   data = processor.load_data('omics_data.csv')
   
   # Step 1: Data Cleaning
   # Remove duplicates
   data = processor.remove_duplicates(data, subset=['sample_id'])
   
   # Validate data types
   column_types = {
       'sample_id': 'str',
       'age': 'int',
       'expression_level': 'float',
       'condition': 'category'
   }
   data = processor.validate_data_types(data, column_types)
   
   # Handle missing values
   data = processor.handle_missing(data, strategy='median', 
                                   columns=['age', 'expression_level'])
   
   # Remove outliers
   data = processor.remove_outliers(data, threshold=3.0, method='zscore')
   
   # Step 2: Feature Engineering
   # Encode categorical variables
   data = processor.encode_categorical(data, method='onehot', 
                                       columns=['condition'])
   
   # Bin continuous variables
   data = processor.bin_continuous_variables(data, 'age', 
                                             bins=[0, 30, 50, 70, 100],
                                             labels=['young', 'middle', 'senior', 'elderly'])
   
   # Step 3: Normalization
   # Apply min-max scaling to expression data
   expression_cols = [col for col in data.columns if 'expression' in col]
   data = processor.normalize(data, method='min-max', columns=expression_cols)
   
   # Step 4: Data Splitting
   train_data, test_data = processor.split_data(data, test_size=0.2, 
                                                 random_state=42,
                                                 stratify_column='condition_control')
   
   print(f"Training set: {len(train_data)} samples")
   print(f"Test set: {len(test_data)} samples")

Dimensionality Reduction Example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from synomics.preprocessing import DataProcessor
   
   processor = DataProcessor()
   data = processor.load_data('high_dimensional_data.csv')
   
   # Apply PCA to reduce dimensions
   data_pca = processor.reduce_dimensions(data, method='pca', n_components=10)
   print(f"Reduced from {data.shape[1]} to {data_pca.shape[1]} features")
   
   # For visualization, use t-SNE
   data_tsne = processor.reduce_dimensions(data, method='tsne', n_components=2)
   
   # Plot the results
   import matplotlib.pyplot as plt
   plt.scatter(data_tsne['tsne_component_1'], data_tsne['tsne_component_2'])
   plt.xlabel('t-SNE Component 1')
   plt.ylabel('t-SNE Component 2')
   plt.title('t-SNE Visualization')
   plt.show()

Cross-Validation Example
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from synomics.preprocessing import DataProcessor
   from sklearn.ensemble import RandomForestClassifier
   from sklearn.metrics import accuracy_score
   
   processor = DataProcessor()
   data = processor.load_data('training_data.csv')
   
   # Preprocess data
   data = processor.handle_missing(data, strategy='mean')
   data = processor.normalize(data, method='z-score')
   
   # Create 5-fold cross-validation splits
   folds = processor.create_folds(data, n_splits=5, shuffle=True, 
                                  random_state=42, stratify_column='target')
   
   # Train and evaluate on each fold
   scores = []
   for i, (train_fold, val_fold) in enumerate(folds):
       X_train = train_fold.drop('target', axis=1)
       y_train = train_fold['target']
       X_val = val_fold.drop('target', axis=1)
       y_val = val_fold['target']
       
       model = RandomForestClassifier(random_state=42)
       model.fit(X_train, y_train)
       y_pred = model.predict(X_val)
       
       score = accuracy_score(y_val, y_pred)
       scores.append(score)
       print(f"Fold {i+1} Accuracy: {score:.3f}")
   
   print(f"Average Accuracy: {sum(scores)/len(scores):.3f}")

Handling Different Data Types
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from synomics.preprocessing import DataProcessor
   
   processor = DataProcessor()
   
   # Load mixed-type data
   data = processor.load_data('mixed_data.csv')
   
   # Separate numeric and categorical columns
   numeric_cols = data.select_dtypes(include=['int64', 'float64']).columns
   categorical_cols = data.select_dtypes(include=['object', 'category']).columns
   
   # Handle missing values differently for each type
   data = processor.handle_missing(data, strategy='mean', columns=numeric_cols)
   data = processor.handle_missing(data, strategy='mode', columns=categorical_cols)
   
   # Normalize numeric features
   data = processor.normalize(data, method='min-max', columns=numeric_cols)
   
   # Encode categorical features
   data = processor.encode_categorical(data, method='onehot', columns=categorical_cols)
   
   # Get summary statistics
   summary = processor.get_summary_statistics(data)
   print(summary)

See Also
--------

* :doc:`synthesizer` - Generate synthetic data using preprocessed data
* :doc:`evaluation` - Evaluate the quality of preprocessed and synthetic data
