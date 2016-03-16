import ROOT
from ROOT import TEG2dm
from ROOT import TCalcPhysVarsEG2

dm = TEG2dm

A           = 12
Path        = "/Users/erezcohen/Desktop/DataMining"
SchemeType  = "SRCPmissXb"
FileName    = "DATA_C12"

InFile      = ROOT.TFile(Path + "/Schemed_EG2_DATA/"+"Schemed_"+SchemeType+"_"+FileName+".root")
InTree      = InFile.Get("T")
Nentries    = InTree.GetEntries()

OutFile     = ROOT.TFile(Path + "/AnaFiles/"+"Ana_"+"ppSRC_"+FileName+".root","recreate")
OutTree     = ROOT.TTree("anaTree","physical variables ppSRC")

calc = TCalcPhysVarsEG2( InTree , OutTree , A )



for entry in range(0, (int)(0.01*Nentries)):

    calc.AcquireNucleons( entry );
#    calc.ComputePhysVariables();


print "done"

