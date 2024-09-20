set -ex

accessions=(SRR29324548 SRR29324549) #SRR29324550 SRR29324551)

for acc in ${accessions[@]}; do
    # minimap2 -ax sr data/AF144305.1.fasta fastq/${acc}.fastq | samtools view -bS - > bam/${acc}.bam
    # samtools sort bam/${acc}.bam -o bam/${acc}.sorted.bam
    # samtools index bam/${acc}.sorted.bam
    # ivar trim -i bam/${acc}.sorted.bam -b AVRL_H5N1_250bpAmpWGS_v1.bed -p bam/${acc}.trimmed -e -x 3 -q 1 -k
    # samtools sort bam/${acc}.trimmed.bam -o bam/${acc}.trimmed.sorted.bam
    # samtools index bam/${acc}.trimmed.sorted.bam
 
    # freyja variants --variants variants/${acc}.variants.tsv --depths variants/${acc}.depths.tsv bam/${acc}.trimmed.sorted.bam --ref data/AF144305.1.fasta
    freyja demix variants/${acc}.variants.tsv variants/${acc}.depths.tsv --output demix/${acc}.demix.tsv --barcodes cattle_barcode.csv #--lineageyml data/cattle_lineages.yml --depthcutoff 10
done

freyja aggregate demix/ --output demix/aggregate.tsv
freyja plot demix/aggregate.tsv --output demix/plot.pdf --lineages