import pandas as pd
import os
import random
import pathlib
from os.path import join, getsize
import subprocess
import logging

def nucleotide_seq_align(pangenome_alignments_dir_path,alleleome_dir_path):
    try:
        logging.info("Starting nucleotide_seq_align in nucleotide_sequence_alignment")
        df=pd.read_csv(os.path.join(alleleome_dir_path,'nuc_genes_present_in_above_5_percent_of_strains.csv'))
        na_query_list=df['Gene'].tolist()
        
        blast_path ='./resources/ncbi-blast-2.14.0+/bin/blastn'

        for r in range(len(na_query_list)):
            query=na_query_list[r]
            if (pd.isnull(query)==False):
                out_file_name = pangenome_alignments_dir_path + query + '/output/' + 'nucleotide_' + 'blast_out_' + query + '.xml'
                args = (blast_path,
                    '-query', pangenome_alignments_dir_path + query + '/input/'+'pan_genes.fna',
                    '-subject', pangenome_alignments_dir_path + query + '/input/'+ 'nucleotide_consensus_'+ query +'.fna' ,
                    '-outfmt', '5',
                    )
                with open(out_file_name, 'w+') as outfile:
                    subprocess.run(args, stdout=outfile)
        logging.info("Completed nucleotide_seq_align in nucleotide_sequence_alignment")   
    except Exception as e:
        logging.error(f"Error in nucleotide_seq_align in nucleotide_sequence_alignment: {e}")         
        raise


