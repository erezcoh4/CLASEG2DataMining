from definitions import *
from my_tools import *
from cuts import *

'''
    usage:
    ---------
    python mac/ppnothing_analysis.py --option=calc
    
    options (can be ran simultaneously):
    ------------------------------------
    reduction       {"first scheme big file"}
    calc            {"calc. phys. vars."}
    scheme          {"scheme ppnothing-SRC"}

'''



# (0) scheme the big data file, e.g. New_NoCTofDATA_C12.root
# ----------------------------------------------------
if 'first scheme big file' in flags.option or 'reduction' in flags.option:
    print_important("python mac/scheme_file.py -A%d --option=\"(e,e'pp?)\" --DataType=New_NoCTofDATA"%A)


# (1) calculate physical variables
# ----------------------------------------
if 'calc. phys. vars.' in flags.option or 'calc' in flags.option:
    print_important("python mac/calc_phys_vars.py -A%d --DataType=New_NoCTofDATA --SchemedType=TwoSlowProtons -evf=1 -p10000"%A)



# (2) scheme for pp-src
# ----------------------------------------
if 'scheme ppnothing-SRC' in flags.option or 'scheme' in flags.option: # scheme to ppp-SRC
    
    XbMin       = 0.8
    cut         = ROOT.TCut("((0.938*0.938 + 2*0.938*q.E() - Q2)<2 && Xb>%f && PcmFinalState.Pt() < 0.4)"%XbMin) # cut: (W2 ~ (Mp2+2Mp\omega-Q2)<2) and small Pmiss-Transverse
    DataName    = "New_NoCTofDATA_%s"%dm.Target(A)
    ana         = TAnalysisEG2()
    scheme.SchemeOnTCut( path+"/AnaFiles" , "Ana_TwoSlowProtons_"+DataName+".root", "anaTree",
                        "Ana_ppnothing_alpha12_vs_XbCutDIS_"+DataName+".root", cut+ana.alpha12_vs_XbCutDIS )
    scheme.SchemeOnTCut( path+"/AnaFiles" , "Ana_TwoSlowProtons_"+DataName+".root", "anaTree",
                        "Ana_ppnothing_alpha12_vs_XbCutCorrelation_"+DataName+".root", cut+ana.alpha12_vs_XbCutCorrelation )
    print 'schemed to alpha12_vs_XbCutDIS and alpha12_vs_XbCutCorrelation'



# (1) SRC and kinematical cuts
# ----------------------------------------
if 'plot ppp sample cuts' in flags.option or 'cuts' in flags.option:
    print_important("ipynb notebooks/ppp_analysis.ipynb")


# (2) count the number of events in our sample
# ----------------------------------------
if "count e,e'p/pp/ppp" in flags.option or 'count' in flags.option:
    print_important("count e,e'p/pp/ppp")
    ana_all.PrintInCuts()

#    print_important("plot ppp sample cuts")
#    cuts_vars = pd.DataFrame({
#                             'var':     ['Xb'   ,'Pmiss.P()'    ,'Pmiss.Pt()'   ,'theta_pq'     ,'p_over_q' ],
#                             'ppp_cut': [xB_cut ,p_miss_cut     ,p_miss_t_cut   ,theta_pq_cut   ,p_over_q_cut],
#                             'xmin':    [0.8    ,0              ,0              ,0              ,0.2],
#                             'xmax':    [4      ,1.5            ,1              ,100            ,1.1],
#                             'nbins':   [30     ,35             ,30             ,40             ,30],
#                             })
#    do1d = False
#    if do1d:
#        plot_hist1d_ppp( cuts_vars , 'Xb' , '$x_B$' )
#        plot_hist1d_ppp( cuts_vars , 'Pmiss.P()' , '|$p_{miss}$| [GeV/c]' )
#        plot_hist1d_ppp( cuts_vars , 'Pmiss.Pt()', '$(p_{miss})_T$ [GeV/c]' )
#    do2d = True
#    if do2d:
##        plot_hist2d_ppp( cuts_vars , 'p_over_q' , 'p/q', 'theta_pq',  '$\\theta(p,q)$ [deg.]' )
#        plot_hist2d_ppp( cuts_vars , 'p_over_q' , 'p/q', 'theta_pq',  '$\\theta(p,q)$ [deg.]' )



