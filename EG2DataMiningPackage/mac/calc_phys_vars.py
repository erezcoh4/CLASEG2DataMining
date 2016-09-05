
'''
    usage:
    --------
    python mac/calc_phys_vars.py -A12 -werez --option=ppSRC --DataType=DATA -evf=1 -p1000 -v2
'''

import ROOT , os , sys
from ROOT import TEG2dm , TSchemeDATA , TAnalysisEG2 , TCalcPhysVarsEG2
sys.path.insert(0, '/Users/erezcohen/larlite/UserDev/mySoftware/MySoftwarePackage/mac')
sys.path.insert(0, '/home/erez/larlite/UserDev/mySoftware/MySoftwarePackage/mac')
import input_flags
flags = input_flags.get_args()

if flags.worker == "erez":
    path = "/Users/erezcohen/Desktop/DataMining"

elif flags.worker == "helion":
    path = "/home/erez/DataMining"


dm  = TEG2dm()
A   = flags.atomic_mass
SchemeType  = "SRCPmissXb"
DataType    = flags.DataType
FileName    = "%s_%s"% (DataType,dm.Target(A))



InFile      = ROOT.TFile(path + "/Schemed_EG2_DATA/"+"Schemed_"+SchemeType+"_"+FileName+".root")
InTree      = InFile.Get("T")
Nentries    = InTree.GetEntries()

OutFile = ROOT.TFile(path + "/AnaFiles/"+"Ana_"+FileName+"_"+flags.option+".root","recreate")

OutTree     = ROOT.TTree("anaTree","physical variables")


axes_frame  = "Pmiss(z) - q(x-z) frame" if flags.option=="ppSRC" else "q(z) - Pmiss(x-z) frame"

calc    = TCalcPhysVarsEG2( InTree , OutTree , A , flags.DataType , axes_frame , flags.verbose)

for entry in range(0, (int)(flags.evnts_frac*Nentries)):
    calc.ComputePhysVars( entry );
    if (flags.verbose>0 and entry%flags.print_mod == 0):
        calc.PrintData( entry )



print "done filling %d events" % OutTree.GetEntries()
print "wrote file " + OutFile.GetName()

OutTree.Write()
OutFile.Close()


