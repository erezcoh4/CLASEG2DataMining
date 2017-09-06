from definitions import *
from root_numpy import hist2array , tree2array
from root_pandas import to_root
from scipy.stats import ks_2samp
from matplotlib.ticker import LinearLocator
from matplotlib.ticker import NullFormatter

from math import sqrt
from scipy.stats.mstats import ttest_onesamp
from scipy.stats import kurtosis
from scipy.stats import skew
from scipy.signal import argrelextrema
from scipy.stats import binom_test
from ndtest import *
from lmfit import  Model

sqrt2pi = np.sqrt(2*np.pi)


# ------------------------------------------------------------------------------- #
# definitions
PmissBins       = [[0.3,0.45]  , [0.45,0.55] , [0.55,0.65]  , [0.65,0.75] , [0.75,1.0]]
targets         = ['C12'        , 'Al27'        , 'Fe56'        , 'Pb208'       ]
labels          = ['$^{12}$C'   , '$^{27}$Al'   , '$^{56}$Fe'   , '$^{208}$Pb'  ]
target_colors   = ['black'      , 'red'         , 'green'       , 'blue'        ]
PvalZ_calculation_methods = ['Fisher','AverageBins','KS2D']


PmissBinsPerTarget = dict( {'C12':[[0.3,0.45]  , [0.45,0.55] , [0.55,0.65]  , [0.65,0.75] , [0.75,1.0]]
                            ,'Al27':[[0.3,0.5]  , [0.5,0.7] , [0.7,1.0]]
                            ,'Fe56':[[0.3,0.45]  , [0.45,0.55] , [0.55,0.65]  , [0.65,0.75] , [0.75,1.0]]
                            ,'Pb208':[[0.3,0.6]  , [0.6,1.0]]})

small10PmissBins = [[0.3,0.4] , [0.4,0.5] , [0.5,0.6] , [0.6,0.7] , [0.7,0.8] , [0.8,0.9] , [0.9,1.0] ]
Q2Bins           = [[0,1.5]     , [1.5,2]     , [2,2.5]      , [2.5,6]]
theta_Pm_qBins   = [[100,135]   , [135,145]   , [145,155]    , [155,180]]

p_binom_array = [0.2,0.225,0.25,0.3,0.33,0.36,0.4,0.45,0.5]


# file names
def CMParsFname( path ):
    return path+"CMparameters.csv"
def CMRooFitsName( path ):
    return path+"CMRooFits.pdf"
def CMfitsFname( path , target='' ):
    return path+"CMfits%s.csv"%target
def CMBandFname( path ):
    return path+"CMparameter_Bands.csv"
def FigureFName( path , target='' ):
    return path+"cm_width_and_mean%s.pdf"%target
def FigureBandFName( path ):
    return path+"cm_width_and_mean_Bands.pdf"
def GeneParsFName( path ):
    return path+"GeneratedParameters.csv"
def resutlsFName( path ):
    return path+"EG_simulated_runs_results_cm_parameters.csv"
def buildup_resultsFName( path ):
    return path+"runs_results.csv"
def root_resutlsFName( path ):
    return path+"runs_results.root"


# ------------------------------------------------------------------------------- #
# fitting functions
def linear(x, slope, intercept):
    return slope * ( x ) + intercept
def linear_06(x, slope, intercept):
    return slope * ( x - 0.6 ) + intercept
def gauss(x,mu_0,sigma_0,A_0):
    return A_0*np.exp(-np.square(x-mu_0)/(2.*np.square(sigma_0)))
# ------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------- #
def calc_pval_ks_scores(ana_sim=None, ana_data=dict(), do_plots=False , run=-1, Nattempts=1, target=''):
    
    nbins = 25 # number of bins for histograms in each direction
    NPmbins = len(PmissBinsPerTarget[target])
    bins_histograms_l = np.linspace(-0.4,1.2,40)
    
#    ks_pval_scores = dict()
    # April-2017, change to Pval using ks-test
    df_sim = tree2array( ana_sim.GetTree() , branches=['pcmX','pcmY','pcmZ','Pmiss3Mag'] )
#    for target in targets: #{

    if do_plots:  #{
        from notebook_tools import *
        gen_info = tree2array( ana_sim.GetTree() , branches=['gen_SigmaX','gen_a1','gen_a2','gen_b1','gen_b2'] )
        if debug>2: print 'gen: SigmaX ',gen_info[0]['gen_SigmaX'],'a1',gen_info[0]['gen_a1'],'a2',gen_info[0]['gen_a2'],'b1',gen_info[0]['gen_b1'],'b2',gen_info[0]['gen_b2']
        fig = plt.figure(figsize=(24,24))
    #}

    ks_pval_scores_target_array , ks_pval_scores_longitudinal_target_array = [] , []
    ks_pval_scores_target = dict()
    df_data = tree2array( ana_data[target].GetTree() , branches=['pcmX','pcmY','pcmZ','Pmiss3Mag'] )
        
    # compare x & y directions in 1 p(miss) bin - since there is no p(miss) dependence
    for i_dir,direction in enumerate(['X','Y']): #{
        x_data = df_data['pcm'+direction]
        x_sim = df_sim['pcm'+direction]
        D_KS , Pval_KS = ks_2samp( x_data , x_sim )
        ks_pval_scores_target['pcm'+direction] = Pval_KS
        ks_pval_scores_target_array.append( Pval_KS )
        if do_plots:#{
            if direction=='X':#{
                ax = fig.add_subplot( 3 , NPmbins , (2,NPmbins) )
                ax.yaxis.set_major_formatter(NullFormatter())
            #}
            h,bins,_=ax.hist(x_sim, bins=nbins,label='sim. $p_{c.m.}^{%s}, Pval=%.1g$'%(direction,Pval_KS)
#                                ,label='sim. $p_{c.m.}^{%s}$ $\\mu=%.3f, \\sigma=%.3f, Pval=%f$'%(direction,np.mean(x_sim),np.std(x_sim),Pval_KS)
                                ,histtype='step',linewidth=3,normed=1)
            ax.hist(x_data , bins=bins,label='data $p_{c.m.}^{%s}$'%direction
#                        ,label=target+' data $p_{c.m.}^{%s}$  $\\mu=%.3f, \\sigma=%.3f$'%(direction,np.mean(x_data),np.std(x_data))
                        ,histtype='step'
                        ,linewidth=3
                        ,normed=1)
            if direction=='Y': #{
                ax.set_title("gen. $\sigma=%.3f$"%gen_info[0]['gen_SigmaX'],y=1.02,fontsize=20)
                ax.legend(loc='best',fontsize=20)
            #}
        #}
    #}
    ks_pval_scores_target['Pval_pcmX_pcmY'] = Fisher_combination_Pvals( [ks_pval_scores_target['pcmX'],ks_pval_scores_target['pcmY']] ) # with a cutoff on 1e-20

    # in z direction - compare in N bins of p(miss)
    for bin in range(len(PmissBinsPerTarget[target])):#{
            
        pmin , pmax = PmissBinsPerTarget[target][bin][0] , PmissBinsPerTarget[target][bin][1]
        df_sim_reduced = df_sim[ (pmin < df_sim['Pmiss3Mag']) & (df_sim['Pmiss3Mag'] < pmax) ]
        df_data_reduced = df_data[ (pmin < df_data['Pmiss3Mag']) & (df_data['Pmiss3Mag'] < pmax) ]
        D_KS , Pval_KS = ks_2samp( df_sim_reduced['pcmZ'] , df_data_reduced['pcmZ'] )
        sim_skew = skew( df_sim_reduced['pcmZ'] )
        sim_kurt = kurtosis( df_sim_reduced['pcmZ'] )
        '''
                Check if the distribution of p(c.m.)-z in this bin is indeed Gaussian,
                and if not - kill it by Pval=0
                find number of local maxima. If greated than 1, kill the run
                '''
        # May-6
        if do_plots:#{
            data_skew = skew( df_data_reduced['pcmZ'] )
            data_kurt = kurtosis( df_data_reduced['pcmZ'] )
            hist , bin_edges = np.histogram (df_data_reduced['pcmZ'] , bins=bins)
            ax_l = fig.add_subplot( 3 , NPmbins , NPmbins + bin + 1 )
            h,bins,_=ax_l.hist(df_sim_reduced['pcmZ'] , bins=bins_histograms_l
                               ,histtype='step',linewidth=3,normed=1
                               ,label='simulation (%d)' %(len(df_sim_reduced)))
#                                   ,label='sim. (%d) \n $\\mu=%.3f$ \n $\\sigma=%.3f$ \n $\\mu_3=%.2f$ \n $\\mu_4=%.2f$'
            ax_l.hist(df_data_reduced['pcmZ'] , bins=bins
                      ,histtype='step',linewidth=3,normed=1
                      ,label=target+' data  (%d)'%len(df_data_reduced))
#                        ,label=target+' data  (%d) \n $\\mu=%.3f$ \n $\\sigma=%.3f$ \n $\\mu_3=%.2f$ \n $\\mu_4=%.2f$'                        %(len(df_data_reduced),np.mean(df_data_reduced['pcmZ']),np.std(df_data_reduced['pcmZ']),data_skew,data_kurt)
                      
            ax_l.set_title('%.2f<$p_{miss}$<%.2f GeV/c, $p_{c.m.}^{z}$ Pval=%g'%(pmin , pmax,Pval_KS),y=1.01,fontsize=15)
            ax_l.legend(fontsize=15,loc='best')
            set_axes(ax_l,"","",fontsize=15)
            ax_l.yaxis.set_major_formatter(NullFormatter())
            ax_l.xaxis.set_ticks(np.linspace(np.min(ax_l.get_xlim())+0.1,np.max(ax_l.get_xlim()),4,endpoint=False))
        #
        
        ks_pval_scores_longitudinal_target_array.append( Pval_KS )
        ks_pval_scores_target['pcmZ_bin%d'%bin] = Pval_KS
        ks_pval_scores_target['pcmZ_bin%d_skew'%bin] = sim_skew
        ks_pval_scores_target['pcmZ_bin%d_kurt'%bin] = sim_kurt
        ks_pval_scores_target_array.append( Pval_KS )

    #}
        
    # --- global Pval from combination of all scores together --- #
    ks_pval_scores_target['PvalTotal'] = Fisher_combination_Pvals( ks_pval_scores_target_array ) # with a cutoff on 1e-20
    # --- global Pval with the Fisher combination of the Pvalues in the z direction along N bins in Pmiss --- #
    ks_pval_scores_target['pcmZ_Fisher'] = Fisher_combination_Pvals( ks_pval_scores_longitudinal_target_array ) # with a cutoff on 1e-20
    # --- global Pval with the average local Pval in the z direction along N bins in Pmiss --- #
    ks_pval_scores_target['pcmZ_AverageBins'] = np.average( ks_pval_scores_longitudinal_target_array )
    # --- global Pval with the Fisher combination of the Pvalues in the z direction along N bins in Pmiss --- #
    ks_pval_scores_target['pcmZ_KS2D'] = ks2d2s( df_sim['Pmiss3Mag'] , df_sim['pcmZ'] , df_data['Pmiss3Mag'] , df_data['pcmZ'] )


    # 2-d KS test
    if do_plots: #{
        ax = fig.add_subplot(3 , NPmbins , (2*NPmbins+1,(int)(2.5*NPmbins) ) )
        ax.set_title('simulation, $P_{val}^{2d-KS}=%g$'% ks_pval_scores_target['pcmZ_KS2D'],fontsize=25,y=1.02)
        plot_2d_hist(df_sim['Pmiss3Mag'] , df_sim['pcmZ'] ,ax=ax ,xlabel='$p_{miss}$ [GeV/c]',ylabel='$p_{cm}$ [GeV/c]')
        ax.set_ylim(-0.2,1.)
        ax = fig.add_subplot(3 , NPmbins , ((int)(2.5*NPmbins) + 1,3*NPmbins) )
        ax.set_title( target +' data',fontsize=25)
        plot_2d_hist(df_data['Pmiss3Mag'] , df_data['pcmZ'] ,ax=ax ,xlabel='$p_{miss}$ [GeV/c]',ylabel='')
        ax.set_ylim(-0.2,1.)
    #}

    for method in PvalZ_calculation_methods: #{
        ks_pval_scores_target['Pval_pcmX_pcmY_pcmZ_'+method] = Fisher_combination_Pvals( [ks_pval_scores_target['pcmX'],
                                                                                              ks_pval_scores_target['pcmY'],
                                                                                              ks_pval_scores_target['pcmZ_'+method]] ) # with a cutoff on 1e-20
        ks_pval_scores_target['Pval_pcmX_pcmY_pcmZ_scaled_1e20_'+method] = ks_pval_scores_target['Pval_pcmX_pcmY_pcmZ_'+method]*1e20
            
        powered_array = np.concatenate( [ ks_pval_scores_target['pcmX']*np.ones(len(PmissBins))
                                             ,ks_pval_scores_target['pcmY']*np.ones(len(PmissBins)) ] )
        powered_array = np.append( powered_array , ks_pval_scores_target['pcmZ_'+method])
        if debug>3: #{
            print "powered_array:",powered_array
        #}
        ks_pval_scores_target['Pval_Powered_pcmX_Powered_pcmY_pcmZ_'+method] = Fisher_combination_Pvals( powered_array )
    #}
    # methods to combine Pvalue [https://arxiv.org/pdf/1212.4966.pdf]
    # Bonferroni: N * min( P1, P2, P3.... , PN)
#    ks_pval_scores_target['pcmZ_Bonferroni'] = 5*np.min( ks_pval_scores_longitudinal_target_array )
#    ks_pval_scores_target['Pval_pcmX_pcmY_pcmZ_Bonferroni'] = 3*np.min( [ks_pval_scores_target['pcmX'],ks_pval_scores_target['pcmY'],ks_pval_scores_target['pcmZ_Bonferroni']] )
    # Ruschendorf: average
#    ks_pval_scores_target['pcmZ_Ruschendorf'] = np.average( ks_pval_scores_longitudinal_target_array )
#    ks_pval_scores_target['Pval_pcmX_pcmY_pcmZ_Ruschendorf'] = np.average( [ks_pval_scores_target['pcmX'],ks_pval_scores_target['pcmY'],ks_pval_scores_target['pcmZ_Ruschendorf']] )


    if do_plots:#{
        ax = fig.add_subplot( 3 , NPmbins , 1 )
        xmin,xmax = np.min(ax.get_xlim()),np.max(ax.get_xlim())
        ax.set_title( "$a_{1}=%.2f , a_{2}=%.2f , b_{1}=%.2f , b_{2}=%.2f$\n"% (gen_info[0]['gen_a1'],gen_info[0]['gen_a2']
                                                                                ,gen_info[0]['gen_b1'],gen_info[0]['gen_b2'])
                     ,y=1.02)
        ax.xaxis.set_major_formatter(NullFormatter()); ax.yaxis.set_major_formatter(NullFormatter())
        text = "$N_{attempts} = %d$\n"%Nattempts
        text += "$Pval_{x-y}=%.1g$\n"%ks_pval_scores_target['Pval_pcmX_pcmY']
        for method in PvalZ_calculation_methods: #{
            #            text += "$Pval_{z}=%g$\n"%ks_pval_scores_target['pcmZ_'+method]
            text += "$Pval^{"+method+"}_{xyz}=%.1g$\n"%ks_pval_scores_target['Pval_pcmX_pcmY_pcmZ_'+method]
            text += "$Pval^{"+method+"}_{x^{%d} y^{%d} z}=%.1g$\n"%(len(PmissBins),len(PmissBins)
                                                                  ,ks_pval_scores_target['Pval_Powered_pcmX_Powered_pcmY_pcmZ_'+method])
        #}
        #        plt.text(xmin + 0.05*(xmax-xmin),0.5*np.max(ax.get_ylim()) ,text,fontsize=25)
        plt.text(np.min(ax.get_xlim())+0.01*(np.max(ax.get_xlim())-np.min(ax.get_xlim())),0.01*np.max(ax.get_ylim()) ,text,fontsize=20)
        if flags.worker == 'erez': figure_path = "/Users/erezcohen/Desktop/TmpPlots"
        elif flags.worker == 'helion': figure_path = "/home/erez/Desktop/TmpPlots"
        fig.tight_layout()
        fig.savefig(figure_path + "/run_%d_%s.pdf"%(run,target))
        print 'saved',figure_path + "/run_%d_%s.pdf"%(run,target)
    #}

    #        ks_pval_scores_target['PvalTotal_allPvals'] = FisherMethodPvals( ks_pval_scores_target_array )
                     #    if debug: #{
                     #        if debug>1:#{
                     #            print "ks-pval["+target+"]['Pval_pcmX_pcmY']:",ks_pval_scores_target['Pval_pcmX_pcmY']
                     #            print "ks-pval["+target+"]['pcmZ_Fisher']:",ks_pval_scores_target['pcmZ_Fisher']
                     #        #}
                     #        print "ks-pval["+target+"]['PvalTotal']:",ks_pval_scores_target['PvalTotal']
                     #    #}

    return ks_pval_scores_target
#        ks_pval_scores[target] = ks_pval_scores_target
    #}
#    if debug>2:#{
#        print 'ks_pval_scores:'
#        for i in ks_pval_scores:#{
#            print i
#            for j in ks_pval_scores[i]:#{
#                print j,ks_pval_scores[i][j]
#            #}
#        #}
#    #}
#
#    return ks_pval_scores
# ------------------------------------------------------------------------------- #






# ------------------------------------------------------------------------------- #
def plot_errorbar_and_fit( ax , x , y , xerr , yerr , color , marker , lstyle , label ,
                          fit_type='const' ,do_plot_fit_pars=False, x_offset=0.6):
    plt.errorbar(x, y, xerr=xerr, yerr=yerr, color=color, marker=marker , linestyle=lstyle , label=None , markersize=15)
    if fit_type=='const':
        if debug>1: print label + ' (const. fit)'
        const_fit , const_fitErr , const_chi2red = fit_as_a_function_of_pmiss( x , y , yerr=yerr , fit_type=fit_type )
        if do_plot_fit_pars: label=label + "$=%.3f\pm%.3f$"%(const_fit,const_fitErr)
        ax.plot(x, np.ones(len(x))*const_fit , color=color , linestyle='--', label=label,linewidth = 2 , )
        if debug>1: #{
            print 'const_fit: %.3f(%.0f) '%(const_fit , 1000*const_fitErr)
        #}
        return [ const_fit , const_fitErr , const_chi2red ]
    
    elif fit_type=='linear':
        if debug>1: print label + ' (linear fit)'
        a1 , a1err , a2 , a2err , chi2red = fit_as_a_function_of_pmiss( x , y ,yerr=yerr, fit_type=fit_type )
        if do_plot_fit_pars: label=label + "$=(%.3f)(p_{miss}-%.1f)+(%.3f)$"%( a1 , x_offset, a2 )
        ax.plot( x , a1 * (x-x_offset) + a2 , color = color ,label=label )
        if debug>1:#{
            print 'a1: %.3f(%.0f)'%(a1 , 1000*a1err)
            print 'a2: %.3f(%.0f)'%(a2 , 1000*a2err)
        #}
        return [ a1 , a1err ,  a2 , a2err  , chi2red ]
# ------------------------------------------------------------------------------- #



# ------------------------------------------------------------------------------- #
def fit_as_a_function_of_pmiss( x , y , yerr=None, fit_type='const' , title='', x_offset=0.6): #{ # the main fitting routine
    
    if fit_type=='const':
#        if len(x)<3: return -100 , 0
        p1,v1 = np.polyfit( x , y , 0 , cov=True)
        v1[0,0] = np.var( y )
        chi2red = -100
        if debug>4: print 'x:',x,'\ny:',y,'\np1:',p1,',\tv1:',v1

        if not p1 or not v1 or len(p1)==0 or len(v1)==0:
            return -100 , 0 , 0
        else:
            return p1[0] , sqrt(v1[0,0]) , chi2red
    #        p2,v2 = np.polyfit( x , y , 1 , cov=True)        # fit a polynomial p2(x) = p2[0] * x + p2[1]
    elif fit_type=='linear':

#        if len(x)<4:
#            return -100 , 0 , -100 , 0
        if x_offset==0: f = linear
        else: f = linear_06
        p2, v2 = curve_fit(f, xdata=x, ydata=y,sigma=yerr)# fit data using SciPy's Levenberg-Marquart method
        chi2red = (np.sum( np.square( (np.polyval(p2, x) - y) / yerr ) ))/(len(x) - 2)

        if debug>4:
            print 'p2:\n',p2,'\nv2:\n',v2

        if p2 is None or v2 is None or p2 is np.inf or v2 is np.inf:
            return -100 , 0 , -100 , 0 , 0
        if p2[0] is np.inf or p2[1] is np.inf or v2[0,0] is np.inf or v2[1,1] is np.inf:
            return -100 , 0 , -100 , 0 , 0
        else:
            return p2[0] , sqrt(float(v2[0,0])) , p2[1] , sqrt(float(v2[1,1])) , chi2red
#}
# ------------------------------------------------------------------------------- #

# ------------------------------------------------------------------------------- #
def calc_cm_parameters( fana  , fPmissBins , unweightedRoofitsFName = '' , weightedRoofitsFName = '' , DoSaveCanvas = False ):
    '''
        Return: df_pMissBin , do_fits (continue or not)
        '''
    do_fits = True
    df_pMissBins = pd.DataFrame()
    
    if DoSaveCanvas:
        canvas_unweighted , canvas_weighted = fana.CreateCanvas( "RooFit plots - unweighted" , "Divide" , 4 , len(fPmissBins) ) , fana.CreateCanvas( "RooFit plots - weighted" , "Divide" , 4 , len(fPmissBins) )

    # Jan 2017, changing to a (weighted) average and variance using numpy
    if fana.GetEntries()==0:
        print 'no entries in anaTree of',fana.GetFileName()
        print 'leaving calc_cm_parameters'
        return pd.DataFrame() , False

    if debug>2: print 'fana.GetFileName():',fana.GetFileName()
    ana = read_root( str(fana.GetFileName()) , key='anaTree' , columns=['pcmX','pcmY','pcmZ','Pmiss3Mag','rooWeight','Mott']  )

    for i in range(len(fPmissBins)):
        pMiss_min , pMiss_max = fPmissBins[i][0] , fPmissBins[i][1]
        ana_reduced = ana[ (pMiss_min < ana.Pmiss3Mag) & (ana.Pmiss3Mag < pMiss_max) ]
        good_bin = True if len(ana_reduced)>0 else False
        
        if DoSaveCanvas:
            unweighted = fana.RooFitCM( pMiss_min , pMiss_max , False , True, flags.verbose, canvas_unweighted, 4*i + 1 )
            weighted = fana.RooFitCM( pMiss_min , pMiss_max , True , True, flags.verbose, canvas_weighted, 4*i + 1 )
        
            df_pMissBin = pd.DataFrame({'pMiss_min':pMiss_min,'pMiss_max':pMiss_max
                                       ,'EvtsInBin':len(ana_reduced)            ,'good_bin':good_bin
                                       ,'mean_x_unweighted':unweighted[0],'mean_xErr_unweighted':unweighted[1],'sigma_x_unweighted':unweighted[2],'sigma_xErr_unweighted':unweighted[3]
                                       ,'mean_y_unweighted':unweighted[4],'mean_yErr_unweighted':unweighted[5],'sigma_y_unweighted':unweighted[6],'sigma_yErr_unweighted':unweighted[7]
                                       ,'mean_t_unweighted':unweighted[8],'mean_tErr_unweighted':unweighted[9],'sigma_t_unweighted':unweighted[10],'sigma_tErr_unweighted':unweighted[11]
                                       ,'mean_z_unweighted':unweighted[12],'mean_zErr_unweighted':unweighted[13],'sigma_z_unweighted':unweighted[14],'sigma_zErr_unweighted':unweighted[15]
                                       ,'mean_x_weighted':weighted[0],'mean_xErr_weighted':weighted[1],'sigma_x_weighted':weighted[2],'sigma_xErr_weighted':weighted[3]
                                       ,'mean_y_weighted':weighted[4],'mean_yErr_weighted':weighted[5],'sigma_y_weighted':weighted[6],'sigma_yErr_weighted':weighted[7]
                                       ,'mean_t_weighted':weighted[8],'mean_tErr_weighted':weighted[9],'sigma_t_weighted':weighted[10],'sigma_tErr_weighted':weighted[11]
                                       ,'mean_z_weighted':weighted[12],'mean_zErr_weighted':weighted[13],'sigma_z_weighted':weighted[14],'sigma_zErr_weighted':weighted[15]}
                                       , index=[i])

        else:
            #            unweighted = fana.RooFitCM( pMiss_min , pMiss_max , False )
            #            weighted = fana.RooFitCM( pMiss_min , pMiss_max , True )

            # Jan 2017, changing to a (weighted) average and variance using numpy
            # ana_reduced = ana[ (pMiss_min < ana.Pmiss3Mag) & (ana.Pmiss3Mag < pMiss_max) ]
            if flags.verbose>1: print 'running p(miss) bin ',i,',',pMiss_min,' to ',pMiss_max,' GeV/c, ',len(ana_reduced),'events in this bin'

            if len(ana_reduced)>0 and sum(ana_reduced.rooWeight)>0:
                good_bin , sqrtN = 1 , sqrt(len(ana_reduced))
                mean_x_unweighted , mean_x_weighted     = np.average( ana_reduced.pcmX ) , np.average( ana_reduced.pcmX , weights=ana_reduced.rooWeight )
                sigma_x_unweighted, sigma_x_weighted    = np.sqrt(np.average( np.square(ana_reduced.pcmX-mean_x_unweighted) )) , np.sqrt(np.average( np.square(ana_reduced.pcmX-mean_x_weighted) , weights=ana_reduced.rooWeight  ))
                mean_y_unweighted , mean_y_weighted     = np.average( ana_reduced.pcmY ) , np.average( ana_reduced.pcmY , weights=ana_reduced.rooWeight )
                sigma_y_unweighted, sigma_y_weighted    = np.sqrt(np.average( np.square(ana_reduced.pcmY-mean_y_unweighted) )) , np.sqrt(np.average( np.square(ana_reduced.pcmY-mean_y_weighted) , weights=ana_reduced.rooWeight  ))
                mean_z_unweighted , mean_z_weighted     = np.average( ana_reduced.pcmZ ) , np.average( ana_reduced.pcmZ , weights=ana_reduced.rooWeight )
                sigma_z_unweighted, sigma_z_weighted    = np.sqrt(np.average( np.square(ana_reduced.pcmZ-mean_z_unweighted) )) , np.sqrt(np.average( np.square(ana_reduced.pcmZ-mean_z_weighted) , weights=ana_reduced.rooWeight  ))
            else:
                good_bin , sqrtN , do_fits  = 0 , 1 , False
                mean_x_unweighted , mean_x_weighted     = -100,-100
                sigma_x_unweighted, sigma_x_weighted    = -100,-100
                mean_y_unweighted , mean_y_weighted     = -100,-100
                sigma_y_unweighted, sigma_y_weighted    = -100,-100
                mean_z_unweighted , mean_z_weighted     = -100,-100
                sigma_z_unweighted, sigma_z_weighted    = -100,-100


            df_pMissBin = pd.DataFrame({'pMiss_min':pMiss_min                   ,'pMiss_max':pMiss_max
                                       ,'EvtsInBin':len(ana_reduced)            ,'good_bin':good_bin
                                       ,'mean_x_unweighted':mean_x_unweighted   ,'mean_xErr_unweighted':sigma_x_unweighted/sqrtN ,'sigma_x_unweighted':sigma_x_unweighted,'sigma_xErr_unweighted':0.02 # resolution uncertainty
                                       ,'mean_y_unweighted':mean_y_unweighted   ,'mean_yErr_unweighted':sigma_y_unweighted/sqrtN ,'sigma_y_unweighted':sigma_y_unweighted,'sigma_yErr_unweighted':0.02 # resolution uncertainty0
                                       ,'mean_z_unweighted':mean_z_unweighted   ,'mean_zErr_unweighted':sigma_z_unweighted/sqrtN ,'sigma_z_unweighted':sigma_z_unweighted,'sigma_zErr_unweighted':0.02 # resolution uncertainty
                                       ,'mean_x_weighted':mean_x_weighted       ,'mean_xErr_weighted':sigma_x_weighted/sqrtN     ,'sigma_x_weighted':sigma_x_weighted    ,'sigma_xErr_weighted':0.02 # resolution uncertainty
                                       ,'mean_y_weighted':mean_y_weighted       ,'mean_yErr_weighted':sigma_y_weighted/sqrtN     ,'sigma_y_weighted':sigma_y_weighted    ,'sigma_yErr_weighted':0.02 # resolution uncertainty
                                       ,'mean_z_weighted':mean_z_weighted       ,'mean_zErr_weighted':sigma_z_weighted/sqrtN     ,'sigma_z_weighted':sigma_z_weighted    ,'sigma_zErr_weighted':0.02 # resolution uncertainty
                                       }
                                       , index=[i])

        df_pMissBins = df_pMissBins.append(df_pMissBin)

    if DoSaveCanvas:#{
        canvas_unweighted.SaveAs(unweightedRoofitsFName)
        print_filename(unweightedRoofitsFName,"unweighted rooFits at")
        canvas_weighted.SaveAs(weightedRoofitsFName)
        print_filename(weightedRoofitsFName,"weighted rooFits at")
        print_line()
    #}
    if debug>1:#{
        print "computed cm parameters for "+fana.InFileName
        print "reconstructed cm parameters"
        if debug>5: print 'df_pMissBins:',df_pMissBins
    #}
    garbage_list = [ ana ]
    del garbage_list

    return df_pMissBins , do_fits
# ------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------- #
# Aug-31,2017
def gaussian_pdf( x=None, mean_gauss=None , sigma_gauss=None  ):#{
    return 1. / (np.sqrt(2*np.pi)*sigma_gauss) * exp(-np.square( x - mean_gauss) /(2*np.square(sigma_gauss)))
#}

# ------------------------------------------------------------------------------- #
# Sep-6
def gaussian(x, amp, mean_gauss, sigma_gauss):
    "1-d gaussian: gaussian(x, amp, cen, wid)"
    return (amp/(sqrt(2*np.pi)*sigma_gauss)) * np.exp(-(x-mean_gauss)**2 /(2*sigma_gauss**2))
gmodel = Model(gaussian)
# ------------------------------------------------------------------------------- #

# ------------------------------------------------------------------------------- #
# Aug-31,2017
def calc_chi2_gauss( data=None, data_errs=None, mean_gauss=None , sigma_gauss=None ):#{
#    function = A / (np.sqrt(2*np.pi)*sigma_gauss) * exp(-np.square((x-mean_gauss)) /(2*np.square(sigma_gauss))
    N = len(data)
    z = ( data - function ) / data_errs
    chi2 = np.sum(z ** 2)
    chi2dof = chi2 / (N - 1)
#}
# ------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------- #
# May-27, 2017
def calc_cm_pars_sigma( fana , unweightedRoofitsFName = '' , weightedRoofitsFName = '' , DoSaveCanvas = False , pMiss_max = 0.6 ):
    '''
            Return: pd.DataFrame ({mean_x , sigma_x ,mean_y , sigma_y , mean_z , sigma_z})
            '''
    df_result = pd.DataFrame()

    if fana.GetEntries()==0:#{
        print 'no entries in anaTree of',fana.GetFileName()
        print 'leaving calc_cm_parameters'
        return pd.DataFrame() , False
    #}
    
    ana = read_root( str(fana.GetFileName()) , key='anaTree' , columns=['pcmX','pcmY','pcmZ','Pmiss3Mag','rooWeight']  )

    # ToDo: I've changed from (DoSaveCanvas) to (DoSaveCanvas == True or DoSaveCanvas==False). Keep it?
    if DoSaveCanvas:#{
        canvas_unweighted = fana.CreateCanvas( "RooFit plots - unweighted" , "Divide" , 3 , 1 )
        unweighted = fana.RooFitCM_1bin( 0.3 , pMiss_max , False , True, flags.verbose, canvas_unweighted )
#        canvas_weighted = fana.CreateCanvas( "RooFit plots - Mott weighted" , "Divide" , 3 , 1 )
#        weighted = fana.RooFitCM_1bin( 0.3 , pMiss_max , True , True, flags.verbose, canvas_weighted )
#        df_result = pd.DataFrame({'Nevts':len(ana)
#                                 ,'mean_x_unweighted':unweighted[0],'mean_xErr_unweighted':unweighted[1],'sigma_x_unweighted':unweighted[2],'sigma_xErr_unweighted':unweighted[3]
#                                 ,'mean_y_unweighted':unweighted[4],'mean_yErr_unweighted':unweighted[5],'sigma_y_unweighted':unweighted[6],'sigma_yErr_unweighted':unweighted[7]
#                                 ,'mean_z_unweighted':unweighted[8],'mean_zErr_unweighted':unweighted[9],'sigma_z_unweighted':unweighted[10],'sigma_zErr_unweighted':unweighted[11]
#                                 ,'chi2red_x_unweighted':unweighted[12],'ndof_x_unweighted':unweighted[13]
#                                 ,'chi2red_y_unweighted':unweighted[14],'ndof_y_unweighted':unweighted[15]
#                                 ,'chi2red_z_unweighted':unweighted[16],'ndof_z_unweighted':unweighted[17]
#                                 
#                                 ,'mean_x_weighted':weighted[0],'mean_xErr_weighted':weighted[1],'sigma_x_weighted':weighted[2],'sigma_xErr_weighted':weighted[3]
#                                 ,'mean_y_weighted':weighted[4],'mean_yErr_weighted':weighted[5],'sigma_y_weighted':weighted[6],'sigma_yErr_weighted':weighted[7]
#                                 ,'mean_z_weighted':weighted[8],'mean_zErr_weighted':weighted[9],'sigma_z_weighted':weighted[10],'sigma_zErr_weighted':weighted[11]
#                                 }
#                                 , index=[0])
#        print df_result
#        # binned Gaussian fit
#        h_x,edges = np.histogram( ana.pcmX , bins=50 )
#        result = gmodel.fit(h_x, x=edges[:-1], amp=1, mean_gauss=np.mean(ana.pcmX), sigma_gauss=np.std(ana.pcmX))
#        print(result.fit_report())
#        h_y,edges = np.histogram( ana.pcmY , bins=50 )
#        result = gmodel.fit(h_y, x=edges[:-1], amp=1, mean_gauss=np.mean(ana.pcmY), sigma_gauss=np.std(ana.pcmY))
#        print(result.fit_report())
#        h_z,edges = np.histogram( ana.pcmZ , bins=50 )
#        result = gmodel.fit(h_z, x=edges[:-1], amp=1, mean_gauss=np.mean(ana.pcmZ), sigma_gauss=np.std(ana.pcmZ))
#        print(result.fit_report())

    #}
    else:#{
        unweighted = fana.RooFitCM_1bin( 0.3 , pMiss_max , False , False, flags.verbose )
#        weighted = fana.RooFitCM_1bin( 0.3 , pMiss_max , True , False, flags.verbose )
    #}
    df_result = pd.DataFrame({'Nevts':len(ana)
                         ,'mean_x_unweighted':unweighted[0],'mean_xErr_unweighted':unweighted[1],'sigma_x_unweighted':unweighted[2],'sigma_xErr_unweighted':unweighted[3]
                         ,'mean_y_unweighted':unweighted[4],'mean_yErr_unweighted':unweighted[5],'sigma_y_unweighted':unweighted[6],'sigma_yErr_unweighted':unweighted[7]
                         ,'mean_z_unweighted':unweighted[8],'mean_zErr_unweighted':unweighted[9],'sigma_z_unweighted':unweighted[10],'sigma_zErr_unweighted':unweighted[11]
                         ,'chi2red_x_unweighted':unweighted[12],'ndof_x_unweighted':unweighted[13]
                         ,'chi2red_y_unweighted':unweighted[14],'ndof_y_unweighted':unweighted[15]
                         ,'chi2red_z_unweighted':unweighted[16],'ndof_z_unweighted':unweighted[17]
                         
#                         ,'mean_x_weighted':weighted[0],'mean_xErr_weighted':weighted[1],'sigma_x_weighted':weighted[2],'sigma_xErr_weighted':weighted[3]
#                         ,'mean_y_weighted':weighted[4],'mean_yErr_weighted':weighted[5],'sigma_y_weighted':weighted[6],'sigma_yErr_weighted':weighted[7]
#                         ,'mean_z_weighted':weighted[8],'mean_zErr_weighted':weighted[9],'sigma_z_weighted':weighted[10],'sigma_zErr_weighted':weighted[11]
                         }
                         , index=[0])

#    else:#{
#        
#        if len(ana)>0:#{
#            # binned Gaussian fit
#            h_x,edges = np.histogram( ana.pcmX , bins=30 )
#            result = gmodel.fit(h_x, x=edges[:-1], amp=1, mean_gauss=np.mean(ana.pcmX), sigma_gauss=np.std(ana.pcmX))
#            print(result.fit_report())
#            
#            sqrtN = sqrt(len(ana))
#            mean_x_unweighted     = np.average( ana.pcmX )
#            sigma_x_unweighted    = np.sqrt(np.average( np.square( ana.pcmX-mean_x_unweighted) ))
#            mean_y_unweighted     = np.average( ana.pcmY )
#            sigma_y_unweighted    = np.sqrt(np.average( np.square( ana.pcmY-mean_y_unweighted) ))
#            mean_z_unweighted     = np.average( ana.pcmZ )
#            sigma_z_unweighted    = np.sqrt(np.average( np.square( ana.pcmZ-mean_z_unweighted) ))

        
#            chi2red_x_unweighted = calc_chi2_gauss( data=ana.pcmX , mean_gauss=mean_x_unweighted , sigma_gauss=sigma_x_unweighted )
        #}
#        if len(ana)>0 and sum(ana.rooWeight)>0:#{
#            sqrtN = sqrt(len(ana))
#            mean_x_unweighted , mean_x_weighted     = np.average( ana.pcmX ) , np.average( ana.pcmX , weights=ana.rooWeight )
#            sigma_x_unweighted, sigma_x_weighted    = np.sqrt(np.average( np.square( ana.pcmX-mean_x_unweighted) )) , np.sqrt(np.average( np.square(ana.pcmX-mean_x_weighted) , weights=ana.rooWeight  ))
#            mean_y_unweighted , mean_y_weighted     = np.average( ana.pcmY ) , np.average( ana.pcmY , weights=ana.rooWeight )
#            sigma_y_unweighted, sigma_y_weighted    = np.sqrt(np.average( np.square( ana.pcmY-mean_y_unweighted) )) , np.sqrt(np.average( np.square(ana.pcmY-mean_y_weighted) , weights=ana.rooWeight  ))
#            mean_z_unweighted , mean_z_weighted     = np.average( ana.pcmZ ) , np.average( ana.pcmZ , weights=ana.rooWeight )
#            sigma_z_unweighted, sigma_z_weighted    = np.sqrt(np.average( np.square( ana.pcmZ-mean_z_unweighted) )) , np.sqrt(np.average( np.square(ana.pcmZ-mean_z_weighted) , weights=ana.rooWeight  ))
#        #}
#        else:#{
#            sqrtN  = 1
#            mean_x_unweighted , mean_x_weighted     = -100,-100
#            sigma_x_unweighted, sigma_x_weighted    = -100,-100
#            mean_y_unweighted , mean_y_weighted     = -100,-100
#            sigma_y_unweighted, sigma_y_weighted    = -100,-100
#            mean_z_unweighted , mean_z_weighted     = -100,-100
#            sigma_z_unweighted, sigma_z_weighted    = -100,-100
#        #}
#        df_result = pd.DataFrame({'Nevts':len(ana)
#                                 ,'mean_x_unweighted':mean_x_unweighted   ,'mean_xErr_unweighted':sigma_x_unweighted/sqrtN ,'sigma_x_unweighted':sigma_x_unweighted,'sigma_xErr_unweighted':0.02 # resolution uncertainty
#                                 ,'mean_y_unweighted':mean_y_unweighted   ,'mean_yErr_unweighted':sigma_y_unweighted/sqrtN ,'sigma_y_unweighted':sigma_y_unweighted,'sigma_yErr_unweighted':0.02 # resolution uncertainty0
#                                 ,'mean_z_unweighted':mean_z_unweighted   ,'mean_zErr_unweighted':sigma_z_unweighted/sqrtN ,'sigma_z_unweighted':sigma_z_unweighted,'sigma_zErr_unweighted':0.02 # resolution uncertainty
##                                 ,'mean_x_weighted':mean_x_weighted   ,'mean_xErr_weighted':sigma_x_weighted/sqrtN ,'sigma_x_weighted':sigma_x_weighted,'sigma_xErr_weighted':0.02 # resolution uncertainty
##                                 ,'mean_y_weighted':mean_y_weighted   ,'mean_yErr_weighted':sigma_y_weighted/sqrtN ,'sigma_y_weighted':sigma_y_weighted,'sigma_yErr_weighted':0.02 # resolution uncertainty0
##                                 ,'mean_z_weighted':mean_z_weighted   ,'mean_zErr_weighted':sigma_z_weighted/sqrtN ,'sigma_z_weighted':sigma_z_weighted,'sigma_zErr_weighted':0.02 # resolution uncertainty
#                                 }
#                                 , index=[0])
    #}

    if DoSaveCanvas:#{
        canvas_unweighted.SaveAs(unweightedRoofitsFName)
        print_filename(unweightedRoofitsFName,"unweighted rooFits at")
#        canvas_weighted.SaveAs(weightedRoofitsFName)
#        print_filename(weightedRoofitsFName,"Mott-weighted rooFits at")
        print_line()
    #}

    if debug>2:#{
        print "in calc_cm_pars_sigma(fana)"
        print "filename:",str(fana.GetFileName())
        print "fana.GetTree().GetName():",fana.GetTree().GetName()
        print "fana.GetTree().GetEntries():",fana.GetTree().GetEntries()
        print "len(ana):",len(ana)
    #}

    print "calculated cm parameters for " + fana.InFileName
    if debug>1:#{
        print "reconstructed cm parameters"
        if debug>5: print 'df_result:',df_result
    #}
    garbage_list = [ ana ]
    del garbage_list
    return df_result
# ------------------------------------------------------------------------------- #



# ------------------------------------------------------------------------------- #
def set_frame( ax , title , xlabel , ylabel , legend_location="upper left" , ncol=1):

    plt.title( title ,fontsize=35)
    plt.xlabel( xlabel,fontsize=35)
    plt.ylabel( ylabel,fontsize=35)
    ax.tick_params(axis='both', which='major', labelsize=35)
    ax.legend(loc=legend_location,scatterpoints=1,fontsize=35,ncol=ncol)
# ------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------- #
def fit_par_plot( fig , i_subplot , data , var , weight , title , do_plot_fit_pars=True): # a sub-routine to fit a single parameter

    Pmiss = (data.pMiss_max + data.pMiss_min)/2.
    pMissUpErr , pMissLowErr = data.pMiss_max - Pmiss , Pmiss - data.pMiss_min
    ax = fig.add_subplot( i_subplot )
    ax.grid(True,linestyle='-',color='0.95')
    ax.set_xlim(0.3,1.0)
    [Xfit,XfitErr,Xchi2red] = plot_errorbar_and_fit( ax , Pmiss, data[ var + '_x_' + weight] , [np.zeros(len(pMissLowErr)),np.zeros(len(pMissLowErr))] , [data[ var + '_xErr_' + weight ],data[ var + '_xErr_' + weight ]], 'black','v','none',r'$x-direction$' ,'const',do_plot_fit_pars=do_plot_fit_pars)
    [Yfit,YfitErr,Ychi2red] = plot_errorbar_and_fit( ax , Pmiss, data[ var + '_y_' + weight] , [np.zeros(len(pMissLowErr)),np.zeros(len(pMissLowErr))] , [data[ var + '_yErr_' + weight ],data[ var + '_yErr_' + weight ]], 'red'  ,'o','none',r'$y-direction$' ,'const',do_plot_fit_pars=do_plot_fit_pars)
    [Za1,Za1err,Za2,Za2err,Zchi2red] = plot_errorbar_and_fit( ax , Pmiss, data[ var + '_z_' + weight] , [np.zeros(len(pMissLowErr)),np.zeros(len(pMissLowErr))] , data[ var + '_zErr_' + weight ], 'blue' ,'s','none',r'$\vec{p}_{miss}-direction$' ,'linear',do_plot_fit_pars=do_plot_fit_pars)
    #    set_frame( ax , r'%s $%s$'%(weight,title) , r'$p_{miss}$ [GeV/c]' , r'c.m. momentum $%s$ [Gev/c]'%title , "upper left",ncol=2)
    set_frame( ax , '' , r'$p_{miss}$ [GeV/c]' , r'c.m. momentum $%s$ [Gev/c]'%title , "upper left",ncol=1)
    return [Xfit , XfitErr , Yfit , YfitErr , Za1 , Za1err , Za2 , Za2err , Zchi2red , ax]
# ------------------------------------------------------------------------------- #

# ------------------------------------------------------------------------------- #
def fit_par_noplot( data , var , weight , title ): # a sub-routine to fit a single parameter; same as fit_par_plot without a plot
    # remove empty bins
    data = data[data['good_bin']==1]
    # fit x/y/z as a function of p(miss)
    Pmiss = (data.pMiss_max + data.pMiss_min)/2.
    pMissUpErr , pMissLowErr = data.pMiss_max - Pmiss , Pmiss - data.pMiss_min
    Xfit,XfitErr,Xchi2red = fit_as_a_function_of_pmiss( Pmiss, data[ var + '_x_' + weight] ,'const')
    Yfit,YfitErr,Ychi2red = fit_as_a_function_of_pmiss( Pmiss, data[ var + '_y_' + weight] ,'const')
    Za1,Za1err,Za2,Za2err,Zchi2red = fit_as_a_function_of_pmiss( Pmiss, data[ var + '_z_' + weight], data[ var + '_zErr_' + weight ],'linear')
    return [Xfit , XfitErr , Yfit , YfitErr, Za1 , Za1err , Za2 , Za2err , Zchi2red , None ]
# ------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------- #
def fit_cm_parameters( run , data , do_fits=True , FigureFName = '' , DoPlot = False ): # all parameters
    '''
        Return: df_fit_parameters
        '''
    if do_fits==False:#{
        print 'nothing in cm-paramteres input as data to fit_cm_parameters()'
        print 'leaving fit_cm_parameters by appending -100 to all'
        return pd.DataFrame({ 'run':run,'Nevents':-100
                            ,'SigmaX':-100,'SigmaXerr':0,'MeanX':-100, 'MeanXerr':0
                            ,'SigmaY':-100,'SigmaYerr':0,'MeanY':-100,'MeanYerr':0
                            ,'a1':-100,'a1err':0,'a2':-100,'a2err':0,'a_chi2red':-100
                            ,'b1':-100,'b1err':0,'b2':-100,'b2err':0,'b_chi2red':-100
                            }, index=[0] )
    #}
    if DoPlot: #{ # this means we want plots
        fig = plt.figure(figsize=(40,20)) # four plots, two unweighted and two weighted
    #}
    if DoPlot: #{
        width_fits = fit_par_plot ( fig, 221, data, 'sigma', 'unweighted', '\sigma' , do_plot_fit_pars=True )
        mean_fits = fit_par_plot( fig, 222, data, 'mean', 'unweighted', 'mean')
    #}
    else: #{
        width_fits = fit_par_noplot ( data,'sigma','unweighted','\sigma' )
        mean_fits = fit_par_noplot( data, 'mean','unweighted','mean')
    #}

    [SigmaX, SigmaXerr, SigmaY, SigmaYerr, a1, a1err, a2, a2err, a_chi2red, ax ] = width_fits
    [MeanX, MeanXerr, MeanY, MeanYerr, b1, b1err, b2, b2err, b_chi2red, ax ] = mean_fits

    df_fit_parameters = pd.DataFrame({ 'run':run,'Nevents':(np.sum(data['EvtsInBin']))
                                     ,'SigmaX':SigmaX,'SigmaXerr':SigmaXerr,'MeanX':MeanX, 'MeanXerr':MeanXerr
                                     ,'SigmaY':SigmaY,'SigmaYerr':SigmaYerr,'MeanY':MeanY,'MeanYerr':MeanYerr
                                     ,'a1':a1,'a1err':a1err,'a2':a2,'a2err':a2err,'a_chi2red':a_chi2red
                                     ,'b1':b1,'b1err':b1err,'b2':b2,'b2err':b2err,'b_chi2red':b_chi2red
                                     }, index=[0] )

    if DoPlot:#{
        plt.savefig(FigureFName)
        print_filename( FigureFName , "and plot can be found at" )
        print_line()
    #}
    if debug>1:#{
        print "computed fit parameters for run ",run
        print "completed fiting processes"
        if debug>4:
            print "df_fit_parameters: ",df_fit_parameters
    #}
    return df_fit_parameters
# ------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------- #
def fit_widths_z( cm_pars_list , colors , labels , FigureFName = '' ): # all parameters
    
    Pmiss = (cm_pars_list[0].pMiss_max + cm_pars_list[0].pMiss_min)/2.
    pMissUpErr , pMissLowErr = cm_pars_list[0].pMiss_max - Pmiss , Pmiss - cm_pars_list[0].pMiss_min
    fig , ax = plt.subplots(figsize=(20,10)) # four plots, two unweighted and two weighted
    for color, label , data in zip(colors,labels,cm_pars_list):
        if debug: print 'fiting width of z-direction for ',label
        plot_errorbar_and_fit( ax ,Pmiss,data[ 'sigma_z_unweighted'] ,
                             [pMissLowErr,pMissUpErr] ,
                             data[ 'sigma_zErr_unweighted'],
                             color=color ,marker='s',lstyle='none',
                             label=label ,fit_type='linear')
    set_frame( ax , r'c.m. $\sigma$ (unweighted by the cross-section)' ,
              r'$p_{miss}$ [GeV/c]' ,
              r'longitudinal c.m. momentum $\sigma$ [Gev/c]' , "upper left")
    ax.set_ylim(0.11,0.31)
    fig.tight_layout()
    plt.savefig(FigureFName)
    print_filename( FigureFName , "longitudinal widths plot at" )
# ------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------- #
def fit_means_z( cm_pars_list , colors , labels , FigureFName = '' ): # all parameters
    
    Pmiss = (cm_pars_list[0].pMiss_max + cm_pars_list[0].pMiss_min)/2.
    pMissUpErr , pMissLowErr = cm_pars_list[0].pMiss_max - Pmiss , Pmiss - cm_pars_list[0].pMiss_min
    fig , ax = plt.subplots(figsize=(20,10)) # four plots, two unweighted and two weighted
    for color, label , data in zip(colors,labels,cm_pars_list):
        plot_errorbar_and_fit( ax ,Pmiss,data[ 'mean_z_unweighted'] ,
                              [pMissLowErr,pMissUpErr] ,
                              data[ 'mean_zErr_unweighted'],
                              color=color ,marker='s',lstyle='none',
                              label=label ,fit_type='linear')
    set_frame( ax , r'c.m. $mean$ (unweighted by the cross-section)' ,
              r'$p_{miss}$ [GeV/c]' ,
              r'longitudinal c.m. momentum $mean$ [Gev/c]' , "upper left")
    ax.set_ylim(0,0.5)
    fig.tight_layout()
    plt.savefig(FigureFName)
    print_filename( FigureFName , "longitudinal widths plot at" )
# ------------------------------------------------------------------------------- #



# ------------------------------------------------------------------------------- #
def get_pmiss_bins( path , NRand ): # for pp/p analysis

    # define the bins - 4 bins in each large p(miss) bin that we have in the analysis
    twenty_pmiss_bins = []

    for i in range(len(PmissBins)):#{
        pmin , pmax = PmissBins[i][0] , PmissBins[i][1]
        for j in range(4):#{
            twenty_pmiss_bins.append( [ pmin + float(j*(pmax-pmin))/4 , pmin + float((j+1)*(pmax-pmin))/4 ])
        #}
    #}

    # get the number of generated events per bin
    evtsgen_pmiss_bins = []
    evtsgen_Q2pmiss_bins = np.zeros( (len(twenty_pmiss_bins) , len(Q2Bins)) )
    evtsgen_thetapmqpmiss_bins = np.zeros( (len(twenty_pmiss_bins) , len(thetapmqBins)) )

    p1 = TPlots(path + '/DATA/SRC_e1p_C_GoodRuns_coulomb.root' , 'T')
    p2 = TPlots(path + '/DATA/SRC_e2p_C_GoodRuns_coulomb.root' , 'T')

    for i in range( len(twenty_pmiss_bins) ):
        pmin , pmax = twenty_pmiss_bins[i][0] , twenty_pmiss_bins[i][1]
        p_cut = ROOT.TCut("%f<Pmiss_size && Pmiss_size<%f"%(pmin , pmax))
        evtsgen_pmiss_bins.append( NRand * (p1.GetEntries(p_cut) + p2.GetEntries(p_cut)) )
        
        for j in range( len(Q2Bins) ):
            Q2min , Q2max = Q2Bins[j][0] , Q2Bins[j][1]
            q2_cut = ROOT.TCut("%f<Q2 && Q2<%f"%(Q2min , Q2max))
            evtsgen_Q2pmiss_bins[i][j] = NRand * (p1.GetEntries(p_cut+q2_cut) + p2.GetEntries(p_cut+q2_cut))
    
        for j in range( len(thetapmqBins) ):
            thetapmqmin , thetapmqmax = thetapmqBins[j][0] , thetapmqBins[j][1]
            thetapmq_cut = ROOT.TCut("%f<Pmiss_q_angle && Pmiss_q_angle<%f"%(thetapmqmin , thetapmqmax))
            evtsgen_thetapmqpmiss_bins[i][j] = NRand * (p1.GetEntries(p_cut+thetapmq_cut) + p2.GetEntries(p_cut+thetapmq_cut))

    p1.Close()
    p2.Close()

    return pmiss_bins , evtsgen_pmiss_bins , evtsgen_Q2pmiss_bins , evtsgen_thetapmqpmiss_bins
# ------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------- #
def get_loss_pmiss_bins( pmiss_bins , evtsgen_pmiss_bins , Q2Bins , evtsgen_Q2pmiss_bins, thetapmqBins , evtsgen_thetapmqpmiss_bins , ana_sim ):
    # in p(miss) bins
    loss_pmiss_bins = []
    # in Q2 bins and p(miss) bins
    accepted_Q2pmiss_bins = np.zeros( (len(pmiss_bins) , len(Q2Bins) ))
    loss_Q2pmiss_bins = np.zeros( (len(pmiss_bins) , len(Q2Bins) ))
    # in theta(pm,q) bins and p(miss) bins
    accepted_thetapmqpmiss_bins = np.zeros( (len(pmiss_bins) , len(thetapmqBins) ))
    loss_thetapmqpmiss_bins = np.zeros( (len(pmiss_bins) , len(thetapmqBins) ))
    
    for i in range( len(pmiss_bins) ):
        pmin , pmax = pmiss_bins[i][0] , pmiss_bins[i][1]
        evts_gen = evtsgen_pmiss_bins[i]
        p_cut = ROOT.TCut("%f<Pmiss3Mag && Pmiss3Mag<%f"%(pmin , pmax))
        evts_acc = ana_sim.GetEntries(p_cut)
        loss_pmiss_bins.append( float(evts_gen-evts_acc)/evts_gen )
        
        # in Q2 bins
        for j in range( len(Q2Bins) ):
            Q2min , Q2max = Q2Bins[j][0] , Q2Bins[j][1]
            q2_cut = ROOT.TCut("%f<Q2 && Q2<%f"%(Q2min , Q2max))
            accepted_Q2pmiss_bins[i][j] = ana_sim.GetEntries( p_cut + q2_cut )
            if evtsgen_Q2pmiss_bins[i][j]>0:
                loss_Q2pmiss_bins[i][j] = float(evtsgen_Q2pmiss_bins[i][j] - accepted_Q2pmiss_bins[i][j])/evtsgen_Q2pmiss_bins[i][j]
            else:
                loss_Q2pmiss_bins[i][j] = 0.0
    
        # in theta(pm,q) bins
        for j in range( len(Q2Bins) ):
            thetapmqmin , thetapmqmax = thetapmqBins[j][0] , thetapmqBins[j][1]
            thetapmq_cut = ROOT.TCut("%f< TMath::RadToDeg()*theta_miss_q && TMath::RadToDeg()*theta_miss_q<%f"%(thetapmqmin , thetapmqmax))
            accepted_thetapmqpmiss_bins[i][j] = ana_sim.GetEntries( p_cut + thetapmq_cut )
            if evtsgen_thetapmqpmiss_bins[i][j]>0:
                loss_thetapmqpmiss_bins[i][j] = float(evtsgen_thetapmqpmiss_bins[i][j] - accepted_thetapmqpmiss_bins[i][j])/evtsgen_thetapmqpmiss_bins[i][j]
            else:
                loss_thetapmqpmiss_bins[i][j] = 0.0

    return loss_pmiss_bins , loss_Q2pmiss_bins , loss_thetapmqpmiss_bins
# ------------------------------------------------------------------------------- #

# ------------------------------------------------------------------------------- #
def get_Pval_scores( data_fits , reco_fits , name='' ):
    # XX delete by April 30
    # No Mott/FF - weighting (un - weighted roofit results)
    Pval_array = compute_Pval_parameters( data_fits , reco_fits , 'unweighted' )
    
    [PvalSigmaX_unweighted, PvalSigmaY_unweighted ,
     PvalMeanZa1_unweighted , PvalMeanZa2_unweighted ,
     PvalSigmaZa1_unweighted , PvalSigmaZa2_unweighted ] = Pval_array
     
    PvalTotal_unweighted = Fisher_combination_Pvals( Pval_array )
    PvalTotal_largePvals = FisherCombinationLargePvals( Pval_array )
    PvalTotal_allPvals   = FisherMethodPvals( Pval_array )

    if debug>2: print "got unweighted P(value) results, PvalTotal_unweighted=%g, PvalTotal_largePvals=%g, PvalTotal_allPvals=%g"%(PvalTotal_unweighted,PvalTotal_largePvals,PvalTotal_allPvals)
 
    # With Mott/FF - weighting (un - weighted roofit results)
    Pval_array = compute_Pval_parameters( data_fits , reco_fits , 'weighted' )
    
    [PvalSigmaX_weighted, PvalSigmaY_weighted ,
     PvalMeanZa1_weighted , PvalMeanZa2_weighted ,
     PvalSigmaZa1_weighted , PvalSigmaZa2_weighted ] = Pval_array

    PvalTotal_weighted = Fisher_combination_Pvals( Pval_array )
    
    if debug>2: print "got weighted P(value) results, PvalTotal_weighted=%g"%PvalTotal_weighted

    # tweeking the uncertainty in the a1 and a2 of \sigma_Z
    Pval_array = compute_Pval_parameters( data_fits , reco_fits , 'unweighted' , tweeked=True)
    
    [PvalSigmaX_tw, PvalSigmaY_tw ,
     PvalMeanZa1_tw , PvalMeanZa2_tw ,
     PvalSigmaZa1_tw , PvalSigmaZa2_tw ] = Pval_array
    PvalTotal_tw = Fisher_combination_Pvals( Pval_array )
         
    if debug>2: print "got tweeked P(value) results, PvalTotal_tw=%g"%PvalTotal_tw

    PvalSigmaZa1SigmaZa2= Fisher_combination_Pvals( [ PvalSigmaZa1_unweighted , PvalSigmaZa2_unweighted ] )
    PvalMeanZa1MeanZa2  = Fisher_combination_Pvals( [ PvalMeanZa1_unweighted , PvalMeanZa2_unweighted ] )
    PvalSigmaZa1MeanZa1 = Fisher_combination_Pvals( [ PvalSigmaZa1_unweighted , PvalMeanZa1_unweighted ] )
    PvalSigmaZa1MeanZa2 = Fisher_combination_Pvals( [ PvalSigmaZa1_unweighted , PvalMeanZa2_unweighted ] )
    PvalSigmaZa2MeanZa1 = Fisher_combination_Pvals( [ PvalSigmaZa2_unweighted , PvalMeanZa1_unweighted ] )
    PvalSigmaZa2MeanZa2 = Fisher_combination_Pvals( [ PvalSigmaZa2_unweighted , PvalMeanZa2_unweighted ] )
    PvalSigmaTSigmaZa1  = Fisher_combination_Pvals( [ PvalSigmaX_unweighted, PvalSigmaY_unweighted, PvalSigmaZa1_unweighted ] )
    PvalSigmaTSigmaZa2  = Fisher_combination_Pvals( [ PvalSigmaX_unweighted, PvalSigmaY_unweighted, PvalSigmaZa2_unweighted ] )
    PvalSigmaTMeanZa1   = Fisher_combination_Pvals( [ PvalSigmaX_unweighted, PvalSigmaY_unweighted, PvalMeanZa1_unweighted ] )
    PvalSigmaTMeanZa2   = Fisher_combination_Pvals( [ PvalSigmaX_unweighted, PvalSigmaY_unweighted, PvalMeanZa2_unweighted ] )
    

    Pval_scores = pd.DataFrame({'PvalSigmaX_unweighted':PvalSigmaX_unweighted,
                               'PvalSigmaY_unweighted':PvalSigmaY_unweighted ,
                               'PvalMeanZa1_unweighted':PvalMeanZa1_unweighted ,
                               'PvalMeanZa2_unweighted':PvalMeanZa2_unweighted ,
                               'PvalSigmaZa1_unweighted':PvalSigmaZa1_unweighted ,
                               'PvalSigmaZa2_unweighted':PvalSigmaZa2_unweighted,
                               'PvalTotal_unweighted':PvalTotal_unweighted,
                               'PvalSigmaX_weighted':PvalSigmaX_weighted,
                               'PvalSigmaY_weighted':PvalSigmaY_weighted ,
                               'PvalMeanZa1_weighted':PvalMeanZa1_weighted ,
                               'PvalMeanZa2_weighted':PvalMeanZa2_weighted ,
                               'PvalSigmaZa1_weighted':PvalSigmaZa1_weighted ,
                               'PvalSigmaZa2_weighted':PvalSigmaZa2_weighted,
                               'PvalTotal_weighted':PvalTotal_weighted,
                               'PvalSigmaZa1SigmaZa2':PvalSigmaZa1SigmaZa2,
                               'PvalMeanZa1MeanZa2':PvalMeanZa1MeanZa2,
                               'PvalSigmaZa1MeanZa1':PvalSigmaZa1MeanZa1,
                               'PvalSigmaZa1MeanZa2':PvalSigmaZa1MeanZa2,
                               'PvalSigmaZa2MeanZa1':PvalSigmaZa2MeanZa1,
                               'PvalSigmaZa2MeanZa2':PvalSigmaZa2MeanZa2,
                               'PvalSigmaTSigmaZa1':PvalSigmaTSigmaZa1,
                               'PvalSigmaTSigmaZa2':PvalSigmaTSigmaZa2,
                               'PvalSigmaTMeanZa1':PvalSigmaTMeanZa1,
                               'PvalSigmaTMeanZa2':PvalSigmaTMeanZa2,
                               'PvalSigmaX_tw':PvalSigmaX_tw,
                               'PvalSigmaY_tw':PvalSigmaY_tw ,
                               'PvalMeanZa1_tw':PvalMeanZa1_tw ,
                               'PvalMeanZa2_tw':PvalMeanZa2_tw ,
                               'PvalSigmaZa1_tw':PvalSigmaZa1_tw ,
                               'PvalSigmaZa2_tw':PvalSigmaZa2_tw,
                               'PvalTotal_largePvals':PvalTotal_largePvals,
                               'PvalTotal_allPvals':PvalTotal_allPvals,
                               'PvalTotal_tw':PvalTotal_tw,
                               },index=[0])
    
    if debug>1:
        print "got Pval scores " + name

    return Pval_scores
# ------------------------------------------------------------------------------- #



# ------------------------------------------------------------------------------- #
def stream_dataframe_to_root( df , filename , treename='tree' ):
    # if file does not exist create it
    if not os.path.isfile(filename):
        df.to_root(filename, key=treename )
    else: # else just update it
        df.to_root(filename, key=treename , mode='a')
# ------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------- #
def a1a2_create_negative_sigma_z( a1 , a2 ):
    '''
    check if a1 and a2 give \sigma_z < 0,
    since we do not want to use those (unreasonable) values.
    we check for the minimal Pmiss (0.3) and the maximal Pmiss (1.0)
    '''
    if a1*(0.3 - 0.6) + a2 < 0: return True
    if a1*(1.0 - 0.6) + a2 < 0: return True
    return False
# ------------------------------------------------------------------------------- #

# ------------------------------------------------------------------------------- #
def generate_runs_with_random_parameters( option='', hyperparameters=None,
                                         ana_data=dict(),
                                         debug=0 ,
                                         buildup_resultsFName='' ,
                                         reco_fitsFName='', root_resutlsFName='' ,
                                         do_root_file=False, do_reco_fits_file=False, do_resutls_file=True, do_add_plots=False,
                                         ):#{
        
    from definitions import path
    if debug: print hyperparameters
    start_run , Nruns = hyperparameters['start_run'], hyperparameters['Nruns']
    NRand = hyperparameters['NRand']
    
    pAcceptacneFile = ROOT.TFile( path + "/GSIM_DATA/PrecoilAcceptance.root" )
    path = path + "/Analysis_DATA/ppSRCcm"
    if 'helion' in flags.worker: path = "/extra/Erez/DataMining/Analysis_DATA/ppSRCcm"

#    # multiple bins for pp/p ratio
#    twenty_pmiss_bins , evtsgen_pmiss_bins , evtsgen_Q2pmiss_bins  , evtsgen_thetapmqpmiss_bins = get_pmiss_bins( path , int(hyperparameters['NRand']) )

    '''
    recoil proton acceptances:
    (a) efficiency and acceptacne from the 'uniform' map i've generated using virtual CLAS
    (b) proton fiducial cuts (coded inside the event generator class)
    '''
    if 'gen' in option: #{
        h = pAcceptacneFile.Get("hRescaled")
        gen_events = GenerateEvents( path , 0 , debug - 2 )
        gen_events.Set_protonAcceptacne( h )

        gen_events.AddInputChain_eep("Or' coulomb trees")
        gen_events.SetInputChain_eep()

        gen_events.SetNRand( NRand )
        gen_events.Use_protonAcceptacne( hyperparameters['do proton acceptance'] )
        gen_events.SetDo_PrecMinCut ( hyperparameters['do p(rec)>0.35 cut'] )
        gen_events.SetDo_PrecFiducial ( hyperparameters['do p(rec) FV cuts'] ) # in the data we do not apply FV for p(recoil)
        gen_events.Use_PrecResolution ( hyperparameters['do p(rec) resolution smearing'] , hyperparameters['p(rec) resolution smearing'] )

        gen_events.SetPmissBins()
        gen_events.Set10PmissBins()
        gen_events.Set4Q2Bins()
        gen_events.Set4theta_Pm_qBins()
    
        # set the desired number of events when the simulation ends in 5 Pmiss bins
        # as a 100 times the number of 12C (e,e'pp) events in each bin
        Ntimes = hyperparameters['Ntimes']
        gen_events.SetNeventsPerPmissBin( 71*Ntimes , 143*Ntimes , 132*Ntimes , 96*Ntimes , 56*Ntimes )
        # if we don't reach these numbers after generating NMAX events, the parameters should be discarded
        # by Pval = 0, which can be obtained by killing the run and flaggind it as a bad run
        gen_events.SetNgenMax( hyperparameters['NgenMax'] )
        gen_events.MapInputEntriesInPmissBins()
    #}

    # event generation (and analysis) loop
    irun=0
    for run in range( start_run , start_run + Nruns ): #{

        # (1) generate the simulated data (the 'run')
        # ----------------------------
        if 'gen' in option: #{
            
            # sample the geneated parameters uniformly within the ranges
            gen_MeanX = -0.02
            gen_MeanY = 0.0
            gen_SigmaX = gen_SigmaY = np.random.uniform( np.min(hyperparameters['range_sigma_t']),np.max(hyperparameters['range_sigma_t']) )
            gen_a1  = np.random.uniform( np.min(hyperparameters['range_a1']),np.max(hyperparameters['range_a1']) )
            gen_a2  = np.random.uniform( np.min(hyperparameters['range_a2']),np.max(hyperparameters['range_a2']) )
            gen_b1  = np.random.uniform( np.min(hyperparameters['range_b1']),np.max(hyperparameters['range_b1']) )
            gen_b2  = np.random.uniform( np.min(hyperparameters['range_b2']),np.max(hyperparameters['range_b2']) )

            
            if debug: print 'run',run,'gen_SigmaX',gen_SigmaX,'gen_a1',gen_a1,'gen_a2',gen_a2,'gen_b1',gen_b1,'gen_b2',gen_b2
            if a1a2_create_negative_sigma_z( gen_a1 , gen_a2 ):
                if debug: print 'a1 (%.2f) and a2(%.2f) create together a negative sigma_z, killing run %d'%( gen_a1 , gen_a2 , run );print_line()
                continue
 
            gen_events.Set_eep_Parameters( gen_MeanX , gen_SigmaX , gen_MeanY , gen_SigmaY , gen_b1 , gen_b2 , gen_a1 , gen_a2 )
            gen_events.InitRun()
            Nevents = gen_events.DoGenerate_eepp_from_eep( run )
            Nattempts = gen_events.GetNattempts()
            if debug: print 'Nevents to analyze:',Nevents
        #}
        else: #{ for debugging...
            Nevents=Nattempts=1
            gen_MeanX = gen_MeanY = gen_SigmaX = gen_SigmaY = 0.
            gen_a1  = gen_a2  = gen_b1  = gen_b2  = 0.
        #}


        # (2) analyze the simulated data (the 'run') similarly to the data - reconstructed parameters
        # ----------------------------
        if 'ana' in option and Nevents!=-1: #{
            if debug>1: print "analyzing run %d"%run
            
            ana_sim = TAnalysisEG2( path + '/eg_rootfiles', 'run%d'%run )
            results = pd.DataFrame({'run':int(run)
                                   ,'time':str(datetime.datetime.now().strftime("%Y%B%d"))
                                   ,'NentriesSimRun':ana_sim.GetEntries(), 'Nattempts':Nattempts
                                   ,'gen_MeanX':gen_MeanX, 'gen_SigmaX':gen_SigmaX, 'gen_MeanY':gen_MeanY, 'gen_SigmaY':gen_SigmaY
                                   ,'gen_a1':gen_a1, 'gen_a2':gen_a2, 'gen_b1':gen_b1, 'gen_b2':gen_b2
                                   }, index = [int(run)])
                                
            # N(attempts) is used as an indicator using a binomial test of number of successes
            binom_test_Pval = []
            for i,p in enumerate(p_binom_array):#{
                binom_test_Pval.append(binom_test( x=Nevents/100 ,n=Nattempts/100 , p=p )) # divide by a factor of 100 to soften the Pvalue distribution
                results['Pval_binom_%.2f_test_Nsucsseses'%p] = binom_test_Pval[i]
            #}
                
#            loss_pmiss_bins , loss_Q2pmiss_bins , loss_thetapmqpmiss_bins = get_loss_pmiss_bins( twenty_pmiss_bins, evtsgen_pmiss_bins ,
#                                                                                                Q2Bins , evtsgen_Q2pmiss_bins ,
#                                                                                                thetapmqBins, evtsgen_thetapmqpmiss_bins ,
#                                                                                                ana_sim )

            # from now on we work in 4 targets - since each has its own Pmiss binning
            for target in targets: #{
            # reconstruct c.m. parameters and fit
                reco_parameters, do_fits = calc_cm_parameters( ana_sim  , PmissBinsPerTarget[target] )
                reco_fits = fit_cm_parameters( run , reco_parameters , do_fits=do_fits )
                ks_pval_scores = calc_pval_ks_scores( ana_sim , ana_data , do_plots=hyperparameters['do_ks_plots'] , run=run , Nattempts=Nattempts , target=target)

                for fit_parameter in ['MeanX','SigmaX','MeanY','SigmaY','a1','a2','b1','b2']: #{
                    results['rec'+fit_parameter+'_'+target] = float(reco_fits[fit_parameter])
                #}
                results['NLostEvents'] = (9907*float(NRand) - ana_sim.GetEntries())
                results['fracLostEvents'] = (float((9907.0*float(NRand)) - ana_sim.GetEntries())/(9907.0*float(NRand)))
                results['parameters_reconstructed_well'] = True if do_fits else False
                
                # reconstructed parameters in N p(miss) bins
                for i in range(len(PmissBinsPerTarget[target])):#{
                    pmin , pmax = PmissBinsPerTarget[target][i][0] , PmissBinsPerTarget[target][i][1]
                    results['EvtsInBin'+'_bin%d'%i] = reco_parameters.get_value(i,'EvtsInBin')
                    for parname in ['mean','sigma']: #{
                        for direction in ['x','y','z']: #{
                        
                            parnamedir = parname + '_' + direction
                            recparnamedir = 'rec'+parnamedir+'_bin%d'%i
                            results[recparnamedir] = float(reco_parameters.get_value(i,parnamedir+'_unweighted')) if do_fits else -100
                            parnamedirErr = parnamedir+'Err'
                            recparnamedirErr = 'rec'+parnamedirErr+'_bin%d'%i
                            results[recparnamedirErr] = float(reco_parameters.get_value(i,parnamedirErr+'_unweighted')) if do_fits else -100
                        #}
                    #}
                #}
                # KS Pvalues
                for bin in range(len(PmissBinsPerTarget[target])):#{
                    results['ks_local_Pval_'+'pcmZ_bin%d'%bin+'_'+target] = ks_pval_scores['pcmZ_bin%d'%bin]
                #}
                for direction in ['X','Y']: #{
                    results['ks_local_Pval_'+'pcm'+direction+'_'+target] = ks_pval_scores['pcm'+direction]
                #}
                results['ks_Pval_pcmX_pcmY'+'_'+target] = ks_pval_scores['Pval_pcmX_pcmY']


                # --- global Pval from combination of all scores together --- #
                results['ks_PvalTotal'+'_'+target] = ks_pval_scores['PvalTotal'] # with a cutoff on 1e-20
                
                for method in PvalZ_calculation_methods: #{
                    results['ks_local_Pval_'+'pcmZ_'+method+'_'+target] = ks_pval_scores['pcmZ_'+method]
                    results['ks_Pval_pcmX_pcmY_pcmZ_'+method+'_'+target] = ks_pval_scores['Pval_pcmX_pcmY_pcmZ_'+method]
                    results['ks_Pval_pcmX_pcmY_pcmZ_scaled_1e20_'+method+'_'+target] = ks_pval_scores['Pval_pcmX_pcmY_pcmZ_scaled_1e20_'+method]
                    results['ks_Pval_Powered_pcmX_Powered_pcmY_pcmZ_'+method+'_'+target] = ks_pval_scores['Pval_Powered_pcmX_Powered_pcmY_pcmZ_'+method]
                    
                    

                    for i,p in enumerate(p_binom_array):#{

                        results['Pval_pcmXYZ_'+method+'_binom_%.2f_'%p+target] = Fisher_combination_Pvals( [ binom_test_Pval[i] , ks_pval_scores['Pval_pcmX_pcmY_pcmZ_'+method ] ] )
                        results['PvalTotal_'+method+'_binom_%.2f_'%p+target] = Fisher_combination_Pvals( [ binom_test_Pval[i] , ks_pval_scores['PvalTotal' ] ] )
                        results['Pval_Powered_pcmXY_pcmZ_'+method+'_binom_%.2f_'%p+target] = Fisher_combination_Pvals( [ binom_test_Pval[i] , ks_pval_scores['Pval_Powered_pcmX_Powered_pcmY_pcmZ_'+method ] ] )
                    #}
                #}
            #}
        
        
            # events loss in 10 p(miss) bins, for pp/p analysis
            # -- - -- -- -- - -- - -- - - -- - -- -- -- -- -- - -- -
            for i in range( len(small10PmissBins) ):#{
                pmin , pmax = small10PmissBins[i][0] , small10PmissBins[i][1]
                fracAcc_pmiss_bin = float( gen_events.NAcc10PmissBins[i] )/gen_events.NGen10PmissBins[i]
                results['fracAcc_pmiss_%.3f_%.3f'%(pmin , pmax)] = fracAcc_pmiss_bin
                fracLoss_pmiss_bin = float( gen_events.NLoss10PmissBins[i] )/gen_events.NGen10PmissBins[i]
                results['fracLoss_pmiss_%.3f_%.3f'%(pmin , pmax)] = fracLoss_pmiss_bin
                
                # Q2 and p(miss) bins
                for j in range( len(Q2Bins) ):#{
                    Q2min , Q2max = Q2Bins[j][0] , Q2Bins[j][1]
                    if gen_events.GetNGen10PmissBins_4Q2Bins(i,j):#{
                        fracAcc_pmiss_Q2_bin = float( gen_events.GetNAcc10PmissBins_4Q2Bins(i,j) )/gen_events.GetNGen10PmissBins_4Q2Bins(i,j)
                        fracLoss_pmiss_Q2_bin = float( gen_events.GetNLoss10PmissBins_4Q2Bins(i,j))/gen_events.GetNGen10PmissBins_4Q2Bins(i,j)
                    else: #{
                        fracAcc_pmiss_Q2_bin = 1
                        fracLoss_pmiss_Q2_bin = 0
                    #}
                    results['fracAcc_pmiss_%.3f_%.3f_Q2_%.1f_%.1f'%(pmin , pmax , Q2min , Q2max)] = fracAcc_pmiss_Q2_bin
                    results['fracLoss_pmiss_%.3f_%.3f_Q2_%.1f_%.1f'%(pmin , pmax , Q2min , Q2max)] = fracLoss_pmiss_Q2_bin
                #}

                # theta(pm,q) and p(miss) bins
                for j in range( len(theta_Pm_qBins) ):#{
                    theta_Pm_q_min , theta_Pm_q_max = theta_Pm_qBins[j][0] , theta_Pm_qBins[j][1]
                    if gen_events.GetNGen10PmissBins_4theta_Pm_qBins(i,j):#{
                        fracAcc_pmiss_theta_Pm_q_bin = float( gen_events.GetNAcc10PmissBins_4theta_Pm_qBins(i,j) )/gen_events.GetNGen10PmissBins_4theta_Pm_qBins(i,j)
                        fracLoss_pmiss_theta_Pm_q_bin = float( gen_events.GetNLoss10PmissBins_4theta_Pm_qBins(i,j) )/gen_events.GetNGen10PmissBins_4theta_Pm_qBins(i,j)
                    #}
                    else: #{
                        fracAcc_pmiss_theta_Pm_q_bin = 1
                        fracLoss_pmiss_theta_Pm_q_bin = 0
                    #}
                    results['fracAcc_pmiss_%.3f_%.3f_theta_Pm_q_%.1f_%.1f'%(pmin , pmax , theta_Pm_q_min , theta_Pm_q_max)] = fracAcc_pmiss_theta_Pm_q_bin
                    results['fracLoss_pmiss_%.3f_%.3f_theta_Pm_q_%.1f_%.1f'%(pmin , pmax , theta_Pm_q_min , theta_Pm_q_max)] = fracLoss_pmiss_theta_Pm_q_bin
                #}
            #}
            if do_reco_fits_file:   stream_dataframe_to_file( reco_fits, reco_fitsFName  )
            if do_resutls_file:     stream_dataframe_to_file( results, buildup_resultsFName , float_format='%f' )
            if do_root_file:        stream_dataframe_to_root( results, root_resutlsFName, 'ppSRCsimanaTree')
            ana_sim.CloseFile()
        #}
        if 'delete' in option:#{
            delete_file( path + '/eg_rootfiles/run%d.root'%run  , debug )
        #}
        irun += 1
        print_important("completed run %d [%.0f"%(run,100.*float(irun)/Nruns) + "%]"+" at %4d-%02d-%02d %d:%d:%d"%time.localtime()[0:6] )
        print_line()
    #}


    if 'gen' in option: #{
            gen_events.ReleaseInputChain_eep()
    #}

    if 'ana' in option:#{
        if do_reco_fits_file:   print_filename( reco_fitsFName , "reconstructed parameters fits wrote to" )
        if do_resutls_file:     print_filename( buildup_resultsFName , "results wrote to " )
        if do_root_file:        print_filename( root_resutlsFName , "results converted also to root format " )
    #}

    print_important("done...") ; print_line()
#}
# ------------------------------------------------------------------------------- #





# ------------------------------------------------------------------------------- #
# May-27, 2017
def generate_runs_with_random_sigma( option='generate analyze delete',
                                    hyperparameters=None,
                                    debug=0,
                                    buildup_resultsFName='' ,
                                    reco_fitsFName='',
                                    do_results_file=True
                                    ):#{
    
    from definitions import path
    if debug: print hyperparameters
    start_run , Nruns = hyperparameters['start_run'], hyperparameters['Nruns']
    NRand = hyperparameters['NRand']
    
    pAcceptacneFile = ROOT.TFile( path + "/GSIM_DATA/PrecoilAcceptance.root" )
    path = path + "/Analysis_DATA/ppSRCcm"
    if 'helion' in flags.worker: path = "/extra/Erez/DataMining/Analysis_DATA/ppSRCcm"
    
    '''
        recoil proton acceptances:
        (a) efficiency and acceptacne from the 'uniform' map i've generated using virtual CLAS
        (b) proton fiducial cuts (coded inside the event generator class)
        '''
    if 'gen' in option: #{
        h = pAcceptacneFile.Get("hRescaled")
        gen_events = GenerateEvents( path , 0 , debug - 2 )
        gen_events.Set_protonAcceptacne( h )
        
        gen_events.AddInputChain_eep("300<p(miss)<600 MeV/c",hyperparameters['my target name'])
        gen_events.SetInputChain_eep()
        
        gen_events.SetNRand( NRand )
        gen_events.Use_protonAcceptacne( hyperparameters['do proton acceptance'] )
        gen_events.SetDo_PrecMinCut ( hyperparameters['do p(rec)>0.35 cut'] )
        gen_events.SetDo_PrecFiducial ( hyperparameters['do p(rec) FV cuts'] ) # in the data we do not apply FV for p(recoil)
        gen_events.Use_PrecResolution ( hyperparameters['do p(rec) resolution smearing'] , hyperparameters['p(rec) resolution smearing'] )
        gen_events.SetDoRandomEntry( hyperparameters['do random entry'] )
        
        gen_events.SetPmissBins()
        gen_events.Set10PmissBins()
        # set the desired number of events when the simulation ends in 5 Pmiss bins
        # as a 100 times the number of 12C (e,e'pp) events in each bin
        gen_events.SetNAcceptedEvents( hyperparameters['N(accepted-events)'] )
        # if we don't reach these numbers after generating NMAX events, the parameters should be discarded
        gen_events.SetNgenMax( hyperparameters['NgenMax'] )
    #}
    
    # event generation (and analysis) loop
    irun=0
    for run in range( start_run , start_run + Nruns ): #{
        
        # (1) generate the simulated data (the 'run')
        # ----------------------------
        if 'gen' in option: #{
            
            # set a new seed
            fseed = int(np.random.uniform(1,100000))
            gen_events.gRandom.SetSeed( fseed )

            # sample the geneated parameters uniformly within the ranges
            gen_MeanX = hyperparameters['generated mean(x)']
            gen_MeanY = hyperparameters['generated mean(y)']
            gen_Sigma_t = np.random.uniform( np.min(hyperparameters['range_sigma_t']),np.max(hyperparameters['range_sigma_t']) )
            
            if hyperparameters['generation method']=='N(uncertainties) band around measured values': #{
                gen_MeanZ = np.random.normal( hyperparameters['measured mean(z)'] , hyperparameters['N(uncertainties) in generation'] * hyperparameters['measured mean(z) err'] )
                gen_SigmaZ = np.random.normal( hyperparameters['measured sigma(z)'] , hyperparameters['N(uncertainties) in generation'] * hyperparameters['measured sigma(z) err'] )
            
                if debug: print 'run',run,'gen_Sigma_t',gen_Sigma_t,'gen_MeanZ',gen_MeanZ,'gen_SigmaZ',gen_SigmaZ
                gen_events.Set_eep_Parameters_MeanXYZ_Sigma( gen_MeanX , gen_MeanY , gen_MeanZ , gen_Sigma_t , gen_SigmaZ )
                rootfilename_suffix = "_"+hyperparameters['my target name']+"_SigmaT%.3f_SigmaZ%.3f_MeanZ%.3f"%(gen_Sigma_t,gen_SigmaZ,gen_MeanZ)
            #}
            elif hyperparameters['generation method']=='const mean(z), N(uncertainties) band around measured sigma(z)':#{
                gen_MeanZ = hyperparameters['const mean(z)']
                gen_SigmaZ = np.random.normal( hyperparameters['measured sigma(z)'] , hyperparameters['N(uncertainties) in generation'] * hyperparameters['measured sigma(z) err'] )
                if debug: print 'run',run,'gen_Sigma_t',gen_Sigma_t,'gen_MeanZ',gen_MeanZ,'gen_SigmaZ',gen_SigmaZ
                gen_events.Set_eep_Parameters_MeanXYZ_Sigma( gen_MeanX , gen_MeanY , gen_MeanZ , gen_Sigma_t , gen_SigmaZ )
                rootfilename_suffix = "_"+hyperparameters['my target name']+"_SigmaT%.3f_SigmaZ%.3f_MeanZ%.3f"%(gen_Sigma_t,gen_SigmaZ,gen_MeanZ)
            #}
            elif hyperparameters['generation method']=='max mean(z), N(uncertainties) band around measured sigma(z)':#{
                gen_MeanZ_max = hyperparameters['max mean(z)']
                gen_MeanZ = np.random.normal( hyperparameters['measured mean(z)'] , hyperparameters['N(uncertainties) in generation'] * hyperparameters['measured mean(z) err'] )
                # if the generated mean(z) is larger than the maximal allowed value, generated again...
                while gen_MeanZ > gen_MeanZ_max:#{
                    gen_MeanZ = np.random.normal( hyperparameters['measured mean(z)'] , hyperparameters['N(uncertainties) in generation'] * hyperparameters['measured mean(z) err'] )
                #}
                gen_SigmaZ = np.random.normal( hyperparameters['measured sigma(z)'] , hyperparameters['N(uncertainties) in generation'] * hyperparameters['measured sigma(z) err'] )
                if debug: print 'run',run,'gen_Sigma_t',gen_Sigma_t,'gen_MeanZ',gen_MeanZ,'gen_SigmaZ',gen_SigmaZ
                gen_events.Set_eep_Parameters_MeanXYZ_Sigma( gen_MeanX , gen_MeanY , gen_MeanZ , gen_Sigma_t , gen_SigmaZ )
                rootfilename_suffix = "_"+hyperparameters['my target name']+"_SigmaT%.3f_SigmaZ%.3f_MeanZ%.3f"%(gen_Sigma_t,gen_SigmaZ,gen_MeanZ)
            #}

            elif hyperparameters['generation method']=='unifrom N(uncertainties) band around measured': #{
                mean_z_mid = hyperparameters['measured mean(z)']
                mean_z_lim = hyperparameters['N(uncertainties) in generation'] * hyperparameters['measured mean(z) err']
                gen_MeanZ = np.random.uniform( mean_z_mid - mean_z_lim ,  mean_z_mid + mean_z_lim )
                
                sigma_z_mid = hyperparameters['measured sigma(z)']
                sigma_z_lim = hyperparameters['N(uncertainties) in generation'] * hyperparameters['measured sigma(z) err']
                gen_SigmaZ = np.random.uniform( sigma_z_mid - sigma_z_lim ,  sigma_z_mid + sigma_z_lim )

                if debug: print 'run',run,'gen_Sigma_t',gen_Sigma_t,'gen_MeanZ',gen_MeanZ,'gen_SigmaZ',gen_SigmaZ
                gen_events.Set_eep_Parameters_MeanXYZ_Sigma( gen_MeanX , gen_MeanY , gen_MeanZ , gen_Sigma_t , gen_SigmaZ )
                rootfilename_suffix = "_"+hyperparameters['my target name']+"_SigmaT%.3f_SigmaZ%.3f_MeanZ%.3f"%(gen_Sigma_t,gen_SigmaZ,gen_MeanZ)
            #}
            
            elif hyperparameters['generation method'] ==  'constant band': #{
                gen_MeanZ = np.random.normal( hyperparameters['measured mean(z)'] , hyperparameters['measured mean(z) err band'] )
                gen_SigmaZ = np.random.normal( hyperparameters['measured sigma(z)'] , hyperparameters['measured sigma(z) err band'] )
                
                if debug: print 'run',run,'gen_Sigma_t',gen_Sigma_t,'gen_MeanZ',gen_MeanZ,'gen_SigmaZ',gen_SigmaZ
                gen_events.Set_eep_Parameters_MeanXYZ_Sigma( gen_MeanX , gen_MeanY , gen_MeanZ , gen_Sigma_t , gen_SigmaZ )
                rootfilename_suffix = "_"+hyperparameters['my target name']+"_SigmaT%.3f_SigmaZ%.3f_MeanZ%.3f"%(gen_Sigma_t,gen_SigmaZ,gen_MeanZ)
            #}
            
            elif hyperparameters['generation method']=='mean(z) linear in Pmiss': #{
                # sample the geneated parameters uniformly within the ranges
                average_slope = np.average( [hyperparameters['minimal slope'] , hyperparameters['maximal slope']] )
                width_slope = average_slope - hyperparameters['minimal slope'] # its symmetric to (hyperparameters['maximal slope']-average_slope)
                gen_MeanZ_slope  = np.random.normal( average_slope  , width_slope )
                gen_SigmaZ = np.random.normal( hyperparameters['measured sigma(z)'] , hyperparameters['N(uncertainties) in generation'] * hyperparameters['measured sigma(z) err'] )

                if debug: print 'run',run,'gen_MeanX',gen_MeanX,'gen_MeanY',gen_MeanY,'gen_Sigma_t',gen_Sigma_t,'gen_SigmaZ',gen_SigmaZ,'gen_MeanZ_slope',gen_MeanZ_slope
                gen_events.Set_MeanZ_Pmiss_vanish_at_03()
                gen_events.Set_eep_Parameters_Pmiss_vanish_at_03( gen_MeanX , gen_MeanY , gen_Sigma_t , gen_SigmaZ , gen_MeanZ_slope )
                rootfilename_suffix = "_"+hyperparameters['my target name']+"_SigmaT%.3f_SigmaZ%.3f_MeanZSlope%.3f"%(gen_Sigma_t,gen_SigmaZ,gen_MeanZ_slope)
            #}
            
            
            gen_events.InitRun()
            if debug: print 'gRandom seed for this run:',gen_events.gRandom.GetSeed()
            Nevents = gen_events.DoGenerate_eepp_from_eep_SingleParameterSigma( run , rootfilename_suffix )
            if debug: print 'Nevents to analyze:',Nevents
        #}
        
        # (2) analyze the simulated data (the 'run') similarly to the data - reconstructed parameters
        # ----------------------------
        if 'ana' in option: #{
            if debug>1: print "analyzing run %d"%run,rootfilename_suffix
            
            genfile = ROOT.TFile( path + '/eg_rootfiles/run%d'%run+rootfilename_suffix+'.root' )
            NgenEntries = genfile.Get('genTree').GetEntries()
            genfile.Close()
            
            ana_sim = TAnalysisEG2( path + '/eg_rootfiles', 'run%d'%run+rootfilename_suffix )
            results = pd.DataFrame({'run':int(run)
                                   ,'time':str(datetime.datetime.now().strftime("%Y%B%d"))
                                   ,'Ngenenerated':NgenEntries
                                   ,'Naccepted':ana_sim.GetEntries(ROOT.TCut(""))
                                   ,'gen_MeanX':gen_MeanX,'gen_MeanY':gen_MeanY
                                   ,'gen_MeanZ':gen_MeanZ if hyperparameters['generation method']!='mean(z) linear in Pmiss' else -1
                                   ,'gen_MeanZ_slope':gen_MeanZ_slope if hyperparameters['generation method']=='mean(z) linear in Pmiss' else -1
                                   ,'gen_Sigma_t':gen_Sigma_t
                                   ,'gen_SigmaZ':gen_SigmaZ,
                                   }
                                   , index = [int(run)])

            if Nevents!=-1: #{  Nevents==-1 means that the generation of events could not be completed (too bad of acceptance)
                reco_parameters = calc_cm_pars_sigma( ana_sim )
                for direction in ['x','y','z']: #{
                    for reco_parameter_name in ['mean','sigma']: #{
                        results['rec' + '_' + reco_parameter_name + '_' + direction] = reco_parameters.get_value(0,reco_parameter_name + '_' + direction + '_unweighted')
                        if debug>2: print "results[rec+'_'"+reco_parameter_name+" + '_' + "+direction+"]:",results['rec' + '_' + reco_parameter_name + '_' + direction]
                    #}
                        results['chi2red' + '_' + direction] = reco_parameters.get_value(0,'chi2red' + '_' + direction + '_unweighted')
                        results['ndof' + '_' + direction] = reco_parameters.get_value(0,'ndof' + '_' + direction + '_unweighted')
                #}
                if debug>3:#{
                    if np.abs(reco_parameters.get_value(0,'sigma_x_unweighted')-gen_Sigma_t)<0.02: print_important("!! rec_sigma_x-gen_Sigma_t = %.3f !!"%(reco_parameters.get_value(0,'sigma_x_unweighted')-gen_Sigma_t))
                #}
                if hyperparameters['do print results']:#{
                    print "results:"
                    print results
                #}
                if do_results_file: stream_dataframe_to_file( results, buildup_resultsFName , float_format='%f' )
            #}
            ana_sim.CloseFile()
        #}
        if 'delete' in option:#{
            delete_file( path + '/eg_rootfiles/run%d'%run+rootfilename_suffix+'.root'  , debug )
        #}
        irun += 1
        print_important("completed run %d [%.0f"%(run,100.*float(irun)/Nruns) + "%]"+" at %4d-%02d-%02d %d:%d:%d"%time.localtime()[0:6] )
        print_line()
    #}

    if 'gen' in option: #{
        gen_events.ReleaseInputChain_eep()
    #}

    if do_results_file:  print_filename( buildup_resultsFName , "results wrote to " )
    print_important("done...") ; print_line()
#}
# ------------------------------------------------------------------------------- #


