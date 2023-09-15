# ADC-database-generation-scripts
Python scripts for accessing and parsing data from bioinformatics resources to create a database for identifying potential ADC protein targets

## Description of scripts
1) **dwnLoadHPA_dataandWritetoDB.py** - Download data expression data from Human protein atlas and write to ADC database.
2) **GetDataFromUniProtAndPickle.py** - Download protein data from Uniprot, including sequences and pickle. For each protein download corresponding ENSEMBL gene IDs from ENSEMBL.
3) **WriteUniprotDatatoDB.py** - Write UniProt protein data to ADC database
4) **getFastaFilesUniProt.py** - Download fasta files of protein sequences from UniProt
5) **proTargetMakeTables.py** - Python helper functions for connecting to and creating new MySQL databases
6) **proteinTarTables.py** - MySQL strings for generating ADC database tables
7) **python_mysql_db_config.py** - Helper function for retrieving database config
8) **readTMResults.py** - Script to parse transmembrane prediction results from topcons web server
9) **tmResultsToDB.py** - Write transmembrane prediction results to ADC database
10) **uniProtToDBFunctions.py** - Helper functions to write Uniprot data to ADC database
