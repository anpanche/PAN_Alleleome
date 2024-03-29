import pandas as pd
from Bio import SeqIO
import os
import logging




def process_nucleotide_sequences(pangenome_alignments_dir_path,alleleome_dir_path):
    """
    Processes nucleotide sequences to compute the number of strains and gene length.

    Parameters:
    pangenome_alignments_dir_path: Path to the main directory containing gene folders.
    alleleome_dir_path: Path to the directory containing the CSV file with gene data.
    """
    try:
        logging.info("Starting process_nucleotide_sequences in QCQA_1")

        df = pd.read_csv(os.path.join(alleleome_dir_path, 'df_pangene_summary_v2.csv'))
        gene_list = (df['pangenome_class_2'].groupby(df['Gene']).any()).pipe(lambda x: x.index[x].tolist())
        
        genes_df = pd.DataFrame()

        for gene in gene_list:
            total_length = 0
            count = 0
            nuc_allele_file = os.path.join(pangenome_alignments_dir_path, gene, 'input', 'pangenes.fna')
        
            with open(nuc_allele_file, 'r') as file:
                for seq_record in SeqIO.parse(file, "fasta"):
                    gene_length = len(seq_record)
                    count += 1
                    total_length += gene_length

                    gene_data = {
                        "Gene": gene,
                         "Number_of_strains": count,
                        }
                    gene_df = pd.DataFrame(gene_data, index=[0])
                genes_df = pd.concat([genes_df, gene_df])
        genes_df.to_csv(os.path.join(alleleome_dir_path, 'genes_nuc_number_of_strains.csv'))
        num_strains= max(genes_df['Number_of_strains'])
        #calculate the 5% based on total number of strain
        genes_df['5%_of_strains']=num_strains*0.05
        genes_df['greater_than_5%']=genes_df['Number_of_strains'] > genes_df['5%_of_strains']
        df1=genes_df[genes_df['greater_than_5%']== True]
        df1.to_csv(os.path.join(alleleome_dir_path,'nuc_genes_present_in_above_5_percent_of_strains.csv'))
        logging.info("Completed process_nucleotide_sequences in QCQA_1")   
    except Exception as e:
        logging.error(f"Error in process_nucleotide_sequences in QCQA_1: {e}")         
        raise

