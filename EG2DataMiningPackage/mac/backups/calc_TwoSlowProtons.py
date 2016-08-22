import ROOT , os , sys
from ROOT import TEG2dm , TSchemeDATA , TAnalysisEG2 , TCalcPhysVarsEG2

sys.path.insert(0, '/Users/erezcohen/larlite/UserDev/mySoftware/MySoftwarePackage/mac')
import input_flags
flags = input_flags.get_args()



A   = flags.atomic_mass
DataType    = "no ctof"


Path        = "/Users/erezcohen/Desktop/DataMining"
SchemeType  = "TwoSlowProtons"
dm          = TEG2dm()

if DataType == "data":
    FileName    = "DATA_%s"% dm.Target(A)
else :
    FileName    = "New_NoCTofDATA_%s"% dm.Target(A) # Aug-2016

InFile      = ROOT.TFile(Path + "/Schemed_EG2_DATA/"+"Schemed_"+SchemeType+"_"+FileName+".root")
InTree      = InFile.Get("T")
Nentries    = InTree.GetEntries()

OutFile     = ROOT.TFile(Path + "/AnaFiles/Ana_%s"%dm.Target(A)+"_" + SchemeType + ".root","recreate")
OutTree     = ROOT.TTree("anaTree","physical variables two slow protons SRC")

calc        = TCalcPhysVarsEG2( InTree , OutTree , A , DataType , "q(z) - Pmiss(x-z) frame" )



for entry in range(0, (int)(1.*Nentries)):
    
    calc.ComputePhysVars( entry );
    if (flags.verbose>0 and entry%flags.print_mod==0):
        print "entry %d"%entry
        calc.PrintData( entry );

if (flags.verbose>0):
    print "done filling %d events" % OutTree.GetEntries()
    print "wrote file " + OutFile.GetName()

OutTree.Write()
OutFile.Close()


