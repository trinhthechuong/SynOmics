Synthesizer Module
==================

The Synthesizer module provides multiple state-of-the-art methods for generating synthetic omics data. 
Each method offers different strengths and is suitable for various data types and use cases.

Overview
--------

The Synthesizer module includes five powerful synthesis methods:

1. **CT-GAN**: Conditional Tabular Generative Adversarial Network
2. **TVAE**: Tabular Variational AutoEncoder
3. **Gaussian Copula**: Statistical copula-based synthesis
4. **SynthPop**: Synthetic population generation
5. **Avatars**: Privacy-preserving synthetic data generation

Each method can be used to generate high-quality synthetic data that preserves the statistical properties 
and relationships present in the original omics data.

Synthesis Methods
-----------------

CT-GAN (Conditional Tabular GAN)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

CT-GAN is a deep learning-based method using Generative Adversarial Networks specifically designed for tabular data.

**Key Features:**

* Handles mixed data types (continuous and categorical)
* Preserves complex relationships between features
* Mode-specific normalization for continuous columns
* Conditional generation capabilities

**When to Use:**

* Large datasets with complex patterns
* Mixed data types
* When capturing non-linear relationships is critical

**Usage Example:**

.. code-block:: python

   from synomics.synthesizer import CTGAN
   
   # Initialize CT-GAN
   synthesizer = CTGAN(
       epochs=300,
       batch_size=500,
       generator_dim=(256, 256),
       discriminator_dim=(256, 256)
   )
   
   # Fit the model
   synthesizer.fit(preprocessed_data)
   
   # Generate synthetic data
   synthetic_data = synthesizer.generate(n_samples=1000)

TVAE (Tabular Variational AutoEncoder)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TVAE uses a variational autoencoder architecture optimized for tabular data synthesis.

**Key Features:**

* Probabilistic latent space representation
* Efficient for moderate-sized datasets
* Good reconstruction of distributional properties
* Faster training compared to GANs

**When to Use:**

* Medium-sized datasets
* When interpretability of latent space is important
* Faster synthesis requirements

**Usage Example:**

.. code-block:: python

   from synomics.synthesizer import TVAE
   
   # Initialize TVAE
   synthesizer = TVAE(
       epochs=300,
       batch_size=500,
       compress_dims=(128, 128),
       decompress_dims=(128, 128)
   )
   
   # Fit the model
   synthesizer.fit(preprocessed_data)
   
   # Generate synthetic data
   synthetic_data = synthesizer.generate(n_samples=1000)

Gaussian Copula
~~~~~~~~~~~~~~~

A statistical method that models the correlation structure using copulas and marginal distributions.

**Key Features:**

* Fast and interpretable
* No training required
* Captures correlation structures effectively
* Works well with smaller datasets

**When to Use:**

* Smaller datasets
* When computational resources are limited
* When explainability is paramount
* Gaussian-like data distributions

**Usage Example:**

.. code-block:: python

   from synomics.synthesizer import GaussianCopula
   
   # Initialize Gaussian Copula
   synthesizer = GaussianCopula()
   
   # Fit the model
   synthesizer.fit(preprocessed_data)
   
   # Generate synthetic data
   synthetic_data = synthesizer.generate(n_samples=1000)

SynthPop
~~~~~~~~

A sequential modeling approach that generates synthetic populations by fitting conditional distributions.

**Key Features:**

* Sequential conditional modeling
* Preserves local dependencies
* Flexible parametric and non-parametric methods
* Handles missing data naturally

**When to Use:**

* Survey data and population studies
* When maintaining specific statistical properties is critical
* Hierarchical data structures

**Usage Example:**

.. code-block:: python

   from synomics.synthesizer import SynthPop
   
   # Initialize SynthPop
   synthesizer = SynthPop(
       method='cart',  # Classification and Regression Trees
       visit_sequence=None  # Auto-determine sequence
   )
   
   # Fit the model
   synthesizer.fit(preprocessed_data)
   
   # Generate synthetic data
   synthetic_data = synthesizer.generate(n_samples=1000)

Avatars
~~~~~~~

A privacy-preserving synthesis method designed to protect individual privacy while maintaining data utility.

**Key Features:**

* Built-in privacy guarantees
* Differential privacy mechanisms
* Balance between privacy and utility
* Suitable for sensitive omics data

**When to Use:**

* Highly sensitive data (e.g., patient genomic data)
* When regulatory compliance requires privacy preservation
* Data sharing scenarios

**Usage Example:**

.. code-block:: python

   from synomics.synthesizer import Avatars
   
   # Initialize Avatars with privacy budget
   synthesizer = Avatars(
       epsilon=1.0,  # Privacy budget
       k_anonymity=5
   )
   
   # Fit the model
   synthesizer.fit(preprocessed_data)
   
   # Generate synthetic data
   synthetic_data = synthesizer.generate(n_samples=1000)

Comparison of Methods
---------------------

.. list-table:: Method Comparison
   :header-rows: 1
   :widths: 20 15 15 15 15 20

   * - Method
     - Data Size
     - Training Time
     - Quality
     - Privacy
     - Best For
   * - CT-GAN
     - Large
     - High
     - Excellent
     - Medium
     - Complex patterns
   * - TVAE
     - Medium
     - Medium
     - Very Good
     - Medium
     - Balanced approach
   * - Gaussian Copula
     - Small-Medium
     - Low
     - Good
     - Medium
     - Quick synthesis
   * - SynthPop
     - Medium
     - Medium
     - Very Good
     - Medium
     - Survey data
   * - Avatars
     - Any
     - Medium
     - Good
     - High
     - Privacy-critical

Common Parameters
-----------------

Most synthesizers share common parameters:

* **n_samples**: Number of synthetic samples to generate
* **random_state**: Random seed for reproducibility
* **verbose**: Control logging output

Advanced Usage
--------------

Conditional Generation
~~~~~~~~~~~~~~~~~~~~~~

Generate synthetic data conditioned on specific features:

.. code-block:: python

   # Generate samples with specific conditions
   conditions = {
       'age_group': 'elderly',
       'disease_status': 'positive'
   }
   
   synthetic_data = synthesizer.generate(
       n_samples=500,
       conditions=conditions
   )

Batch Generation
~~~~~~~~~~~~~~~~

Generate large datasets in batches:

.. code-block:: python

   # Generate in batches to manage memory
   all_synthetic_data = []
   
   for i in range(10):
       batch = synthesizer.generate(n_samples=1000)
       all_synthetic_data.append(batch)

Best Practices
--------------

1. **Choose the Right Method**: Consider dataset size, complexity, and privacy requirements
2. **Tune Hyperparameters**: Each method has parameters that can be optimized
3. **Validate Synthetic Data**: Always evaluate using the Evaluation module
4. **Use Preprocessed Data**: Apply appropriate preprocessing before synthesis
5. **Monitor Training**: Track metrics during training for deep learning methods
6. **Set Random Seeds**: Ensure reproducibility in your experiments

See Also
--------

* :doc:`preprocessing` - Prepare data before synthesis
* :doc:`evaluation` - Evaluate synthetic data quality
