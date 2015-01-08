#!/usr/bin/python

import MySQLdb

# Open database connection
db = MySQLdb.connect("localhost","rodney","password","variants" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

# Drop table if it already exist using execute() method.
# Order of dropping tables has to be the same order as any foreign key
# constraints starting with the 'child' table
cursor.execute("DROP TABLE IF EXISTS Classes")
cursor.execute("DROP TABLE IF EXISTS Occurrence")
cursor.execute("DROP TABLE IF EXISTS Episodes")
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
		
cursor.execute("""create table Diseases (Disease VARCHAR(255),
		DiseaseCode VARCHAR(10),
		Primary key (DiseaseCode)
		)""")		
		
cursor.execute("""create table Genes (
		Gene VARCHAR(20) NOT NULL,
		Chromosome VARCHAR(10),
		DiseaseCode VARCHAR(10),
		Primary key(Gene),
		Foreign key(DiseaseCode) References Diseases(DiseaseCode)
		)""")
		
cursor.execute(""" create table Transcripts (Refseq VARCHAR(20),
		Ensembl VARCHAR(20),
		Gene VARCHAR(20),
		Primary key (Refseq),
		Foreign key (Gene) References Genes(Gene)
		)""")
		  
cursor.execute("""create table Variants (Refseq VARCHAR(20) NOT NULL, 
		  GenomicPosition INT,
		  GenomeBuild VARCHAR(20) DEFAULT 'GRCh37/hg19', 
		  Exon INT, 
		  HGVSNomen VARCHAR(255),
		  cDNA VARCHAR(255) NOT NULL,
		  Protein VARCHAR(255),
		  UVform VARCHAR(255),
		  Classification VARCHAR(50) DEFAULT 'Not classified' NOT NULL,
		  Comments TEXT,
		  ClassifiedBy VARCHAR(10),
		  DateClassified DATE,
		  CheckedBy VARCHAR(10),
		  DateChecked DATE,
		  VariantType VARCHAR(50), 
		  Effect VARCHAR(255) ,
		  Location VARCHAR(50) ,
		  ProteinDomain VARCHAR(255),
		  nOrthos INT,
		  conservedOrthos INT,
		  conservedDistSpecies VARCHAR(20) , 
		  GranthamDistance INT, 
		  LSDB TEXT,
		  Literature TEXT,
		  HGMD VARCHAR(255),
		  Phenotype VARCHAR(255),
		  PubmedID INT,
		  HGMDcatergory VARCHAR(5) , 
		  dbSNP VARCHAR(20) ,
		  MAF FLOAT,
		  Allele VARCHAR(255),
		  ESP_AA FLOAT,
		  ESP_EA FLOAT,
		  ESP_ALL FLOAT,
		  distNearestSS INT, 
		  nearestSSType CHAR(2),
		  wtSSFScore FLOAT, 
		  varSSFScore FLOAT,
		  wtMaxEntScore FLOAT, 
		  varMaxEntScore FLOAT,
		  wtNNSScore FLOAT,
		  varNNSScore FLOAT, 
		  wtGSScore FLOAT, 
		  varGSScore FLOAT,
		  wtHSFScore FLOAT, 
		  varHSFScore FLOAT, 
		  nearestSSChange FLOAT, 
		  localSpliceEffect VARCHAR(255),
		  AGVGD VARCHAR(5),
		  AGVGDgv FLOAT,
		  AGVGDgd FLOAT,
		  SIFT VARCHAR(20),
		  SIFTweight FLOAT,
		  SIFTmedian FLOAT, 
		  Polyphen VARCHAR(20) ,
		  PolyphenScore FLOAT, 
		  DateAdded DATE, 
		  DateUpdated DATE,
		  SNPsandGO VARCHAR(255),
		  Mutpred VARCHAR(255), 
		  Alias VARCHAR(255) ,
		  Primary key (cDNA),
		  Foreign key (Refseq) REFERENCES Transcripts(Refseq)
		  )""")
		  
cursor.execute(""" create table Episodes (EpisodeNumber CHAR(15), 
		Phenotype TEXT,
		Worksheet VARCHAR(50),
		Assay VARCHAR(255),
		Date DATE,
		Primary key (EpisodeNumber)
		)""")
		  
cursor.execute(""" create table Occurrence (EpisodeNumber CHAR(15),
		cDNA VARCHAR(255), 
		Comments TEXT, 
		Genotype CHAR(4),
		Foreign Key(EpisodeNumber) References Episodes(EpisodeNumber),
		Foreign Key (cDNA) References Variants(cDNA)
		)""")
		  
# disconnect from server
db.close()