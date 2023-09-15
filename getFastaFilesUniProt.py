# -*- coding: utf-8 -*-
"""
Created on Tue Sep 18 11:38:41 2018

@author: Administrator
"""
import requests
import re
import pickle
''' Programmatically collect all fasta files from Uniprot for the human proteome '''


#''' Stored Uniprot data (don't download each time) '''
#fo = open('uniProtDat.dat', 'rb')
#result3 = pickle.load(fo)
#fo.close()
#
#''' Parse result string ===================================='''
#
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
#dateSeqMod = [] #17
#
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
#
#''' Get fasta protein sequences =========================='''
#
#BASE = 'http://www.uniprot.org'
#KB_ENDPOINT = '/uniprot/'
#TOOL_ENDPOINT = '/uploadlists/'



#payload = {'query': 'name:"polymerase alpha" AND taxonomy:mus AND reviewed:yes',
#'format': 'fasta',
## comment the following line to exclude isoforms
#'include': 'yes',
##}
#payload = {'query': 'proteome:(homo sapiens)',
#'format': 'fasta',
## comment the following line to exclude isoforms
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
#fastaNms = re.findall(r'>\w\w\|\w+\|\w+',result.text, re.MULTILINE) # get the protein Id
# and name from the fasta files    
#
#f = open('humanProteomePrgm.fasta', 'w')
#f.write('./'+ result.text)
#f.close()

with open('humanProteomePrgm.fasta', 'r') as f:
        rtext = f.read()
        
fastaNms = re.findall(r'>\w\w\|\w+\|\w+',rtext, re.MULTILINE) # get the protein Id
seqs = re.findall(r'\n[A-Z\n-]{4,}',rtext, re.MULTILINE) # get th

nmSeq = re.findall(r'>\w\w\|\w+\|\w+.*\n[A-Z\n-]{4,}' , rtext, re.MULTILINE) # get each individual fasta (that is not an isoform)
#
#''' Store proteins in new shorter fasta files '''
pN = 500 # number of proteins in each file

cnt = 0
cntAll = 0

fstStr = ''
for dx in nmSeq:
    fstStr = fstStr + dx
    cnt = cnt + 1
    cntAll = cntAll + 1
    if cnt == pN:
        
        # Write to file
        prtIds = re.findall(r'\|\w+\|', fstStr)
        #f = open('hmnProt_' + prtIds[0].replace("|", "") + 'to' + prtIds[pN - 1].replace("|", "") + '.fasta', 'w+')
        f = open('/home/dave/BioinformaticsWork/HumanProteomeFastaFiles/hmnProt_' + str(cntAll - pN + 1) + 'to' + str(cntAll) + '.fasta', 'w+' )
        f.write(fstStr)
        f.close()
        cnt = 0
        # reset str
        fstStr = ''
    
    if cntAll == 4*pN:
        break
    
        
    