# -*- coding: utf-8 -*-
"""
Created on Wed Nov 21 14:33:34 2018

@author: DavidJames
"""

import pickle

def unPickleUniProt(str):
    
    print('Opening Stored Uniprot results from pickle file')
    fo = open(str, 'rb')
    result3 = pickle.load(fo)
    fo.close()
    
    ''' Parse result string ===================================='''
    print('Parsing Uniprot data results')
    rows = result3.text.split('\n') # split into rows
    
    colNm = rows[0].split('\t') # get column name
    
    rowN = len(rows)
    
    uniPrtId = [] # uniProt Id (up shows it is from uniprot) 0
    proteinName = [] #1
    geneName_up = [] #2
    
    status_up = [] #4
    existence_up = [] #5
    subCelLoc_up = [] #6
    keyword_up = [] #7
    drgBnkID_up = [] #8
    prositeID_up = [] #9
    reactomeID_up = [] #10
    invlDis_up = [] #12
    trnMem_up = [] #13
    GO_up = [] #14
    length_up = []
    dateCreate_up = [] #15
    dateMod = [] #16
    dateSeqMod = [];
    pubMedId_up = [] #18
    
    
    
    #ensemblID = [] # get all the ensembl IDs for every protein
    #ensemblIDSplt = [] # get all ensembl IDs individually
    
    for dx in rows[1:-1]:
        tCol = dx.split('\t')
    
        uniPrtId.append(tCol[0]) # uniProt Id (up shows it is from uniprot) 0
        proteinName.append(tCol[1]) #1
        geneName_up.append(tCol[2]) #2
        status_up.append(tCol[3]) #4
        existence_up.append(tCol[4]) #5
        subCelLoc_up.append(tCol[5]) #6
        keyword_up.append(tCol[6]) #7
        drgBnkID_up.append(tCol[7]) #8
        prositeID_up.append(tCol[8]) #9
        reactomeID_up.append(tCol[9]) #10
        invlDis_up.append(tCol[11]) #12
        trnMem_up.append(tCol[12]) #13
        GO_up.append(tCol[13]) #14
        length_up.append(tCol[14])
        dateCreate_up.append(tCol[15]) #15
        dateMod.append(tCol[16]) #16
        dateSeqMod.append(tCol[17]) #17    
        pubMedId_up.append(tCol[18])
        
    
        
    """ TTickbox of transmembrane and located on cell membrane -----------------"""    
    trnsMemEv_Up = [0]*rowN
    cellTrnsMem_up = [0]*rowN
    secreted_up = [0]*rowN
    
    cnt = 0
    for ex, dx in zip(subCelLoc_up, trnMem_up):# find membrane reference
        if "Secreted" in ex:
            secreted_up[cnt] = 1
        
        if dx:
            trnsMemEv_Up[cnt] = 1
            
            if "Cell membrane" in ex:
                cellTrnsMem_up[cnt] = 1
        cnt += 1    
        
    
    return uniPrtId, proteinName,geneName_up,status_up,existence_up,\
    subCelLoc_up,keyword_up,drgBnkID_up,prositeID_up,reactomeID_up,\
    invlDis_up,trnMem_up,GO_up,length_up,dateCreate_up,dateMod,dateSeqMod,pubMedId_up,\
    trnsMemEv_Up,cellTrnsMem_up,secreted_up