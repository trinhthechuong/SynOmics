Welcome to SynOmics documentation!
===================================

**SynOmics** is a Python library for synthetic and omics data analysis. 
It provides tools for generating synthetic transcriptomics and clinical data, analyzing gene expression, 
and integrating with bioinformatics workflows.

.. note::

   This project is under active development.

Abstract
--------

SynOmics is a comprehensive framework for generating and evaluating synthetic transciptomics data. 
The library consists of three main modules:

1. **Processing Module**: Preprocessing (imputation and scaling), Metadata tools, and Gene Query utilities
2. **Synthesizers Module**: Multiple state-of-the-art synthesis methods (CT-GAN, TVAE, Gaussian Copula, SynthPop, Avatars)
3. **Evaluation Module**: Comprehensive assessment tools for both utility and privacy preservation of synthetic data

Contents
--------

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   usage
   examples

.. toctree::
   :maxdepth: 2
   :caption: Modules

   modules/processing
   modules/synthesizers
   modules/evaluation

.. toctree::
   :maxdepth: 2
   :caption: API Documentation

   api

.. toctree::
   :maxdepth: 2
   :caption: Development

   contributing
   changelog

Indices and tables
------------------

* :ref:`genindex`
* :ref:`search`
