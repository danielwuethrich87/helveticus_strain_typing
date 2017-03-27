Lactobacillus helveticus strain typing
=======================

This script is intended to analyse IonTorrent amplicon-seq data from the slpH gene of Lactobacillus helveticus.<br />

As input the fastq file from the IonTorrent amplicon-seq is needed.<br />

#Requirements:

-Linux 64 bit system<br />

-python (version 2.7)<br />

#Installation:

wget https://github.com/danielwuethrich87/helveticus_strain_typing/archive/master.zip<br />
unzip master.zip<br />
cd helveticus_strain_typing-master<br />


#Usage:

sh assign_reads_to_ST.sh reads.fastq<br />
 
reads.fastq: path to reads file (test file in data/test_reads.fastq)<br />

#Output:

A table with the read count per strain type is printed to the standart output.

Newly detected strain types are printed to new_STs.fasta. These can be added to the Strain type database in data/known_ST.fasta.

