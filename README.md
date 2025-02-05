# Novel pipeline to detect Spliced XBP1 from Bulk RNA-Sequencing Data

**Background**

Endoplasmic reticulum (ER) Stress, caused by accumulation of unfolded proteins in the ER activates a key homeostatic pathway called the Unfolded Protein Response (UPR) to stabilize the cell’s physiological activities. However prolonged effects of ER stress and deregulation of the UPR as a result, has been shown to play an important role in tumorgenesis and tumor progression in some cancers Out of the three known UPR activation mechanisms, the most conserved is the inositol-requiring enzyme 1A (IRE1𝛼) and X-box binding protein 1 (XBP1) interaction pathway. This pathway is activated upon encountering ER stress, which leads to induction of a very specific 26-nucleotide deletion in the canonical XBP1 gene by phosphorylated IRE1𝛼 to create the spliced XBP1(XBP1s). XBP1s is the active transcription factor (TF) which is known to regulate key cell fate pathways downstream and can serve as an important therapeutic target. However, given the frameshift is relatively infinitesimal it is challenging to simply quantify it as an isoform. As a result, the current and only best method to measure the active XBP1s TF relies on qPCR-based quantification and some other in vitro methods4. While this technique has proven to successfully quantify XBP1s levels in smaller sample sets, it would be an extensive effort to quantify the XBP1s levels in larger datasets, such as patient cohorts or functional genomic screens to study effects of ER stress activation. Therefore, building upon our knowledge of ER stress mechanism and quantification techniques, we curated a computational pipeline to detect XBP1s levels directly from RNA-Seq data, as an alternate method. This method of computationally quantifying spliced percentage levels of XBP1s can be used as scores to make associations with relevant ER stress specific molecular and clinical outcomes.  We further apply this pipeline to explore the XBP1s patterns across the pan cancer TCGA dataset to identify subsets of cancer types and key cancer-type specific molecular signatures. Overall, we propose the utility of the XBP1s detection pipeline as a resource for future applications to various RNA-Seq data not just for cancer datasets but across multiple diseases for study of ER Stress activation patterns.  


**Methods**

- A combination of open-source, command line-based bioinformatics tools to process and quantify the indel from raw RNASeq FASTQ
- customized reference for the alignment was generated using the XBP1 gene sequence for Human assemble hg19 and Mus Musculus mm10 RefSeq databases. As gene expression reference we used XBP1 gene with the 1820 bp in length human ortholog (RefSeq id: NM_005080) and 2264 bp Mouse ortholog (RefSeq id: NM_103842.3)
- Using the Karkkainen’s blockwise algorithm based bowtie2-build, the index files for the gene sequence were generated respectively
- The alignment was then performed using bowtie2 aligner, with parameters optimized to make it more sensitive
- instead of local alignment, end-to-end alignment was specified for a relatively lenient alignment for sensitiving pipeline to detecting indels
- Each of the parameters were tested with combinations configured in increments on validation RNASeq data, prior to establishing the selected ones. Below are values for all specified parameters. 

*bowtie2 -p 8 -D 20 -R 3 -N 0 -L 20 -i S,1,0.50 --end-to-end --rdg 1,1 --rfg 1,1 --gbar 10* 
- Samtools paramters are optimized to detect all mutationas and long indels of up to 30bp, to enable detection of the very specific 26 bp XBP1s INDEL
- the bash pipeline here is adapted to run on the SLURM job scheduler, but can be run using any batch jobs scheduler 
- the output directory with sample specific VCF file readouts can then be run through as an agrument to the python script to summarize results to summarized sample level XBP1s indel measure.

**Publications:**

This work was applied and validated in two independent publications. One referencing this pipeline was accepted and one is under review. 
*updates to come soon*

now out: https://www.nature.com/articles/s41467-022-35584-9

published January 2025: https://www.nature.com/articles/s41590-024-02063-w



