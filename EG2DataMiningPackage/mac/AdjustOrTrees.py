
#import sys
#; sys.path.insert(0,'../notebooks')
from cm_tools import *
#from notebook_tools import *


PmissBins = [[0.3,0.45]  , [0.45,0.55] , [0.55,0.65]  , [0.65,0.75] , [0.75,1.0]]
My_targets = ['C12','Al27','Fe56','Pb208']
Or_targets = ['C','Al','Fe','Pb']


# load Or' original trees
OrOriginalTrees_eep, OrOriginalTrees_eepp = dict() , dict()
MyTrees_eep, MyTrees_eepp = dict() , dict()
for My_target,Or_target in zip(My_targets,Or_targets):#{
    file1 = ROOT.TFile( "/Users/erezcohen/Desktop/DataMining/OrAnalysisTrees/OrOriginalTrees/SRC_e1p_%s_GoodRuns_coulomb.root"%Or_target )
    OrOriginalTrees_eep[Or_target] = file1.Get("T")
    out_file1 = ROOT.TFile( "/Users/erezcohen/Desktop/DataMining/OrAnalysisTrees/AdjustedTrees/SRC_e1p_adjusted_%s.root"%My_target , "recreate")
    MyTrees_eep[My_target] = OrOriginalTrees_eep[Or_target].CloneTree(0)
    for i in range(OrOriginalTrees_eep[Or_target].GetEntries()):#{
        OrOriginalTrees_eep[Or_target].GetEntry(i)
        
        MyTrees_eep[My_target].Fill()
    #}
    
    file1.Close()
    MyTrees_eep[My_target].Write()
    out_file1.Close()


    file2 = ROOT.TFile( "/Users/erezcohen/Desktop/DataMining/OrAnalysisTrees/OrOriginalTrees/SRC_e2p_%s_GoodRuns_coulomb.root"%Or_target )
    OrOriginalTrees_eepp[Or_target] = file2.Get("T")
    out_file2 = ROOT.TFile( "/Users/erezcohen/Desktop/DataMining/OrAnalysisTrees/AdjustedTrees/SRC_e2p_adjusted_%s.root"%My_target , "recreate")
    MyTrees_eepp[My_target] = OrOriginalTrees_eepp[Or_target].CloneTree(0)
    for i in range(OrOriginalTrees_eepp[Or_target].GetEntries()):#{
        OrOriginalTrees_eepp[Or_target].GetEntry(i)
        
        # apply vertex cut to the leading and the recoil protons
        
        if (TMath::Abs(Rp[0][2]+22.25)<2.25
            && Pp_size[0]<2.4
            && TMath::Abs(Rp[1][2]+22.25)<2.25
            && Pp_size[1]>0.35):
            
        # apply fiducial cuts to the recoil proton
        MyTrees_eepp[My_target].Fill()
    #}
    file2.Close()
    MyTrees_eepp[My_target].Write()
    out_file2.Close()
#}


for My_target,Or_target in zip(My_targets,Or_targets):#{
    file1 = ROOT.TFile(  "/Users/erezcohen/Desktop/DataMining/OrAnalysisTrees/AdjustedTrees/SRC_e1p_adjusted_%s.root"%My_target )
    MyTrees_eep[My_target] = file1.Get("T")
    print MyTrees_eep[My_target].GetEntries(),My_target,"(e,e'p) entries"
    
    file2 = ROOT.TFile(  "/Users/erezcohen/Desktop/DataMining/OrAnalysisTrees/AdjustedTrees/SRC_e2p_adjusted_%s.root"%My_target )
    MyTrees_eepp[My_target] = file2.Get("T")
    print MyTrees_eepp[My_target].GetEntries(),My_target,"(e,e'pp) entries"
#}