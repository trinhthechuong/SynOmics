Examples
========

This section provides practical examples of using SynOmics for various genomics tasks.

Basic Usage
-----------

Generating Synthetic DNA Sequences
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import synomics
   
   # Generate a 100 bp DNA sequence
   dna_seq = synomics.generate_synthetic_sequence(length=100, sequence_type="DNA")
   print(f"Generated DNA sequence: {dna_seq}")

Generating Synthetic RNA Sequences
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import synomics
   
   # Generate a 150 bp RNA sequence
   rna_seq = synomics.generate_synthetic_sequence(length=150, sequence_type="RNA")
   print(f"Generated RNA sequence: {rna_seq}")

Generating Synthetic Protein Sequences
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import synomics
   
   # Generate a 200 amino acid protein sequence
   protein_seq = synomics.generate_synthetic_sequence(length=200, sequence_type="protein")
   print(f"Generated protein sequence: {protein_seq}")

Advanced Examples
-----------------

Working with Sequence Data
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import synomics
   
   # Generate multiple sequences
   sequences = []
   for i in range(10):
       seq = synomics.generate_synthetic_sequence(length=100, sequence_type="DNA")
       sequences.append(seq)
   
   print(f"Generated {len(sequences)} sequences")

Error Handling
~~~~~~~~~~~~~~

.. code-block:: python

   import synomics
   
   try:
       # This will raise an error
       seq = synomics.generate_synthetic_sequence(length=100, sequence_type="invalid")
   except synomics.InvalidParameterError as e:
       print(f"Error: {e}")

Integration Examples
--------------------

Coming soon: Examples of integrating SynOmics with popular bioinformatics tools.
