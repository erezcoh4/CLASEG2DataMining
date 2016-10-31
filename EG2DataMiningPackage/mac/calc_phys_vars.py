
'''
    usage:
    --------
    python mac/calc_phys_vars.py -A12 -werez --option=ppSRC --DataType=DATA -evf=1 -p1000 -v2
    python mac/calc_phys_vars.py --DataType=GSIM -evf=0.01 -p10000 -r80 
    python mac/calc_phys_vars.py -A12 --DataType=New_NoCTofDATA --SchemedType=TwoSlowProtons_piminus_p -evf=1 -p100
'''
from definitions import *
#import ROOT , os , sys
#from ROOT import TEG2dm , TSchemeDATA , TAnalysisEG2 , TCalcPhysVarsEG2
#sys.path.insert(0, '/Users/erezcohen/larlite/UserDev/mySoftware/MySoftwarePackage/mac')
#sys.path.insert(0, '/home/erez/larlite/UserDev/mySoftware/MySoftwarePackage/mac')
#import input_flags
#flags = input_flags.get_args()

#if flags.worker == "erez":
#    path = "/Users/erezcohen/Desktop/DataMining"

#elif flags.worker == "helion":
#    path = "/home/erez/DataMining"


#dm  = TEG2dm()
#A = flags.atomic_mass
SchemeType  = flags.SchemedType
DataType    = flags.DataType


#if (flags.option == "ppSRC"):
#    axes_frame  = "Pmiss(z) - q(x-z) frame"
#else:
#    axes_frame  = "q(z) - Pmiss(x-z) frame"


if (DataType == "GSIM"):
    FileName    = "GSIM_run%04d_eep"%flags.run
    InFile      = ROOT.TFile(path + "/GSIM_DATA/"+FileName+".root")
    InTree      = InFile.Get("proton_data")
    OutFile     = ROOT.TFile(path + "/AnaFiles/"+"Ana_"+FileName+".root","recreate")
    axes_frame  = "lab frame"

else:
    FileName    = "%s_%s_%s"% (SchemeType,DataType,dm.Target(A))
    InFile      = ROOT.TFile(path + "/Schemed_EG2_DATA/"+"Schemed_"+FileName+".root")
    InTree      = InFile.Get("T")
    OutFile     = ROOT.TFile(path + "/AnaFiles/"+"Ana_"+FileName+".root","recreate")


Nentries    = InTree.GetEntries()
OutTree     = ROOT.TTree("anaTree","physical variables")
calc    	= TCalcPhysVarsEG2( InTree , OutTree , A , flags.DataType , axes_frame , flags.verbose)

if (DataType == "GSIM"):
    calc.SetNp_g(1)

for entry in range(0, (int)(flags.evnts_frac*Nentries)):
    calc.ComputePhysVars( entry );
    if (flags.verbose>0 and entry%flags.print_mod == 0):
        calc.PrintData( entry )



print "done filling %d events" % OutTree.GetEntries()
print "wrote file " + OutFile.GetName()

OutTree.Write()
OutFile.Close()






