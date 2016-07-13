import ROOT , os , sys
from ROOT import TEG2dm , TSchemeDATA , TAnalysisEG2 , TCalcPhysVarsEG2

'''
    july-12, 2016
    analyze meytal events w/ leading n and two p,
    to look only on the recoiling two protons....
'''

A           = 12
DataType    = "(e,e'npp)"
Path        = "/Users/erezcohen/Desktop/DataMining"
SchemeType  = "TwoSlowProtons_npp"
dm          = TEG2dm()
FileName    = "Meytal_npp_DATA_C12"

InFile      = ROOT.TFile(Path + "/Schemed_EG2_DATA/"+"Schemed_"+SchemeType+"_"+FileName+".root")
InTree      = InFile.Get("Tree")
Nentries    = InTree.GetEntries()

OutFile     = ROOT.TFile(Path + "/AnaFiles/Ana_%s"%dm.Target(A)+"_" + SchemeType + ".root","recreate")
OutTree     = ROOT.TTree("anaTree","physical, variables two slow protons + neutron > 1.0 GeV/c")

calc        = TCalcPhysVarsEG2( InTree , OutTree , A , DataType , "q(z) - Pmiss(x-z) frame" )



for entry in range(0, (int)(1.*Nentries)):
    
    calc.ComputePhysVars( entry );
    if (entry>0):
        calc.PrintData( entry );


print "done filling %d events" % OutTree.GetEntries()
print "wrote file " + OutFile.GetName()

OutTree.Write()
OutFile.Close()


