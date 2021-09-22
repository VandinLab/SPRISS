#!/bin/bash
#$ -pe parallel 64
#$ -cwd -m ea

#PERCORSI TOOLS
bwa=../bwa/bwa
samtools=../samtools-1.12/samtools
bcftools=../bcftools-1.12/bcftools
bedtools=../bedtools
bgzip=../samtools-1.12/htslib-1.12/bgzip
rtg=../rtg-tools-3.12.1/rtg

PCOUNT=64

#Reference Files
REF=hg19.fa
SDFREF=hg19.sdf
VCFREF=NA12878.vcf.gz
VCFBED=ConfidentRegions.bed.gz

#Input files
INPUT=$1

#Output directory
WORKING_DIR=$2
BASENAME=$WORKING_DIR/basename

mkdir $WORKING_DIR

#Temporary and output files
LANETEMP=$WORKING_DIR/temporary.tmp
SAM=$WORKING_DIR/aln_bwa_mem_full.sam
BAM=$WORKING_DIR/aln_bwa_mem_full.bam
SORTBAM=$WORKING_DIR/aln.sorted.bam
BAMBED=$WORKING_DIR/sortedbam.bed
DIREVAL=$WORKING_DIR/results

RAWVCF=$WORKING_DIR/call_raw.vcf.gz
VCF=$WORKING_DIR/call_filt.vcf.gz

#necessary indexes and sdf files!
$bwa index $HG19REF
$samtools faidx $HG19REF
$rtg format -o $HG19SDFREF $HG19REF
$rtg index -f vcf $VCFREF
$rtg index -f bed $VCFBED

################## SCRIPT #########################
>&2 date
>&2 echo "Inizio script pipeline"

################## BWA #########################
>&2 date && >&2 echo "--> Allineamento con bwa"

>&2 date && >&2 echo " -> bwa mem"
$bwa mem -t $PCOUNT $REF $INPUT > $SAM

############### SAMTOOLS #######################
>&2 date && >&2 echo "--> Clean up read pairing information and flags"
$samtools fixmate -O bam $SAM $BAM
rm $SAM

>&2 date && >&2 echo "--> Sorting BAM file from name order to coordinate order"
$samtools sort $BAM -T $LANETEMP -@ $PCOUNT -O bam -o $SORTBAM
rm $BAM

>&2 date && >&2 echo "--> Indicizzazione del file BAM"
$samtools index $SORTBAM

>&2 date && >&2 echo "--> Creazione del file BED"
./$bedtools bamtobed -i $SORTBAM > $BAMBED

>&2 date && >&2 echo "--> Variant calling multithread"
$samtools view -H $SORTBAM | grep '\@SQ' | sed 's/^.*SN://g' | cut -f 1 | xargs -I {} -n 1 -P $PCOUNT sh -c "$samtools mpileup -BQ0 -d 100000 -ugf $REF -r {} $SORTBAM | $bcftools call -vmO z > $BASENAME.tmp.{}.vcf.gz"

>&2 date && >&2 echo "--> Merging vcf.gz files"
ITEMLIST=$($samtools view -H $SORTBAM | grep '\@SQ' | sed 's/^.*SN://g' | awk '{print $1}')
ITEM0=$($samtools view -H $SORTBAM | grep '\@SQ' | sed 's/^.*SN://g' | awk '{print $1}' | head -n 1)
zcat $BASENAME.tmp.$ITEM0.vcf.gz | grep "#" | $bgzip > ${RAWVCF}
for item in $ITEMLIST;
do
  zcat $BASENAME.tmp.$item.vcf.gz | grep -v "#" | $bgzip >> ${RAWVCF}
  rm $BASENAME.tmp.$item.vcf.gz
done

rm $SORTBAM.bai
rm $SORTBAM

>&2 date && >&2 echo "--> Filtering"
$bcftools index -f --threads $PCOUNT $RAWVCF
$bcftools filter -O z --threads $PCOUNT -s LOWQUAL -e '%QUAL<0' $RAWVCF -o $VCF

##rm $RAWVCF.csi
##rm $RAWVCF

############### RTGTOOL #########################
>&2 date && >&2 echo "--> Vcf Evaluation"

$rtg index -f vcf $VCF
$rtg vcfeval -t $SDFREF -b $VCFREF --bed-regions=$VCFBED -c $VCF -e $BAMBED -f QUAL -o $DIREVAL

##rm $BAMBED
##rm $VCF
##rm $VCF.tbi

>&2 echo "--> Curva ROC"
$rtg rocplot $DIREVAL/weighted_roc.tsv.gz --svg $DIREVAL/roc.svg

>&2 date && >&2 echo "--> Pulizia file"
##rm -r $TEMP

>&2 date && echo "Fine script pipeline."
