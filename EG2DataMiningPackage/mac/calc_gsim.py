# run:
# > python mac/calc_gsim.py <run-number>

import ROOT , os , sys 
from ROOT import TEG2dm , TSchemeDATA , TAnalysisEG2 , TCalcPhysVarsEG2


if len(sys.argv)>1:
    run     = int(sys.argv[1])
else:
    print '\n run this script with: \n > python mac/calc_gsim.py <run-number> \n\n'
    exit(0)


Path        = "/Users/erezcohen/Desktop/DataMining"
SchemeType  = "SRCPmissXb"
DataType    = "GSIM"
A           = 12
dm          = TEG2dm()
FileName    = "GSIM_run%04d_eep"%run

InFile      = ROOT.TFile(Path + "/GSIM_DATA/"+FileName+".root")
InTree      = InFile.Get("proton_data")
Nentries    = InTree.GetEntries()
OutFile     = ROOT.TFile(Path + "/AnaFiles/"+"Ana_"+FileName+".root","recreate")
OutTree     = ROOT.TTree("anaTree","physical variables GSIM analysis")

calc        = TCalcPhysVarsEG2( InTree , OutTree , A , DataType , "q(z) - Pmiss(x-z) frame" )


for entry in range(0, (int)(1.*Nentries)):
    
    calc.ComputePhysVars( entry );
    if (calc.Np >= 13):
        calc.PrintData( entry );


print "done filling %d events" % OutTree.GetEntries()
print "wrote file " + OutFile.GetName()

OutTree.Write()
OutFile.Close()


