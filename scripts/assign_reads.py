#!/usr/bin/env python


import subprocess
import sys
import os
import operator

inputOptions = sys.argv[1:]

#usage: file1

def main():
	#markers=[(GGCTACACT,GATCAATTAA),(AGTGTAGCC,TTAATTGATC),(CCTTAATGTA,CTGACGATGT),(TACATTAAGG,ACATCGTCAG),(ATTGGTTCAG,GGTGTTGCTA),(CTGAACCAAT,TAGCAACACC)]
	reads=read_reads(inputOptions)
	reads_with_trimmed_seq=search_for_markers(reads)
	compare_reads_to_STs(inputOptions,reads_with_trimmed_seq)
	
	
def read_known_ST(inputOptions):
	input_file = [n for n in open(inputOptions[1],'r').read().replace("\r","").split("\n") if len(n)>0]
	ref_seqs={}
	for line in input_file:
		if line[0:1]==">":
			name=line
			ref_seqs[name]=""
		else:
			ref_seqs[name]+=line
	return ref_seqs

def compare_reads_to_STs(inputOptions,reads_with_trimmed_seq):
	ref_seqs=read_known_ST(inputOptions)
	ref_2_group={}
	counter_new_STs=0
	count_reads_per_ST={}
	new_STs=''

	for read in reads_with_trimmed_seq:
		matched_ST=[]
		for ref_seq in ref_seqs.keys():
			if ref_seqs[ref_seq].find(read.trimmed_sequence) !=-1:
				if (ref_seq in count_reads_per_ST.keys())==bool(0):
					count_reads_per_ST[ref_seq]=0
					ref_2_group[ref_seq]=read.markers[0][2]

				assert (read.markers[0][2] == ref_2_group[ref_seq]),"One ST has several marker groups"
				count_reads_per_ST[ref_seq]+=1
				matched_ST.append(ref_seq)

		if len(matched_ST) >1:
			print 'This sequence matches several STs:'+str(matched_ST)
			print read.name
			print read.sequence			
			print read.info
			print read.quality	
			print read.trimmed_sequence

		if len(matched_ST) ==0:
			counter_new_STs+=1
			new_ST_name=">new_ST_"+str(counter_new_STs)
			ref_seqs[new_ST_name]=read.trimmed_sequence
			count_reads_per_ST[new_ST_name]=1
			new_STs+= new_ST_name+'\n'
			new_STs+= read.trimmed_sequence+'\n'
			ref_2_group[new_ST_name]=read.markers[0][2]
							
	for st in sorted(count_reads_per_ST.items(), key=operator.itemgetter(1),reverse=True):
		print st[0]+"\tgroup_"+str(ref_2_group[st[0]])+"\t"+str(st[1])	

	f = open('new_STs.fasta', 'w')
	f.write(new_STs)
		
			
def search_for_markers(reads):
	reads_with_markers=[]
	markers={1:('GGCTACACT','GATCAATTAA'),2:('CCTTAATGTA','CTGACGATGT'),3:('ATTGGTTCAG','GGTGTTGCTA')}
	for read in reads:
		for seq in [read.sequence, reverse_complement(read.sequence)]:
			for marker_key in markers.keys():
				marker1=markers[marker_key][0]	
				marker2=markers[marker_key][1]
				
				if seq.find(marker1)!=-1 and seq.find(marker2)!=-1:
					read.markers.append([marker1,marker2,marker_key])					
					read.trimmed_sequence=seq[seq.find(marker1):seq.find(marker2)+len(marker2)]

		if len(read.markers) >1:			
			print 'In this read several markers were found:'+str(read.markers)
			print read.name
			print read.sequence			
			print read.info
			print read.quality	
		elif len(read.markers)==1:	
			reads_with_markers.append(read)				
		
	return reads_with_markers


def read_reads(inputOptions):
	input_file = [n for n in open(inputOptions[0],'r').read().replace("\r","").split("\n") if len(n)>0]
	reads=[]
	counter=0
	for line in input_file:
		counter+=1
		if counter==1:
			read=Read(line)
		if counter==2:
			read.sequence=line
		if counter==3:
			read.info=line
		if counter==4:
			read.quality=line
			reads.append(read)
			counter=0
	return reads


def reverse_complement(seq):
    seq_dict = {'A':'T','T':'A','G':'C','C':'G'}
    return "".join([seq_dict[base] for base in reversed(seq)])


class Read:
	def __init__(self, name):
		self.name=name
		self.sequence=""
		self.info=""
		self.quality=""
		self.markers=[]
		self.trimmed_sequence=""

main()




