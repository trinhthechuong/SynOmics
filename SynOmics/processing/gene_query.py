"""
Gene query utilities for SynOmics.

This module provides the GeneQuery class for Ensembl-to-HUGO mapping 
and duplicate gene checking via MyGeneInfo.
"""


class GeneQuery:
    """
    A utility class for gene identifier mapping and duplicate detection.
    
    Provides methods for:
    - Converting Ensembl IDs to HUGO gene symbols via MyGeneInfo API
    - Detecting duplicate genes (identical expression profiles)
    - Handling versioned Ensembl IDs
    
    Args:
        fields (list, optional): Fields to retrieve from MyGeneInfo. Defaults to ["symbol"].
        scopes (list, optional): Search scopes. Defaults to ["ensemblgene"].
        species (list, optional): Species to query. Defaults to ["human"].
        output_dir (str, optional): Directory for output files. Defaults to "outputs".
        
    Attributes:
        fields (list): Fields to retrieve from MyGeneInfo.
        scopes (list): Search scopes for gene queries.
        species (list): Target species for queries.
        output_dir (str): Output directory path.
        
    Examples:
        >>> import pandas as pd
        >>> from SynOmics.processing.gene_query import GeneQuery
        >>> expr = pd.DataFrame({
        ...     "ENSG00000141510.15": [1.2, 3.4, 5.6],
        ...     "ENSG00000157764.13": [7.8, 9.0, 1.1]
        ... })
        >>> gq = GeneQuery(fields=["symbol"], scopes=["ensemblgene"])
        >>> mapping_df = gq.convert_genes(expr)
        >>> dup_groups, dup_symbols = gq.check_duplicates(expr)
    """
    
    def __init__(self, fields=None, scopes=None, species=None, output_dir="outputs"):
        """
        Initialize GeneQuery with configuration parameters.
        
        Args:
            fields (list, optional): Fields to retrieve. Defaults to ["symbol"].
            scopes (list, optional): Search scopes. Defaults to ["ensemblgene"].
            species (list, optional): Species list. Defaults to ["human"].
            output_dir (str, optional): Output directory. Defaults to "outputs".
        """
        self.fields = fields or ["symbol"]
        self.scopes = scopes or ["ensemblgene"]
        self.species = species or ["human"]
        self.output_dir = output_dir
    
    def convert_genes(self, data, from_type="ensembl", to_type="symbol"):
        """
        Convert gene identifiers from one type to another.
        
        Uses MyGeneInfo API to map Ensembl IDs to HUGO symbols.
        Automatically strips version numbers from Ensembl IDs if present.
        
        Args:
            data (pd.DataFrame): Dataframe with gene IDs as columns.
            from_type (str, optional): Source ID type. Defaults to "ensembl".
            to_type (str, optional): Target ID type. Defaults to "symbol".
            
        Returns:
            pd.DataFrame: Mapping dataframe with original and converted IDs.
            
        Raises:
            ValueError: If API query fails.
            ConnectionError: If internet connection is unavailable.
            
        Examples:
            >>> expr = pd.DataFrame({"ENSG00000141510.15": [1, 2, 3]})
            >>> gq = GeneQuery()
            >>> mapping = gq.convert_genes(expr)
        """
        pass
    
    def check_duplicates(self, data, annotate_symbols=True):
        """
        Identify genes with identical expression profiles.
        
        Groups genes (columns) that have identical values across all samples.
        Optionally annotates groups with HUGO symbols.
        
        Args:
            data (pd.DataFrame): Gene expression dataframe.
            annotate_symbols (bool, optional): Add HUGO symbols to output. Defaults to True.
            
        Returns:
            tuple: (duplicate_groups, duplicate_symbols)
                - duplicate_groups (list): List of lists, each containing duplicate gene IDs
                - duplicate_symbols (dict): Mapping of Ensembl IDs to HUGO symbols
                
        Examples:
            >>> expr = pd.DataFrame({
            ...     "ENSG00000141510": [1, 2, 3],
            ...     "ENSG00000171862": [1, 2, 3]  # duplicate profile
            ... })
            >>> gq = GeneQuery()
            >>> groups, symbols = gq.check_duplicates(expr)
        """
        pass
    
    def remove_version_suffix(self, gene_id):
        """
        Remove version number from Ensembl gene ID.
        
        Ensembl IDs often have version suffixes (e.g., ENSG00000141510.15).
        This method removes the .VERSION part.
        
        Args:
            gene_id (str): Ensembl gene ID with or without version.
            
        Returns:
            str: Gene ID without version suffix.
            
        Examples:
            >>> gq = GeneQuery()
            >>> clean_id = gq.remove_version_suffix("ENSG00000141510.15")
            >>> print(clean_id)  # ENSG00000141510
        """
        pass
