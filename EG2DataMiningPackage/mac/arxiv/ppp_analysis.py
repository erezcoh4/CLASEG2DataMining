from ppp_tools import *
'''
    usage:
    ---------
    python mac/ppp_analysis.py --option=scheme
    
    options (can be ran simultaneously):
    calc    {"calc. phys. vars."}
    scheme  {"scheme ppp-SRC"}
    cuts    {"plot ppp sample cuts"}
    count   {"count e,e'p/pp/ppp"}
    
'''




# (1) calculate physical variables
# ----------------------------------------
if 'calc. phys. vars.' in flags.option or 'calc' in flags.option:
    print_important("python mac/calc_phys_vars.py -A%d -werez --option=pppSRC -scheme=SRCXb --DataType=NoCTofDATA -evf=1 -p1000"%flags.atomic_mass)



# (2) scheme for ppp-src
# ----------------------------------------
if 'scheme ppp-SRC' in flags.option or 'scheme' in flags.option: # scheme to ppp-SRC
    
    DataName    = "NoCTofDATA_%s"% dm.Target(flags.atomic_mass)
    SchemedName = "pppSRCCut_%s"% DataName
    cutXb = ROOT.TCut('Xb>0.85')
    ana         = TAnalysisEG2( path+"/AnaFiles" , "Ana_SRCXb_"+DataName , cutXb )
    scheme      = TSchemeDATA()
    scheme.SchemeOnTCut( path+"/AnaFiles" , "Ana_SRCXb_"+DataName+".root", "anaTree", "Ana_"+SchemedName+".root", ana.pppSRCCut )
    '''
        pppSRCCut:
        ---------
        cutSRC = cutXb 
        && "theta_pq < 25"
        && "0.52 < p_over_q && p_over_q < 0.93"
        && "0.3 < Pmiss.P() && Pmiss.P() < 1.0"
        && "3<=Np"
        && cutPmT = "Pmiss.Pt() < 0.4"
        && cutP1 = "(-27 < pVertex[0].Z() && pVertex[0].Z() < -20)"
        && cutP2 = "0.3 < protons[1].P() && (-27 < pVertex[1].Z() && pVertex[1].Z() < -20)"
        && cutP3 = "0.3 < protons[2].P() && (-27 < pVertex[2].Z() && pVertex[2].Z() < -20)"
        && pppEdepCut = Form("%s && %s && %s",pEdepCut[0]->GetName(),pEdepCut[1]->GetName(),pEdepCut[2]->GetName())
        && pppCTOFCut = "pCTOFCut[0] && pCTOFCut[1] && pCTOFCut[2]"
        '''
    print 'schemed to %s'%SchemedName


# (2) merge all nuclei
# ----------------------------------------
if 'merge ppp-SRC all nuclei' in flags.option or 'merge' in flags.option:
    print_important('cd /Users/erezcohen/Desktop/DataMining/AnaFiles \nhadd Ana_pppSRCCut_NoCTofDATA_C12_Al27_Fe56_Pb208.root Ana_pppSRCCut_NoCTofDATA_*')


# (2) mix
# ----------------------------------------
if 'mix ppp-SRC all nuclei' in flags.option or 'mix' in flags.option:
    ana = TAnalysisEG2( path+"/AnaFiles" , "Ana_pppSRCCut_NoCTofDATA_C12_Al27_Fe56_Pb208" , ROOT.TCut('Xb>1.05') )
    mix_ppp_events( ana )


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











