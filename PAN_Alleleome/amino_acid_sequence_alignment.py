import pandas as pd
import os
import subprocess
import logging

def amino_acid_seq_align(pangenome_alignments_dir_path,alleleome_dir_path):
    try:
        logging.info("Starting amino_acid_seq_align in amino_acid_sequence_alignment")
        df=pd.read_csv(os.path.join(alleleome_dir_path,'nuc_genes_present_in_above_5_percent_of_strains.csv'))
        aa_query_list=df['Gene'].tolist()
        blast_path='./resources/ncbi-blast-2.14.0+/bin/blastp'

        for r in range(len(aa_query_list)):
            query=aa_query_list[r]
            if (pd.isnull(query)==False):
                out_file_name = pangenome_alignments_dir_path + '/'+ query + '/output/' + 'amino_acid_' + 'blast_out_' + query + '.xml'
                args = (blast_path,
                    '-query', pangenome_alignments_dir_path + '/'+ query + '/input/'+'pan_genes.faa',
                    '-subject', pangenome_alignments_dir_path + '/'+ query + '/input/'+ 'amino_acid_consensus_'+ query +'.faa' ,
                    '-outfmt', '5',
                    )
                with open(out_file_name, 'w+') as outfile:
                    subprocess.run(args, stdout=outfile)
        logging.info("Completed  amino_acid_seq_align in amino_acid_sequence_alignment")   
    except Exception as e:
        logging.error(f"Error in amino_acid_seq_align in amino_acid_sequence_alignment: {e}")         
        raise


