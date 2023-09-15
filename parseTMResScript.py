# -*- coding: utf-8 -*-
"""
Created on Fri Oct 12 12:18:04 2018

@author: dave
"""

import readTMResults as TMrs

'''Routine for parsing topcons data======================================= '''
pth = '/media/dave/Seagate Backup Plus Drive/Bioinformatics/TransmembraneTools/TopConsResults/FirstAttempt_Protein0to39999_270918/rst_6ea8vY/seq_'
fn = '/query.result.txt'

fnum = [1145]
fnum = [10096]

for fndx in fnum:

    pth = pth + str(fndx)
    f1 = TMrs.topconRes(pth, fn) # inputs 

    f1.runAll()