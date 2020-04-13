##***********************************************************************
#Author: Akanksha Verma
#Date: March 1st, 2015
#Description:Parses per sample output file from XBP1 output and saves it to
#			  specified output file on command line prompt while running  
#			  Each sample

#Run :python Parse_XBP1.py < input BCF INPUT > < Output Summarized Percentage >

##*************************************************************************

from decimal import Decimal
import sys
import os
import re
  #Input file - output of the XBP1 script


def Each_file_parse(Input_BCF,Sample_name,completedSamples):	

	##File Handler
	INPUT=open(Input_BCF,'r')
	#OUTPUT=open(Output_Summary,'w')

	if(os.stat(Input_BCF).st_size == 0):
		Gene_ID="NM_005080"
        	Target_anchor="-"
        	Depth="-"
        	Total_Q13_Bases=0
        	Total_Q13_REF=0
        	Total_Q13_ALT=0
        	position=0
		INDEL_Sequence="-"
        	Percentage_reads_with_indel=0
        #print Gene_ID+"\t"+str(position)+"\t"+ INDEL_Sequence+"\t"+Target_anchor+"\t"+str(Depth)+"\t"+str(Total_Q13_Bases)+"\t"+str(Total_Q13_REF)+"\t"+str(Total_Q13_ALT)+"\t"+str(Percentage_reads_with_indel)+"\t"+Sample_name
	

	for line in  INPUT:

		if (line.startswith('#')):

			continue
		#print line	

		INDEL=line.strip().split("\t")
		#print INDEL
		Gene_ID= INDEL[0]
		position = INDEL[1].strip()
		position = Decimal(position)
		INDEL_Sequence=INDEL[3]
		
		
		

		if(Gene_ID == "NM_005080" and position == 540 and  len(INDEL_Sequence) > 30 ):
		 #if(a len(INDEL_Sequence) >23):	
			Target_anchor=INDEL[4]
			Indel_INFO=INDEL[7].strip().split(";")
			
			if( Indel_INFO[0] == "INDEL"):
				Depth_Coverage=Indel_INFO[3]
				Q13_BASES=Indel_INFO[4].split("=")[1].strip().split(",")  #Extract the Q13 bases
				#print Q13_BASES
				Q13_REF_a = Decimal(Q13_BASES[0]) 
				Q13_REF_b = Decimal(Q13_BASES[1])
				Q13_ALT_a = Decimal(Q13_BASES[2])
				Q13_ALT_b = Decimal(Q13_BASES[3])

		
				Total_Q13_REF = Q13_REF_a + Q13_REF_b #Sum the Reference Q13 bases
				Total_Q13_ALT = Q13_ALT_a + Q13_ALT_b #Sum the Alternate Q13 bases
				Total_Q13_Bases = Total_Q13_REF+Total_Q13_ALT


				Percentage_reads_with_indel = round((Total_Q13_ALT/(Total_Q13_ALT + Total_Q13_REF) )*100,2)
				Depth=Depth_Coverage.split("=")[1]

				#if( Percentage_reads_with_indel > 10):
				print Gene_ID+"\t"+str(position)+"\t"+ INDEL_Sequence+"\t"+Target_anchor+"\t"+str(Depth)+"\t"+str(Total_Q13_Bases)+"\t"+str(Total_Q13_REF)+"\t"+str(Total_Q13_ALT)+"\t"+str(Percentage_reads_with_indel)+"\t"+Sample_name
			  	
			  	completedSamples.append(Sample_name)

	if(  Sample_name not in completedSamples):
                        Gene_ID="NM_005080"
                        position = 540
                        Target_anchor="-"
                        INDEL_Sequence="-"
                        Depth="-"
                        Total_Q13_Bases=0
                        Total_Q13_REF=0
                        Total_Q13_ALT=0
                        Percentage_reads_with_indel=0
                        print Gene_ID+"\t"+str(position)+"\t"+ INDEL_Sequence+"\t"+Target_anchor+"\t"+str(Depth)+"\t"+str(Total_Q13_Bases)+"\t"+str(Total_Q13_REF)+"\t"+str(Total_Q13_ALT)+"\t"+str(Percentage_reads_with_indel)+"\t"+Sample_name
                        
		
		

	return(completedSamples)

Input_BCF_dirpath = sys.argv[1]
#Output_file = sys.argv[2] #Output file where the data is to be saved
print "Gene-ID\tposition\t INDEL_Sequence\tTarget_Anchor\tTotal_Depth\tQ13 bases Total Depth\tTotal_Q13_REF\tTotal_Q13_ALT\tPercentage_of_reads_with_indel_Q13_basecounts\tSample_name\n"
completedSamples=[]
for files in os.listdir(Input_BCF_dirpath):  #Loops through the directory with the BCF file and call on each file 
	if files.endswith("_XBP1.INDELS"):
		#print(files)
		Input_BCF=Input_BCF_dirpath+"/"+files

		completedSamples=Each_file_parse(Input_BCF,files,completedSamples) #Function extract and calculate  percentage for XBP1 INDEL in each sample

