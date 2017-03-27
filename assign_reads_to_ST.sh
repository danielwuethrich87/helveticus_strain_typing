#!/bin/bash

export working_dir=$PWD

java -jar "$working_dir"/scripts/Trimmomatic-0.36/trimmomatic-0.36.jar SE -threads 1 -phred33 "$1"  "$working_dir"/data/filtered_reads.fastq  SLIDINGWINDOW:4:20 MINLEN:101

python "$working_dir"/scripts/assign_reads.py "$working_dir"/data/filtered_reads.fastq "$working_dir"/data/known_ST.fasta 

