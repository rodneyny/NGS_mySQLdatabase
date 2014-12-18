import MySQLdb as dbm
import sys 
from fromFile import filelist

#file = os.path.abspath(sys.argv[1])

record = filelist('vep.txt','record')

# Remove the header from the dictionary
record.remove(record[0])


db = dbm.connect("localhost","rodney","password","VEPvariants" )

cursor = db.cursor()

try:
	for line in record:
		var = line[0:67]
		var.remove(var[3])
		print var
		print len(var)
		# For floats use the %f placeholder instead of the %d placeholder
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
					%s, %s,%s,%s,%s,%s)""" , [var])
		#print "Rows in the Variants table were populated"
except:
	print "an error occurred inserting variants"
	db.rollback()

	
try:
	for line in record:
		PK = line[0]
		sample = line[3]
		gt = line[4]
		cursor.execute("insert ignore into Samples ( SampleNumber)\
					  values ('%s')" % (sample))
		#print "Rows in the Samples table were populated"
		
		cursor.execute("insert into Occurrence (SampleNumber, cDNA, Genotype) \
					   values ('%s', '%s', '%s')" % (sample, PK, gt))
		#print "Rows in the Occurrence table were populated" 
		db.commit()
	print "records successfully added to database"
except:
	print "an error occured"
	db.rollback()

db.close()