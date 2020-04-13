#!/bin/bash -l
#SBATCH --job-name=XBP1M
#SBATCH --ntasks-per-node=2
#SBATCH --time=48:00:00
#SBATCH --workdir="/athena/elementolab/scratch/akv3001/SLURM_Scripts/SLURM_WorkLog"
#SBATCH --output=XBP1M_%A_%a.out
#SBATCH --error=XBP1M_%A_%a.err
#sbatch --mem=8G

## LOAD SPACK DEPENDENSIES###
spack load -r sra-toolkit@2.8.2-1
spack load -r bowtie2@2.3.1
spack load -r bzip2


path=$1 #path to all the samples
OUTDIR=$2
DataType=$3 # If data is seq or from geo

echo "Path=$path"
echo "TASK_ID=${SLURM_ARRAY_TASK_ID}"

file=$(ls --ignore="*.gz" ${path}| tail -n +${SLURM_ARRAY_TASK_ID}| head -1)


echo "Processing $file"
cd $TMPDIR  #copy the samples foldeRa


echo "Path=$path"
Sample=$(basename "$file")
Sample=${Sample%.*}

#Temp Sample info
#Sample=$(echo "$file"|cut -d "/" -f10)

echo "Sample Name = $Sample"
rsync -r -v -a   $path/$file/*.gz ./ #copy the samples foldeRa

ls $TMPDIR

# Select file based on data type
#if [[ $DataType == 'seq']]
#then
#	echo "seq raw"
	R1=$(ls $TMPDIR/*_R1*|tr "\n" ',')
	R2=$(ls $TMPDIR/*_R2*|tr " " ',')


#elif [[ $DataType == 'geo' ]]; then
	#statements
	echo "seq - from GEO"
	R1=$(ls $TMPDIR/*_1*|tr " " ',')
	R2=$(ls $TMPDIR/*_2*|tr " " ',')
#fi

echo "R1=${R1}"
echo "R1=${R2}"

# bowtie XBP1 index : /home/ole2001/PROGRAMS/SNPseeqer/REFDATA/NOXBP1/refGene.txt.25Nov2009.fa.bt2idx

bowtie2 -p 8  -D 20 -R 3 -N 0 -L 20 -i S,1,0.50 --end-to-end --rdg 1,1 --rfg 1,1 --gbar 10 -x \
 /athena/elementolab/scratch/akv3001/GenomeReference_mm10/Xbp1_ensmbleMouseRef/mm10EnsmblGenomicRef \
  -1 ${R1} -2${R2} -S $TMPDIR/${Sample}_aligned.sam


# SAMTOOLS INDEXING and SORTING
samtools view -bS  $TMPDIR/${Sample}_aligned.sam  | samtools sort -T ${Sample}_aligned_sorted -o $TMPDIR/${Sample}_aligned_sorted.bam -

samtools index $TMPDIR/${Sample}_aligned_sorted.bam


samtools index $TMPDIR/${Sample}_aligned_sorted.bam


# SAMTOOLS Mutation Calling
/home/akv3001/Programs/samtools-1.2/samtools mpileup -m 3 -L 50000  \
  -F 0.0002 -u -r "mm10_ensGene_ENSMUST00000063084" \
 -f /athena/elementolab/scratch/akv3001/GenomeReference_mm10/Xbp1_ensmbleMouseRef/Mouse_ensmbl_Sequence_mRNA.fa \
$TMPDIR/${Sample}_aligned_sorted.bam |bcftools view   -    >  $TMPDIR/${Sample}_XBP1_Mouse.INDELS


### COPY RESULTS ###
output_dir=$(dirname $path)

mkdir ${output_dir}/AlignedBams

rsync -r -v $TMPDIR/${Sample}_aligned_sorted.bam* ${output_dir}/AlignedBams

mkdir ${output_dir}/XBP1s_Calls

rsync -r -v $TMPDIR/${Sample}_XBP1_Mouse.INDELS \
${output_dir}/XBP1s_Calls
