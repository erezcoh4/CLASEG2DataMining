import ROOT,os, sys , math , os.path , math
from ROOT import TEG2dm , TSchemeDATA
sys.path.insert(0, '/Users/erezcohen/larlite/UserDev/mySoftware/MySoftwarePackage/mac')
sys.path.insert(0, '/home/erez/larlite/UserDev/mySoftware/MySoftwarePackage/mac')
import input_flags
flags = input_flags.get_args()

'''
    usage:
    --------
    > python scheme_file.py -A12 -werez --option='SRCPmissXb' -var="data"
'''

if flags.worker == "erez":
    path = "/Users/erezcohen/Desktop/DataMining"

elif flags.worker == "helion":
    path = "/home/erez/DataMining"


dm  = TEG2dm()
A   = flags.atomic_mass
DataType = flags.DataType


# ------------------------------------------------------------------ #
if (flags.option=="SRCPmissXb"):
    
    FileName    = "DATA_%s"% dm.Target(A)
    scheme = TSchemeDATA("data",path,FileName,"T")
    scheme.SRCPmissXb( 2 , 1.1 ) # target-type = 2, Bjorken x > 1.1
    print 'schemed for SRC in nuclear target (1 > p(miss) > 0.3 GeV/c) and Xb > 1.1'
# ------------------------------------------------------------------ #


# ------------------------------------------------------------------ #
elif (flags.option == "two slow protons-nothing else"):

    FileName    = "New_NoCTofDATA_%s"% dm.Target(A)
    scheme      = TSchemeDATA("no ctof",path,FileName,"T")
    pMin = 0.3
    pMax = 0.7
    scheme.TwoSlowProtons( 2 , pMin , pMax ) # target-type = 2, momentum minimum and maximum
    print "schemed in nuclear target, for 2 protons with momentum %.1f < p < %.1f..."%(pMin,pMax)
# ------------------------------------------------------------------ #


# ------------------------------------------------------------------ #
elif (flags.option=="two slow protons-ppp"):
    
    FileName    = "Meytal_npp_DATA_C12"
    scheme      = TSchemeDATA("(e,e'npp)",path,FileName,"Tree")

    FileName    = "NoCTofDATA_%s"% dm.Target(A)
    scheme      = TSchemeDATA("no ctof",path,FileName,"T")

    pMin = 0.3
    pMax = 0.7
    scheme.TwoSlowProtons_ppp( 2 , pMin , pMax ) # target-type = 2, momentum minimum and maximum
    print "schemed in nuclear target, for 2 protons with momentum %.1f < p < %.1f..."%(pMin,pMax)

# ------------------------------------------------------------------ #


# ------------------------------------------------------------------ #
elif (flags.option=="two slow protons-npp"):

    FileName    = "Meytal_npp_DATA_C12"
    scheme      = TSchemeDATA("(e,e'npp)",path,FileName,"Tree")

    pMin = 0.3
    pMax = 0.7
    n_pMin = 1.0  # neutron minimum momentum = 1.1 GeV/c
    scheme.TwoSlowProtons_npp( n_pMin, pMin , pMax )
    print "schemed in nuclear target, for 2 protons with momentum %.1f < p < %.1f..."%(pMin,pMax)
# ------------------------------------------------------------------ #


# ------------------------------------------------------------------ #
elif (flags.option=="gsim"):

    run = int(input("which run number? > "))
    DataType    = "GSIM"
    Path        = path + "/GSIM_DATA"
    FileName    = "GSIM_run%04d"%run

    scheme = TSchemeDATA()
    scheme.SchemeOnTCut( Path, FileName+".root", "proton_data", FileName + "_eep.root", ROOT.TCut("P_nmb>0"))
    
    print "schemed gsim file "+FileName
# ------------------------------------------------------------------ #





# ------------------------------------------------------------------ #
elif (flags.option="3pSRC"):
    if DataType == "data":
        FileName    = "DATA_%s"% dm.Target(A)
    else :
        FileName    = "NoCTofDATA_%s"% dm.Target(A)
    scheme = TSchemeDATA(DataType,path,FileName,"T")
    scheme.SRCPmissXb( 2 , 0.9 ) # target-type = 2, Bjorken x > 0.9
    print 'schemed for SRC in nuclear target (1 > p(miss) > 0.3 GeV/c) and Xb > 0.9'
# ------------------------------------------------------------------ #



else:
    
    print 'not scheming...'



print "done"

