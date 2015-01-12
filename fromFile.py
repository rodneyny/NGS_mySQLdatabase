#!/usr/bin/python

def filelist(file, lst):
	# open a given file 
	f = open(file, 'r')
	# create an empty list with the provided list name 
	lst = []
	for row in f:
		row = row.strip().split('\t')
		
		row = [ x.strip('"') for x in row ]
		
	#Append each row from the file into the given list
		lst.append(row)
	return lst

def openfile(file):
	f = open(file, 'r')
	return f.read()

	
