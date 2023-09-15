# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 15:04:30 2018

@author: dave
"""

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
#
#""" Request Uniprot data ==================================================="""
#
#BASE = 'http://www.uniprot.org'
#KB_ENDPOINT = '/uniprot/'
#TOOL_ENDPOINT = '/uploadlists/'
##
#col = ['id', # uniprot id
#       'entry_name', # protein name
#       'genes', # gene name
#       'reviewed', # reviewed or unreviewed
#       'existence', # where does it exist
#       'comment(SUBCELLULAR LOCATION)', # cellular location
#       'keywords',
#       'database(DrugBank)',
#       'database(PROSITE)',
#       'database(Reactome)',
#       'database(ENSEMBL)',
#       'comment(DISEASE)',
#       'feature(TRANSMEMBRANE)',
#       'go',
#       'length',
#       'created',
#       'last-modified',
#       'sequence-modified',
#       'citation'
#    ]
#
#
#payload3 = {'query': 'proteome:(homo sapiens)','format': 'tab',
#           'columns':
#            ','.join(col),
#            }
#
#
##payload3 = {'query': 'name:"polymerase alpha" \
##AND taxonomy:mus AND reviewed:yes','format': 'tab', \
##           'columns': 'acc,entry_name,reviewed,length,created'}
#
#print('About to retrieve data from Uniprot')
#result3 = requests.get(BASE + KB_ENDPOINT, params=payload3)
#print('\n')
#if result3.ok:
#    print('Uniprot data retrival OK')
#    #print(result3.text)
#else:
#    print('Something went wrong ', result3.status_code)
#  
#
#with open('uniProtRawDat' + time.strftime("%d_%m_%Y") + '.dat', 'wb') as ff:
#    pickle.dump(result3, ff)
#ff.close()
#
#
#
#''' Stored Uniprot data (don't download each time) ========================='''
##print('Opening Stored Uniprot results from pickle file')
##fo = open('uniProtDat071118.dat', 'rb')
##result3 = pickle.load(fo)
##fo.close()
#
##f = open('test.txt', 'w')
##f.write(result3.text)
##f.close()
#
#''' Parse result string ===================================='''
#print('Parsing Uniprot data results')
#rows = result3.text.split('\n') # split into rows
#
#colNm = rows[0].split('\t') # get column name
#
#rowN = len(rows)
#
#uniPrtId = [] # uniProt Id (up shows it is from uniprot) 0
#proteinName = [] #1
#geneName_up = [] #2
#
#status_up = [] #4
#existence_up = [] #5
#subCelLoc_up = [] #6
#keyword_up = [] #7
#drgBnkID_up = [] #8
#prositeID_up = [] #9
#reactomeID_up = [] #10
#invlDis_up = [] #12
#trnMem_up = [] #13
#GO_up = [] #14
#length_up = []
#dateCreate_up = [] #15
#dateMod = [] #16
#dateSeqMod = [];
#pubMedId_up = [] #18
#
#
#
##ensemblID = [] # get all the ensembl IDs for every protein
##ensemblIDSplt = [] # get all ensembl IDs individually
#
#for dx in rows[1:-1]:
#    tCol = dx.split('\t')
#
#    uniPrtId.append(tCol[0]) # uniProt Id (up shows it is from uniprot) 0
#    proteinName.append(tCol[1]) #1
#    geneName_up.append(tCol[2]) #2
#    status_up.append(tCol[3]) #4
#    existence_up.append(tCol[4]) #5
#    subCelLoc_up.append(tCol[5]) #6
#    keyword_up.append(tCol[6]) #7
#    drgBnkID_up.append(tCol[7]) #8
#    prositeID_up.append(tCol[8]) #9
#    reactomeID_up.append(tCol[9]) #10
#    invlDis_up.append(tCol[11]) #12
#    trnMem_up.append(tCol[12]) #13
#    GO_up.append(tCol[13]) #14
#    length_up.append(tCol[14])
#    dateCreate_up.append(tCol[15]) #15
#    dateMod.append(tCol[16]) #16
#    dateSeqMod.append(tCol[17]) #17    
#    pubMedId_up.append(tCol[18])
#    
#
#    
#""" Tickbox of transmembrane and located on cell membrane -----------------"""    
#trnsMemEv_Up = [0]*rowN
#cellTrnsMem_up = [0]*rowN
#secreted_up = [0]*rowN
#
#cnt = 0
#for ex, dx in zip(subCelLoc_up, trnMem_up):# find membrane reference
#    if "Secreted" in ex:
#        secreted_up[cnt] = 1
#    
#    if dx:
#        trnsMemEv_Up[cnt] = 1
#        
#        if "Cell membrane" in ex:
#            cellTrnsMem_up[cnt] = 1
#    cnt += 1
#
#
#
#""" Get fasta sequences ===================================================="""
#print('Getting fasta sequences')
##
#BASE = 'http://www.uniprot.org'
#KB_ENDPOINT = '/uniprot/'
#TOOL_ENDPOINT = '/uploadlists/'
##
#payload = {'query': 'proteome:(homo sapiens)',
#'format': 'fasta',
### comment the following line to exclude isoforms
##'include': 'yes',
#}
#
#
#result = requests.get(BASE + KB_ENDPOINT, params=payload)
#if result.ok:
#    print(result.text[:500])
#else:
#    print('Something went wrong: ', result.status_code)
#    
#fastaNms = re.findall(r'>\w\w\|\w+\|\w+',result.text, re.MULTILINE) # get the protein Id and name from the fasta files    
#seqs = re.findall(r'\n[A-Z\n-]{4,}',result.text, re.MULTILINE) # get sequences
#
#nmSeq = re.findall(r'>\w\w\|\w+\|\w+.*\n[A-Z\n-]{4,}' , result.text, re.MULTILINE) # get each individual fasta (that is not an isoform)
#
#f = open('humanProteomePrgm.fasta', 'w')
#f.write('./'+ result.text)
#f.close()
#
#""" Pickle sequences -------------------------------------------------------"""
#with open('fastaDat' + time.strftime("%d_%m_%Y") + '.dat', 'wb') as ff:
#    pickle.dump(nmSeq, ff)
#ff.close()
#
#with open('proteinSeqs' + time.strftime("%d_%m_%Y") + '.dat', 'wb') as ff:
#    pickle.dump(seqs, ff)
#ff.close()
#
#with open('ProteinNms' + time.strftime("%d_%m_%Y") + '.dat', 'wb') as ff:
#    pickle.dump(fastaNms, ff)
#ff.close()
#
#""" get ensembl Ids ========================================================"""
#BASE = 'http://www.uniprot.org'
#KB_ENDPOINT = '/uniprot/'
#TOOL_ENDPOINT = '/uploadlists/'
#
#
#print("Getting Ensembl Id's sequences")
#cnt = 0
#
#ensId = []#[None]*len(uniPrtId) # store the ensembl IDs
#uniPrtEnsId = []#[None]*len(uniPrtId) # store uniprt ID relating to the ensembl ones
#
#
## seem to be able to get about 1000 ids at a time, a lot quicker than
### getting them individually
#n = 1000
#
#for dx in range(0, rowN, n):
#    
#    st = dx
#    ed = dx + n 
#      
#    
#    if ed > rowN:
#        ed = rowN
#        
#    print('Collecting ensembl IDs ' +  str(st) + ' to ' + str(ed) + ' of ' +  str(rowN))
#    
#    payload = {'from': 'ACC + ID', \
#               'to':'ENSEMBL_ID', \
#               'format' : 'tab', \
#               'query': ' '.join(uniPrtId[st:ed]), \
#    }
#    time.sleep(0.5)
#    response = requests.get(BASE + TOOL_ENDPOINT, params=payload)
#    strp = response.text.strip().split()
#    
#    tCnt = 0
#    
##    if strp[-2] != uniPrtId[ed - 1]:
##        print('Haven\'t got last result')
#        
#    
#    for ex in range(2, len(strp), 2):
#        
#        
##        uniPrtEnsId[tCnt] = strp[ex]
##        ensId[tCnt] = strp[ex + 1]
#        uniPrtEnsId.append(strp[ex])
#        ensId.append(strp[ex + 1])        
#        tCnt = tCnt + 1
#    
#    cnt = cnt + 1
#    
#''' pickle ensembl IDs ====================================================='''
#
#ensUniPrtIds = [ensId, uniPrtEnsId]
#
#
#with open('ensId'+ time.strftime("%d_%m_%Y") +'.dat', 'wb') as ff:
#    pickle.dump(ensUniPrtIds, ff)
#ff.close()

''' Get gene names from ensembl============================================='''
with open('ensId21_11_2018.dat', 'rb') as fff:
    ensUniPrtIds2 = pickle.load(fff)
ensId = ensUniPrtIds2[0][:]
uniPrtEnsId = ensUniPrtIds2[1][:]

server = "http://rest.ensembl.org"
ext = "/lookup/id"
headers={ "Content-Type" : "application/json", "Accept" : "application/xml"}

ensIdN = 1000 # number of 
#assNm = [None]*len(ensId)

disNm = {}#[None]*len(ensId)

ensIdSetLst = list(set(ensId))
ensIdChk = [None]*len(ensIdSetLst)

for cx in range(0, math.ceil(len(ensIdSetLst)), ensIdN):
    
    st = cx
    ed = cx + ensIdN
    
    
    
    if ed > len(ensIdSetLst):
        ed = len(ensIdSetLst)
        
    print('Extracting names: ', st, ' to ', ed )    

    cnt = 0
    dat = '{"ids" : ['
    for dx in ensIdSetLst[st:ed]:
        cnt = cnt + 1
        
        if cnt < ed - st:
            dat = dat +'"' + dx +'", '
        else:
            dat = dat +'"' + dx +'" '
    
    dat = dat + '] }'

    r = requests.post(server+ext, headers=headers, data=dat)
    ensemInfo = json.loads(r.text)
    
    for ex, fx in zip(ensIdSetLst[st:ed], range(st, ed)):
        if ensemInfo[ex]:
            disNm[ex] =  ensemInfo[ex]['display_name']           
        else:
            disNm[ex] = ''
            
        
        #assNm[fx] = ensemInfo[ex]['assembly_name']
#        disNm[fx] = ensemInfo[ex]['display_name']
        ensIdChk[fx] = ex

#    if cx > 1:
#        break
with open('geneNmENSEBL_Dict' + time.strftime("%d_%m_%Y") + '.dat', 'wb') as ff:
    pickle.dump(disNm, ff)
ff.close()
