import ROOT , os , sys
from ROOT import TEG2dm , TSchemeDATA , TAnalysisEG2 , TCalcPhysVarsEG2
sys.path.insert(0, '/Users/erezcohen/larlite/UserDev/mySoftware/MySoftwarePackage/mac')
import input_flags
flags = input_flags.get_args()


A = flags.atomic_mass
DataType    = "no ctof"
SchemeType  = "everything"
Path        = "/Users/erezcohen/Desktop/DataMining"
dm          = TEG2dm()

FileName    = "NoCTofDATA_%s"% dm.Target(A)
InFile      = ROOT.TFile(Path + "/Schemed_EG2_DATA/"+"Schemed_"+SchemeType+"_"+FileName+".root")
if (flags.verbose>1): print InFile
InTree      = InFile.Get("T")
if (flags.verbose>1): print InTree
Nentries    = InTree.GetEntries()
if (flags.verbose>1): print "Nentries: ",Nentries

OutFile     = ROOT.TFile(Path + "/AnaFiles/"+"Ana_"+SchemeType+"_"+FileName+".root","recreate")
OutTree     = ROOT.TTree("anaTree","physical variables ppp SRC")

calc        = TCalcPhysVarsEG2( InTree , OutTree , A , DataType , "q(z) - Pmiss(x-z) frame" )



for entry in range(0, (int)(flags.evnts_frac*Nentries)):
    
    calc.ComputePhysVars( entry );
    if (flags.verbose>1 and (entry%flags.print_mod==0)):
        calc.PrintData( entry )



print "done filling %d events" % OutTree.GetEntries()
print "wrote file " + OutFile.GetName()

OutTree.Write()
OutFile.Close()


