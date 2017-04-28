'''
    usage:
    --------
    python mac/scheme_file.py  --DataType=DATA --option=SRCXb -A12
    python mac/scheme_file.py -A12  --option="(e,e'pp?)" --DataType=New_NoCTofDATA
    python mac/scheme_file.py -A12  --option=GSIM -r93
'''
from definitions import *

DataType    = flags.DataType
FileName    = DataType+"_%s"% dm.Target(A)
scheme      = TSchemeDATA( DataType , eg2_data_path , schemed_eg2_data_path , FileName , "T" , flags.verbose )
pMin , pMax = 0.3 , 0.7


# ------------------------------------------------------------------ #
if (flags.option=="SRCXb"):
    scheme.SRCXb( 2 , 1.0 , 1 , 100 , "" , A ) # target-type = 2, Bjorken x > 1.0
    print "schemed for SRC in nuclear target Xb > 1.0, Nprotons>1"
# ------------------------------------------------------------------ #

# ------------------------------------------------------------------ #
if (flags.option=="SRCPmissXb"):
    scheme.SRCPmissXb( 2 , 1.0 , 1 , 20 , "" , A ) # target-type = 2, Bjorken x > 0.8
    print "schemed for SRC in nuclear target (1 > p(miss) > 0.3 GeV/c) and Xb > 0.8, 1-4 protons"
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
elif (flags.option=="gsim" or flags.option=="GSIM"):

    run         = flags.run
    DataType    = "GSIM"
    Path        = path + "/GSIM_DATA"
    FileName    = "GSIM_run%04d"%run

    scheme = TSchemeDATA()
    scheme.SchemeOnTCut( Path, FileName+".root", "proton_data", FileName + "_eep.root", flags.cut )
    
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

