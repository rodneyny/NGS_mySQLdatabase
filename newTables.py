#!/usr/bin/python

from fromFile import filelist
from connection import connect 

database = connect()
cursor = database[0]
db = database[1]

# Drop table if it already exist using execute() method.
# Order of dropping tables has to be the same order as any foreign key
# constraints starting with the 'child' table
cursor.execute("DROP TABLE IF EXISTS Classes")
cursor.execute("DROP TABLE IF EXISTS Occurrence")
cursor.execute("DROP TABLE IF EXISTS Samples")
cursor.execute("DROP TABLE IF EXISTS Variants")
cursor.execute("DROP TABLE IF EXISTS Transcripts")
cursor.execute("DROP TABLE IF EXISTS Genes")
cursor.execute("DROP TABLE IF EXISTS Diseases")

# Create table as per requirement
# When creating a new table which has a relationship with another table
# the 'parent' table should be created before the 'child' table

cursor.execute(""" create table Classes (Classification VARCHAR(50),
		Description VARCHAR(50),
		Primary key(Classification)
		)""")
print "Classes table created"
		
cursor.execute("""create table Diseases (Disease VARCHAR(255),
		DiseaseCode VARCHAR(10),
		Primary key (DiseaseCode)
		)""")
print "Diseases table created"		
		
cursor.execute("""create table Genes (
		Gene VARCHAR(20) NOT NULL,
		Chromosome VARCHAR(10),
		DiseaseCode VARCHAR(10),
		Primary key(Gene),
		Foreign key(DiseaseCode) References Diseases(DiseaseCode)
		)""")
print "Genes table created"	
	
cursor.execute(""" create table Transcripts (Refseq VARCHAR(20),
		Ensembl VARCHAR(20),
		Gene VARCHAR(20),
		Primary key (Refseq),
		Foreign key (Gene) References Genes(Gene)
		)""")
print "Transcripts table created"		

cursor.execute("""create table Variants (cDNA VARCHAR(255) NOT NULL, 
				Refseq VARCHAR(20) NOT NULL,
				HGVSNomen VARCHAR(255),
				GT CHAR(3),
				GQ INT,
				SDP INT,
				DP INT,
				RD INT,
				AD INT,
				FREQ VARCHAR(10),
				PVAL FLOAT,
				RBQ	INT,
				ABQ	INT,
				RDF	INT,
				RDR	INT,
				ADF	INT,
				ADR	INT,
				CHROM VARCHAR(5),	
				POS	INT,
				REF	VARCHAR(255),
				ALT	VARCHAR(255),
				ID	VARCHAR(255),
				info_ADP INT,
				info_WT INT,
				info_HET INT,
				info_HOM INT,
				info_NC INT,
				CSQ_Allele VARCHAR(255),	
				CSQ_Gene VARCHAR(20),
				CSQ_Feature VARCHAR(20),
				CSQ_Feature_type VARCHAR(20),
				CSQ_Consequence	VARCHAR(255),
				CSQ_cDNA_position VARCHAR(255),
				CSQ_CDS_position VARCHAR(255),
				CSQ_Protein_position VARCHAR(255),
				CSQ_Amino_acids	VARCHAR(255),
				CSQ_Codons	VARCHAR(255),
				CSQ_Existing_variation VARCHAR(255),	
				CSQ_AA_MAF	FLOAT,
				CSQ_EA_MAF	FLOAT,
				CSQ_ALLELE_NUM INT,	
				CSQ_EXON VARCHAR(255),
				CSQ_INTRON VARCHAR(255),
				CSQ_DISTANCE VARCHAR(255),	
				CSQ_CLIN_SIG VARCHAR(255),	
				CSQ_CANONICAL VARCHAR(255),
				CSQ_SYMBOL VARCHAR(255),
				CSQ_BIOTYPE VARCHAR(255),	
				CSQ_ENSP VARCHAR(255),
				CSQ_DOMAINS	VARCHAR(255),
				CSQ_CCDS VARCHAR(255),	
				CSQ_AFR_MAF FLOAT,	
				CSQ_AMR_MAF	FLOAT,
				CSQ_ASN_MAF	FLOAT,
				CSQ_EUR_MAF	FLOAT,
				CSQ_FATHMM VARCHAR(255),	
				SIFT VARCHAR(255),	
				SIFT_scoe FLOAT,	
				POLYPHEN VARCHAR(255),	
				POLYPHEN_SCORE FLOAT,	
				1KG_Allele VARCHAR(255),	
				1KG_MAF	FLOAT,
				HGVS_transcript	VARCHAR(255),
				HGVSc VARCHAR(255),	
				HGVS_protein VARCHAR(255),	
				HGVSp VARCHAR(255),	
				Classification VARCHAR(50) DEFAULT 'Not classified' NOT NULL,
				Frequency INT,
				Primary key (cDNA),
				Foreign key (Refseq) REFERENCES Transcripts(Refseq)
				)""")
print "Variants table created"

cursor.execute(""" create table Samples (SampleNumber CHAR(15), 
		Phenotype TEXT,
		Worksheet VARCHAR(50),
		Assay VARCHAR(255),
		Date DATE,
		Primary key (SampleNumber)
		)""")
print "Samples table created"
		  
cursor.execute(""" create table Occurrence (SampleNumber CHAR(15),
		cDNA VARCHAR(255), 
		Comments TEXT, 
		Genotype CHAR(4),
		Primary Key (SampleNumber, cDNA),
		Foreign Key(SampleNumber) References Samples(SampleNumber),
		Foreign Key (cDNA) References Variants(cDNA)
		)""")
print "Occurrence table created"
		  

		
genes = filelist('Genes.txt','genes')
classes = filelist('Classes.txt','classes')
diseases = filelist('Diseases.txt', 'diseases')
transcripts = filelist('Transcripts.txt','transcripts')

try:
	for line in diseases:
		disease = line[0]
		code = line[1]
		cursor.execute("insert into Diseases(Disease,DiseaseCode)\
		 values ('%s','%s')" % \
		 (disease, code))
		db.commit()
	print "Rows in the Diseases table were populated"
except:
	print "No diseases were added to the Diseases table"
	db.rollback()

try:
	for line in genes:
		gene = line[0]
		chr = line[1]
		dis = line[2]
		sql = "insert into Genes(Gene, Chromosome,DiseaseCode)\
		 values ('%s', '%s', '%s')" % \
		 (gene, chr, dis)
	   # Execute the SQL command
		cursor.execute(sql)
	   # Commit your changes in the database
		db.commit()
	print "Rows in the Genes table were populated"	
except:
	print "No Genes were added to the Genes table"
	# Rollback in case there is any error
	db.rollback()
	
try:
	for line in classes:
		classification = line[0]
		description = line[1]
		cursor.execute("insert into Classes(Classification, Description)\
		 values ('%s','%s')" % \
		 (classification, description))
		 
		db.commit()
	print "Rows in the Classes table were populated"
except:
	print "No Classifications were added to the Classes table"
	db.rollback()
	
	
try:
	for line in transcripts:
		refseq = line[0]
		ensembl = line[1]
		gene = line[2]
		cursor.execute("insert into Transcripts(Refseq, Ensembl,Gene)\
		 values ('%s', '%s', '%s')" % \
		 (refseq, ensembl, gene))
		db.commit()
	print "Rows in the Transcripts table have been populated"
except:
	print "No Transcripts were added to the Transcripts table"
	db.rollback()

# disconnect from server
db.close()