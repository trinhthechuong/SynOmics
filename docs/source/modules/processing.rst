Processing Module
=================

Overview
--------

The processing module provides utilities for preparing omics and clinical datasets and an end-to-end
integration pipeline. It includes:

- preprocessing: data cleaning, encoding, scaling, KNN-based imputation with indicators
- metadata: automatic feature-type classification and helpers for metadata IO/mapping
- gene_query: Ensembl-to-HUGO mapping and duplicate gene checking via MyGeneInfo
- DataIntegrationPipeline: a configurable pipeline combining the above features

Quick Start Examples
--------------------

Preprocessing: impute categorical, ordinal, and numeric data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import pandas as pd
   from SynOmics.processing.preprocessing import DataProcessor

   raw = pd.DataFrame({
       "sex": ["M", "F", None],
       "stage": ["low", "medium", "high"],
       "age": [20, None, 40]
   })

   out = DataProcessor.data_imputation(
       data=raw,
       dummy_cat_columns=["sex"],        # one-hot encode
       ordinal_cat_columns=["stage"],    # ordinal encode
       numerical_columns=["age"],        # scale numeric
       scaler="minmax",
       n_neighbors=3,
       add_indicators=True,
       verbose=False
   )

   # Columns typically include decoded categories, inverse-scaled numeric, and missing indicators
   print(sorted(out.columns))

GeneQuery: map Ensembl IDs to HUGO and find duplicate genes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import pandas as pd
   from SynOmics.processing.gene_query import GeneQuery

   # Example feature matrix with Ensembl IDs as columns (trailing version integers allowed)
   expr = pd.DataFrame({
       "ENSG00000141510.15": [1.2, 3.4, 5.6],
       "ENSG00000171862.9":  [1.2, 3.4, 5.6],   # intentionally identical to create duplicates
       "ENSG00000157764.13": [7.8, 9.0, None],
   })

   gq = GeneQuery(
       fields=["symbol"],
       scopes=["ensemblgene"],
       species=["human"],
       output_dir="outputs"
   )

   # 1) Convert Ensembl to HUGO symbol
   mapping_df = gq.convert_genes(expr)

   # 2) Group genes with identical expression profiles and annotate symbols
   dup_groups, dup_symbols = gq.check_duplicates(expr)

Metadata: classify and export feature types
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import pandas as pd
   from SynOmics.processing.metadata import MetaData

   df = pd.DataFrame({
       "age": [20, 40, 60, None],
       "sex": ["M", "F", "M", None],
       "stage": ["I", "II", "III", "II"],      # optionally treat as ordinal via parameter
       "flag": [0, 1, 0, 1]                     # binary treated as dummy categorical
   })

   # 1) Classify features
   dummy_cols, num_cols = MetaData.classify_features_types(
       data=df,
       threshold_unique_values=10,
       ordinal_features=["stage"]   # optional: enforce ordinal
   )

   # 2) Build a metadata dictionary (unclassified features are warned)
   meta = MetaData.get_metadata(
       data=df,
       threshold_unique_values=10,
       id_columns=None,
       ordinal_features=["stage"]
   )

   # 3) Save / load metadata as JSON
   MetaData.save(meta, output_dir="outputs", filename="feature_metadata")
   meta_loaded = MetaData.load("outputs/feature_metadata.json")

   # 4) Grouping helper for downstream use
   grouped = MetaData.grouping_features_astype(df, meta_loaded)

   # 5) Map to SDV-style metadata
   sdv_meta = MetaData.metadata_as_SDV(df, meta_loaded)

End-to-end: DataIntegrationPipeline
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import pandas as pd
   from SynOmics.processing.data_integration_pipeline import DataIntegrationPipeline

   # Example clinical and transcriptomics inputs (toy)
   clinical = pd.DataFrame({
       "PATIENT_ID": ["P1", "P2", "P3"],
       "age": [45, None, 60],
       "sex": ["M", "F", None],
       "stage": ["I", "II", "III"]
   })

   transcriptomics = pd.DataFrame({
       "SAMPLE_ID": ["P1", "P2", "P4"],
       "ENSG00000141510.15": [1.2, 3.4, None],   # example Ensembl IDs
       "ENSG00000157764.13": [7.8, 9.0, 1.1]
   })

   pipeline = DataIntegrationPipeline(output_dir="outputs", logger="demo")

   results = pipeline.run_pipeline(
       clinical_data=clinical,
       transcriptomics_data=transcriptomics,
       clinical_id_column="PATIENT_ID",
       transcriptomics_id_column="SAMPLE_ID",
       integration_id_column="PATIENT_ID",
       steps_config={
           "remove_undefined": True,
           "remove_duplicates": True,
           "remove_overmissing_samples": True,
           "check_duplicate_genes": True,   # internet access required
           "mapping_genes": True,           # internet access required
           "feature_engineering": True,
           "integrate_data": True
       },
       overmissing_samples_threshold=50.0,
       overmissing_features_threshold=50.0,
       unique_threshold=10,
       scaler="minmax",
       n_neighbors=5,
       ordinal_cat_columns=["stage"],
       add_indicators=True,
       verbose=False
   )

   processed_clinical = results["processed_clinical"]
   processed_transcriptomics = results["processed_transcriptomics"]
   integrated = results["integrated_data"]  # may be None if integration is disabled

API: Classes and Methods
------------------------

Docstrings from your code are rendered below for convenience.

Preprocessing (DataProcessor)
-----------------------------

Class: DataProcessor
~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

    DataProcessor provides static methods for preprocessing, encoding, imputing, and engineering features
    in omics or clinical datasets.

    This class enables duplicate removal, missing value filtering, encoding of categorical features,
    normalization, KNN imputation, and feature engineering classification.

    Methods are tailored for pandas DataFrame workflows in bioinformatics and genomics.

Method: remove_duplications
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

    Remove duplicate rows or columns from the DataFrame.

    Args:
        data (pd.DataFrame): Input DataFrame.
        axis (int): 0 to remove duplicate rows, 1 to remove duplicate columns.

    Returns:
        pd.DataFrame: DataFrame with duplicates removed.

    Raises:
        TypeError: If input is not a pandas DataFrame.
        ValueError: If axis is not 0 or 1.
        RuntimeError: On error during duplicate removal.

Method: remove_unknown_entities
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

    Remove rows where the identifier column contains missing values.

    Args:
        data (pd.DataFrame): Input DataFrame.
        id_column (str): Name of the identifier column.

    Returns:
        pd.DataFrame: Filtered DataFrame.

    Raises:
        TypeError: If input is not a pandas DataFrame.
        KeyError: If id_column is not in DataFrame.

Method: remove_overmissing_entities
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

    Remove rows (entities) with missing value percentage above a threshold.

    Args:
        data (pd.DataFrame): Input DataFrame.
        threshold (float): Percentage threshold (0-100).

    Returns:
        pd.DataFrame: DataFrame with over-missing entities removed.

    Raises:
        TypeError: If input is not a pandas DataFrame.
        ValueError: If threshold is not between 0 and 100.

Method: find_missing_percent
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

    Calculate the percentage of missing values for each column.

    Args:
        data (pd.DataFrame): Input DataFrame.

    Returns:
        pd.DataFrame: DataFrame with columns 'ColumnName' and 'PercentMissing'.

    Raises:
        TypeError: If input is not a pandas DataFrame.
        RuntimeError: On error during calculation.

Method: remove_overmissing_features
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

    Remove columns (features) with missing value percentage above a threshold.

    Args:
        data (pd.DataFrame): Input DataFrame.
        threshold (float): Percentage threshold (0-100).

    Returns:
        pd.DataFrame: DataFrame with over-missing features removed.

    Raises:
        TypeError: If input is not a pandas DataFrame.
        ValueError: If threshold is not between 0 and 100.

Method: encode_dummy_features
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

    Encode categorical features into dummy/one-hot columns.

    Args:
        data (pd.DataFrame): DataFrame with categorical features.

    Returns:
        pd.DataFrame: Dummy-encoded DataFrame.

    Raises:
        TypeError: If input is not a pandas DataFrame.
        ValueError: If encoding fails.

Method: encode_ordinal_features
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

    Encode ordinal categorical features using OrdinalEncoder.

    Args:
        data (pd.DataFrame): DataFrame with ordinal categorical features.

    Returns:
        Tuple[pd.DataFrame, OrdinalEncoder]: Encoded DataFrame and fitted encoder.

    Raises:
        TypeError: If input is not a pandas DataFrame.
        ValueError: If encoding fails.

Method: standardization
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

    Standardize numerical features using specified scaler.

    Args:
        data (pd.DataFrame): DataFrame with numerical features.
        scaler (str): Scaler type ('standard', 'minmax', or 'robust').

    Returns:
        Tuple[pd.DataFrame, BaseEstimator]: Scaled DataFrame and scaler object.

    Raises:
        ValueError: If scaler type is invalid.
        TypeError: If input is not a pandas DataFrame.
        RuntimeError: If scaling fails.

Method: knn_imputer
~~~~~~~~~~~~~~~~~~~

.. code-block:: text

    Impute missing values using KNNImputer, with special handling for dummy and ordinal features.

    Args:
        data (pd.DataFrame): Preprocessed DataFrame.
        dummy_cat_columns (list): List of dummy categorical feature names.
        ordinal_cat_columns (List, optional): List of ordinal categorical feature names.
        n_neighbors (int): Number of neighbors for KNN.
        add_indicators (bool, optional): Whether to add missing indicators.
        **kwargs: Additional KNNImputer arguments.

    Returns:
        pd.DataFrame: DataFrame with imputed values and indicators.

    Raises:
        TypeError: On invalid input types.
        ValueError: On imputation errors.

Method: extract_missingindicator_columns
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

    Extract columns indicating missingness from imputed DataFrame.

    Args:
        data (pd.DataFrame): DataFrame after imputation.

    Returns:
        pd.DataFrame: DataFrame with only missing indicator columns.

    Raises:
        TypeError: If input is not a pandas DataFrame.
        ValueError: On extraction errors.

Method: inverse_dummy_features
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

    Decode dummy-encoded categorical features back to original categories.

    Args:
        data (pd.DataFrame): DataFrame with dummy-encoded features.
        dummy_cat_columns (list): List of dummy categorical feature names.

    Returns:
        pd.DataFrame: DataFrame with decoded categorical columns.

    Raises:
        TypeError: On invalid input types or empty list.
        ValueError: On decoding errors.

Method: inverse_ordinal_features
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

    Decode ordinal categorical features from encoded values back to original categories.

    Args:
        data (pd.DataFrame): DataFrame with encoded ordinal features.
        encoder (OrdinalEncoder): Fitted ordinal encoder.

    Returns:
        pd.DataFrame: Decoded ordinal categorical features.

    Raises:
        AttributeError: If encoder is not initialized.
        TypeError: If input is not a DataFrame.
        ValueError: On decoding errors.

Method: inverse_standardization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

    Undo normalization/standardization on numerical features.

    Args:
        data (pd.DataFrame): DataFrame with normalized features.
        scaler (BaseEstimator): Fitted scaler.

    Returns:
        pd.DataFrame: DataFrame with original scale restored.

    Raises:
        AttributeError: If scaler is not initialized.
        TypeError: If input is not a DataFrame.
        ValueError: On inverse normalization errors.

Method: data_imputation
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

    Perform full preprocessing and KNN imputation, including encoding, normalization, and postprocessing.

    Args:
        data (pd.DataFrame): Input DataFrame.
        dummy_cat_columns (List, optional): Dummy categorical columns.
        ordinal_cat_columns (List, optional): Ordinal categorical columns.
        numerical_columns (List, optional): Numerical columns.
        scaler (str, optional): Scaler type ('minmax', 'standard', 'robust').
        n_neighbors (int, optional): KNN neighbors.
        add_indicators (bool, optional): Add missing indicators.
        verbose (bool, optional): Print progress.
        **kwargs: Additional KNNImputer arguments.

    Returns:
        pd.DataFrame: DataFrame after imputation and decoding.

    Raises:
        TypeError: On invalid input.
        ValueError: On missing columns or errors.

Method: feature_engineering
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

    Perform feature engineering for omics or clinical data:
    removes over-missing features, classifies feature types, and imputes missing data.

    Args:
        data (pd.DataFrame): Input DataFrame.
        data_type (str): Type of data ('transcriptomics' or 'clinical').
        overmissing_threshold (float, optional): Threshold for missingness to remove features.
        ordinal_cat_columns (List, optional): List of known ordinal categorical columns.
        unique_threshold (int, optional): Threshold for unique values to classify dummy features.
        scaler (str, optional): Scaler type for normalization.
        n_neighbors (int, optional): KNN neighbors.
        add_indicators (bool, optional): Add missing indicators.
        verbose (bool, optional): Print progress.
        **kwargs: Additional arguments for imputation.

    Returns:
        tuple: (processed DataFrame, list of numerical features, list of dummy categorical features)

    Raises:
        TypeError: On invalid input.
        ValueError: On classification or processing errors.

Metadata
~~~~~~~~

Note: The following docstrings are taken directly from metadata_handler.py. Some methods in the script did not
include docstrings; those are noted accordingly.

Class: MetaData
~~~~~~~~~~~~~~~

.. code-block:: text

    (No class-level docstring provided in script.)

Method: classify_features_types
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

    (No docstring provided in script.)

Method: get_metadata
~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

    (No docstring provided in script.)

Method: grouping_features_astype
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

    Extract column type metadata from a JSON file and assign columns to corresponding types.

    Args:
        data (pd.DataFrame): DataFrame used to filter available columns.
        metadata (str): metadata dictionary.

    Returns:
        dict: Dictionary with keys 'numerical', 'ordinal_categorical', 'dummy_categorical', and
            'missing_categorical', mapping to lists of column names.

    Raises:
        FileNotFoundError: If the metadata file is not found.
        json.JSONDecodeError: If the metadata file is not a valid JSON.

Method: metadata_as_SDV
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

    Extract column type metadata from a JSON file and assign columns to corresponding types follow SDV library format.

    Args:
        data (pd.DataFrame): DataFrame used to filter available columns.
        metadata (str): metadata dictionary.

    Returns:
        dict: Dictionary followed SDV format.

    Raises:
        FileNotFoundError: If the metadata file is not found.
        json.JSONDecodeError: If the metadata file is not a valid JSON.

Method: get_column_indices
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

    Get indices of columns in a given list in a given dataframe.

    Args:
        data (pd.DataFrame): The DataFrame containing columns extracted indices.
        column_list (list): List of columns.

    Returns:
        np.array: Array containing the column indices.

    Raises:
        ValueError: If a specified column does not exist in the DataFrame.

Method: save
~~~~~~~~~~~~

.. code-block:: text

    (No docstring provided in script.)

Method: load
~~~~~~~~~~~~

.. code-block:: text

    Load metadata from a JSON file.

    Args:
        metadata_path (str): Path to the metadata JSON file.

    Returns:
        dict: Loaded metadata.
    
    Raises:
        FileNotFoundError: If the metadata file does not exist.
        json.JSONDecodeError: If the metadata file is not a valid JSON.

Gene Query
~~~~~~~~~~

Class: GeneQuery
~~~~~~~~~~~~~~~~

.. code-block:: text

    A class to query gene information using MyGeneInfo and convert Ensembl IDs to HUGO symbols.

    This class facilitates querying gene data, checking for duplicates, and mapping Ensembl gene IDs
    to HUGO symbols. Results are saved as JSON/CSV files, and operations are logged for debugging.

    Attributes:
        fields (List[str]): Fields to retrieve from MyGeneInfo (e.g., ["symbol"]).
        scopes (List[str]): Scopes for gene queries (e.g., ["ensembl.gene"]).
        species (List[str]): Species to query (e.g., ["human"]).
        output_dir (str): Directory to save results and logs.
        logger (logging.Logger): Logger instance for debugging and error tracking.

Method: __init__
~~~~~~~~~~~~~~~~

.. code-block:: text

    Initialize GeneQuery with query parameters and logging setup.

    Args:
        fields: Fields to retrieve from MyGeneInfo queries.
        scopes: Scopes defining the gene identifier types.
        species: Species to include in the query.
        output_dir: Directory to store output files and logs.

    Raises:
        RuntimeError: If the log file cannot be created due to permissions or path issues.

Method: gene_query
~~~~~~~~~~~~~~~~~~

.. code-block:: text

    Query gene information using MyGeneInfo.

    Args:
        genes_list: List of gene identifiers to query.
        **kwargs: Additional arguments for MyGeneInfo.querymany.

    Returns:
        List of dictionaries containing gene mapping information.

    Raises:
        ValueError: If the query fails due to network issues or invalid parameters.

Method: check_duplicates
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

    Identify and group duplicate genes based on expression values.

    Args:
        data: DataFrame with samples as rows and genes as columns.
        **kwargs: Additional arguments for gene_query.

    Returns:
        Tuple of two dictionaries:
        - Mapping of unique gene IDs to lists of duplicate gene IDs.
        - Mapping of unique gene IDs to their HUGO symbols.

    Raises:
        ValueError: If duplicate checking fails due to invalid data or query errors.

Method: convert_genes
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

    Convert Ensembl gene IDs to HUGO symbols.

    Args:
        data: DataFrame with Ensembl gene IDs as columns.
        **kwargs: Additional arguments for gene_query.

    Returns:
        DataFrame containing gene mapping information.

    Raises:
        ValueError: If conversion fails due to invalid input or query errors.

Method: _save_json
~~~~~~~~~~~~~~~~~~

.. code-block:: text

    Save a dictionary to a JSON file.

    Args:
        data: Dictionary to save.
        filename: Name of the JSON file.

Integration Pipeline
~~~~~~~~~~~~~~~~~~~~

Class: DataIntegrationPipeline
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

    End-to-end pipeline for processing and integrating clinical and transcriptomics data.

    This pipeline:
    - Cleans data (removes undefined IDs, deduplicates, filters over-missing samples)
    - Performs feature engineering (over-missing feature filtering, type classification, imputation)
    - Optionally maps Ensembl gene IDs to HUGO symbols
    - Integrates processed clinical and transcriptomics data on a common ID
    - Exports a feature metadata JSON and logs detailed progress for easy monitoring

    Args:
        output_dir (str): Directory where logs and outputs (e.g., feature_metadata.json) are saved.
        logger (str): Suffix for the log filename (e.g., Preprocess_{logger}.log).

    Returns:
        None

    Raises:
        OSError: If the output directory cannot be created.

Method: __init__
~~~~~~~~~~~~~~~~

.. code-block:: text

    Initialize the data integration pipeline and configure logging.

    Args:
        output_dir (str): Directory where logs and outputs are stored.
        logger (str): Suffix for the log filename.

    Returns:
        None

    Raises:
        OSError: If the output directory cannot be created.

Method: process_transcriptomics_data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

    Process raw transcriptomics data with configurable steps.

    Args:
        transcriptomics_data (pd.DataFrame): Raw transcriptomics data.
        transcriptomics_id_column (str): Column name for sample/patient IDs.
        steps_config (dict): Flags controlling which steps to run.
        overmissing_samples_threshold (float): Remove rows with missingness > threshold (0-100).
        overmissing_features_threshold (float): Remove columns with missingness > threshold (0-100).
        unique_threshold (int): Threshold to classify categorical features (not used for transcriptomics).
        scaler (str): Scaler type for numerical features ('minmax', 'standard', 'robust').
        n_neighbors (int): Number of neighbors for KNN imputation.
        add_indicators (bool): Whether to add missingness indicator columns during imputation.
        verbose (bool): Print progress from lower-level utilities.
        **kwargs: Additional keyword arguments forwarded to KNNImputer.

    Returns:
        pd.DataFrame: Processed transcriptomics data with imputed features and optional indicators.

    Raises:
        KeyError: If transcriptomics_id_column is not found in the input DataFrame.
        TypeError: If transcriptomics_data is not a pandas DataFrame.
        ValueError: On invalid thresholds or processing errors in underlying steps.

Method: process_clinical_data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

    Process raw clinical data with configurable steps.

    Args:
        clinical_data (pd.DataFrame): Raw clinical data.
        clinical_id_column (str): Column name for sample/patient IDs.
        steps_config (dict): Flags controlling which steps to run.
        overmissing_samples_threshold (float): Remove rows with missingness > threshold (0-100).
        overmissing_features_threshold (float): Remove columns with missingness > threshold (0-100).
        unique_threshold (int): Unique value threshold to classify categorical features.
        scaler (str): Scaler type for numerical features ('minmax', 'standard', 'robust').
        n_neighbors (int): Number of neighbors for KNN imputation.
        ordinal_cat_columns (list, optional): Known ordinal categorical columns.
        add_indicators (bool): Whether to add missingness indicator columns during imputation.
        verbose (bool): Print progress from lower-level utilities.
        **kwargs: Additional keyword arguments forwarded to KNNImputer.

    Returns:
        pd.DataFrame: Processed clinical data with imputed features and indicators.

    Raises:
        KeyError: If clinical_id_column is not found in clinical_data.
        TypeError: If clinical_data is not a pandas DataFrame.
        ValueError: On invalid thresholds or processing errors in underlying steps.

Method: integrate_data
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

    Integrate processed clinical and transcriptomics data on a common ID.

    Args:
        processed_clinical (pd.DataFrame): Processed clinical dataset.
        processed_transcriptomics (pd.DataFrame): Processed transcriptomics dataset.
        clinical_id_column (str): ID column in processed_clinical.
        transcriptomics_id_column (str): ID column in processed_transcriptomics.
        integration_id_column (str): Name for the common ID column after renaming.
        steps_config (dict): Flags controlling whether to integrate.

    Returns:
        pd.DataFrame or None: Integrated dataset if integration is enabled; otherwise None.

    Raises:
        KeyError: If required ID columns are missing in the provided DataFrames.
        TypeError: If inputs are not pandas DataFrames.

Method: run_pipeline
~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

    Run the full pipeline across transcriptomics and clinical data and optionally integrate them.

    Args:
        clinical_data (pd.DataFrame): Raw clinical data.
        transcriptomics_data (pd.DataFrame): Raw transcriptomics data.
        clinical_id_column (str): ID column name in clinical_data.
        transcriptomics_id_column (str): ID column name in transcriptomics_data.
        integration_id_column (str): Common ID column name for integration.
        steps_config (dict, optional): Dict specifying which steps to run; defaults enable all steps.
        overmissing_samples_threshold (float): Remove rows with missingness > threshold (0-100).
        overmissing_features_threshold (float): Remove columns with missingness > threshold (0-100).
        unique_threshold (int): Unique value threshold to classify categorical features (clinical).
        scaler (str): Scaler type for numerical features ('minmax', 'standard', 'robust').
        n_neighbors (int): Number of neighbors for KNN imputation.
        ordinal_cat_columns (list, optional): Ordinal categorical columns in clinical data.
        add_indicators (bool): Whether to add missingness indicator columns during imputation.
        verbose (bool): Print progress from lower-level utilities.
        **kwargs: Additional keyword arguments forwarded to KNNImputer.

    Returns:
        dict: Dictionary containing:
            - 'processed_clinical' (pd.DataFrame): Processed clinical data
            - 'processed_transcriptomics' (pd.DataFrame): Processed transcriptomics data
            - 'integrated_data' (pd.DataFrame or None): Integrated dataset if integration enabled

    Raises:
        TypeError: If inputs are not pandas DataFrames.
        KeyError: If required ID columns are missing.
        ValueError: On processing errors in underlying steps.
