Preprocessing Module (Processing Module)
=========================================

The Preprocessing module, also known as the **Processing Module**, is the first and foundational module of SynOmics. 
It provides essential data preparation and cleaning capabilities for synthetic data generation through two main components:

1. **DataPreprocessor** (``data_processor.py``): Core preprocessing functionality
2. **IntegrationPipeline** (``data_integration_pipeline.py``): Pipeline orchestration and workflow management

Overview
--------

Before generating synthetic data, real-world omics data often requires preprocessing to ensure quality and consistency. 
This module handles various preprocessing tasks including data cleaning, normalization, transformation, and feature engineering.

The Processing Module serves as the entry point for all data in SynOmics, ensuring that data is properly prepared before 
being passed to the Synthesizer Module for synthetic data generation.

DataPreprocessor Features
--------------------------

The ``DataPreprocessor`` class provides the following features:

1. Data Loading
~~~~~~~~~~~~~~~

Load omics data from various file formats:

.. code-block:: python

   preprocessor = DataPreprocessor()
   
   # Load CSV file
   data = preprocessor.load_data('data.csv')
   
   # Load TSV file
   data = preprocessor.load_data('data.tsv')
   
   # Load Excel file
   data = preprocessor.load_data('data.xlsx', sheet_name='Sheet1')

2. Missing Value Handling
~~~~~~~~~~~~~~~~~~~~~~~~~~

Handle missing values with multiple strategies:

.. code-block:: python

   # Impute with mean (default)
   data = preprocessor.handle_missing(data, strategy='mean')
   
   # Impute with median
   data = preprocessor.handle_missing(data, strategy='median')
   
   # Impute with most frequent value
   data = preprocessor.handle_missing(data, strategy='most_frequent')
   
   # Impute with constant value
   data = preprocessor.handle_missing(data, strategy='constant', fill_value=0)

3. Outlier Detection and Removal
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Remove outliers using statistical methods:

.. code-block:: python

   # Remove outliers using Z-score method (default)
   data = preprocessor.remove_outliers(data, threshold=3.0, method='zscore')
   
   # Remove outliers using IQR method
   data = preprocessor.remove_outliers(data, threshold=1.5, method='iqr')

4. Data Normalization
~~~~~~~~~~~~~~~~~~~~~

Normalize numeric features using various methods:

.. code-block:: python

   # Min-Max scaling (default: 0-1)
   data = preprocessor.normalize(data, method='min-max')
   
   # Min-Max scaling with custom range
   data = preprocessor.normalize(data, method='min-max', feature_range=(-1, 1))
   
   # Z-score standardization
   data = preprocessor.normalize(data, method='z-score')
   
   # Log transformation
   data = preprocessor.normalize(data, method='log')

5. Categorical Encoding
~~~~~~~~~~~~~~~~~~~~~~~

Encode categorical variables for machine learning:

.. code-block:: python

   # One-hot encoding (recommended for synthesis)
   data = preprocessor.encode_categorical(data, method='onehot')
   
   # Label encoding
   data = preprocessor.encode_categorical(data, method='label')
   
   # Encode specific columns only
   data = preprocessor.encode_categorical(data, method='onehot', 
                                         columns=['category1', 'category2'])

6. Dimensionality Reduction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Apply PCA for high-dimensional data:

.. code-block:: python

   # Keep 95% of variance (default)
   data = preprocessor.apply_pca(data, n_components=0.95)
   
   # Keep specific number of components
   data = preprocessor.apply_pca(data, n_components=10)
   
   # Apply to specific columns
   data = preprocessor.apply_pca(data, n_components=5, 
                                 columns=['gene1', 'gene2', 'gene3'])

7. Data Splitting
~~~~~~~~~~~~~~~~~

Split data for training and testing:

.. code-block:: python

   # Simple split
   train_data, test_data = preprocessor.split_data(data, test_size=0.2)
   
   # Stratified split (preserves class distribution)
   train_data, test_data = preprocessor.split_data(data, test_size=0.2,
                                                   stratify_column='label')
   
   # Custom random state for reproducibility
   train_data, test_data = preprocessor.split_data(data, test_size=0.3,
                                                   random_state=123)

8. Data Summary
~~~~~~~~~~~~~~~

Get comprehensive statistics about your data:

.. code-block:: python

   summary = preprocessor.get_data_summary()
   print(summary)
   
   # Output includes:
   # - Data shape (rows, columns)
   # - Number of numeric vs categorical features
   # - Missing value counts per column
   # - Memory usage

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

Module Architecture
-------------------

The Processing Module consists of two main components that work together:

.. code-block:: text

   ┌─────────────────────────────────────────────────────────────────┐
   │                     Processing Module                           │
   │                    (First Module of SynOmics)                   │
   ├─────────────────────────────────────────────────────────────────┤
   │                                                                 │
   │  ┌────────────────────────┐      ┌─────────────────────────┐  │
   │  │   DataPreprocessor     │      │  IntegrationPipeline    │  │
   │  │  (data_processor.py)   │◄─────┤ (data_integration_      │  │
   │  │                        │      │      pipeline.py)       │  │
   │  ├────────────────────────┤      ├─────────────────────────┤  │
   │  │ • Data Loading         │      │ • Pipeline Orchestration│  │
   │  │ • Missing Value        │      │ • Step Chaining         │  │
   │  │   Handling             │      │ • Configuration Mgmt    │  │
   │  │ • Outlier Detection    │      │ • Serialization         │  │
   │  │ • Normalization        │      │ • Reproducibility       │  │
   │  │ • Categorical Encoding │      │ • Preset Pipelines      │  │
   │  │ • Feature Engineering  │      │                         │  │
   │  │ • Data Splitting       │      │                         │  │
   │  └────────────────────────┘      └─────────────────────────┘  │
   │                                                                 │
   │                           ▼                                     │
   │              ┌────────────────────────┐                         │
   │              │   Preprocessed Data    │                         │
   │              │  Ready for Synthesis   │                         │
   │              └────────────────────────┘                         │
   └─────────────────────────────────────────────────────────────────┘

Component 1: DataPreprocessor
------------------------------

The ``DataPreprocessor`` class provides core preprocessing functionality with individual methods 
for each preprocessing task. It can be used standalone or as part of the ``IntegrationPipeline``.

Component 2: IntegrationPipeline  
---------------------------------

The ``IntegrationPipeline`` class orchestrates the preprocessing workflow by chaining multiple 
preprocessing steps together. It provides configuration management, reproducibility, and the 
ability to save/load preprocessing pipelines.

Usage Examples
--------------

Example 1: Using DataPreprocessor (Direct Approach)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For simple, one-off preprocessing tasks, use the ``DataPreprocessor`` directly:

.. code-block:: python

   from synomics.processing import DataPreprocessor
   
   # Initialize preprocessor
   preprocessor = DataPreprocessor()
   
   # Load your omics data
   data = preprocessor.load_data('path/to/data.csv')
   
   # Handle missing values
   data = preprocessor.handle_missing(data, strategy='mean')
   
   # Normalize features
   data = preprocessor.normalize(data, method='min-max')
   
   # Remove outliers
   data = preprocessor.remove_outliers(data, threshold=3.0)
   
   # Encode categorical variables
   data = preprocessor.encode_categorical(data, method='onehot')
   
   # Split data
   train_data, test_data = preprocessor.split_data(data, test_size=0.2)

Example 2: Using IntegrationPipeline (Recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For reproducible and configurable workflows, use the ``IntegrationPipeline``:

.. code-block:: python

   from synomics.processing import IntegrationPipeline
   
   # Method 1: Using a configuration dictionary
   config = {
       'steps': [
           {'name': 'handle_missing', 'params': {'strategy': 'mean'}},
           {'name': 'remove_outliers', 'params': {'threshold': 3.0}},
           {'name': 'normalize', 'params': {'method': 'min-max'}},
           {'name': 'encode_categorical', 'params': {'method': 'onehot'}}
       ]
   }
   
   pipeline = IntegrationPipeline(config=config)
   
   # Load and process data
   data = pipeline.load_data('path/to/data.csv')
   processed_data = pipeline.fit_transform(data)
   
   # Save the pipeline for later use
   pipeline.save_pipeline('my_preprocessing_pipeline')

Example 3: Building a Pipeline Step-by-Step
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from synomics.processing import IntegrationPipeline
   
   # Create an empty pipeline
   pipeline = IntegrationPipeline()
   
   # Add preprocessing steps
   pipeline.add_step('handle_missing', {'strategy': 'median'})
   pipeline.add_step('remove_outliers', {'threshold': 3.0, 'method': 'zscore'})
   pipeline.add_step('normalize', {'method': 'z-score'})
   pipeline.add_step('encode_categorical', {'method': 'label'})
   
   # Print pipeline summary
   pipeline.print_pipeline_summary()
   
   # Load and process data
   data = pipeline.load_data('path/to/data.csv')
   pipeline.fit(data)
   processed_data = pipeline.get_processed_data()

Example 4: Using Preset Pipelines
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For common use cases, SynOmics provides preset pipelines:

.. code-block:: python

   from synomics.processing import IntegrationPipeline
   
   # Use default pipeline (general-purpose)
   pipeline = IntegrationPipeline.create_default_pipeline()
   data = pipeline.load_data('path/to/data.csv')
   processed_data = pipeline.fit_transform(data)
   
   # Or use genomics-optimized pipeline
   genomics_pipeline = IntegrationPipeline.create_genomics_pipeline()
   genomics_data = genomics_pipeline.load_data('path/to/genomics_data.csv')
   processed_genomics = genomics_pipeline.fit_transform(genomics_data)

Example 5: Loading a Saved Pipeline
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from synomics.processing import IntegrationPipeline
   
   # Load a previously saved pipeline
   pipeline = IntegrationPipeline()
   pipeline.load_pipeline('my_preprocessing_pipeline')
   
   # Transform new data with the same preprocessing steps
   new_data = pipeline.load_data('path/to/new_data.csv')
   processed_new_data = pipeline.transform(new_data)

Example 6: Complete Workflow
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Here's a complete example showing how to use the Processing Module in a typical workflow:

.. code-block:: python

   from synomics.processing import IntegrationPipeline
   
   # Step 1: Create and configure the pipeline
   config = {
       'steps': [
           {'name': 'handle_missing', 'params': {'strategy': 'mean'}},
           {'name': 'remove_outliers', 'params': {'threshold': 3.0}},
           {'name': 'normalize', 'params': {'method': 'min-max'}},
           {'name': 'apply_pca', 'params': {'n_components': 0.95}}
       ]
   }
   
   pipeline = IntegrationPipeline(config=config)
   
   # Step 2: Load data
   print("Loading data...")
   data = pipeline.load_data('omics_data.csv')
   
   # Step 3: Display pipeline summary
   pipeline.print_pipeline_summary()
   
   # Step 4: Fit and transform the data
   print("\nProcessing data...")
   processed_data = pipeline.fit_transform(data)
   
   # Step 5: Get summary of processed data
   summary = pipeline.preprocessor.get_data_summary()
   print(f"\nProcessed data shape: {summary['shape']}")
   print(f"Memory usage: {summary['memory_usage']}")
   
   # Step 6: Save the pipeline
   pipeline.save_pipeline('omics_preprocessing_pipeline')
   
   # Step 7: Use processed data for synthesis
   # (This would be passed to the Synthesizer Module)
   print("\nData ready for synthesis!")
   
   # The processed_data can now be used with the Synthesizer Module
   # from synomics.synthesizer import CTGAN
   # synthesizer = CTGAN()
   # synthesizer.fit(processed_data)
   # synthetic_data = synthesizer.generate(n_samples=1000)

IntegrationPipeline Features
-----------------------------

The ``IntegrationPipeline`` class provides advanced pipeline management:

1. Pipeline Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~

Define preprocessing workflows using configuration dictionaries:

.. code-block:: python

   config = {
       'steps': [
           {'name': 'handle_missing', 'params': {'strategy': 'mean'}},
           {'name': 'normalize', 'params': {'method': 'min-max'}},
           {'name': 'remove_outliers', 'params': {'threshold': 3.0}}
       ]
   }
   
   pipeline = IntegrationPipeline(config=config)

2. Step-by-Step Building
~~~~~~~~~~~~~~~~~~~~~~~~~

Build pipelines incrementally:

.. code-block:: python

   pipeline = IntegrationPipeline()
   pipeline.add_step('handle_missing', {'strategy': 'mean'})
   pipeline.add_step('normalize', {'method': 'z-score'})
   pipeline.add_step('encode_categorical', {'method': 'onehot'})

3. Pipeline Execution
~~~~~~~~~~~~~~~~~~~~~~

Execute the entire preprocessing workflow:

.. code-block:: python

   # Fit the pipeline on training data
   pipeline.fit(train_data)
   
   # Transform new data using fitted pipeline
   test_processed = pipeline.transform(test_data)
   
   # Or fit and transform in one step
   processed_data = pipeline.fit_transform(data)

4. Pipeline Serialization
~~~~~~~~~~~~~~~~~~~~~~~~~~

Save and load pipelines for reproducibility:

.. code-block:: python

   # Save the pipeline
   pipeline.save_pipeline('my_pipeline')
   # Creates: my_pipeline_config.json and my_pipeline_transformers.pkl
   
   # Load the pipeline later
   loaded_pipeline = IntegrationPipeline()
   loaded_pipeline.load_pipeline('my_pipeline')
   
   # Use it on new data
   new_processed = loaded_pipeline.transform(new_data)

5. Preset Pipelines
~~~~~~~~~~~~~~~~~~~

Use pre-configured pipelines for common scenarios:

.. code-block:: python

   # Default general-purpose pipeline
   pipeline = IntegrationPipeline.create_default_pipeline()
   
   # Genomics-optimized pipeline (includes log transformation and PCA)
   genomics_pipeline = IntegrationPipeline.create_genomics_pipeline()

6. Pipeline Monitoring
~~~~~~~~~~~~~~~~~~~~~~

Track and visualize pipeline execution:

.. code-block:: python

   # Get pipeline summary
   summary = pipeline.get_pipeline_summary()
   print(summary)
   
   # Print formatted summary
   pipeline.print_pipeline_summary()
   
   # Output shows:
   # - Number of steps
   # - Fitted status
   # - Data shape
   # - Detailed step configuration

How to Run IntegrationPipeline
-------------------------------

Basic Workflow
~~~~~~~~~~~~~~

Follow these steps to run the ``IntegrationPipeline``:

**Step 1: Import the module**

.. code-block:: python

   from synomics.processing import IntegrationPipeline

**Step 2: Create a pipeline**

Choose one of three methods:

.. code-block:: python

   # Method A: Use preset pipeline
   pipeline = IntegrationPipeline.create_default_pipeline()
   
   # Method B: Create from configuration
   config = {
       'steps': [
           {'name': 'handle_missing', 'params': {'strategy': 'mean'}},
           {'name': 'normalize', 'params': {'method': 'min-max'}}
       ]
   }
   pipeline = IntegrationPipeline(config=config)
   
   # Method C: Build step-by-step
   pipeline = IntegrationPipeline()
   pipeline.add_step('handle_missing', {'strategy': 'mean'})
   pipeline.add_step('normalize', {'method': 'min-max'})

**Step 3: Load your data**

.. code-block:: python

   data = pipeline.load_data('path/to/your/data.csv')
   
   # Or load from other formats
   # data = pipeline.load_data('data.xlsx', sheet_name='Sheet1')
   # data = pipeline.load_data('data.tsv')

**Step 4: Execute the pipeline**

.. code-block:: python

   # Option 1: Fit and transform together
   processed_data = pipeline.fit_transform(data)
   
   # Option 2: Fit and transform separately
   pipeline.fit(data)
   processed_data = pipeline.get_processed_data()

**Step 5: (Optional) Save the pipeline**

.. code-block:: python

   pipeline.save_pipeline('my_preprocessing_pipeline')

**Step 6: Use processed data**

.. code-block:: python

   # The processed data is now ready for synthesis
   print(f"Processed data shape: {processed_data.shape}")
   
   # Pass to Synthesizer Module
   # from synomics.synthesizer import CTGAN
   # synthesizer = CTGAN()
   # synthesizer.fit(processed_data)

Complete Example Script
~~~~~~~~~~~~~~~~~~~~~~~~

Here's a complete runnable script:

.. code-block:: python

   #!/usr/bin/env python3
   """
   Example script demonstrating the IntegrationPipeline usage
   """
   
   from synomics.processing import IntegrationPipeline
   
   def main():
       # Create pipeline with custom configuration
       print("Creating preprocessing pipeline...")
       config = {
           'steps': [
               {'name': 'handle_missing', 'params': {'strategy': 'mean'}},
               {'name': 'remove_outliers', 'params': {'threshold': 3.0}},
               {'name': 'normalize', 'params': {'method': 'min-max'}},
               {'name': 'encode_categorical', 'params': {'method': 'onehot'}}
           ]
       }
       
       pipeline = IntegrationPipeline(config=config)
       
       # Display pipeline configuration
       print("\n" + "="*60)
       pipeline.print_pipeline_summary()
       
       # Load data
       print("\nLoading data...")
       data = pipeline.load_data('omics_data.csv')
       
       # Process the data
       print("\nExecuting pipeline...")
       processed_data = pipeline.fit_transform(data)
       
       # Get data summary
       print("\nData Summary:")
       summary = pipeline.preprocessor.get_data_summary()
       print(f"  Original shape: {data.shape}")
       print(f"  Processed shape: {processed_data.shape}")
       print(f"  Memory usage: {summary['memory_usage']}")
       
       # Save the pipeline for future use
       print("\nSaving pipeline...")
       pipeline.save_pipeline('omics_preprocessing')
       
       # Save processed data
       print("\nSaving processed data...")
       processed_data.to_csv('processed_omics_data.csv', index=False)
       
       print("\n" + "="*60)
       print("Pipeline execution completed successfully!")
       print("="*60)
       
       return processed_data
   
   if __name__ == '__main__':
       processed_data = main()

Running from Command Line
~~~~~~~~~~~~~~~~~~~~~~~~~~

Save the above script as ``run_pipeline.py`` and execute:

.. code-block:: bash

   python run_pipeline.py

Advanced Usage: Training and Testing Data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For workflows requiring separate training and testing sets:

.. code-block:: python

   from synomics.processing import IntegrationPipeline
   
   # Create and configure pipeline
   pipeline = IntegrationPipeline.create_default_pipeline()
   
   # Load data
   data = pipeline.load_data('omics_data.csv')
   
   # Split data first
   train_data, test_data = pipeline.preprocessor.split_data(
       data, test_size=0.2, random_state=42
   )
   
   # Fit pipeline on training data only
   pipeline.fit(train_data)
   train_processed = pipeline.get_processed_data()
   
   # Transform test data using fitted pipeline
   test_processed = pipeline.transform(test_data)
   
   # Save the fitted pipeline
   pipeline.save_pipeline('fitted_pipeline')
   
   print(f"Train set: {train_processed.shape}")
   print(f"Test set: {test_processed.shape}")

Advanced Usage: Reusing Saved Pipelines
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Load and reuse a previously saved pipeline:

.. code-block:: python

   from synomics.processing import IntegrationPipeline
   
   # Load the saved pipeline
   pipeline = IntegrationPipeline()
   pipeline.load_pipeline('fitted_pipeline')
   
   # Load new data
   new_data = pipeline.load_data('new_omics_data.csv')
   
   # Transform using the same preprocessing steps
   new_processed = pipeline.transform(new_data)
   
   # The new data is now preprocessed consistently
   # with the original training data
   print(f"New processed data: {new_processed.shape}")

API Reference
-------------

.. note::

   Detailed API documentation will be available in future releases.

DataPreprocessor Class
~~~~~~~~~~~~~~~~~~~~~~

**Methods:**

* ``load_data(filepath, **kwargs)``: Load data from file
* ``handle_missing(data, strategy, fill_value)``: Handle missing values
* ``remove_outliers(data, threshold, method)``: Remove statistical outliers
* ``normalize(data, method, feature_range)``: Normalize numeric features
* ``encode_categorical(data, method, columns)``: Encode categorical variables
* ``apply_pca(data, n_components, columns)``: Apply PCA for dimensionality reduction
* ``split_data(data, test_size, random_state, stratify_column)``: Split data
* ``get_data_summary(data)``: Get dataset statistics

IntegrationPipeline Class
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Methods:**

* ``__init__(config)``: Initialize pipeline with configuration
* ``add_step(step_name, params)``: Add a preprocessing step
* ``load_data(filepath, **kwargs)``: Load data through pipeline
* ``fit(data)``: Fit pipeline on training data
* ``transform(data)``: Transform new data using fitted pipeline
* ``fit_transform(data)``: Fit and transform in one step
* ``get_processed_data()``: Get the processed data
* ``save_pipeline(filepath)``: Save pipeline configuration and transformers
* ``load_pipeline(filepath)``: Load saved pipeline
* ``get_pipeline_summary()``: Get pipeline configuration summary
* ``print_pipeline_summary()``: Print formatted pipeline summary

**Class Methods:**

* ``create_default_pipeline()``: Create default preprocessing pipeline
* ``create_genomics_pipeline()``: Create genomics-optimized pipeline

Best Practices
--------------

1. **Understand Your Data**: Always perform exploratory data analysis before preprocessing
2. **Handle Missing Data Carefully**: Choose imputation strategies appropriate for your data type
3. **Scale Appropriately**: Different synthesis methods may require different scaling approaches
4. **Preserve Data Characteristics**: Ensure preprocessing doesn't remove important data patterns
5. **Document Transformations**: Keep track of all preprocessing steps for reproducibility

See Also
--------

* :doc:`synthesizer` - Generate synthetic data using preprocessed data
* :doc:`evaluation` - Evaluate the quality of preprocessed and synthetic data
