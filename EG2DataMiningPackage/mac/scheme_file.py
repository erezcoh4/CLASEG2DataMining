'''
    usage:
    --------
    python mac/scheme_file.py -A12  --option="(e,e'pp?)" --DataType="New_NoCTofDATA"
'''

import ROOT,os, sys , math , os.path , math
from ROOT import TEG2dm , TSchemeDATA
sys.path.insert(0, '/Users/erezcohen/larlite/UserDev/mySoftware/MySoftwarePackage/mac')
sys.path.insert(0, '/home/erez/larlite/UserDev/mySoftware/MySoftwarePackage/mac')
import input_flags
flags = input_flags.get_args()


if flags.worker == "erez":
    path = "/Users/erezcohen/Desktop/DataMining"

elif flags.worker == "helion":
    path = "/home/erez/DataMining"


dm          = TEG2dm()
A           = flags.atomic_mass
DataType    = flags.DataType

FileName    = DataType+"_%s"% dm.Target(A)
scheme      = TSchemeDATA( DataType , path , FileName , "T")
pMin , pMax = 0.3 , 0.7

# ------------------------------------------------------------------ #
if (flags.option=="SRCPmissXb"):
    scheme.SRCPmissXb( 2 , 1.1 ) # target-type = 2, Bjorken x > 1.1
    print "schemed for SRC in nuclear target (1 > p(miss) > 0.3 GeV/c) and Xb > 1.1"
# ------------------------------------------------------------------ #


# ------------------------------------------------------------------ #
elif (flags.option == "(e,e'pp?)"):
    scheme.TwoSlowProtons( 2 , pMin , pMax ) # target-type = 2, momentum minimum and maximum
    print "schemed in nuclear target, for 2 protons with momentum %.1f < p < %.1f..."%(pMin,pMax)
# ------------------------------------------------------------------ #

# ------------------------------------------------------------------ #
elif (flags.option == "(e,e'pp[pi-,p])"):
    scheme.TwoSlowProtons_piminus_p( 2 , pMin , pMax ) # target-type = 2, momentum minimum and maximum
    print "schemed in nuclear target, for 2 protons with momentum %.1f < p < %.1f and additional pi- and p..."%(pMin,pMax)
# ------------------------------------------------------------------ #



# ------------------------------------------------------------------ #
elif (flags.option=="two slow protons-ppp"):
    scheme.TwoSlowProtons_ppp( 2 , pMin , pMax ) # target-type = 2, momentum minimum and maximum
    print "schemed in nuclear target, for 2 protons with momentum %.1f < p < %.1f..."%(pMin,pMax)

# ------------------------------------------------------------------ #


# ------------------------------------------------------------------ #
elif (flags.option=="two slow protons-npp"):
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
elif (flags.option=="3pSRC"):
    scheme = TSchemeDATA(DataType,path,FileName,"T")
    scheme.SRCPmissXb( 2 , 0.9 ) # target-type = 2, Bjorken x > 0.9
    print 'schemed for SRC in nuclear target (1 > p(miss) > 0.3 GeV/c) and Xb > 0.9'
# ------------------------------------------------------------------ #



else:
    
    print 'not scheming...'



print "done"

