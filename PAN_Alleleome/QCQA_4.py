import os
import pandas as pd
import shutil
import logging

def process_genes(pangenome_alignments_dir_path,alleleome_dir_path):
    """
    Processes genes by copying gene sequence files and creating output directories for each gene.

    Parameters:
    - pangenome_alignments_dir_path: Path to the main directory containing gene folders.
    - alleleome_dir_path: Path to the directory containing the gene data CSV files.
    """
    try:
        logging.info("Starting process_genes in QCQA_4")

        # Read genes data
        df=pd.read_csv(os.path.join(alleleome_dir_path,'nuc_genes_present_in_above_5_percent_of_strains.csv'))
        gene_list=df['Gene'].tolist()
        # Read gene alleles data
        df1 = pd.read_csv(os.path.join(alleleome_dir_path, 'nuc_alleles_with_length_less_than_2std_less_than_mean_length.csv'))
        edit_list = df1['Gene'].tolist()
        new_gene_list = set(edit_list)
        # Process each gene
        for gene in gene_list:
            # Copy gene sequence files if gene not in new_gene_list
            if gene not in new_gene_list:
                aa_allele_path = pangenome_alignments_dir_path + gene + '/input/' 
                aa_file=aa_allele_path +'pangenes.faa'
                new_file=aa_allele_path +'pan_genes.faa'
                na_file=aa_allele_path +'pangenes.fna'
                new_na_file=aa_allele_path +'pan_genes.fna'
                shutil.copyfile(aa_file, new_file)
                shutil.copyfile(na_file, new_na_file)

            # Create output directory for the gene
            output_path = os.path.join(pangenome_alignments_dir_path, gene, 'output')
            os.makedirs(output_path, exist_ok=True)
        logging.info("Completed process_genes in QCQA_4")   
    except Exception as e:
        logging.error(f"Error in process_genes in QCQA_4: {e}")         
        raise

