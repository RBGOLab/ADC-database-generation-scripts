# -*- coding: utf-8 -*-
"""
Created on Fri Sep  7 17:09:24 2018

@author: dave
"""
TabNms = ['ProteinEvidence_UP', 'UniProt_Proteins',  'ENSEMBL_Genes', 'UniProtENSEMBLJunc']

""" TABLES ================================================================"""
TABLES = {} # starts life as empty dictionar


dx = 0
""" Protein Evidence ---------------------------------------------- """

TABLES[TabNms[dx]] = (
        "CREATE table IF NOT EXISTS `" + TabNms[dx] + "` ("
        "`Id` int(4) NOT NULL AUTO_INCREMENT, "
        "`Existence` varchar(40) UNIQUE, "
        "PRIMARY KEY (Id)"
        ") ENGINE=InnoDB"
    )
        
""" Proteins_UniProt table -------------------------------------------------""" 
dx = dx + 1        
TABLES[TabNms[dx]] = (
    " CREATE table IF NOT EXISTS `" + TabNms[dx] + "` ("
    "`Id` int(20) NOT NULL AUTO_INCREMENT, "
    "`Accession` varchar(10) NOT NULL UNIQUE," #"`Existence` varchar(40),"  
    "`ExistenceId` int(4),"
    "`Length` int(11), "
    "`SubCellularLocation` text,"
    "`TM_RegionsYN` bit(1),"
    "`TM_CellMembraneYN` bit(1),"
    "`SecretedYN` bit(1),"
    "`ProteinSequence` text,"
    "`DateCreated_UP` DATE,"
    "`DateModified_UP` DATE,"
    "`DateSeqModified_UP` DATE,"
    "`DateUploadedToADCTargeter` DATE,"
    "KEY (Accession), "
    "KEY (TM_RegionsYN),"
    "KEY (TM_CellMembraneYN),"
    "KEY (DateModified_UP),"
    "KEY (DateSeqModified_UP),"
    "PRIMARY KEY (Id),"
    "INDEX `proteinExInd` (ExistenceId),"
    "FOREIGN KEY (ExistenceId) "
    "REFERENCES ProteinEvidence_UP(Id) "
    "ON DELETE CASCADE"
    ")  ENGINE=InnoDB")  
    
    
"""To add later: Keywords, Invo, transmembrane, secreted """


""" ENSEMBL_Genes ----------------------------------------------------------"""
dx = dx + 1
TABLES[TabNms[dx]] = (
    "CREATE table IF NOT EXISTS `"+TabNms[dx]+"` ("
    "`Id` int(20) NOT NULL AUTO_INCREMENT, "
    "`Ensembl_Gene_Id` char(15) NOT NULL UNIQUE, "
    "`GeneName` char(30),"
    "KEY (Ensembl_Gene_Id),"
    "PRIMARY KEY (Id)"
    ")  ENGINE=InnoDB")

""" UniProt_ENSEMBL_Junction """
dx = dx + 1
TABLES[TabNms[dx]] = (
    "CREATE table IF NOT EXISTS `"+TabNms[dx]+"`( "
    "`UniProt_Accession` varchar(10), "
    "`ENSEMBL_Gene_Id` char(15),"
    "PRIMARY KEY (UniProt_Accession, ENSEMBL_Gene_Id),"
    ""    
    "FOREIGN KEY (UniProt_Accession)"
    "REFERENCES UniProt_Proteins(Accession)"
    "ON DELETE CASCADE,"
    ""
    "FOREIGN KEY (ENSEMBL_Gene_ID)"
    "REFERENCES ENSEMBL_Genes(Ensembl_Gene_Id)"
    "ON DELETE CASCADE"
    ")  ENGINE=InnoDB")



#addProtein = ("INSERT INTO Proteins_UniProt
#    
#    "")

""" HPA data tables ========================================================"""
TabNmHPA = ['Tissues_HPA', 'HealthyTissueLevels_HPA', 'CellType_HPA', 'HealthyCellLevels_HPA'] #,Healthy_HPA', 'Cancer_HPA']

ex = -1
TABLES_HPA = {}

''' Tissues HPA table -------------------------------------------------------'''
ex = ex + 1
TABLES_HPA[TabNmHPA[ex]] = (
    "CREATE TABLE IF NOT EXISTS `" + TabNmHPA[ex] + "`("
    "`Id` int(20) NOT NULL AUTO_INCREMENT,"
    "TissueName varchar(20) NOT NULL UNIQUE,"
    "PRIMARY KEY (Id)"
    ") ENGINE = InnoDB"
)

''' HealthyTissueLevels_HPA table ----------------------------------------'''
# Also stores the expression level for a particular protein, tissue combination
# Technically a junction table between ENSEMBL genes and tissues tables with 
# additional levels column

ex = ex + 1
TABLES_HPA[TabNmHPA[ex]] = (
    "CREATE TABLE IF NOT EXISTS `" + TabNmHPA[ex] + "`("
    "`ENSEMBL_Gene_Id` char(15),"
    "Tissue_Id int(20),"
    "HealthyTissueLevel varchar(20),"
    "PRIMARY KEY (ENSEMBL_Gene_Id, Tissue_Id),"
    "KEY (HealthyTissueLevel),"
    " "
    "FOREIGN KEY (ENSEMBL_Gene_Id) "
    "REFERENCES ENSEMBL_Genes(Ensembl_Gene_Id) "
    "ON DELETE CASCADE, "
    " "
    "FOREIGN KEY (Tissue_Id) "
    "REFERENCES Tissues_HPA(Id) "
    "ON DELETE CASCADE"
    ") ENGINE = InnoDB"    
)



''' Cell type HPA table -----------------------------------------------------'''

ex = ex + 1
TABLES_HPA[TabNmHPA[ex]] = (
    "CREATE TABLE IF NOT EXISTS `" + TabNmHPA[ex] + "`("
    "`Id` int(20) NOT NULL AUTO_INCREMENT,"
    "CellType varchar(40) NOT NULL UNIQUE,"
    "PRIMARY KEY (Id)"
    ") ENGINE = InnoDB"
)

''' HealthyCellLevels junction table ----------------------------------------'''
# References ENSEMBL ID, CellType_HPA and Tissue_HPA

ex = ex + 1
TABLES_HPA[TabNmHPA[ex]] = (
    "CREATE TABLE IF NOT EXISTS `" + TabNmHPA[ex] + "`("
    "HealthyCellLevel varchar(20),"
    "ENSEMBL_Gene_Id char(15),"
    "Tissue_Id int(20),"
    "CellType_Id int(20),"
    "PRIMARY KEY (ENSEMBL_Gene_Id, Tissue_Id, CellType_Id), "
    "KEY (HealthyCellLevel),"
    " "
    "FOREIGN KEY (ENSEMBL_Gene_Id) "
    "REFERENCES ENSEMBL_Genes(Ensembl_Gene_Id) "
    "ON DELETE CASCADE, "
    " "
    "FOREIGN KEY (Tissue_Id) "
    "REFERENCES Tissues_HPA(Id) "
    "ON DELETE CASCADE, "
    " "
    "FOREIGN KEY (CellType_Id) "
    "REFERENCES CellType_HPA(Id) "
    " ON DELETE CASCADE "
    ") ENGINE = InnoDB"    
)


''' Cancer tissues HPA ----------------------------------------------------'''

fx = -1 
TABLES_HPA_PATH = {}


TabNmHPAPath = ['CancerTissue_HPA', 'CancerStainLoc_HPA', 'CancerTissueLevel_HPA', 'CancerTissuePatients_HPA']


'''CancerousTissue tables --------------------------------------------------'''
fx = fx + 1
TABLES_HPA_PATH[TabNmHPAPath[fx]] = (
    "CREATE TABLE IF NOT EXISTS `" + TabNmHPAPath[fx] + "`("
    "Id INT(8) NOT NULL AUTO_INCREMENT,"
    "TissueName varchar(40) NOT NULL UNIQUE,"
    "PRIMARY KEY (Id)"
    ") ENGINE = InnoDB"    
)

''' Stain location table ---------------------------------------------------'''

fx = fx + 1
TABLES_HPA_PATH[TabNmHPAPath[fx]] = (
    "CREATE TABLE IF NOT EXISTS `" + TabNmHPAPath[fx] + "`("
    "Id INT(8) NOT NULL AUTO_INCREMENT,"
    "StainLocation varchar(50) NOT NULL UNIQUE,"
    "PRIMARY KEY (Id)"
    ") ENGINE = InnoDB"    
)

''' Cancer tissue levels table ---------------------------------------------'''
fx = fx + 1
TABLES_HPA_PATH[TabNmHPAPath[fx]] = (
    "CREATE TABLE IF NOT EXISTS `" + TabNmHPAPath[fx] + "`("
    "ENSEMBL_Gene_Id char(15),"
    "CancTissue_Id int(8),"
    "Antigen_HPA_Id char(9),"
    "LevelNotDetectedM int(8),"
    "LevelLowM int(8),"
    "LevelMediumM int(8),"
    "LevelHighM int(8),"
    "LevelNotDetectedF int(8),"
    "LevelLowF int(8),"
    "LevelMediumF int(8),"
    "LevelHighF int(8),"
    "PRIMARY KEY (ENSEMBL_Gene_Id, CancTissue_Id, Antigen_HPA_Id),"
    "KEY (LevelHighF), "
    "KEY (LevelHIghM), "
    " "
    "FOREIGN KEY (ENSEMBL_Gene_Id) "
    "REFERENCES ENSEMBL_Genes(Ensembl_Gene_Id) "
    "ON DELETE CASCADE, "
    " "
    "FOREIGN KEY (CancTissue_Id) "
    "REFERENCES CancerTissue_HPA(Id) "
    "ON DELETE CASCADE"    
    ") ENGINE = InnoDB"    
)

''' Cancer tissue stats individual pateints --------------------------------'''

fx = fx + 1
TABLES_HPA_PATH[TabNmHPAPath[fx]] = (
    "CREATE TABLE IF NOT EXISTS `" + TabNmHPAPath[fx] + "`("
    "ENSEMBL_Gene_Id char(15),"
    "CancTissue_Id int(8),"
    "StainLoc_Id int(8),"
    "PatientId int(8),"
    "Quantity char(20), "
    "Intensity char(20), "
    "StainLevel char(20),"
    "Age tinyint,"
    "Sex char(6),"
    "ImageURL varchar(1200)," 
    "Antigen_HPA_Id char(9),"
    " "
    "PRIMARY KEY (ENSEMBL_Gene_Id, CancTissue_Id, PatientId, StainLoc_Id),"
    " "
    "FOREIGN KEY (ENSEMBL_Gene_Id) "
    "REFERENCES ENSEMBL_Genes(Ensembl_Gene_Id) "
    "ON DELETE CASCADE, "
    " "
    "FOREIGN KEY (StainLoc_Id) "
    "REFERENCES CancerStainLoc_HPA(Id) "
    "ON DELETE CASCADE, "
    " "
    "FOREIGN KEY (CancTissue_Id) "
    "REFERENCES CancerTissue_HPA(Id) "
    "ON DELETE CASCADE"    
    ") ENGINE = InnoDB"    
)    
    

''' Create view to summarize levels in cancer ------------------------------''' 



""" ADC tables ============================================================="""

""" Software tables ========================================================"""

sofTabNms = ['Softwares', 'TMPredSummary']#, 'Topcons', 'Spoctopus', 'Octopus', 'Scampi', 'Philius', \
    #'PolyPhobius', 'MEMSAT3', 'MEMSAT_SVM', 'hmmtop', 'tmhmm']

TABLES_SOFT = {}
''' Summary table ----------------------------------------------------------'''
sx = 0

TABLES_SOFT[sofTabNms[sx]] = (
        "CREATE table IF NOT EXISTS `" + sofTabNms[sx] + "` ("
        "`Id` int(4) NOT NULL AUTO_INCREMENT, "
        "`SoftwareName` varchar(30) NOT NULL,"
        "PRIMARY KEY (Id)"
        ") ENGINE=InnoDB"
    )

sx = sx + 1
# the xxxTM columns give whether a software predicts TM regions
# this is a protein centric table, with every protein that is predicted to contain
# TM by at least one software is referenced
TABLES_SOFT[sofTabNms[sx]] = (
        "CREATE table IF NOT EXISTS `" + sofTabNms[sx] + "` ("
        "`Id` int(4) NOT NULL AUTO_INCREMENT, "
        "`UniprotId` int(20), "
        "`TopconsTM_N` tinyint(1), "
        "`OctopusTM_N` tinyint(1), "
        "`SpoctopusTM_N` tinyint(1), "
        "`PhiliusTM_N` tinyint(1), "
        "`ScampiTM_N` tinyint(1),"
        "`PolyPhobiusTM_N` tinyint(1),"
        "`TopconsO_N` tinyint(1), "
        "`OctopusO_N` tinyint(1), "
        "`SpoctopusO_N` tinyint(1), "
        "`PhiliusO_N` tinyint(1), "
        "`ScampiO_N` tinyint(1),"
        "`PolyPhobiusO_N` tinyint(1),"        
        "`LongestO` int(2),"
        "`ShortestO` int(2),"
        "PRIMARY KEY (Id), "
        " "
        "FOREIGN KEY (UniProtId) "
        "REFERENCES UniProt_Proteins(Id) "
        "ON DELETE CASCADE"
        ") ENGINE=InnoDB"
    )

''' Spoctopus table --------------------------------------------------------'''


''' Octopus table ----------------------------------------------------------'''


