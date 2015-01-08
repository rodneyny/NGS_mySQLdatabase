# Python mySQL database

This is a repository of a database to store NGS variants that have been annotated by Variante Effect Predictor (VEP).

##Tutorials
- Tutorial for setting up mySQL on Ubuntu https://www.digitalocean.com/community/tutorials/a-basic-mysql-tutorial
- Creating mySQL users https://www.digitalocean.com/community/tutorials/how-to-create-a-new-user-and-grant-permissionsin-mysql 
- Python mySQL database access tutorial http://www.tutorialspoint.com/python/python_database_access.htm
- MySQL Python tutorial http://zetcode.com/db/mysqlpython/

##Requirements before running scripts:
- mySQl version 5.5.40
- Python version 2.7.3

##Essential scripts and files:
* newTables.py - Creates all the tables required for the database and populates the generic database tables using provided text files.
* fromFile.py - Contains functions for reading and formating files before the data they contain can be inserted into the relevant table 
* Class.txt - Variant classifications with their descriptions.  
* Diseases.txt - List of diseases which are linked to genes in the Genes table
* Genes.txt - List of genes, their chromosomal location and disease tested for
* Transcripts.txt - Refseq transcripts with their closest ensembl equivalent and which gene the transcript belongs to
* VEP.py - Inserts data into the database from the VEP output file. 

##Tables:
- Classes
- Diseases
- Genes
- Occurrence
- Samples
- Transcripts
- Variants

##Schema:
