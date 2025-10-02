Evaluation Module
=================

The Evaluation module provides comprehensive tools to assess the quality of synthetic data along two critical dimensions: 
**Utility** and **Privacy**. This ensures that synthetic data maintains the statistical properties of the original data 
while protecting individual privacy.

Overview
--------

When generating synthetic data, it is crucial to evaluate:

1. **Utility**: How well the synthetic data preserves the statistical properties and usefulness of the original data
2. **Privacy**: How effectively the synthetic data protects individual-level information from the original dataset

The Evaluation module provides metrics and visualizations for both aspects.

Part 1: Utility Evaluation
---------------------------

Utility evaluation assesses how well synthetic data can substitute for real data in downstream analyses.

Statistical Similarity Metrics
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Univariate Statistics**

Compare distributions of individual features:

* **Mean and Standard Deviation**: Compare central tendency and spread
* **Kolmogorov-Smirnov Test**: Test distribution similarity
* **Chi-Square Test**: For categorical variables
* **Jensen-Shannon Divergence**: Measure distribution distance

**Multivariate Statistics**

Assess relationships between features:

* **Correlation Matrices**: Compare correlation structures
* **Covariance Matrices**: Evaluate joint distributions
* **Principal Component Analysis**: Compare PCA projections
* **Mutual Information**: Measure feature dependencies

Machine Learning Utility
~~~~~~~~~~~~~~~~~~~~~~~~

Evaluate synthetic data through ML model performance:

* **Train on Synthetic, Test on Real (TSTR)**: Train models on synthetic data and test on real data
* **Train on Real, Test on Synthetic (TRTS)**: Train models on real data and test on synthetic data
* **Feature Importance**: Compare feature importance rankings
* **Model Performance**: Classification/regression metrics (accuracy, F1, RMSE, etc.)

Visual Comparisons
~~~~~~~~~~~~~~~~~~

Graphical methods for intuitive assessment:

* **Distribution Plots**: Histograms and KDE plots
* **Box Plots**: Compare quartiles and outliers
* **Scatter Plots**: Visualize bivariate relationships
* **Heatmaps**: Compare correlation matrices
* **PCA Plots**: Visualize high-dimensional structure

Usage Example - Utility
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from synomics.evaluation import UtilityEvaluator
   
   # Initialize utility evaluator
   evaluator = UtilityEvaluator()
   
   # Compare distributions
   stats_report = evaluator.statistical_similarity(
       real_data=real_data,
       synthetic_data=synthetic_data
   )
   
   # Evaluate ML utility
   ml_report = evaluator.ml_efficiency(
       real_data=real_data,
       synthetic_data=synthetic_data,
       target_column='outcome',
       task='classification'
   )
   
   # Generate visual comparisons
   evaluator.plot_distributions(
       real_data=real_data,
       synthetic_data=synthetic_data,
       columns=['age', 'gene_expression_1', 'gene_expression_2']
   )
   
   # Generate comprehensive report
   utility_score = evaluator.overall_utility_score(
       real_data=real_data,
       synthetic_data=synthetic_data
   )
   
   print(f"Overall Utility Score: {utility_score:.3f}")

Part 2: Privacy Evaluation
---------------------------

Privacy evaluation ensures that synthetic data doesn't leak sensitive information about individuals in the original dataset.

Distance-Based Privacy Metrics
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Nearest Neighbor Distance Ratio (NNDR)**

Measures how close synthetic records are to real records:

* **5th Percentile Distance**: Check if synthetic records are too similar to real ones
* **Distance Ratio**: Compare distances to nearest real vs. nearest synthetic neighbors

**Distance to Closest Record (DCR)**

Evaluates the minimum distance between synthetic and real records:

* Helps identify potential memorization
* Lower distances indicate higher privacy risk

Membership Inference Attacks
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Test if an attacker can determine whether a record was in the training data:

* **Attack Success Rate**: Percentage of correctly identified members
* **Attack Advantage**: Performance above random guessing
* **Confidence Scores**: Measure attacker certainty

Attribute Inference Attacks
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Evaluate if sensitive attributes can be inferred:

* **Attribute Disclosure Risk**: Probability of inferring sensitive features
* **Feature Prediction Accuracy**: How well features can be predicted from others

Re-identification Risk
~~~~~~~~~~~~~~~~~~~~~~

Assess the risk of linking synthetic records back to real individuals:

* **k-Anonymity**: Ensure k similar records exist
* **l-Diversity**: Check diversity of sensitive attributes
* **t-Closeness**: Measure distribution similarity of sensitive attributes

Differential Privacy Metrics
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For methods with formal privacy guarantees:

* **Epsilon (ε) Budget**: Track privacy budget consumption
* **Delta (δ) Parameter**: Probability of privacy breach
* **Privacy Loss Distribution**: Analyze worst-case privacy guarantees

Usage Example - Privacy
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from synomics.evaluation import PrivacyEvaluator
   
   # Initialize privacy evaluator
   evaluator = PrivacyEvaluator()
   
   # Distance-based privacy
   dcr_score = evaluator.distance_to_closest_record(
       real_data=real_data,
       synthetic_data=synthetic_data
   )
   
   nndr_score = evaluator.nearest_neighbor_distance_ratio(
       real_data=real_data,
       synthetic_data=synthetic_data
   )
   
   # Membership inference attack
   mia_results = evaluator.membership_inference_attack(
       real_data=real_data,
       synthetic_data=synthetic_data,
       holdout_data=holdout_data
   )
   
   # Attribute inference risk
   aia_results = evaluator.attribute_inference_risk(
       real_data=real_data,
       synthetic_data=synthetic_data,
       sensitive_attributes=['diagnosis', 'genetic_marker']
   )
   
   # Re-identification risk
   reid_score = evaluator.reidentification_risk(
       real_data=real_data,
       synthetic_data=synthetic_data,
       quasi_identifiers=['age', 'gender', 'location']
   )
   
   # Overall privacy score
   privacy_score = evaluator.overall_privacy_score(
       real_data=real_data,
       synthetic_data=synthetic_data
   )
   
   print(f"Overall Privacy Score: {privacy_score:.3f}")

Comprehensive Evaluation
-------------------------

Combine utility and privacy for holistic assessment:

.. code-block:: python

   from synomics.evaluation import ComprehensiveEvaluator
   
   # Initialize comprehensive evaluator
   evaluator = ComprehensiveEvaluator()
   
   # Run full evaluation
   report = evaluator.evaluate(
       real_data=real_data,
       synthetic_data=synthetic_data,
       target_column='outcome',
       sensitive_attributes=['diagnosis'],
       quasi_identifiers=['age', 'gender']
   )
   
   # Generate detailed report
   evaluator.generate_report(
       report=report,
       output_path='evaluation_report.html'
   )
   
   # Plot utility vs privacy tradeoff
   evaluator.plot_utility_privacy_tradeoff(report)

Evaluation Metrics Summary
---------------------------

Utility Metrics
~~~~~~~~~~~~~~~

.. list-table:: Utility Metrics
   :header-rows: 1
   :widths: 30 50 20

   * - Metric
     - Description
     - Range
   * - Statistical Similarity
     - Distribution comparison (KS, JSD)
     - 0-1 (higher is better)
   * - Correlation Preservation
     - Correlation matrix similarity
     - 0-1 (higher is better)
   * - ML Efficiency (TSTR)
     - Model performance ratio
     - 0-1 (higher is better)
   * - Feature Importance
     - Feature ranking similarity
     - 0-1 (higher is better)

Privacy Metrics
~~~~~~~~~~~~~~~

.. list-table:: Privacy Metrics
   :header-rows: 1
   :widths: 30 50 20

   * - Metric
     - Description
     - Range
   * - DCR (Distance to Closest Record)
     - Minimum distance to real records
     - 0-∞ (higher is better)
   * - NNDR
     - Nearest neighbor distance ratio
     - 0-∞ (higher is better)
   * - MIA Success Rate
     - Membership inference accuracy
     - 0-1 (lower is better)
   * - Re-identification Risk
     - Probability of re-identification
     - 0-1 (lower is better)

Best Practices
--------------

1. **Evaluate Both Dimensions**: Always assess both utility and privacy
2. **Use Multiple Metrics**: No single metric captures all aspects
3. **Compare Across Methods**: Evaluate different synthesis approaches
4. **Set Thresholds**: Define acceptable utility and privacy levels
5. **Document Results**: Keep detailed records of evaluation results
6. **Iterate**: Use evaluation results to improve synthesis parameters
7. **Consider Context**: Privacy requirements vary by use case and regulations

Interpreting Results
--------------------

Utility-Privacy Tradeoff
~~~~~~~~~~~~~~~~~~~~~~~~

There is often a tradeoff between utility and privacy:

* **High utility, low privacy**: Synthetic data very similar to real data (potential privacy leaks)
* **Low utility, high privacy**: Very private but less useful synthetic data
* **Balanced approach**: Find optimal point for your application

Recommended Thresholds
~~~~~~~~~~~~~~~~~~~~~~

General guidelines (adjust based on your requirements):

* **Utility Score**: > 0.7 for acceptable quality
* **Privacy Score**: > 0.8 for sensitive data
* **DCR**: > 0.1 for adequate privacy
* **MIA Success Rate**: < 0.6 for acceptable privacy

See Also
--------

* :doc:`preprocessing` - Prepare data before synthesis
* :doc:`synthesizer` - Generate synthetic data to evaluate
