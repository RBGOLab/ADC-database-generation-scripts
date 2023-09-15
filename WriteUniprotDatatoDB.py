# -*- coding: utf-8 -*-
"""
Created on Wed Nov 14 14:11:41 2018

@author: dave
"""

#
import requests # library to access url
#import matplotlib #
#import map_retrieve as mr
#import map_retrieve2 as mr2
import pickle
import time 
import math
from mysql.connector import connection, errorcode, MySQLConnection, Error
from python_mysql_db_config import read_db_config, connect
#from mySqlInsertEG import insert_cols

from xml.etree import ElementTree as ET

import re
import proTargetMakeTables as mkTb
import proteinTarTables as tabls
import json
import uniProtToDBFunctions2 as f

""" Open pickled Uniprot data =============================================="""

uniPrtId, proteinName,geneName_up,status_up,existence_up,\
    subCelLoc_up,keyword_up,drgBnkID_up,prositeID_up,reactomeID_up,\
    invlDis_up,trnMem_up,GO_up,length_up,dateCreate_up,dateMod,dateSeqMod,pubMedId_up,\
    trnsMemEv_Up,cellTrnsMem_up,secreted_up = f.unPickleUniProt('uniProtRawDat19_11_2018.dat')
    
""" Open fasta sequences ==================================================="""

fo = open('proteinSeqs19_11_2018.dat', 'rb')
proSeqs = pickle.load(fo)
fo.close()

fo = open('ProteinNms19_11_2018.dat', 'rb')
proNms = pickle.load(fo)
fo.close()

""" Open pickled ENSEMBL data =============================================="""

with open('ensId21_11_2018.dat', 'rb') as fff:
    ensUniPrtIds2 = pickle.load(fff)
ensId = ensUniPrtIds2[0][:]
uniPrtEnsId = ensUniPrtIds2[1][:] 

with open('geneNmENSEBL_Dict26_11_2018.dat', 'rb') as fff:
    disNm = pickle.load(fff)

""" Connect to database ===================================================="""

cnx, cur = mkTb.dbconnect( '127.0.0.1', 'root','Four4Legs!Word#Rate0', 'ADC_211118') # connect to DB

""" Write data to DB tables ================================================"""

""" Write Uniprot_Proteins table -------------------------------------------"""

''' Make tables ............................................................'''

for dx in reversed(tabls.TabNms): # delete old tables if they exist
    print('Deleting' + dx)
    cur.execute("DROP TABLE IF EXISTS " + dx)    

for dx in (tabls.TabNms): # uses the list of tables specified in proteinTarTables.py
    print('Creating table' + dx)
    cur.execute(tabls.TABLES[dx])
  
print('Created tables')
tabDx = -1

tabDx = tabDx + 1
existSet = (set(existence_up))    
existN = len(existSet)
existList = list(existSet)

existId = [None]*existN
cnt = 0
for ex in existSet:
    cur.execute("INSERT IGNORE INTO "+tabls.TabNms[tabDx]+"(Existence) VALUES(%s)", (ex,))
    cur.execute('SELECT Id FROM ProteinEvidence_UP WHERE Existence LIKE %s ', (ex, ))
    existId[cnt] = cur.fetchone()[0]
    cnt = cnt + 1
print('Inserted existence')
existDict = dict(zip(existList, existId))

''' Populate Uniprot_Protein table..........................................'''
tabDx = tabDx + 1
for ac, ex, lng, subCelLocDx, trnsMemBoolDx, celTrnBoolDx, secretedBoolDx, proNmsDx, proSeqDx, dtCrtDx, dtModDx, dtModSeqDx \
    in zip(uniPrtId, existence_up, length_up,subCelLoc_up,  trnsMemEv_Up, cellTrnsMem_up,secreted_up, proNms, proSeqs, dateCreate_up, dateMod, dateSeqMod):
    # Need to check the Names for the uniprot 
    
    if ac in proNmsDx: 
        exId = str(existDict[ex]) 
        cur.execute("INSERT IGNORE INTO "+tabls.TabNms[tabDx]+"(Accession, ExistenceId, Length, SubCellularLocation\
    , TM_RegionsYN, TM_CellMembraneYN, SecretedYN, ProteinSequence, DateCreated_UP, DateModified_UP, DateSeqModified_UP) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", \
    (ac,exId, lng, subCelLocDx, trnsMemBoolDx, celTrnBoolDx, secretedBoolDx, proSeqDx, dtCrtDx, dtModDx, dtModSeqDx))
    
    else:
        print('Uniprot Accession name' + ac + ' does not match fasta sequence ' +  proNmsDx + ' not added to DB')
    
print('Populated UniProt protein table')

''' Populate ENSEMBL_Genes table and Uniprot_ENSEMBLJunc ==================='''

print('Populate ENSEMBL genes table and Uniprot/ENSEMBL junction table')
tabDx = tabDx + 1
for updx, endx in zip(uniPrtEnsId, ensId):
    # Insert into genes table
    cur.execute("INSERT IGNORE INTO " +tabls.TabNms[tabDx]+"(Ensembl_Gene_Id, GeneName) VALUES(%s, %s)",(endx,disNm[endx]) )
    # Insert into junction table
    cur.execute("INSERT IGNORE INTO " + tabls.TabNms[tabDx + 1] + "(UniProt_Accession, ENSEMBL_Gene_Id) VALUES(%s, %s)", (updx, endx))
print('Inserted EnsemblGenes')

cnx.commit()
cur.close()
cnx.close()


