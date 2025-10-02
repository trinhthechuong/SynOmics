"""
SynOmics - Python library for synthetic genomics and omics data analysis.
"""

__version__ = "0.1.0"


class InvalidParameterError(Exception):
    """Raised if a parameter is invalid."""
    pass


def generate_synthetic_sequence(length=100, sequence_type="DNA"):
    """
    Generate a synthetic biological sequence.

    :param length: Length of the sequence to generate.
    :type length: int
    :param sequence_type: Type of sequence - "DNA", "RNA", or "protein".
    :type sequence_type: str
    :raise synomics.InvalidParameterError: If the sequence type is invalid.
    :return: The generated sequence.
    :rtype: str
    """
    if sequence_type not in ["DNA", "RNA", "protein"]:
        raise InvalidParameterError(f"Invalid sequence type: {sequence_type}")
    
    # Placeholder implementation
    if sequence_type == "DNA":
        return "ATCG" * (length // 4)
    elif sequence_type == "RNA":
        return "AUCG" * (length // 4)
    else:
        return "ACDEFGHIKLMNPQRSTVWY" * (length // 20)
