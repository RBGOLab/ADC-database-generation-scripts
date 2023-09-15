# -*- coding: utf-8 -*-
"""
Created on Fri Oct 12 12:13:50 2018

@author: dave
"""
import re
import os.path



class topconRes: 
    ''' Class to read in and parse topcons result file '''    
    
    ''' Constructor '''
    def __init__(self, pth, fn, resDirPre, seqNo, gnNm): # constructor
        self.resPth = pth + resDirPre + str(seqNo) + fn

        if os.path.isfile(pth + resDirPre + str(seqNo) + fn):         
        
            self.exst = 1
            #print('File ' +  pth + resDirPre + str(seqNo) + fn + ' DOES exist')
            
        else:
            
            self.exst = 0
            
            print('File ' +  pth + resDirPre + str(seqNo) + fn + ' does not exist')
     
        self.gnNm = gnNm
        self.seqNo = seqNo
    ''' Varaibles =========================================================='''
    
    ''' Gene name '''
    #gnNm = ''    
    
    ''' Topologies '''
    seq = ''
    predTOPCONS = ''
    predOct = ''
    predPhil = ''
    predPolPho = ''
    predScampi = ''
    predSpoct = ''  
  
    
    ''' TM regions '''
    topConTMDx = None
    octTMDx = None
    philTMDx = None
    polPhoTMDx = None
    scampiTMDx = None
    spoctTMDx = None
    
    ''' Number of TM regions '''
    topConTMN = None
    octTMN = None
    philTMN = None
    polPhoTMN = None
    scampiTMN = None
    spoctTMN = None
    
    noTMPreds = None

    ''' Outside regions '''    
    topConODx = None
    octODx = None
    philODx = None
    polPhoODx = None
    scampiODx = None
    spoctODx = None

    ''' Number of O regions '''
    topConON = None
    octON = None
    philON = None
    polPhoON = None
    scampiON = None
    spoctON = None
    
    ''' Length of O regions '''
    
    topConOLens = None
    octOLens = None
    philOLens = None
    polPhoOLens = None
    scampiOLens = None
    spoctOLens = None
                 
    ''' Public Methods ====================================================='''
    def readRes(self): # read line text file
        with open(self.resPth) as self.file:
            self.dat = self.file.readlines()
        
            
            
        self.tgnNm = re.search(r'\|\w+\|', self.dat[6])
        if self.tgnNm:
            s = self.tgnNm[0]
            ss = s.replace('|', '')
            if ss != self.gnNm:
                print("Gene names don't match finishedSeqNm = " + self.gnNm + " query.results.txt gnNm = " + ss + " fndx = " + str(self.seqNo))
            
    def assignRes(self):# assign results to string varaibles
        self.seq = self.dat[9].rstrip()
        self.prtnLen = len(self.seq)
        self.predTOPCONS = self.dat[13].rstrip()
        self.predOct = self.dat[17].rstrip()
        self.predPhil = self.dat[21].rstrip()
        self.predPolPho = self.dat[25].rstrip()
        self.predScampi = self.dat[29].rstrip()
        self.predSpoct = self.dat[33].rstrip()
         
    def getTMRegions(self): # get the start and end indices of transmembrane regions
        self.topConTMDx = self.getSpan(self.predTOPCONS, 'M*')        
        self.octTMDx = self.getSpan(self.predOct, 'M*')
        self.philTMDx = self.getSpan(self.predPhil, 'M*')
        self.polPhoTMDx = self.getSpan(self.predPolPho, 'M*')
        self.scampiTMDx = self.getSpan(self.predScampi, 'M*')
        self.spoctTMDx = self.getSpan(self.predSpoct, 'M*')
        
        self.topConTMN = len(self.topConTMDx)
        self.octTMN = len(self.octTMDx)
        self.philTMN = len(self.philTMDx)
        self.polPhoTMN = len(self.polPhoTMDx)
        self.scampiTMN = len(self.scampiTMDx)
        self.spoctTMN = len(self.spoctTMDx) 
        
        t_tmN = [self.topConTMN, self.topConTMN, self.philTMN, self.polPhoTMN, self.scampiTMN, self.spoctTMN]       
        
        self.noTMPreds = sum([x for x in t_tmN if x > 0])

    def getORegions(self): # get the outside regions        
        self.topConODx = self.getSpan(self.predTOPCONS, 'o*')        
        self.octODx = self.getSpan(self.predOct, 'o*')
        self.philODx = self.getSpan(self.predPhil, 'o*')
        self.polPhoODx = self.getSpan(self.predPolPho, 'o*')
        self.scampiODx = self.getSpan(self.predScampi, 'o*')
        self.spoctODx = self.getSpan(self.predSpoct, 'o*')
        
        self.topConON = len(self.topConODx)
        self.octON = len(self.octODx)
        self.philON = len(self.philODx)
        self.polPhoON = len(self.polPhoODx)
        self.scampiON = len(self.scampiODx)
        self.spoctON = len(self.spoctODx)
        
        self.topConOLens = self.getLens(self.topConODx)        
        self.octOLens = self.getLens(self.octODx)
        self.philOLens = self.getLens(self.philODx)
        self.polPhoOLens = self.getLens(self.polPhoODx)
        self.scampiOLens = self.getLens(self.scampiODx)
        self.spoctOLens = self.getLens(self.spoctODx)        
    
    def getSigPep(self): # find if any of the signal peptide predictors predict signal peps    
        self.topConSDx = self.getSpan(self.predTOPCONS, 'S*')
        self.spoctSDx = self.getSpan(self.predSpoct, 'S*') 
        self.polyPhoSDx = self.getSpan(self.predPolPho, 'S*') 
        self.philSDx = self.getSpan(self.predPhil, 'S*') 

    ''' Close the file ===================================================='''
    def closeFile(self):
        self.file.close()    
    
    ''' Run all the functions to parse data and write to files ============='''
    def runAll(self):
        if self.exst:
            self.readRes()
            self.assignRes()
            self.getTMRegions()
            self.getORegions()
            self.getSigPep()
            self.closeFile()
        else:
            
            print('Could not find the file, no results')
    

    ''' Private methods ==================================================='''
    
            
    def getSpan(self, strng, expr): # returns the start and end index of each  
        
        dx = [(m.span()) for m in re.finditer(expr, strng) if m.group()] # returns index of each 
    
        return dx
                
    def getLens(self, pdx): # finds the lengths of the regions
        l = [None]*len(pdx)
        cnt = 0        
        for dx in pdx:
            l[cnt] = dx[1] - dx[0]
            cnt = cnt + 1
            
        return l
            
"""========================================================================"""   
class topConFinSeq:
    
    ''' Constructor ========================================================'''
    def __init__(self, pth, fnFinSeq): # constructor

        self.finSeqPth = pth + fnFinSeq
        
            
        if os.path.isfile(pth + fnFinSeq):         
        
            self.exstFinSeqs = 1
            print('Ok')
            
        else:
            
            self.exstFinSeqs  = 0
            
            print('File ' +  pth + fnFinSeq + ' does not exist') 
            
    ''' Load file =========================================================='''
    def loadFile(self):
        with open(self.finSeqPth) as self.file:
            self.dat = self.file.readlines()
            
    ''' Close the file ====================================================='''
    def closeFile(self):
        self.file.close()
            
    def orderBySeqNm(self):
        self.orderedSeqs = [None]*len(self.dat) # empty list
        self.gnNm = [None]*len(self.dat) # empty list
        for dx in self.dat:
            seqStr = re.findall(r'seq_\d*', dx)
            seqStr = seqStr[0]
            seqN = int(seqStr.replace('seq_', ''))
            
            gnNmStr = re.findall(r'\|\w*\|',dx) # get just the sequence name
            gnNmStr = gnNmStr[0]
            
            self.orderedSeqs[seqN] = dx
            s = gnNmStr.replace('|', '')
            self.gnNm[seqN] = s 
        
            
            
        
        
        