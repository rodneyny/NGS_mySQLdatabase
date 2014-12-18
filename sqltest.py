#!/usr/bin/python

import MySQLdb as dbm
import sys 
from fromFile import filelist

#file = os.path.abspath(sys.argv[1])

record = filelist('vep.txt','record')

# Remove the header from the dictionary
record.remove(record[0])

# Open database connection
db = dbm.connect("localhost","rodney","password","VEPvariants" )

# # prepare a cursor object using cursor() method
cursor = db.cursor()

# Prepare SQL query to INSERT a record into the database.


# for line in record:
	# PK = line[0]
	# refseq = line[1]
	# hgvsnomen = line[2]
	# effect = line[32]
	# dbsnp = line[38]
	# maf = float(line[62])
	# espaa = float(line[39])
	# espea = float(line[40])
	# sift = line[57]
	# siftscore = float(line[58])
	# polyphen = line[59]
	# polyphenscore = float(line[60])
	# protein = line[66]
	# proteindom = line[50]
	# cursor.execute("insert ignore into Variants(cDNA, Refseq, \
		  # HGVSNomen, Effect, dbSNP, MAF, ESP_AA, ESP_EA, SIFT, SIFTweight, \
		  # Polyphen, PolyphenScore, Protein, ProteinDomain) \
		  # values ('%s', '%s', '%s', '%s', '%s', '%d', '%d', '%d', '%s', '%d', \
		  # '%s', '%d', '%s', '%s')" % \
		  # (PK, refseq, hgvsnomen, effect, dbsnp, maf,espaa \
		  # , espea, sift, siftscore, polyphen, polyphenscore, \
	      # protein, proteindom))
	# print "row added"
	
for line in record:
	r = line[0:67]
	r.remove(r[3])
	#print len(r)
	#print r
	
	# For floats use the %f placeholder instead of the %d placeholder
	#print r

	# cmd = """insert ignore into Variants (cDNA,
			# Refseq, HGVSNomen, GT, GQ, SDP, DP, RD,
			# AD, FREQ, PVAL, RBQ, ABQ, RDF, RDR, ADF,
			# ADR, CHROM, POS, REF, ALT, ID, info_ADP,
			# info_WT, info_HET, info_HOM, info_NC, CSQ_Allele,	
			# CSQ_Gene, CSQ_Feature, CSQ_Feature_type, CSQ_Consequence,
			# CSQ_cDNA_position, CSQ_CDS_position, CSQ_Protein_position,
			# CSQ_Amino_acids, CSQ_Codons, CSQ_Existing_variation,	
			# CSQ_AA_MAF, CSQ_EA_MAF, CSQ_ALLELE_NUM, CSQ_EXON, CSQ_INTRON,
			# CSQ_DISTANCE, CSQ_CLIN_SIG, CSQ_CANONICAL, CSQ_SYMBOL,
			# CSQ_BIOTYPE, CSQ_ENSP, CSQ_DOMAINS, CSQ_CCDS, CSQ_AFR_MAF, CSQ_AMR_MAF,
			# CSQ_ASN_MAF, CSQ_EUR_MAF, CSQ_FATHMM, SIFT, SIFT_scoe, POLYPHEN, POLYPHEN_SCORE,	
			# 1KG_Allele,	1KG_MAF, HGVS_transcript, HGVSc, HGVS_protein, HGVSp)
			# values(%s,%s,%s,%s,%s,%s,%s,
			# %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, 
			# %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, 
			# %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, 
			# %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""" 

	# cursor.executemany(cmd,[r])	
	
	cursor.executemany("""insert ignore into Variants (cDNA, 
					Refseq, HGVSNomen, GT, GQ, SDP, DP, RD,
					AD, FREQ, PVAL, RBQ, ABQ, RDF, RDR, ADF,
					ADR, CHROM, POS, REF, ALT, ID, info_ADP,
					info_WT, info_HET, info_HOM, info_NC, CSQ_Allele,	
					CSQ_Gene, CSQ_Feature, CSQ_Feature_type, CSQ_Consequence,
					CSQ_cDNA_position, CSQ_CDS_position, CSQ_Protein_position,
					CSQ_Amino_acids, CSQ_Codons, CSQ_Existing_variation,	
					CSQ_AA_MAF, CSQ_EA_MAF, CSQ_ALLELE_NUM, CSQ_EXON, CSQ_INTRON,
					CSQ_DISTANCE, CSQ_CLIN_SIG, CSQ_CANONICAL, CSQ_SYMBOL,
					CSQ_BIOTYPE, CSQ_ENSP, CSQ_DOMAINS, CSQ_CCDS, CSQ_AFR_MAF, CSQ_AMR_MAF,
					CSQ_ASN_MAF, CSQ_EUR_MAF, CSQ_FATHMM, SIFT, SIFT_scoe, POLYPHEN, POLYPHEN_SCORE,	
					1KG_Allele,	1KG_MAF, HGVS_transcript, HGVSc, HGVS_protein,	HGVSp) 
					values (%s,%s,%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,
					%s,%s,%s,%s,%s,%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,
					%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, 
					%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s,%s,%s,%s,%s,%s, 
					%s, %s,%s,%s,%s,%s)""" , [r])
	print "Rows in the Variants table were populated"
	db.commit()

# disconnect from server
db.close()