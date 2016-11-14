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



