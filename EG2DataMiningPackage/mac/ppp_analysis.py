from ppp_tools import *
'''
    usage:
    ---------
    python mac/ppp_analysis.py --option=cuts
    
    options (can be ran simultaneously):
    calc    {"calc. phys. vars."}
    scheme  {"scheme ppp-SRC"}
    cuts    {"plot ppp sample cuts"}
    count   {"count e,e'p/pp/ppp"}
    
'''




# (1) calculate physical variables
# ----------------------------------------
if 'calc. phys. vars.' in flags.option or 'calc' in flags.option:
    print_important("python mac/calc_phys_vars.py -A%d -werez --option=pppSRC --DataType=NoCTofDATA -evf=1 -p1000"%flags.atomic_mass)



# (2) scheme for pp-src
# ----------------------------------------
if 'scheme ppp-SRC' in flags.option or 'scheme' in flags.option: # scheme to ppp-SRC
    
    DataName    = "NoCTofDATA_%s"% dm.Target(flags.atomic_mass)
    SchemedName = "pppSRCCut_%s"% DataName
    ana         = TAnalysisEG2( path+"/AnaFiles" , "Ana_SRCPmissXb_"+DataName , ROOT.TCut('Xb>1.05') )
    scheme      = TSchemeDATA()
    scheme.SchemeOnTCut( path+"/AnaFiles" , "Ana_SRCPmissXb_"+DataName+".root", "anaTree", "Ana_"+SchemedName+".root", ana.pppSRCCut )
    print 'schemed to %s'%SchemedName



# (1) SRC and kinematical cuts
# ----------------------------------------
if 'plot ppp sample cuts' in flags.option or 'cuts' in flags.option:
    print_important("ipynb notebooks/ppp_analysis.ipynb")



# (2) count the number of events in our sample
# ----------------------------------------
if "count e,e'p/pp/ppp" in flags.option or 'count' in flags.option:
    print_important("count e,e'p/pp/ppp")
    ana_all.PrintInCuts()




# (3) merge 12C/27Al/56Fe/208Pb
# ----------------------------------------
if "count e,e'p/pp/ppp" in flags.option or 'count' in flags.option:
    print_important('cd /Users/erezcohen/Desktop/DataMining/AnaFiles/')
    print_important('hadd Ana_pppSRCCut_NoCTofDATA_C12_Al27_Fe56_Pb208.root Ana_pppSRCCut_NoCTofDATA_*')











