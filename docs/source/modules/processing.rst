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

Preprocessing
~~~~~~~~~~~~~

.. autoclass:: SynOmics.processing.preprocessing.DataProcessor
   :members:
   :undoc-members:
   :show-inheritance:

Metadata
~~~~~~~~

.. autoclass:: SynOmics.processing.metadata.MetaData
   :members:
   :undoc-members:
   :show-inheritance:

Gene Query
~~~~~~~~~~

.. autoclass:: SynOmics.processing.gene_query.GeneQuery
   :members:
   :undoc-members:
   :show-inheritance:

Integration Pipeline
~~~~~~~~~~~~~~~~~~~~

.. autoclass:: SynOmics.processing.data_integration_pipeline.DataIntegrationPipeline
   :members:
   :undoc-members:
   :show-inheritance:
