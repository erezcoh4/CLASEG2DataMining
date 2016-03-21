import ROOT
from ROOT import TEG2dm
from ROOT import TSchemeDATA
from ROOT import TAnalysisEG2
from ROOT import TCalcPhysVarsEG2


# options are: "data" / "no ctof"
DataType    = "no ctof"


A           = 12
Path        = "/Users/erezcohen/Desktop/DataMining"
SchemeType  = "SRCPmissXb"

if DataType == "data":
    FileName    = "DATA_C12"
else :
    FileName    = "NoCTofDATA_C12"

InFile      = ROOT.TFile(Path + "/Schemed_EG2_DATA/"+"Schemed_"+SchemeType+"_"+FileName+".root")
InTree      = InFile.Get("T")
Nentries    = InTree.GetEntries()

OutFile     = ROOT.TFile(Path + "/AnaFiles/"+"Ana_"+FileName+".root","recreate")
OutTree     = ROOT.TTree("anaTree","physical variables ppp SRC")

calc        = TCalcPhysVarsEG2( InTree , OutTree , A , DataType , "q(z) - Pmiss(x-z) frame" )
dm          = TEG2dm()
scheme      = TSchemeDATA()
anaEG2      = TAnalysisEG2()
anaEG2.SetSRCCuts()



for entry in range(0, (int)(1.*Nentries)):
    
    calc.ComputePhysVars( entry );
#    calc.PrintData( entry );


print "done filling %d events" % OutTree.GetEntries()
print "wrote file " + OutFile.GetName()

OutTree.Write()
OutFile.Close()



#scheme.SchemeOnTCut(Path+"/AnaFiles", "Ana_ppSRC_"+FileName+".root", "anaTree","Ana_ppSRC_"+FileName+"_FullCuts.root", anaEG2.ppSRCCut)
