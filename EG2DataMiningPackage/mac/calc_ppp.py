# run:
# > python mac/calc_ppp.py <target A>

import ROOT , os , sys 
from ROOT import TEG2dm , TSchemeDATA , TAnalysisEG2 , TCalcPhysVarsEG2


# options are: "data" / "no ctof"
if len(sys.argv)>1:
    A       = int(sys.argv[1])
DataType    = "no ctof"


Path        = "/Users/erezcohen/Desktop/DataMining"
SchemeType  = "SRCPmissXb"
dm          = TEG2dm()
if DataType == "data":
    FileName    = "DATA_%s"% dm.Target(A)
else :
    FileName    = "NoCTofDATA_%s"% dm.Target(A)

InFile      = ROOT.TFile(Path + "/Schemed_EG2_DATA/"+"Schemed_"+SchemeType+"_"+FileName+".root")
InTree      = InFile.Get("T")
Nentries    = InTree.GetEntries()

OutFile     = ROOT.TFile(Path + "/AnaFiles/"+"Ana_"+FileName+".root","recreate")
OutTree     = ROOT.TTree("anaTree","physical variables ppp SRC")

calc        = TCalcPhysVarsEG2( InTree , OutTree , A , DataType , "q(z) - Pmiss(x-z) frame" )
#scheme      = TSchemeDATA()
#anaEG2      = TAnalysisEG2()



for entry in range(0, (int)(1.*Nentries)):
    
    calc.ComputePhysVars( entry );
    if (calc.Np >= 3):
        calc.PrintData( entry );


print "done filling %d events" % OutTree.GetEntries()
print "wrote file " + OutFile.GetName()

OutTree.Write()
OutFile.Close()


