Contributing to SynOmics
========================

We welcome contributions to SynOmics! This document provides guidelines for contributing to the project.

Getting Started
---------------

1. Fork the repository on GitHub
2. Clone your fork locally:

.. code-block:: console

   $ git clone https://github.com/YOUR_USERNAME/SynOmics.git
   $ cd SynOmics

3. Create a virtual environment and install dependencies:

.. code-block:: console

   $ python -m venv .venv
   $ source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   $ pip install -e ".[dev]"

Development Workflow
--------------------

1. Create a new branch for your feature:

.. code-block:: console

   $ git checkout -b feature/your-feature-name

2. Make your changes and add tests
3. Run tests to ensure everything works:

.. code-block:: console

   $ pytest

4. Commit your changes:

.. code-block:: console

   $ git commit -m "Add feature: description"

5. Push to your fork and submit a pull request

Code Style
----------

* Follow PEP 8 guidelines
* Use type hints where appropriate
* Write docstrings for all public functions and classes
* Keep functions focused and concise

Testing
-------

* Write tests for all new features
* Ensure all tests pass before submitting a pull request
* Aim for high code coverage

Documentation
-------------

* Update documentation for any API changes
* Add examples for new features
* Keep documentation clear and concise

Questions?
----------

If you have questions about contributing, please open an issue on GitHub.
