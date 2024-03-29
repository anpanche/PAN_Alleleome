from Bio import AlignIO
from Bio.Align import AlignInfo
from Bio.Align.Applications import MafftCommandline
import os
import pandas as pd
import logging

def build_consensus(pangenome_alignments_dir_path,alleleome_dir_path):
    try:
        logging.info("Starting build_consensus in build_consensus_sequence")
        df=pd.read_csv(os.path.join(alleleome_dir_path,'nuc_genes_present_in_above_5_percent_of_strains.csv'))
        aa_query_list=df['Gene'].tolist()

        for k in aa_query_list:
            allele_file_path = pangenome_alignments_dir_path + k + '/input/' 
            aa_allele = allele_file_path + 'pan_genes.faa'
            na_allele = allele_file_path + 'pan_genes.fna'
        
            generate_consensus(aa_allele, k, 'amino_acid', pangenome_alignments_dir_path)
            generate_consensus(na_allele, k, 'nucleotide', pangenome_alignments_dir_path)
        logging.info("Completed build_consensus in build_consensus_sequence")   
    except Exception as e:
        logging.error(f"Error in build_consensus in build_consensus_sequence: {e}")         
        raise

def generate_consensus(allele, k, type, pangenome_alignments_dir_path):
    if os.stat(allele).st_size == 0:
        print("The file is empty")
        return
    
    mafft_cline = MafftCommandline(input=allele)
    stdout, stderr = mafft_cline()
    
    if type == 'amino_acid':
        file_suffix = 'amino_acid'
        ext = '.faa'
    else:
        file_suffix = 'nucleotide'
        ext = '.fna'

    mafft_out_file = ''.join(pangenome_alignments_dir_path + k + '/output/' + 'mafft_' + file_suffix + '_' + k + '.fasta')
    with open(mafft_out_file, "w") as handle:
        handle.write(stdout)
    
    myalign = AlignIO.read(mafft_out_file, "fasta")
    summary = AlignInfo.SummaryInfo(myalign)
    consensus = summary.dumb_consensus(threshold=0.5)
    seq = str(consensus).upper()
    
    consensus_file_path = os.path.join(pangenome_alignments_dir_path + k + '/input/' + file_suffix + '_consensus_' + k + ext)
    with open(consensus_file_path, 'w+') as consensus_file:
        consensus_seq = ''.join(['>' + k + '\n' + seq])        
        consensus_file.write(consensus_seq)



