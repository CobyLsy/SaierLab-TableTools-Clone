#! /usr/bin/env python

import os,sys
from decimal import Decimal
from substrate import get_substrate_data
from chebi_parser import build_ontology,find_predecessor


'''
A small Script to take tsv files containing results form genome analysis projects and creating an overall table

**modified on 09/11/19 for Steven's genome project
'''

def readLines(file):

	openFile = open(file,'r')

	lines = openFile.readlines()

	return lines[1:]

def mapTCID(lines,tcids,accessions):

	tcidMap = {}

	for line in lines:

		line = line.rstrip()

		fields = line.split('\t')

		acc = fields[1]
		tcid = fields[2]
		query = [fields[0]]+fields[3:]

		tcids.add(tcid)

		#Overall Data
		if tcid not in accessions:

			accessions[tcid] = []

		if acc not in accessions[tcid]:

			accessions[tcid].append(acc)



		#Genome-specifc data
		if tcid not in tcidMap:

			tcidMap[tcid] = {}


		if acc in tcidMap[tcid]:


			if float(query[3]) < float(tcidMap[tcid][acc][1]):


				tcidMap[tcid][acc] = query

		else:


			tcidMap[tcid][acc] = query


	return tcidMap,tcids,accessions


def getTCID(line):

	fields = line.split('\t')

	return fields[2]

def getSubstrate(tcid,substrate_data,ontology,classes):

	data = []

	if tcid in substrate_data:

		for substrate in substrate_data[tcid]:

			print(substrate)

			id,name = substrate

			cat = find_predecessor(ontology,id,classes=classes)

			for category in cat:
				print(category)

				data.append('{}({})-{}({})'.format(category[0],category[1],id,name))

		return ', '.join(data)

	return 'none'

def getProtein(line):

	fields = line.split('\t')

	return fields[0]

def addEntry(tcidMap,tcid,protein):

	if tcid not in tcidMap:

		tcidMap[tcid] = []

	tcidMap[tcid].append(protein)

	return tcidMap


def getGenomes(directory):

	genomes = []

	genomeFiles = {}

	for file in os.listdir(directory):

		filePath = '{}/{}'.format(directory,file)
		fileName = file.replace('.tsv','')

		print(fileName)

		genomes.append(fileName)

		genomeFiles[fileName] = filePath

	return genomes,genomeFiles

def printTable(genomes,tcids,tcidMaps,accessions,substrate_data,ontology,classes,output):

	outputFile = open(output,'w')

	outputFile.write('#TCID\tAcc\tSubstrate\thit_tms_no\tSMU\tSPN\tSPY\tSSA\tquery_tms_no\te_value\tquery_acc\tquery_tms_no\te_value\tquery_acc\tquery_tms_no\te_value\tquery_acc\tquery_tms_no\te_value\tquery_acc\n')


	for tcid in tcids:


		for acc in accessions[tcid]:

			hits = []
			pos = []

			for genome in genomes:


				if tcid in tcidMaps[genome]:

					if acc in tcidMaps[genome][tcid]:

						hits.append('\t'.join(tcidMaps[genome][tcid][acc]))
						pos.append('+')

					else:

						hits.append('none\tnone\tnone')
						pos.append('-')
				else:

					hits.append('none\tnone\tnone')
					pos.append('-')

			substrateData = getSubstrate(tcid,substrate_data,ontology,classes)


			print('{}\t{}\t{}\t{}\t{}\n'.format(tcid,acc,substrateData,'\t'.join(pos),'\t'.join(hits)))



	outputFile.close()

if __name__ == "__main__":

	#Initialize tcids
	tcids = set()

	#initialize maps
	tcidMaps = {}
	substrates = {}
	accessions = {}


	directory = sys.argv[1]
	output = sys.argv[2]

	genomes,genomeFiles = getGenomes(directory)


	#get substrate information
	classes = set(['CHEBI:33696','CHEBI:33838','CHEBI:36976','CHEBI:23888','CHEBI:33281','CHEBI:18059','CHEBI:33229',
                    'CHEBI:25696','CHEBI:33575','CHEBI:24834','CHEBI:25697','CHEBI:36915','CHEBI:33709','CHEBI:16670',
                    'CHEBI:26672','CHEBI:31432','CHEBI:35381','CHEBI:50699','CHEBI:18154','CHEBI:72813','CHEBI:88061',
                    'CHEBI:10545','CHEBI:25367','CHEBI:24403','CHEBI:23357','CHEBI:17627','CHEBI:83821','CHEBI:17237'])

	substrate_data = get_substrate_data('http://www.tcdb.org/cgi-bin/substrates/getSubstrates.py')
	ontology = build_ontology('./chebi.obo')


	for genome in genomes:

		lines = readLines(genomeFiles[genome])

		tcidMaps[genome],tcids,accessions = mapTCID(lines,tcids,accessions)

	tcids = sorted(list(tcids),key=lambda x: x.split('.'))

	printTable(genomes,tcids,tcidMaps,accessions,substrate_data,ontology,classes,output)
