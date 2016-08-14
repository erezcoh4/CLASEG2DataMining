import ROOT , os , sys 
from ROOT import TEG2dm , TSchemeDATA , TAnalysisEG2 , TCalcPhysVarsEG2
sys.path.insert(0, '/Users/erezcohen/larlite/UserDev/mySoftware/MySoftwarePackage/mac')
sys.path.insert(0, '/home/erez/larlite/UserDev/mySoftware/MySoftwarePackage/mac')
import input_flags
flags = input_flags.get_args()

'''
    usage:
    --------
    > python calc_phys_vars.py -A12 -werez --option='A(e,e'p)X' -data='data' -evf=1 -p100
'''

if flags.worker == "erez":
    path = "/Users/erezcohen/Desktop/DataMining"

elif flags.worker == "helion":
    path = "/home/erez/DataMining"


dm  = TEG2dm()
A   = flags.atomic_mass
DataType = flags.DataType
SchemeType  = "SRCPmissXb"



if DataType == "data":
    FileName    = "DATA_%s"% dm.Target(A)
elif DataType == "no ctof":
    FileName    = "NoCTofDATA_%s"% dm.Target(A)



InFile      = ROOT.TFile(path + "/Schemed_EG2_DATA/"+"Schemed_"+SchemeType+"_"+FileName+".root")
InTree      = InFile.Get("T")
Nentries    = InTree.GetEntries()

OutFile     = ROOT.TFile(path + "/AnaFiles/"+"Ana_"+FileName+".root","recreate")
OutTree     = ROOT.TTree("anaTree","physical variables")





if option=="A(e,e'p)X":
    calc    = TCalcPhysVarsEG2( InTree , OutTree , A , DataType , "q(z) - Pmiss(x-z) frame" )

    for entry in range(0, (int)(flags.evf*Nentries)):
    
        calc.ComputePhysVars( entry );
        if (entry%flags.print_mod == 0):
            calc.PrintData( entry )


print "done filling %d events" % OutTree.GetEntries()
print "wrote file " + OutFile.GetName()

OutTree.Write()
OutFile.Close()


