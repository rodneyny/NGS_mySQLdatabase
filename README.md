# testrepo2

This is a repository of a database to store NGS variants that have been annotated by Variante Effect Predictor (VEP).

Tutorial for setting up mySQL on Ubuntu https://www.digitalocean.com/community/tutorials/a-basic-mysql-tutorial

Creating mySQL users https://www.digitalocean.com/community/tutorials/how-to-create-a-new-user-and-grant-permissions-in-mysql 

Python mySQL database access tutorial http://www.tutorialspoint.com/python/python_database_access.htm

Requirements before running scripts:
mySQl version 5.5.40
Python version 2.7.3

Contents:
newTables.py - Creates all the tables required for the database and populates the generic database tables using provided text files. 
Class.txt - Variant classifications with their descriptions.  
Diseases.txt - List of diseases which are linked to genes in the Genes table
Genes.txt - List of genes, their chromosomal location and disease tested for
Transcripts.txt - refseq transcripts with their closest ensembl equivalent and which gene the transcript belongs to
VEP.py - inserts data into the database from the VEP output file. 

Tables:
Classes
Diseases
Genes
Occurrence
Samples
Transcripts
Variants

Schema:
