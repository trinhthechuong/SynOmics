# Processing Module - Quick Start Guide

## Overview

The **Processing Module** is the first and foundational module of SynOmics. It provides comprehensive data preprocessing capabilities for preparing omics data before synthetic data generation.

## Components

### 1. DataPreprocessor (`data_processor.py`)
Core preprocessing functionality with individual methods for each task.

### 2. IntegrationPipeline (`data_integration_pipeline.py`)
Pipeline orchestration for chaining multiple preprocessing steps together.

## Quick Start

### Installation

```bash
pip install pandas numpy scikit-learn
```

### Basic Usage

```python
from synomics.processing import IntegrationPipeline

# Create a pipeline
pipeline = IntegrationPipeline.create_default_pipeline()

# Load and process data
data = pipeline.load_data('your_data.csv')
processed_data = pipeline.fit_transform(data)

# Save the pipeline
pipeline.save_pipeline('my_pipeline')
```

## Features

### DataPreprocessor Features

- ✅ Data loading (CSV, TSV, Excel)
- ✅ Missing value handling (mean, median, most_frequent, constant)
- ✅ Outlier detection and removal (Z-score, IQR methods)
- ✅ Data normalization (min-max, z-score, log)
- ✅ Categorical encoding (one-hot, label)
- ✅ PCA for dimensionality reduction
- ✅ Data splitting with stratification
- ✅ Comprehensive data summaries

### IntegrationPipeline Features

- ✅ Pipeline configuration management
- ✅ Sequential step execution
- ✅ Pipeline serialization (save/load)
- ✅ Preset pipelines (default, genomics-optimized)
- ✅ Pipeline monitoring and summary
- ✅ Reproducible workflows

## Example Workflows

### Workflow 1: Simple Preprocessing

```python
from synomics.processing import DataPreprocessor

preprocessor = DataPreprocessor()
data = preprocessor.load_data('data.csv')
data = preprocessor.handle_missing(data, strategy='mean')
data = preprocessor.normalize(data, method='min-max')
data = preprocessor.encode_categorical(data, method='onehot')
```

### Workflow 2: Pipeline with Configuration

```python
from synomics.processing import IntegrationPipeline

config = {
    'steps': [
        {'name': 'handle_missing', 'params': {'strategy': 'mean'}},
        {'name': 'remove_outliers', 'params': {'threshold': 3.0}},
        {'name': 'normalize', 'params': {'method': 'min-max'}},
        {'name': 'encode_categorical', 'params': {'method': 'onehot'}}
    ]
}

pipeline = IntegrationPipeline(config=config)
data = pipeline.load_data('data.csv')
processed_data = pipeline.fit_transform(data)
```

### Workflow 3: Preset Pipelines

```python
from synomics.processing import IntegrationPipeline

# For general data
pipeline = IntegrationPipeline.create_default_pipeline()

# For genomics data (includes log transform and PCA)
genomics_pipeline = IntegrationPipeline.create_genomics_pipeline()

data = pipeline.load_data('data.csv')
processed_data = pipeline.fit_transform(data)
```

### Workflow 4: Save and Reuse Pipelines

```python
from synomics.processing import IntegrationPipeline

# Train a pipeline
pipeline = IntegrationPipeline.create_default_pipeline()
pipeline.fit(train_data)
pipeline.save_pipeline('trained_pipeline')

# Later, load and use it
new_pipeline = IntegrationPipeline()
new_pipeline.load_pipeline('trained_pipeline')
new_processed = new_pipeline.transform(new_data)
```

## Documentation

For complete documentation, see: `docs/source/modules/preprocessing.rst`

Or build the documentation:

```bash
cd docs
make html
```

Then open `docs/build/html/modules/preprocessing.html` in your browser.

## Module Architecture

```
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
```

## Testing

Run the test script to verify functionality:

```bash
python tests/test_processing_module.py
```

## Next Steps

After preprocessing your data with the Processing Module:

1. Use the **Synthesizer Module** to generate synthetic data
2. Use the **Evaluation Module** to assess synthetic data quality

## Support

For issues or questions, please refer to the documentation or open an issue on GitHub.
