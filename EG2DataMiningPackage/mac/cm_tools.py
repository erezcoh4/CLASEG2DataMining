from definitions import *
from root_numpy import hist2array , tree2array
from root_pandas import to_root
from scipy.stats import ks_2samp
from matplotlib.ticker import LinearLocator
from math import sqrt
from scipy.stats.mstats import ttest_onesamp
sqrt2pi = np.sqrt(2*np.pi)


# ------------------------------------------------------------------------------- #
# definitions
PmissBins   = [[0.3,0.45]  , [0.45,0.55] , [0.55,0.65]  , [0.65,0.75] , [0.75,1.0]]
Pmiss3Bins  = [[0.3,0.52]  , [0.52,0.68]  , [0.68,1.0]]
Q2Bins      = [[0,1.5]     , [1.5,2]     , [2,2.5]      , [2.5,6]]
thetapmqBins= [[100,135]   , [135,145]   , [145,155]    , [155,180]]
targets         = ['C12'        , 'Al27'        , 'Fe56'        , 'Pb208'       ]
labels          = ['$^{12}$C'   , '$^{27}$Al'   , '$^{56}$Fe'   , '$^{208}$Pb'  ]
target_colors   = ['black'      , 'red'         , 'green'       , 'blue'        ]



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
def buildup_resutlsFName( path ):
    return path+"runs_results.csv"
def root_resutlsFName( path ):
    return path+"runs_results.root"


# ------------------------------------------------------------------------------- #
def Pval( dataset1 , dataset2  , var   , weighting , tweeked=False):
    
    weightsuffix = '_' + weighting if weighting is not '' else ''
    v1 , v1Err = float(dataset1[var+weightsuffix]) , float(dataset1[var+'err'+weightsuffix])
    v2 , v2Err = float(dataset2[var+weightsuffix]) , float(dataset2[var+'err'+weightsuffix])
    
    if tweeked and ('a1' in var or 'a2' in var) :
        v1Err , v2Err = v1Err/10 , v2Err/10
    
    return Pval2varsAssumeGausDist( v1 , v1Err , v2 , v2Err , flags.verbose  , name=var+' '+weighting )
# ------------------------------------------------------------------------------- #

# ------------------------------------------------------------------------------- #
def generate_a_gaussian_from_value_and_error( dataframe=None , parname=None, parerrname=None , N=1000 , PmissBin=None ):
    if PmissBin is None: #{
        mean = dataframe[parname]
        sigma = dataframe[parerrname]
    #}
    else: #{
        mean = dataframe.get_value( PmissBin , parname )
        sigma = dataframe.get_value( PmissBin , parerrname )
    #}
    return np.random.normal( mean , sigma , N )
# ------------------------------------------------------------------------------- #

# ------------------------------------------------------------------------------- #
def CalcKS2sampAssumingGaussian( data_df=None, sim_df=None, parname=None, parerrname=None , PmissBin=None):
    '''
        calculate the KS test p-value for 2-sample comparison,
        by assuming that the fit values were sampled from a Gaussian distribution function
        '''
    data_gaussian = generate_a_gaussian_from_value_and_error( dataframe=data_df, parname=parname, parerrname=parerrname, PmissBin=PmissBin )
    sim_gaussian = generate_a_gaussian_from_value_and_error( dataframe=sim_df, parname=parname, parerrname=parerrname, PmissBin=PmissBin )
    D_ks, Pval_ks = ks_2samp( data_gaussian , sim_gaussian )
    # print 'for',parname,'comparing ',np.mean(data_gaussian),'+/-',np.std(data_gaussian),'and',np.mean(sim_gaussian),'+/-',np.std(sim_gaussian)
    # print 'Pval_ks:',Pval_ks
    return Pval_ks
# ------------------------------------------------------------------------------- #

# ------------------------------------------------------------------------------- #
def compute_Pval_parameters(data_cm_pars=None, data_fits=None ,
                            reco_fits=None, reco_parameters=None,
                            ):
    #                            target=None,
    #                            cm_pars_as_gaussians=None, fits_pars_as_gaussians=None
    #                            weighting='' ,
    
    # My Pval pairwise comparison
    #    PvalSigmaX = Pval( data_fits , reco_fits  , 'SigmaX'   , weighting , tweeked=tweeked)
    #    PvalSigmaY = Pval( data_fits , reco_fits  , 'SigmaY'   , weighting , tweeked=tweeked)
    #    PvalMeanX = Pval( data_fits , reco_fits  , 'SigmaX'   , weighting , tweeked=tweeked)
    #    PvalMeanY = Pval( data_fits , reco_fits  , 'SigmaY'   , weighting , tweeked=tweeked)
    #    PvalMeanZa1 = Pval( data_fits , reco_fits  , 'MeanZa1'   , weighting , tweeked=tweeked)
    #    PvalMeanZa2 = Pval( data_fits , reco_fits  , 'MeanZa2'   , weighting , tweeked=tweeked)
    #    PvalSigmaZa1 = Pval( data_fits , reco_fits  , 'SigmaZa1'   , weighting , tweeked=tweeked)
    #    PvalSigmaZa2 = Pval( data_fits , reco_fits  , 'SigmaZa2'   , weighting , tweeked=tweeked)
    #    return [PvalSigmaX, PvalSigmaY, PvalMeanZa1, PvalMeanZa2, PvalSigmaZa1, PvalSigmaZa2]
    
    #    Pval_mean_x  = Pval( data_fits , reco_fits  , 'SigmaX'   , weighting )
    #    Pval_sigma_x = Pval( data_fits , reco_fits  , 'SigmaX'   , weighting )
    #    Pval_mean_y  = Pval( data_fits , reco_fits  , 'SigmaY'   , weighting )
    #    Pval_sigma_y = Pval( data_fits , reco_fits  , 'SigmaY'   , weighting )
    #    Pval_a1 = Pval( data_fits , reco_fits  , 'a1'   , weighting )
    #    Pval_a2 = Pval( data_fits , reco_fits  , 'a2'   , weighting )
    #    Pval_b1 = Pval( data_fits , reco_fits  , 'b1'   , weighting )
    #    Pval_b2 = Pval( data_fits , reco_fits  , 'b2'   , weighting )
    #    return [Pval_mean_x, Pval_mean_y ,Pval_sigma_x, Pval_sigma_y, Pval_a1 , Pval_a2 , Pval_b1 , Pval_b2 ]
    
    
    # April-2017, change to Pval using ks-test
    pval_fits_scores = dict()
    pval_fits_scores_array = []
    for i,parname in enumerate(['MeanX','MeanY','SigmaX','SigmaY','a1','a2','b1','b2']):#{
        pval_fits_scores[parname] = CalcKS2sampAssumingGaussian( data_df=data_fits, sim_df=reco_fits, parname=parname, parerrname=parname+'err' )
        pval_fits_scores_array.append(pval_fits_scores[parname])
    #}
    pval_fits_scores['Pval_array'] = pval_fits_scores_array
    pval_fits_scores['PvalTotal'] = Fisher_combination_Pvals( pval_fits_scores_array ) # with a cutoff on 1e-20
    pval_fits_scores['PvalTotal_allPvals'] = FisherMethodPvals( pval_fits_scores_array )
    if debug>2: print 'pval_fits_scores:',pval_fits_scores

    pval_cm_pars_scores = dict()
    pval_cm_pars_scores_array = []
    for bin in range(len(PmissBins)):#{
        pmin , pmax = PmissBins[bin][0] , PmissBins[bin][1]
        for parameter in ['mean','sigma']:#{
            for direction in ['x','y','z']:#{
                parname = parameter + '_' + direction
                pval_cm_pars_scores[parname+'_bin%d'%bin] = CalcKS2sampAssumingGaussian( data_df=data_cm_pars, sim_df=reco_parameters, parname=parname+'_unweighted', parerrname=parname+'Err_unweighted' , PmissBin=bin)
                pval_cm_pars_scores_array.append( pval_cm_pars_scores[parname+'_bin%d'%bin] )
            #}
        #}
    #}


    pval_cm_pars_scores['Pval_array'] = pval_cm_pars_scores_array
    pval_cm_pars_scores['PvalTotal'] = Fisher_combination_Pvals( pval_cm_pars_scores_array ) # with a cutoff on 1e-20
    pval_cm_pars_scores['PvalTotal_allPvals'] = FisherMethodPvals( pval_cm_pars_scores_array )
    if debug>2: print 'pval_cm_pars_scores:',pval_cm_pars_scores


    return pval_fits_scores , pval_cm_pars_scores
# ------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------- #
def KStest( PmissBins , ana_sim , ana_data , var , Nbins=20, do_save_plots=False):
    # [http://docs.scipy.org/doc/scipy-0.15.1/reference/generated/scipy.stats.ks_2samp.html]
    data = tree2array( ana_data.GetTree() , branches=var )
    sim = tree2array( ana_sim.GetTree() , branches=var )
    D_KS , Pval_KS = ks_2samp( sim , data )
    if do_save_plots :
        fig,ax = plt.subplots(figsize=[20,20])
        for array,col in zip([sim , data],['black','red']):
            g=sns.distplot( array, bins=np.linspace(-1, 2 , Nbins), ax=ax, color=col , axlabel=var )
        fig.savefig( path + "/cmHistos_%s.pdf"%var)
        print_important( "KS test of data vs. simulation for %s is D = %f, Pvalue = %f"%(var , D_KS , Pval_KS) )

    return D_KS , Pval_KS
# ------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------- #
def calc_pval_ks_scores(ana_sim=None, ana_data=dict(), do_plots=False , run=-1):
    
    ks_pval_scores = dict()
    # April-2017, change to Pval using ks-test
    df_sim = tree2array( ana_sim.GetTree() , branches=['pcmX','pcmY','pcmZ','Pmiss3Mag'] )
    for target in targets: #{
        
        if do_plots:  #{
            gen_info = tree2array( ana_sim.GetTree() , branches=['gen_SigmaX','gen_a1','gen_a2','gen_b1','gen_b2'] )
            if debug>2: print 'gen: SigmaX ',gen_info[0]['gen_SigmaX'],'a1',gen_info[0]['gen_a1'],'a2',gen_info[0]['gen_a2'],'b1',gen_info[0]['gen_b1'],'b2',gen_info[0]['gen_b2']
            fig_t = plt.figure(figsize=(20,12))
            fig_l = plt.figure(figsize=(30,6))
        #}
        ks_pval_scores_target_array , ks_pval_scores_transverse_target_array , ks_pval_scores_longitudinal_target_array = [] , [] , []
        ks_pval_scores_target = dict()
        df_data = tree2array( ana_data[target].GetTree() , branches=['pcmX','pcmY','pcmZ','Pmiss3Mag'] )
        
        
        ks_pval_scores_target_array , ks_pval_scores_transverse_target_array , ks_pval_scores_longitudinal_target_array = [] , [] , []
        ks_pval_scores_target = dict()
        df_data = tree2array( ana_data[target].GetTree() , branches=['pcmX','pcmY','pcmZ','Pmiss3Mag'] )
        
        # compare x & y directions in 1 p(miss) bin - since there is no p(miss) dependence
        for i_dir,direction in enumerate(['X','Y']): #{
            x_data = df_data['pcm'+direction]
            x_sim = df_sim['pcm'+direction]
            D_KS , Pval_KS = ks_2samp( x_data , x_sim )
            ks_pval_scores_target['pcm'+direction] = Pval_KS
            ks_pval_scores_target_array.append( Pval_KS )
            ks_pval_scores_transverse_target_array.append( Pval_KS )
            if do_plots:#{
                ax_t = fig_t.add_subplot( 1 , 2 , i_dir+1 )
                h,bins,_=ax_t.hist(x_sim , bins=25,label='sim. $\\mu=%.3f, \\sigma=%.3f$'%(np.mean(x_sim),np.std(x_sim)),histtype='step',linewidth=3,normed=1)
                h,bins,_=ax_t.hist(x_data , bins=bins,label=target+' data $\\mu=%.3f, \\sigma=%.3f$'%(np.mean(x_data),np.std(x_data)),histtype='step',linewidth=3,normed=1)
                ax_t.legend(loc='best',fontsize=10)
                ax_t.set_title('$p_{c.m.}^{%s}$, Pval=%f'%(direction,Pval_KS),y=1.01,fontsize=15)
            #}
        #}
        ks_pval_scores_target['Pval_pcmX_pcmY'] = Fisher_combination_Pvals( [ks_pval_scores_target['pcmX'],ks_pval_scores_target['pcmY']] ) # with a cutoff on 1e-20
        if do_plots:#{
            fig_t.savefig("/Users/erezcohen/Desktop/TmpPlots/run_%d_pcmT_%s.pdf"%(run,target))
        #}
      
        # in z direction - compare in 5 bins of p(miss)
        for bin in range(len(PmissBins)):#{
            
            pmin , pmax = PmissBins[bin][0] , PmissBins[bin][1]
            df_sim_reduced = df_sim[ (pmin < df_sim['Pmiss3Mag']) & (df_sim['Pmiss3Mag'] < pmax) ]
            df_data_reduced = df_data[ (pmin < df_data['Pmiss3Mag']) & (df_data['Pmiss3Mag'] < pmax) ]
            D_KS , Pval_KS = ks_2samp( df_sim_reduced['pcmZ'] , df_data_reduced['pcmZ'] )
            
            if do_plots:#{  and target == 'C12'
                ax_l = fig_l.add_subplot(1 , 5, bin+1 )
                bins=np.linspace(-0.5,2,50)
                h,bins,_=ax_l.hist(df_sim_reduced['pcmZ'] , bins=np.linspace(-0.5,2,50),histtype='step',linewidth=3,normed=1
                                   ,label='sim. (%d) \n m=%f,\n s=%f'%(len(df_sim_reduced),np.mean(df_sim_reduced['pcmZ']),np.std(df_sim_reduced['pcmZ'])))
                ax_l.hist(df_data_reduced['pcmZ'] , bins=bins,label=target+' data',histtype='step',linewidth=3,normed=1)
                ax_l.set_title('%.2f<$p_{miss}$<%.2f GeV/c, $p_{c.m.}^{z}$ Pval=%f'%(pmin , pmax,Pval_KS),y=1.01,fontsize=15)
                ax_l.legend(fontsize=15)
            #}
            
            ks_pval_scores_target['pcmZ_bin%d'%bin] = Pval_KS
            ks_pval_scores_target_array.append( Pval_KS )
            hist , bin_edges = np.histogram (df_sim_reduced['pcmZ'] , bins=np.linspace(-0.5,2,50))
            x_bins = (bin_edges[1:]+bin_edges[:-1])/2 # for len(x)==len(y)
            params,cov=curve_fit(gauss,x_bins,hist,(np.mean(df_sim_reduced['pcmZ']),np.std(df_sim_reduced['pcmZ']),len(df_sim_reduced)))
            fit_sigma_std_ratio = params[1]/np.std(df_sim_reduced['pcmZ'])
            if fit_sigma_std_ratio<0.75:
                if debug>2: print 'fit_sigma_std_ratio = ' , fit_sigma_std_ratio,', implying more than a single Gaussian peak. substituting Pval=0'
                Pval_KS = 0
            ks_pval_scores_longitudinal_target_array.append( Pval_KS )
            #}
        #}
        if do_plots:#{
            fig_l.savefig("/Users/erezcohen/Desktop/TmpPlots/run_%d_pcmZ_%s.pdf"%(run,target))
        #}

        ks_pval_scores_target['pcmZ'] = Fisher_combination_Pvals( ks_pval_scores_longitudinal_target_array ) # with a cutoff on 1e-20
    
        ks_pval_scores_target['Pval_pcmX_pcmY_pcmZ'] = FisherMethodPvals( [ks_pval_scores_target['pcmX'],ks_pval_scores_target['pcmY'],ks_pval_scores_target['pcmZ']] )
        ks_pval_scores_target['Pval_pcmX_pcmY_pcmZ_scaled_1T'] = ks_pval_scores_target['Pval_pcmX_pcmY_pcmZ']*1000000000
        ks_pval_scores_target['PvalTotal'] = Fisher_combination_Pvals( ks_pval_scores_target_array ) # with a cutoff on 1e-20
        ks_pval_scores_target['PvalTotal_allPvals'] = FisherMethodPvals( ks_pval_scores_target_array )

        ks_pval_scores[target] = ks_pval_scores_target
    #}
    if debug>2:
        print 'ks_pval_scores:'
        for i in ks_pval_scores:
            print i
            for j in ks_pval_scores[i]:
                print j,ks_pval_scores[i][j]

    return ks_pval_scores
# ------------------------------------------------------------------------------- #



# ------------------------------------------------------------------------------- #
def get_KS_scores( PmissBins ,ana_sim , ana_data , h3_pcm_data ):

    if ana_sim.GetEntries():
        # 1d KS tests
        KSpCMx , KSxPval = KStest( PmissBins ,ana_sim , ana_data , "pcmX" )
        KSpCMy , KSyPval = KStest( PmissBins ,ana_sim , ana_data , "pcmY" )
        KSpCMt , KStPval = KStest( PmissBins ,ana_sim , ana_data , "pcmT" )
        KSpCMz , KSzPval = KStest( PmissBins ,ana_sim , ana_data , "pcmZ" )
        KSPval_tot = Fisher_combination_Pvals([ KSxPval , KSyPval , KSzPval ])
    
        # 3d KS test
        #        h3_pcm_sim = ana_sim.H3("pcmX","pcmY","pcmZ",ROOT.TCut(),"goff",nbins_pcm_3d,-1,1,nbins_pcm_3d,-1,1,nbins_pcm_3d,-1,1)
        #        KS3dHistPval = h3_pcm_sim.KolmogorovTest(h3_pcm_data)
        # this routine has a problem of acquiring too much memoory without allocating it; Since its not that crucial (not helpfull) I removed it temporarily
    else:
        KSxPval=KSyPval=KSzPval=KStPval=KSPval_tot=KS3dHistPval=0
    # make it a data-frame
    KS_scores = pd.DataFrame({'KSxPval':KSxPval,'KSyPval':KSyPval,'KSzPval':KSzPval,'KStPval':KStPval,
                             'KSPval_tot':KSPval_tot,
                             #                             'KS3dHistPval':KS3dHistPval
                             },index=[0])

    if debug>1:
        print "performed KS tests"
        if debug>3:
            print "KS scores:",KS_scores

    return KS_scores
# ------------------------------------------------------------------------------- #

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
def plot_errorbar_and_fit( ax , x , y , xerr , yerr , color , marker , lstyle , label ,
                          fit_type='const' ,do_plot_fit_pars=False, x_offset=0.6):
    plt.errorbar(x, y, xerr=xerr, yerr=yerr, color=color, marker=marker , linestyle=lstyle , label=None , markersize=15)
    if fit_type=='const':
        const_fit , const_fitErr , const_chi2red = fit_as_a_function_of_pmiss( x , y , yerr=yerr , fit_type=fit_type )
        if do_plot_fit_pars: label=label + "$=%.3f\pm%.3f$"%(const_fit,const_fitErr)
        ax.plot(x, np.ones(len(x))*const_fit , color=color , linestyle='--', label=label,linewidth = 2 , )
        if debug>1: print 'const fit of ' + label + " : $=%.3f\pm%.3f$"%(const_fit,const_fitErr)
        return [ const_fit , const_fitErr , const_chi2red ]
    
    elif fit_type=='linear':
        a1 , a1err , a2 , a2err , chi2red = fit_as_a_function_of_pmiss( x , y ,yerr=yerr, fit_type=fit_type )
        if do_plot_fit_pars: label=label + "$=(%.3f)(p_{miss}-%.1f)+(%.3f)$"%( a1 , x_offset, a2 )
        ax.plot( x , a1 * (x-x_offset) + a2 , color = color ,label=label )
        if debug>1: print 'linear fit of ' + label + " : $=(%.3f)(p_{miss}-%.1f)+(%.3f)$"%( a1 ,x_offset ,  a2 )
        return [ a1 , a1err ,  a2 , a2err  , chi2red ]
# ------------------------------------------------------------------------------- #




# ------------------------------------------------------------------------------- #
def fit_as_a_function_of_pmiss( x , y , yerr=None, fit_type='const' , title='', x_offset=0.6): # the main fitting routine
    
    if fit_type=='const':
        if len(x)<3:
            return -100 , 0

        p1,v1 = np.polyfit( x , y , 0 , cov=True)
        chi2red = -100
        if debug>4:
            print 'p1:',p1,',\tv1:',v1

        if not p1 or not v1 or len(p1)==0 or len(v1)==0:
            return -100 , 0
        else:
            return p1[0] , sqrt(v1[0,0]) , chi2red
    
    #        p2,v2 = np.polyfit( x , y , 1 , cov=True)        # fit a polynomial p2(x) = p2[0] * x + p2[1]
    elif fit_type=='linear':

        if len(x)<4:
            return -100 , 0 , -100 , 0

        if x_offset==0:
            f = linear
        else:
            f = linear_06
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
# ------------------------------------------------------------------------------- #

# ------------------------------------------------------------------------------- #
def calc_cm_parameters( fana  , PmissBins , unweightedRoofitsFName = '' , weightedRoofitsFName = '' , DoSaveCanvas = False ):
    '''
        Return: df_pMissBin , do_fits (continue or not)
        '''
    do_fits = True
    df_pMissBins = pd.DataFrame()
    
    if DoSaveCanvas:
        canvas_unweighted , canvas_weighted = fana.CreateCanvas( "RooFit plots - unweighted" , "Divide" , 4 , len(PmissBins) ) , fana.CreateCanvas( "RooFit plots - weighted" , "Divide" , 4 , len(PmissBins) )

    # Jan 2017, changing to a (weighted) average and variance using numpy
    if fana.GetEntries()==0:
        print 'no entries in anaTree of',fana.GetFileName()
        print 'leaving calc_cm_parameters'
        return pd.DataFrame() , False

    ana = read_root( str(fana.GetFileName()) , key='anaTree' , columns=['pcmX','pcmY','pcmZ','Pmiss3Mag','rooWeight']  )

    for i in range(len(PmissBins)):
        pMiss_min , pMiss_max = PmissBins[i][0] , PmissBins[i][1]
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

    if DoSaveCanvas:
        canvas_unweighted.SaveAs(unweightedRoofitsFName)
        print_filename(unweightedRoofitsFName,"unweighted rooFits at")
        canvas_weighted.SaveAs(weightedRoofitsFName)
        print_filename(weightedRoofitsFName,"weighted rooFits at")
        print_line()
    print "computed cm parameters for "+fana.InFileName
    if debug>1:
        print "reconstructed cm parameters"
        if debug>5:
            print 'df_pMissBins:',df_pMissBins

    garbage_list = [ ana ]
    del garbage_list

    return df_pMissBins , do_fits
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
    [Xfit,XfitErr,Xchi2red] = plot_errorbar_and_fit( ax , Pmiss, data[ var + '_x_' + weight] , [np.zeros(len(pMissLowErr)),np.zeros(len(pMissLowErr))] , [data[ var + '_xErr_' + weight ],data[ var + '_xErr_' + weight ]], 'black','v','none',r'$x-direction$' ,'const',do_plot_fit_pars=do_plot_fit_pars)
    [Yfit,YfitErr,Ychi2red] = plot_errorbar_and_fit( ax , Pmiss, data[ var + '_y_' + weight] , [np.zeros(len(pMissLowErr)),np.zeros(len(pMissLowErr))] , [data[ var + '_yErr_' + weight ],data[ var + '_yErr_' + weight ]], 'red'  ,'o','none',r'$y-direction$' ,'const',do_plot_fit_pars=do_plot_fit_pars)
    [Za1,Za1err],[Za2,Za2err],Zchi2red = plot_errorbar_and_fit( ax , Pmiss, data[ var + '_z_' + weight] , [np.zeros(len(pMissLowErr)),np.zeros(len(pMissLowErr))] , data[ var + '_zErr_' + weight ], 'blue' ,'s','none',r'$\vec{p}_{miss}-direction$' ,'linear',do_plot_fit_pars=do_plot_fit_pars)
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
    if do_fits==False:
        print 'nothing in cm-paramteres input as data to fit_cm_parameters()'
        print 'leaving fit_cm_parameters by appending -100 to all'
#        return pd.DataFrame({ 'run':run
#                            ,'SigmaX_unweighted':-100      ,'SigmaXerr_unweighted':0
#                            ,'SigmaY_unweighted':-100      ,'SigmaYerr_unweighted':0
#                            ,'SigmaZa1_unweighted':-100    ,'SigmaZa1err_unweighted':0
#                            ,'SigmaZa2_unweighted':-100    ,'SigmaZa2err_unweighted':0
#                            ,'MeanX_unweighted':-100       ,'MeanXerr_unweighted':0
#                            ,'MeanY_unweighted':-100       ,'MeanYerr_unweighted':0
#                            ,'MeanZa1_unweighted':-100     ,'MeanZa1err_unweighted':0
#                            ,'MeanZa2_unweighted':-100     ,'MeanZa2err_unweighted':0
#                            ,'SigmaX_weighted':-100        ,'SigmaXerr_weighted':0
#                            ,'SigmaY_weighted':-100        ,'SigmaYerr_weighted':0
#                            ,'SigmaZa1_weighted':-100      ,'SigmaZa1err_weighted':0
#                            ,'SigmaZa2_weighted':-100      ,'SigmaZa2err_weighted':0
#                            ,'MeanX_weighted':-100         ,'MeanXerr_weighted':0
#                            ,'MeanY_weighted':-100         ,'MeanYerr_weighted':0
#                            ,'MeanZa1_weighted':-100       ,'MeanZa1err_weighted':0
#                            ,'MeanZa2_weighted':-100       ,'MeanZa2err_weighted':0 }
#                            , index=[0] )
        return pd.DataFrame({ 'run':run,'Nevents':-100
                            ,'SigmaX':-100,'SigmaXerr':0,'MeanX':-100, 'MeanXerr':0
                            ,'SigmaY':-100,'SigmaYerr':0,'MeanY':-100,'MeanYerr':0
                            ,'a1':-100,'a1err':0,'a2':-100,'a2err':0,'a_chi2red':-100
                            ,'b1':-100,'b1err':0,'b2':-100,'b2err':0,'b_chi2red':-100
                            }, index=[0] )

    if DoPlot: # this means we want plots
        fig = plt.figure(figsize=(40,20)) # four plots, two unweighted and two weighted

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

#
#    [SigmaX_unweighted  , SigmaXerr_unweighted,
#     SigmaY_unweighted  , SigmaYerr_unweighted,
#     SigmaZa1_unweighted, SigmaZa1err_unweighted,
#     SigmaZa2_unweighted, SigmaZa2err_unweighted, ax ] = fit_par_plot ( fig, 221, data, 'sigma', 'unweighted', '\sigma' , do_plot_fit_pars=True ) if DoPlot else fit_par_noplot ( data,'sigma','unweighted','\sigma' )
#
#    [MeanX_unweighted   , MeanXerr_unweighted,
#     MeanY_unweighted   , MeanYerr_unweighted,
#     MeanZa1_unweighted , MeanZa1err_unweighted,
#     MeanZa2_unweighted , MeanZa2err_unweighted, ax ] = fit_par_plot( fig, 222, data, 'mean', 'unweighted', 'mean') if DoPlot else fit_par_noplot( data, 'mean','unweighted','mean')
#
#    [SigmaX_weighted  , SigmaXerr_weighted,
#     SigmaY_weighted  , SigmaYerr_weighted,
#     SigmaZa1_weighted, SigmaZa1err_weighted,
#     SigmaZa2_weighted, SigmaZa2err_weighted, ax ] = fit_par_plot ( fig, 223, data, 'sigma', 'weighted', '\sigma'  , do_plot_fit_pars=True ) if DoPlot else fit_par_noplot ( data,'sigma','weighted','\sigma')
#
#    [MeanX_weighted   , MeanXerr_weighted,
#     MeanY_weighted   , MeanYerr_weighted,
#     MeanZa1_weighted , MeanZa1err_weighted,
#     MeanZa2_weighted , MeanZa2err_weighted, ax ] = fit_par_plot( fig, 224, data, 'mean', 'weighted', 'mean') if DoPlot else fit_par_noplot( data, 'mean','weighted','mean')
#

#    df_fit_parameters = pd.DataFrame({ 'run':run
#                                      ,'SigmaX_unweighted':SigmaX_unweighted     ,'SigmaXerr_unweighted':SigmaXerr_unweighted
#                                      ,'SigmaY_unweighted':SigmaY_unweighted     ,'SigmaYerr_unweighted':SigmaYerr_unweighted
#                                      ,'SigmaZa1_unweighted':SigmaZa1_unweighted ,'SigmaZa1err_unweighted':SigmaZa1err_unweighted
#                                      ,'SigmaZa2_unweighted':SigmaZa2_unweighted ,'SigmaZa2err_unweighted':SigmaZa2err_unweighted
#                                      ,'MeanX_unweighted':MeanX_unweighted       ,'MeanXerr_unweighted':MeanXerr_unweighted
#                                      ,'MeanY_unweighted':MeanY_unweighted       ,'MeanYerr_unweighted':MeanYerr_unweighted
#                                      ,'MeanZa1_unweighted':MeanZa1_unweighted   ,'MeanZa1err_unweighted':MeanZa1err_unweighted
#                                      ,'MeanZa2_unweighted':MeanZa2_unweighted   ,'MeanZa2err_unweighted':MeanZa2err_unweighted
#                                      ,'SigmaX_weighted':SigmaX_weighted         ,'SigmaXerr_weighted':SigmaXerr_weighted
#                                      ,'SigmaY_weighted':SigmaY_weighted         ,'SigmaYerr_weighted':SigmaYerr_weighted
#                                      ,'SigmaZa1_weighted':SigmaZa1_weighted     ,'SigmaZa1err_weighted':SigmaZa1err_weighted
#                                      ,'SigmaZa2_weighted':SigmaZa2_weighted     ,'SigmaZa2err_weighted':SigmaZa2err_weighted
#                                      ,'MeanX_weighted':MeanX_weighted           ,'MeanXerr_weighted':MeanXerr_weighted
#                                      ,'MeanY_weighted':MeanY_weighted           ,'MeanYerr_weighted':MeanYerr_weighted
#                                      ,'MeanZa1_weighted':MeanZa1_weighted       ,'MeanZa1err_weighted':MeanZa1err_weighted
#                                      ,'MeanZa2_weighted':MeanZa2_weighted       ,'MeanZa2err_weighted':MeanZa2err_weighted }
#                                      , index=[0] )

    if DoPlot:
        plt.savefig(FigureFName)
        print_filename( FigureFName , "and plot can be found at" )
        print_line()
    print "computed fit parameters for run ",run
    if debug>1:
        print "completed fiting processes"
        if debug>4:
            print "df_fit_parameters: ",df_fit_parameters

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
def plot_band_around_cm_parameter_fits( fig , i_subplot , data , var , weight , title  , TBandMin , TBandMax , ZBandMin , ZBandMax ):

    Pmiss = (data.pMiss_max + data.pMiss_min)/2.
    pMissUpErr , pMissLowErr = data.pMiss_max - Pmiss , Pmiss - data.pMiss_min
    [a1,a2,a3,a4,a5,a8,a9,a10,ax] = fit_par_plot( fig , i_subplot , data , var , weight , title , do_plot_fit_pars=False)
    plt.fill_between(Pmiss, TBandMin , TBandMax ,alpha=0.5, edgecolor='#CC4F1B', facecolor='#FF9848')
    plt.fill_between(Pmiss, ZBandMin , ZBandMax ,alpha=0.5, edgecolor='#C14F1B', facecolor='#1122CC')
    return ax
# ------------------------------------------------------------------------------- #

# ------------------------------------------------------------------------------- #
def linspace_parameter( band_min  , band_max  , Npts ):
    return np.linspace( band_min + (band_max - band_min) / (Npts+1) , band_max , Npts , endpoint=False)
# ------------------------------------------------------------------------------- #

# ------------------------------------------------------------------------------- #
def generate_cm_bands( cm_parameters , fit_pars , N ,
                      debug ,
                      CMBandFname , FigureBandFName , GeneParsFName ,
                      DoSaveCanvas = False , do_add_text = False,
                      SigmaTBandRange   = None,
                      SigmaZa1BandRange = None,
                      SigmaZa2BandRange = None,
                      MeanZa1BandRange  = None,
                      MeanZa2BandRange  = None,
                      nom_vals          = None):
 
    Pmiss = (cm_parameters.pMiss_max + cm_parameters.pMiss_min)/2.

    # ----------------------------------------------------------------------------------------------------------------------------------
    # width
    print "N: ",N
    # sigma-t
    if SigmaTBandRange is None:
        SigmaTBandMin   , SigmaTBandMax     = 0.7*np.min( [fit_pars.SigmaX_unweighted , fit_pars.SigmaY_unweighted] ) , 1.2*np.max( [fit_pars.SigmaX_unweighted,fit_pars.SigmaY_unweighted] )
    elif int(N.SigmaT)==1:
        SigmaTBandMin   , SigmaTBandMax     = float(nom_vals.SigmaT)-float(nom_vals.SigmaT_err) , float(nom_vals.SigmaT)+float(nom_vals.SigmaT_err)
    else:
        SigmaTBandMin   , SigmaTBandMax     = SigmaTBandRange[0] , SigmaTBandRange[1]
    # sigma-z a1
    if SigmaZa1BandRange is None:
        SigmaZa1BandMin , SigmaZa1BandMax   = fit_pars.SigmaZa1_unweighted*0.6,fit_pars.SigmaZa1_unweighted*1.3 # 0.9 , 1.1
    elif int(N.SigmaZa1)==1:
        SigmaZa1BandMin , SigmaZa1BandMax   = float(nom_vals.SigmaZa1)-float(nom_vals.SigmaZa1_err) , float(nom_vals.SigmaZa1)+float(nom_vals.SigmaZa1_err)
    else:
        SigmaZa1BandMin , SigmaZa1BandMax   = SigmaZa1BandRange[0] , SigmaZa1BandRange[1]
    # sigma-z a2
    if SigmaZa2BandRange is None:
        SigmaZa2BandMin , SigmaZa2BandMax   = fit_pars.SigmaZa2_unweighted*0.0,fit_pars.SigmaZa2_unweighted*3
    elif int(N.SigmaZa2)==1:
        SigmaZa2BandMin , SigmaZa2BandMax   = float(nom_vals.SigmaZa2)-float(nom_vals.SigmaZa2_err) , float(nom_vals.SigmaZa2)+float(nom_vals.SigmaZa2_err)
    else:
        SigmaZa2BandMin , SigmaZa2BandMax   = SigmaZa2BandRange[0] , SigmaZa2BandRange[1]

    SigmaZBandMin = float(SigmaZa1BandMin)*(Pmiss)+float(SigmaZa2BandMin)
    SigmaZBandMax = float(SigmaZa1BandMax)*(Pmiss)+float(SigmaZa2BandMax)

    # mean-z b1
    MeanTBandMin   , MeanTBandMax       = np.zeros(len(Pmiss)) , np.zeros(len(Pmiss))
    if MeanZa1BandRange is None:
        MeanZa1BandMin , MeanZa1BandMax   = fit_pars.MeanZa1_unweighted*0.5,fit_pars.MeanZa1_unweighted*1.5 # 0.7 , 1.3
    elif int(N.MeanZa1)==1:
        MeanZa1BandMin , MeanZa1BandMax   = float(nom_vals.MeanZa1)-float(nom_vals.MeanZa1_err) , float(nom_vals.MeanZa1)+float(nom_vals.MeanZa1_err)
    else:
        MeanZa1BandMin , MeanZa1BandMax   = MeanZa1BandRange[0] , MeanZa1BandRange[1]
    # mean-z b2
    if MeanZa2BandRange is None:
        MeanZa2BandMin , MeanZa2BandMax   = np.min([fit_pars.MeanZa2_unweighted*0.2,fit_pars.MeanZa2_unweighted*2]) , np.max([fit_pars.MeanZa2_unweighted*0.2,fit_pars.MeanZa2_unweighted*2])
    elif int(N.MeanZa2)==1:
        MeanZa2BandMin , MeanZa2BandMax   = float(nom_vals.MeanZa2)-float(nom_vals.MeanZa2_err) , float(nom_vals.MeanZa2)+float(nom_vals.MeanZa2_err)
    else:
        MeanZa2BandMin , MeanZa2BandMax   = MeanZa2BandRange[0] , MeanZa2BandRange[1]

    MeanZBandMax = np.max([float(MeanZa1BandMax),float(MeanZa1BandMin)])*(Pmiss) + np.max([float(MeanZa2BandMax),float(MeanZa2BandMin)])
    MeanZBandMin = np.min([float(MeanZa1BandMax),float(MeanZa1BandMin)])*(Pmiss) + np.min([float(MeanZa2BandMax),float(MeanZa2BandMin)])

    # ----------------------------------------------------------------------------------------------------------------------------------

    if DoSaveCanvas:
        fig = plt.figure(figsize=(40,20))
        ax = plot_band_around_cm_parameter_fits( fig , 221, cm_parameters , 'sigma', 'unweighted' , '\sigma' , SigmaTBandMin , SigmaTBandMax , SigmaZBandMin , SigmaZBandMax  )
        if do_add_text:
            ax.text(0.7, 0.06, r'$%.2f<\sigma(x,y)<%.2f$'%(min_SigmaXY , max_SigmaXY), fontsize=35 , color='#FF9848')
            ax.text(0.7, 0.04, r'$%.2f<\sigma(z): a_{1}<%.2f$'%(SigmaZa1BandMin , SigmaZa1BandMax), fontsize=35, color='#1122CC')
            ax.text(0.7, 0.02, r'$%.2f<\sigma(z): a_{2}<%.2f$'%(SigmaZa2BandMin , SigmaZa2BandMax), fontsize=35, color='#1122CC')
        ax.set_xlim(0.3,1)
        ax = plot_band_around_cm_parameter_fits( fig , 222, cm_parameters , 'mean', 'unweighted' , 'mean' , MeanTBandMin , MeanTBandMax , MeanZBandMin , MeanZBandMax  )
        if do_add_text:
            ax.text(0.71, -0.24, r'$%.2f<\mu(z): a_{1}<%.2f$'%(MeanZa1BandMin , MeanZa1BandMax), fontsize=35, color='#1122CC')
            ax.text(0.68, -0.32, r'$%.2f<\mu(z): a_{2}<%.2f$'%(MeanZa2BandMin , MeanZa2BandMax), fontsize=35, color='#1122CC')
        ax.set_xlim(0.3,1)
        plt.savefig(FigureBandFName)
        print_filename( FigureBandFName , "plots to file" )


    bands = pd.DataFrame({'SigmaTBandMin':SigmaTBandMin,'SigmaTBandMax':SigmaTBandMax
                            ,'SigmaZa1Min':SigmaZa1BandMin,'SigmaZa1Max':SigmaZa1BandMax
                            ,'SigmaZa2Min':SigmaZa2BandMin,'SigmaZa2Max':SigmaZa2BandMax
                            ,'MeanZa1Min':MeanZa1BandMin,'MeanZa1Max':MeanZa1BandMax
                            ,'MeanZa2Min':MeanZa2BandMin,'MeanZa2Max':MeanZa2BandMax},
                            index=[0])
    SigmaT   = linspace_parameter( float(SigmaTBandMin)    , float(SigmaTBandMax)   , int(N.SigmaT) )
    SigmaZa1 = linspace_parameter( float(SigmaZa1BandMin)  , float(SigmaZa1BandMax) , int(N.SigmaZa1) )
    SigmaZa2 = linspace_parameter( float(SigmaZa2BandMin)  , float(SigmaZa2BandMax) , int(N.SigmaZa2) )
    MeanZa1  = linspace_parameter( float(MeanZa1BandMin)   , float(MeanZa1BandMax)  , int(N.MeanZa1) )
    MeanZa2  = linspace_parameter( float(MeanZa2BandMin)   , float(MeanZa2BandMax)  , int(N.MeanZa2) )
    StartRun = int(N.StartRun)
    EndRun   = int(StartRun + len(SigmaT)*len(SigmaZa1)*len(SigmaZa2)*len(MeanZa1)*len(MeanZa2))
#    if debug>1:
#        print "SigmaT:",SigmaT , "\nSigmaZa1:",SigmaZa1 , "\nSigmaZa2:",SigmaZa2 , "\nMeanZa1:",MeanZa1, "\nMeanZa2:",MeanZa2 , "\n mean(pcmZ) = %f * p(miss) + %f"%(MeanZa1 , MeanZa2  )
    print '\033[95m' + "generating parameters for runs %d to %d"%(StartRun, EndRun) + '\033[0m'

    run , irun  = StartRun , 0
    # write generated parameters to file
    for sigma_transverse in SigmaT:
        for sigma_longitudinal_a1 in SigmaZa1:
            for sigma_longitudinal_a2 in SigmaZa2:
                for mean_longitudinal_a1 in MeanZa1:
                    for mean_longitudinal_a2 in MeanZa2:
                        run = run+1
                        irun = irun+1
                        if irun%((EndRun-StartRun)/20)==0:
                            print 100.*irun/(EndRun-StartRun),'%'

                        generated_parameters = pd.DataFrame({'run':run
                                                            ,'genMeanX':0                           ,'genSigmaX':sigma_transverse
                                                            ,'genMeanY':0                           ,'genSigmaY':sigma_transverse
                                                            ,'genMeanZa1':mean_longitudinal_a1      ,'genMeanZa2':mean_longitudinal_a2
                                                            ,'genSigmaZa1':sigma_longitudinal_a1    ,'genSigmaZa2':sigma_longitudinal_a2
                                                            },
                                                            index = [run])
                        stream_dataframe_to_file( generated_parameters, GeneParsFName , float_format='%.3f' )


    bands.to_csv( CMBandFname , header=True , index = False)
    print_filename( CMBandFname , "wrote bands around cm paramters fits to" )
    print_filename( GeneParsFName , '\033[95m' + "appended " + '\033[0m' + "generation parameters to" )
    print_line()
# ------------------------------------------------------------------------------- #

# ------------------------------------------------------------------------------- #
def get_pmiss_bins( PmissBins , Q2Bins , thetapmqBins , path , NRand ): # for pp/p analysis

    # define the bins - 4 bins in each large p(miss) bin that we have in the analysis
    pmiss_bins = []

    for i in range(len(PmissBins)):
        pmin , pmax = PmissBins[i][0] , PmissBins[i][1]
        for j in range(4):
            pmiss_bins.append( [ pmin + float(j*(pmax-pmin))/4 , pmin + float((j+1)*(pmax-pmin))/4 ])

    # get the number of generated events per bin
    evtsgen_pmiss_bins = []
    evtsgen_Q2pmiss_bins = np.zeros( (len(pmiss_bins) , len(Q2Bins)) )
    evtsgen_thetapmqpmiss_bins = np.zeros( (len(pmiss_bins) , len(thetapmqBins)) )

    p1 = TPlots(path + '/DATA/SRC_e1_C.root' , 'T')
    p2 = TPlots(path + '/DATA/SRC_e2_C.root' , 'T')

    for i in range( len(pmiss_bins) ):
        pmin , pmax = pmiss_bins[i][0] , pmiss_bins[i][1]
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
def generate_runs_with_different_parameters( option,
                                            data_fits_12C, data_fits_27Al, data_fits_56Fe, data_fits_208Pb,
                                            generated_parameters ,
                                            debug , PmissBins , Q2Bins , thetapmqBins ,
                                            buildup_resutlsFName ,
                                            reco_fitsFName , target ,
                                            N ,
                                            root_resutlsFName ,
                                            do_root_file=False, do_reco_fits_file=False, do_resutls_file=True, do_add_plots=False,
                                            main_cut = ROOT.TCut()):
    
    from definitions import path
    ana_data = TAnalysisEG2( path+"/AnaFiles" ,"Ana_ppSRCCut_DATA_%s"% target )
    h3_pcm_data = ana_data.H3("pcmX","pcmY","pcmZ",ROOT.TCut(),"goff",nbins_pcm_3d,-1,1,nbins_pcm_3d,-1,1,nbins_pcm_3d,-1,1) # for binned 3d-KS test

    pAcceptacneFile = ROOT.TFile(path+"/GSIM_DATA/PrecoilAcceptance.root")
    path = path + "/Analysis_DATA/ppSRCcm"
    if 'helion' in flags.worker:
        path = "/extra/Erez/DataMining/Analysis_DATA/ppSRCcm"



    # the bands around data (around nominal values)
    if debug>2: print "generated_parameters:",generated_parameters
    if debug:
        print generated_parameters.run.tolist()
        print '\033[95m' + 'processing %d runs'%len(generated_parameters)+ '\033[0m'

    # multiple bins for pp/p ratio
    pmiss_bins , evtsgen_pmiss_bins , evtsgen_Q2pmiss_bins  , evtsgen_thetapmqpmiss_bins = get_pmiss_bins( PmissBins , Q2Bins , thetapmqBins , path , int(N.NRand) )


    '''
        recoil proton acceptances:
        (a) efficiency and acceptacne from the 'uniform' map i've generated using virtual CLAS
        (b) proton fiducial cuts (coded inside the event generator class)
    '''
    if 'gen' in option:
        h = pAcceptacneFile.Get("hRescaled")
        gen_events = GenerateEvents( path , 0 , debug - 2 )
        gen_events.SetNRand( int(N.NRand) )
        gen_events.Use_protonAcceptacne( True )
        gen_events.Set_protonAcceptacne( h )
        gen_events.SetInputChain_eep()


    # event generation (and analysis) loop
    Nruns = len(generated_parameters.run.tolist())
    irun = 0
    for run in generated_parameters.run.tolist():
        run = int(run)
        irun = irun+1
        genMeanX    = genMeanY = 0
        genSigmaX   = genSigmaY = float(generated_parameters[generated_parameters.run==run].genSigmaX)
        genSigmaZa1 = float(generated_parameters[generated_parameters.run==run].genSigmaZa1)
        genSigmaZa2 = float(generated_parameters[generated_parameters.run==run].genSigmaZa2)
        genMeanZa1  = float(generated_parameters[generated_parameters.run==run].genMeanZa1)
        genMeanZa2  = float(generated_parameters[generated_parameters.run==run].genMeanZa2)
        if flags.verbose>2:
            print 'run:',run,',i(run):',irun,',parameters:', genSigmaX , genSigmaZa1 , genSigmaZa2 , genMeanZa1 , genMeanZa2
            
        # (1) generate the simulated data (the 'run')
        # ----------------------------
        if 'gen' in option:
                            
            gen_events.Set_eep_Parameters( genMeanX , genSigmaX , genMeanY , genSigmaY , genMeanZa1 , genMeanZa2 , genSigmaZa1 , genSigmaZa2 )
            gen_events.DoGenerateRun_eepp( run )
                            
            # and now scheme them to our desired pp-SRC cuts
            ana_sim = TAnalysisEG2( path + '/eg_rootfiles', 'run%d'%run , ROOT.TCut('') )
            scheme.SchemeOnTCut( path + '/eg_rootfiles' , 'run%d.root'%run , "anaTree", 'run%d.root'%run , ana_sim.EGppSRCCut + ana_sim.PrecFiducial + main_cut )
                            
            ana_sim.CloseFile()
            garbage_list = [ ana_sim ]
            del garbage_list
                    
                    
                    
        # (2) analyze the simulated data (the 'run') similarly to the data - reconstructed parameters
        # ----------------------------
        if 'ana' in option:
                            
            if debug>1: print "analyzing run %d"%run
            ana_sim = TAnalysisEG2( path + '/eg_rootfiles', 'run%d'%run , main_cut )
                
            loss_pmiss_bins , loss_Q2pmiss_bins , loss_thetapmqpmiss_bins = get_loss_pmiss_bins( pmiss_bins , evtsgen_pmiss_bins ,
                                                                                                Q2Bins , evtsgen_Q2pmiss_bins ,
                                                                                                thetapmqBins , evtsgen_thetapmqpmiss_bins ,
                                                                                                ana_sim )

            if do_add_plots:
                reco_parameters , do_fits = calc_cm_parameters( ana_sim  , PmissBins , CMRooFitsName( path + '/eg_cm_roofits/run%d_unweighted_'%run ), CMRooFitsName( path + '/eg_cm_roofits/run%d_weighted_'%run ) , True )
                fit_cm_parameters( run , reco_parameters , FigureFName( path + '/eg_cm_figures/run%d_'%run ) , True )
            
            # reconstruct c.m. parameters and fit
            reco_parameters, do_fits = calc_cm_parameters( ana_sim  , PmissBins )
            reco_fits = fit_cm_parameters( run , reco_parameters , do_fits=do_fits )


            KS_scores = get_KS_scores( PmissBins ,ana_sim , ana_data , h3_pcm_data )

            results = pd.DataFrame({'run':int(run)
                                   ,'time':str(datetime.datetime.now().strftime("%Y%B%d"))
                                   ,'NentriesSimRun':ana_sim.GetEntries()
                                   
                                   # generated
                                   ,'genMeanX':float(genMeanX)     ,'genSigmaX':float(genSigmaX)      ,'genMeanY':float(genMeanY)        ,'genSigmaY':float(genSigmaY)
                                   ,'genMeanZa1':float(genMeanZa1) ,'genMeanZa2':float(genMeanZa2)    ,'genSigmaZa1':float(genSigmaZa1)  ,'genSigmaZa2':float(genSigmaZa2)
                                   
                                   # reconstructed fits - unweighted
                                   ,'recMeanX_unweighted':float(reco_fits.MeanX_unweighted)         ,'recMeanY_unweighted':float(reco_fits.MeanY_unweighted)
                                   ,'recSigmaX_unweighted':float(reco_fits.SigmaX_unweighted)       ,'recSigmaY_unweighted':float(reco_fits.SigmaY_unweighted)
                                   ,'recMeanZa1_unweighted':float(reco_fits.MeanZa1_unweighted)     ,'recMeanZa2_unweighted':float(reco_fits.MeanZa2_unweighted)
                                   ,'recSigmaZa1_unweighted':float(reco_fits.SigmaZa1_unweighted)   ,'recSigmaZa2_unweighted':float(reco_fits.SigmaZa2_unweighted)
                                   
                                   # reconstructed fits - weighted by Mott+FF cross section
                                   ,'recMeanX_weighted':float(reco_fits.MeanX_weighted)         ,'recMeanY_weighted':float(reco_fits.MeanY_weighted)
                                   ,'recSigmaX_weighted':float(reco_fits.SigmaX_weighted)       ,'recSigmaY_weighted':float(reco_fits.SigmaY_weighted)
                                   ,'recMeanZa1_weighted':float(reco_fits.MeanZa1_weighted)     ,'recMeanZa2_weighted':float(reco_fits.MeanZa2_weighted)
                                   ,'recSigmaZa1_weighted':float(reco_fits.SigmaZa1_weighted)   ,'recSigmaZa2_weighted':float(reco_fits.SigmaZa2_weighted)
                                   
                                   ,'KSxPval':float(KS_scores.KSxPval)
                                   ,'KSyPval':float(KS_scores.KSyPval)
                                   ,'KSzPval':float(KS_scores.KSzPval)
                                   ,'KStPval':float(KS_scores.KStPval)
                                   ,'KSPval_tot':float(KS_scores.KSPval_tot)
                                   # ,'KS3dHistPval':float(KS_scores.KS3dHistPval)
                                   
                                   # events loss
                                   ,'NLostEvents':(9907*float(N.NRand) - ana_sim.GetEntries())
                                   ,'fracLostEvents':(float((9907.0*float(N.NRand)) - ana_sim.GetEntries())/(9907.0*float(N.NRand)))
                                   }
                                   
                                   , index = [int(run)])
            # all nuclei
            for target,data_fits in zip(['12C','27Al','56Fe','208Pb'],
                                        [data_fits_12C,data_fits_27Al,data_fits_56Fe,data_fits_208Pb]):
                Pval_scores  = get_Pval_scores( data_fits , reco_fits , target )

                results['PvalSigmaX_unweighted_%s'%target]  = float(Pval_scores.PvalSigmaX_unweighted)
                results['PvalSigmaY_unweighted_%s'%target]  = float(Pval_scores.PvalSigmaY_unweighted)
                results['PvalMeanZa1_unweighted_%s'%target] = float(Pval_scores.PvalMeanZa1_unweighted)
                results['PvalMeanZa2_unweighted_%s'%target] = float(Pval_scores.PvalMeanZa2_unweighted)
                results['PvalSigmaZa1_unweighted_%s'%target]= float(Pval_scores.PvalSigmaZa1_unweighted)
                results['PvalSigmaZa2_unweighted_%s'%target]= float(Pval_scores.PvalSigmaZa2_unweighted)
                results['PvalTotal_unweighted_%s'%target]   = float(Pval_scores.PvalTotal_unweighted)
                
                results['PvalSigmaX_weighted_%s'%target]    = float(Pval_scores.PvalSigmaX_weighted)
                results['PvalSigmaY_weighted_%s'%target]    = float(Pval_scores.PvalSigmaY_weighted)
                results['PvalMeanZa1_weighted_%s'%target]   = float(Pval_scores.PvalMeanZa1_weighted)
                results['PvalMeanZa2_weighted_%s'%target]   = float(Pval_scores.PvalMeanZa2_weighted)
                results['PvalSigmaZa1_weighted_%s'%target]  = float(Pval_scores.PvalSigmaZa1_weighted)
                results['PvalSigmaZa2_weighted_%s'%target]  = float(Pval_scores.PvalSigmaZa2_weighted)
                results['PvalTotal_weighted_%s'%target]     = float(Pval_scores.PvalTotal_weighted)
                
                results['PvalSigmaZa1SigmaZa2_%s'%target]   = float(Pval_scores.PvalSigmaZa1SigmaZa2)
                results['PvalMeanZa1MeanZa2_%s'%target]     = float(Pval_scores.PvalMeanZa1MeanZa2)
                results['PvalSigmaZa1MeanZa1_%s'%target]    = float(Pval_scores.PvalSigmaZa1MeanZa1)
                results['PvalSigmaZa1MeanZa2_%s'%target]    = float(Pval_scores.PvalSigmaZa1MeanZa2)
                results['PvalSigmaZa2MeanZa1_%s'%target]    = float(Pval_scores.PvalSigmaZa2MeanZa1)
                results['PvalSigmaZa2MeanZa2_%s'%target]    = float(Pval_scores.PvalSigmaZa2MeanZa2)
                results['PvalSigmaZa2MeanZa2_%s'%target]    = float(Pval_scores.PvalSigmaZa2MeanZa2)
                results['PvalSigmaTSigmaZa1_%s'%target]     = float(Pval_scores.PvalSigmaTSigmaZa1)
                results['PvalSigmaTSigmaZa2_%s'%target]     = float(Pval_scores.PvalSigmaTSigmaZa2)
                results['PvalSigmaTMeanZa1_%s'%target]      = float(Pval_scores.PvalSigmaTMeanZa1)
                results['PvalSigmaTMeanZa2_%s'%target]      = float(Pval_scores.PvalSigmaTMeanZa2)
                
                results['PvalTotal_allPvals_%s'%target]     = float(Pval_scores.PvalTotal_allPvals)
                results['PvalTotal_largePvals_%s'%target]   = float(Pval_scores.PvalTotal_largePvals)
                
                results['PvalSigmaX_tw_%s'%target]          = float(Pval_scores.PvalSigmaX_tw)
                results['PvalSigmaY_tw_%s'%target]          = float(Pval_scores.PvalSigmaY_tw)
                results['PvalMeanZa1_tw_%s'%target]         = float(Pval_scores.PvalMeanZa1_tw)
                results['PvalMeanZa2_tw_%s'%target]         = float(Pval_scores.PvalMeanZa2_tw)
                results['PvalSigmaZa1_tw_%s'%target]        = float(Pval_scores.PvalSigmaZa1_tw)
                results['PvalSigmaZa2_tw_%s'%target]        = float(Pval_scores.PvalSigmaZa2_tw)

                results['PvalTotal_tw_%s'%target]           = float(Pval_scores.PvalTotal_tw)




            # reconstructed parameters in 5 big p(miss) bins
            for i in range(len(PmissBins)):
                pmin , pmax = PmissBins[i][0] , PmissBins[i][1]
                results['recMeanX_unweighted_pmiss_%.3f_%.3f'%(pmin , pmax)]    = float(reco_parameters.get_value(i,'mean_x_unweighted'))  if do_fits else 0
                results['recSigmaX_unweighted_pmiss_%.3f_%.3f'%(pmin , pmax)]   = float(reco_parameters.get_value(i,'sigma_x_unweighted')) if do_fits else 0
                results['recMeanY_unweighted_pmiss_%.3f_%.3f'%(pmin , pmax)]    = float(reco_parameters.get_value(i,'mean_y_unweighted'))  if do_fits else 0
                results['recSigmaY_unweighted_pmiss_%.3f_%.3f'%(pmin , pmax)]   = float(reco_parameters.get_value(i,'sigma_y_unweighted')) if do_fits else 0
                results['recMeanZ_unweighted_pmiss_%.3f_%.3f'%(pmin , pmax)]    = float(reco_parameters.get_value(i,'mean_z_unweighted'))  if do_fits else 0
                results['recSigmaZ_unweighted_pmiss_%.3f_%.3f'%(pmin , pmax)]   = float(reco_parameters.get_value(i,'sigma_z_unweighted')) if do_fits else 0

            # events loss in 20 p(miss) bins, for pp/p analysis
            for i in range( len(pmiss_bins) ):
                # p(miss) bins
                pmin , pmax = pmiss_bins[i][0] , pmiss_bins[i][1]
                results['fracLoss_pmiss_%.3f_%.3f'%(pmin , pmax)] = loss_pmiss_bins[i]
                # Q2 and p(miss) bins
                for j in range( len(Q2Bins) ):
                    Q2min , Q2max = Q2Bins[j][0] , Q2Bins[j][1]
                    results['fracLoss_pmiss_%.3f_%.3f_Q2bin_%.1f_%.1f'%(pmin , pmax , Q2min , Q2max)] = loss_Q2pmiss_bins[i][j]
                # theta(pm,q) and p(miss) bins
                for j in range( len(thetapmqBins) ):
                    thetapmqmin , thetapmqmax = thetapmqBins[j][0] , thetapmqBins[j][1]
                    results['fracLoss_pmiss_%.3f_%.3f_thetapmq_%.1f_%.1f'%(pmin , pmax , thetapmqmin , thetapmqmax)] = loss_thetapmqpmiss_bins[i][j]
            # ----------------------------
                


            if do_reco_fits_file:   stream_dataframe_to_file( reco_fits, reco_fitsFName  )
            if do_resutls_file:     stream_dataframe_to_file( results, buildup_resutlsFName , float_format='%f' )
            if do_root_file:        stream_dataframe_to_root( results, root_resutlsFName, 'ppSRCsimanaTree')

            ana_sim.CloseFile()
            if debug>1: #{
                print "appended into results"
                if debug>5: print "results: ",results
            #}
            garbage_list = [ ana_sim , reco_parameters , reco_fits
                            , results
                            , Pval_scores , KS_scores , loss_pmiss_bins , loss_Q2pmiss_bins , loss_thetapmqpmiss_bins
                            ]
            del garbage_list
            gc.collect() # collect() calls PyInt_ClearFreeList()
                    
        print_important( "completed run %d [%.0f"%(run,100.*float(irun)/Nruns) + "%]" + " at %4d-%02d-%02d %d:%d:%d"%time.localtime()[0:6] )
        print_line()
        
        # (1) generate the simulated data (the 'run')
        # ----------------------------
        if 'delete' in option:
            delete_file( path + '/eg_rootfiles/run%d.root'%run  , debug )



    if 'gen' in option:
        gen_events.ReleaseInputChain_eep()
    
    if 'ana' in option:
        if do_reco_fits_file:   print_filename( reco_fitsFName , "reconstructed parameters fits wrote to" )
        if do_resutls_file:     print_filename( buildup_resutlsFName , "results wrote to " )

    if do_root_file:     print_filename( root_resutlsFName , "results converted also to root format " )
    print_important("done...") ; print_line()
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
                                         cm_pars=dict(), cm_fits=dict(),
                                         debug=0 , PmissBins=None , Q2Bins=None , thetapmqBins=None ,
                                         buildup_resutlsFName='' ,
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

    # multiple bins for pp/p ratio
    pmiss_bins , evtsgen_pmiss_bins , evtsgen_Q2pmiss_bins  , evtsgen_thetapmqpmiss_bins = get_pmiss_bins( PmissBins , Q2Bins , thetapmqBins , path , int(hyperparameters['NRand']) )

    # cm_pars_as_gaussians, fits_pars_as_gaussians = get_cm_pars_and_fit_pars_as_gaussians( cm_pars=cm_pars, cm_fits=cm_fits , do_plots=False)
    
    '''
    recoil proton acceptances:
    (a) efficiency and acceptacne from the 'uniform' map i've generated using virtual CLAS
    (b) proton fiducial cuts (coded inside the event generator class)
    '''
    if 'gen' in option: #{
        h = pAcceptacneFile.Get("hRescaled")
        gen_events = GenerateEvents( path , 0 , debug - 2 )
        gen_events.Set_protonAcceptacne( h )

        gen_events.SetInputChain_eep()

        gen_events.SetNRand( NRand )
        gen_events.Use_protonAcceptacne( True ) # True
        gen_events.SetDo_PrecFiducial ( True ) # True
        gen_events.SetDo_PrecMinCut ( True ) # True

        gen_events.SetPmissBins()
        gen_events.Set10PmissBins()
    
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
            gen_MeanX  = gen_MeanY = 0
            gen_SigmaX = gen_SigmaY = np.random.uniform( np.min(hyperparameters['range_sigma_t']),np.max(hyperparameters['range_sigma_t']) )
            gen_a1  = np.random.uniform( np.min(hyperparameters['range_a1']),np.max(hyperparameters['range_a1']) )
            gen_a2  = np.random.uniform( np.min(hyperparameters['range_a2']),np.max(hyperparameters['range_a2']) )
            gen_b1  = np.random.uniform( np.min(hyperparameters['range_b1']),np.max(hyperparameters['range_b1']) )
            gen_b2  = np.random.uniform( np.min(hyperparameters['range_b2']),np.max(hyperparameters['range_b2']) )

            
#            gen_MeanX = -0.02
#            gen_MeanY = 0.0
#            gen_SigmaX = gen_SigmaY = 0.146739
#            gen_a1  = 0.871854
#            gen_a2  = 0.325626
#            gen_b1  = 0.066809
#            gen_b2  = 0.116201

            if debug: print 'run',run,'gen_SigmaX',gen_SigmaX,'gen_a1',gen_a1,'gen_a2',gen_a2,'gen_b1',gen_b1,'gen_b2',gen_b2
            if a1a2_create_negative_sigma_z( gen_a1 , gen_a2 ):
                if debug: print 'a1 (%.2f) and a2(%.2f) create together a negative sigma_z, killing run %d'%( gen_a1 , gen_a2 , run );print_line()
                continue
 
            gen_events.Set_eep_Parameters( gen_MeanX , gen_SigmaX , gen_MeanY , gen_SigmaY , gen_b1 , gen_b2 , gen_a1 , gen_a2 )
            gen_events.InitRun()
            Nevents = gen_events.DoGenerate_eepp_from_eep( run )
            if debug: print 'Nevents to analyze:',Nevents
        #}
        
        # (2) analyze the simulated data (the 'run') similarly to the data - reconstructed parameters
        # ----------------------------
        if 'ana' in option: #{
            if debug>1: print "analyzing run %d"%run
            
            ana_sim = TAnalysisEG2( path + '/eg_rootfiles', 'run%d'%run )
            results = pd.DataFrame({'run':int(run)
                                   ,'time':str(datetime.datetime.now().strftime("%Y%B%d"))
                                   ,'NentriesSimRun':ana_sim.GetEntries()
                                   ,'gen_MeanX':gen_MeanX, 'gen_SigmaX':gen_SigmaX, 'gen_MeanY':gen_MeanY, 'gen_SigmaY':gen_SigmaY
                                   ,'gen_a1':gen_a1, 'gen_a2':gen_a2, 'gen_b1':gen_b1, 'gen_b2':gen_b2
                                   }, index = [int(run)])
            if Nevents!=-1: #{
                # Nevents==-1 means that the generation of events could not be completed (too bad of acceptance)
                
                loss_pmiss_bins , loss_Q2pmiss_bins , loss_thetapmqpmiss_bins = get_loss_pmiss_bins( pmiss_bins , evtsgen_pmiss_bins ,
                                                                                                    Q2Bins , evtsgen_Q2pmiss_bins ,
                                                                                                    thetapmqBins , evtsgen_thetapmqpmiss_bins ,
                                                                                                    ana_sim )
                # reconstruct c.m. parameters and fit
                reco_parameters, do_fits = calc_cm_parameters( ana_sim  , PmissBins )
                reco_fits = fit_cm_parameters( run , reco_parameters , do_fits=do_fits )
                ks_pval_scores = calc_pval_ks_scores( ana_sim , ana_data , do_plots=hyperparameters['do_ks_plots'] , run=run )

                for fit_parameter in ['MeanX','SigmaX','MeanY','SigmaY','a1','a2','b1','b2']: #{
                    results['rec'+fit_parameter] = float(reco_fits[fit_parameter])
                #}
                results['NLostEvents'] = (9907*float(NRand) - ana_sim.GetEntries())
                results['fracLostEvents'] = (float((9907.0*float(NRand)) - ana_sim.GetEntries())/(9907.0*float(NRand)))
                results['parameters_reconstructed_well'] = True if do_fits else False
                
                # reconstructed parameters in 5 big p(miss) bins
                for i in range(len(PmissBins)):#{
                    pmin , pmax = PmissBins[i][0] , PmissBins[i][1]
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
                for target in targets: #{
                    #                    if debug>2: print '---------------\npluging ks-Pvalue scores for ',target,'\n------------------'
                    for bin in range(len(PmissBins)):#{
                        results['ks_local_Pval_'+'pcmZ_bin%d'%bin+'_'+target] = ks_pval_scores[target]['pcmZ_bin%d'%bin]
                    #}
                    for direction in ['X','Y','Z']: #{
                        results['ks_local_Pval_'+'pcm'+direction+'_'+target] = ks_pval_scores[target]['pcm'+direction]
                    #}
                    if debug>2: print "ks-pval["+target+"]['PvalTotal_allPvals'],ks-pval["+target+"]['PvalTotal']:",ks_pval_scores[target]['PvalTotal_allPvals'],ks_pval_scores[target]['PvalTotal']
                    results['ks_Pval_pcmX_pcmY'+'_'+target] = ks_pval_scores[target]['Pval_pcmX_pcmY']
                    results['ks_Pval_pcmX_pcmY_pcmZ'+'_'+target] = ks_pval_scores[target]['Pval_pcmX_pcmY_pcmZ']
                    results['ks_Pval_pcmX_pcmY_pcmZ_scaled_1T'+'_'+target] = ks_pval_scores[target]['Pval_pcmX_pcmY_pcmZ_scaled_1T']
                    results['ks_PvalTot_allPvals'+'_'+target] = ks_pval_scores[target]['PvalTotal_allPvals']
                    results['ks_PvalTotal'+'_'+target] = ks_pval_scores[target]['PvalTotal'] # with a cutoff on 1e-20
                #}
        
                # events loss in 20 p(miss) bins, for pp/p analysis
                for i in range( len(pmiss_bins) ):#{
                    pmin , pmax = pmiss_bins[i][0] , pmiss_bins[i][1]
                    results['fracLoss_pmiss_%.3f_%.3f'%(pmin , pmax)] = loss_pmiss_bins[i]
                
                    # Q2 and p(miss) bins
                    for j in range( len(Q2Bins) ):#{
                        Q2min , Q2max = Q2Bins[j][0] , Q2Bins[j][1]
                        results['fracLoss_pmiss_%.3f_%.3f_Q2bin_%.1f_%.1f'%(pmin , pmax , Q2min , Q2max)] = loss_Q2pmiss_bins[i][j]
                    #}

                    # theta(pm,q) and p(miss) bins
                    for j in range( len(thetapmqBins) ):#{
                        thetapmqmin , thetapmqmax = thetapmqBins[j][0] , thetapmqBins[j][1]
                        results['fracLoss_pmiss_%.3f_%.3f_thetapmq_%.1f_%.1f'%(pmin,pmax,thetapmqmin,thetapmqmax)] = loss_thetapmqpmiss_bins[i][j]
                    #}
                #}
            #}
            else: #{
                for target in targets: #{
                    for bin in range(len(PmissBins)):#{
                        results['ks_local_Pval_pcmZ_bin%d'%bin+'_'+target] = 0
                    #}
                    for direction in ['X','Y','Z']: #{
                        results['ks_local_Pval_pcm'+direction+'_'+target] = 0
                    #}
                    results['ks_Pval_pcmX_pcmY'+'_'+target] = results['ks_Pval_pcmX_pcmY_pcmZ'+'_'+target] = results['ks_Pval_pcmX_pcmY_pcmZ_scaled_1T'+'_'+target] = 0
                    results['ks_PvalTotal'+'_'+target] = results['ks_PvalTot_allPvals'+'_'+target] = 0
                    for i in range( len(pmiss_bins) ):#{
                        results['fracLoss_pmiss_%.3f_%.3f'%(pmiss_bins[i][0] , pmiss_bins[i][1])] = 1
                        for j in range( len(Q2Bins) ): results['fracLoss_pmiss_%.3f_%.3f_Q2bin_%.1f_%.1f'%(pmiss_bins[i][0] , pmiss_bins[i][1] , Q2Bins[i][0] , Q2Bins[i][1] )] = 1
                        for j in range( len(thetapmqBins) ): results['fracLoss_pmiss_%.3f_%.3f_thetapmq_%.1f_%.1f'%(pmiss_bins[i][0] , pmiss_bins[i][1] ,thetapmqBins[j][0] , thetapmqBins[j][1])] = 1
                    #}
                #}
                for fit_parameter in ['MeanX','SigmaX','MeanY','SigmaY','a1','a2','b1','b2']: #{
                    results['rec'+fit_parameter] = -100
                #}
                results['NLostEvents'] = 9907*float(NRand)
                results['fracLostEvents'] = 1
                results['parameters_reconstructed_well'] = 0
                for i in range(len(PmissBins)):#{
                    results['EvtsInBin'+'_bin%d'%i] = reco_parameters.get_value(i,'EvtsInBin')
                    for parname in ['mean','sigma']: #{
                        for direction in ['x','y','z']: #{
                            results['rec'+parname + '_' + direction+'_bin%d'%i] = results['rec'+parname + 'Err_' + direction+'_bin%d'%i] =  -100
                        #}
                    #}
                #}
            # ------------------------------------------------------------------------------------------------------------------------------------------------
            
            
            
            if do_reco_fits_file:   stream_dataframe_to_file( reco_fits, reco_fitsFName  )
            if do_resutls_file:     stream_dataframe_to_file( results, buildup_resutlsFName , float_format='%f' )
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
        if do_resutls_file:     print_filename( buildup_resutlsFName , "results wrote to " )
        if do_root_file:        print_filename( root_resutlsFName , "results converted also to root format " )
    #}

    print_important("done...") ; print_line()
#}
# ------------------------------------------------------------------------------- #


#            # Pvalues
#            for target in targets: #{
#                #print '---------------\ncalculating Pvalue for ',target,'\n------------------'
#                pval_fits_scores, pval_cm_pars_scores = compute_Pval_parameters(data_cm_pars=cm_pars[target], data_fits=cm_fits[target], reco_fits=reco_fits, reco_parameters=reco_parameters)
##                pval_fits_scores, pval_cm_pars_scores = compute_Pval_parameters( target=target,
##                                                                                reco_fits=reco_fits,
##                                                                                reco_parameters=reco_parameters,
##                                                                                cm_pars_as_gaussians=cm_pars_as_gaussians,
##                                                                                fits_pars_as_gaussians=fits_pars_as_gaussians)
#
#                for parameter in ['MeanX','MeanY','SigmaX','SigmaY','a1','a2','b1','b2']:#{
#                    results['local_Pval_'+parameter+'_'+target] = pval_fits_scores[parameter]
#                #}
#                results['PvalTotal'] = pval_fits_scores['PvalTotal']
#                results['PvalTotal_allPvals'] = pval_fits_scores['PvalTotal_allPvals']
#
#                for bin in range(len(PmissBins)):#{
#                    for parameter in ['mean','sigma']:#{
#                        for direction in ['x','y','z']:#{
#                            parname = parameter + '_' + direction
#                            parnamebin = parname+'_bin%d'%bin
#                            results['local_Pval_'+parnamebin+'_'+target] = pval_cm_pars_scores[parname+'_bin%d'%bin]
#                        #}
#                    #}
#                #}
#                results['PvalTotal'] = pval_cm_pars_scores['PvalTotal']
#                results['PvalTotal_allPvals'] = pval_cm_pars_scores['PvalTotal_allPvals']
#            #}

