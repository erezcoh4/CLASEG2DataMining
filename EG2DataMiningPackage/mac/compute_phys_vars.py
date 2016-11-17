'''
    usage:
    --------
    python mac/compute_phys_vars.py -A12 -werez --option=TwoSlowProtons --DataType=New_NoCTofDATA
    other DataType options:  NoCTofDATA  New_NoCTofDATA  GSIM
'''

import ROOT,os, sys , math , os.path , math
from ROOT import TEG2dm , TSchemeDATA , TCalcPhysVarsEG2
sys.path.insert(0, '/Users/erezcohen/larlite/UserDev/mySoftware/MySoftwarePackage/mac')
sys.path.insert(0, '/home/erez/larlite/UserDev/mySoftware/MySoftwarePackage/mac')
import input_flags
flags = input_flags.get_args()


if flags.worker == "erez":
    Path = "/Users/erezcohen/Desktop/DataMining"

elif flags.worker == "helion":
    Path = "/home/erez/DataMining"



pars  = {}

pars['SchemeType'] = ""
pars['calc'] = 0
dm          = TEG2dm()
A           = flags.atomic_mass
DataType    = flags.DataType
Path        = "/Users/erezcohen/Desktop/DataMining"
FileName    = DataType  + "_" + str(dm.Target(A))



def set_input_output():
    
    
    print "setting input & output..."
    
    pars['InFile']      = ROOT.TFile(Path + "/Schemed_EG2_DATA/"+"Schemed_" + pars['SchemeType'] + "_" + FileName + ".root")
    pars['InTree']      = pars['InFile'].Get("T")
    pars['Nentries']    = pars['InTree'].GetEntries()
    
    pars['OutFile']     = ROOT.TFile(Path + "/AnaFiles/"+"Ana_"+FileName+"_" + pars['SchemeType']+".root","recreate")
    pars['OutTree']     = ROOT.TTree("anaTree","physical variables " + pars['SchemeType'])







def compute_phys_vars():
    
    print "computing physical variables..."
    calc = pars['calc']
    
    for entry in range(0, (int)(flags.evnts_frac*pars['Nentries'])):
        
        calc.ComputePhysVars( entry )
        if (flags.verbose>0 and entry%flags.print_mod==0):
            calc.PrintData( entry )


    print "done filling %d events" % pars['OutTree'].GetEntries()
    print "wrote file " + pars['OutFile'].GetName()
    
    pars['OutTree'].Write()
    pars['OutFile'].Close()







# ------------------------------------------------------------------ #
if (flags.option=="ppp" or flags.option=="pp"):
    

    pars['SchemeType']  = "SRCPmissXb"

    set_input_output()

    axes_frame =  "q(z) - Pmiss(x-z) frame" if flags.option=="ppp" else "Pmiss(z) - q(x-z) frame"


    pars['calc'] = TCalcPhysVarsEG2( pars['InTree'] , pars['OutTree'] , A , DataType , axes_frame )


    compute_phys_vars()
    
    
    print "computed physical variables for " + flags.option

# ------------------------------------------------------------------ #





# ------------------------------------------------------------------ #
elif (flags.option=="TwoSlowProtons"):

    pars['SchemeType']  = "TwoSlowProtons"

    set_input_output()

    pars['calc'] = TCalcPhysVarsEG2( pars['InTree'] , pars['OutTree'] , A , DataType , "q(z) - Pmiss(x-z) frame" )

    compute_phys_vars()

    print "computed physical variables for " + flags.option

# ------------------------------------------------------------------ #



else:
    
    print 'not working...'







