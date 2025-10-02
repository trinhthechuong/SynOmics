Usage
=====

.. _installation:

Installation
------------

To use SynOmics, first install it using pip:

.. code-block:: console

   (.venv) $ pip install synomics

Quick Start
-----------

Here's a simple example to get you started with SynOmics:

.. code-block:: python

   import synomics
   
   # Generate a synthetic DNA sequence
   dna_sequence = synomics.generate_synthetic_sequence(length=100, sequence_type="DNA")
   print(f"Generated DNA: {dna_sequence}")
   
   # Generate a synthetic RNA sequence
   rna_sequence = synomics.generate_synthetic_sequence(length=100, sequence_type="RNA")
   print(f"Generated RNA: {rna_sequence}")
   
   # Generate a synthetic protein sequence
   protein_sequence = synomics.generate_synthetic_sequence(length=100, sequence_type="protein")
   print(f"Generated protein: {protein_sequence}")

Core Features
-------------

SynOmics provides several core features for working with synthetic genomics data:

Sequence Generation
~~~~~~~~~~~~~~~~~~~

Generate synthetic biological sequences for testing and research purposes:

* DNA sequences
* RNA sequences
* Protein sequences

For more detailed examples, see the :doc:`examples` section.

API Overview
------------

SynOmics provides a simple and intuitive API for working with synthetic genomics data.

For detailed API documentation, see the :doc:`api` section.

