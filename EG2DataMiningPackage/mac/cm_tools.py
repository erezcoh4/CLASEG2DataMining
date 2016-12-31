from definitions import *
from root_numpy import hist2array , tree2array
from root_pandas import to_root
from scipy.stats import ks_2samp
from math import sqrt

# ------------------------------------------------------------------------------- #
# definitions
nbins_pcm_3d = 100
cm_pars_columns = ['pMiss_min','pMiss_max'
                   ,'mean_x_unweighted','mean_xErr_unweighted','sigma_x_unweighted','sigma_xErr_unweighted'
                   ,'mean_y_unweighted','mean_yErr_unweighted','sigma_y_unweighted','sigma_yErr_unweighted'
                   ,'mean_t_unweighted','mean_tErr_unweighted','sigma_t_unweighted','sigma_tErr_unweighted'
                   ,'mean_z_unweighted','mean_zErr_unweighted','sigma_z_unweighted','sigma_zErr_unweighted'
                   ,'mean_x_weighted','mean_xErr_weighted','sigma_x_weighted','sigma_xErr_weighted'
                   ,'mean_y_weighted','mean_yErr_weighted','sigma_y_weighted','sigma_yErr_weighted'
                   ,'mean_t_weighted','mean_tErr_weighted','sigma_t_weighted','sigma_tErr_weighted'
                   ,'mean_z_weighted','mean_zErr_weighted','sigma_z_weighted','sigma_zErr_weighted']



# file names
def CMParsFname( path ):
    return path+"CMparameters.csv"
def CMRooFitsName( path ):
    return path+"CMRooFits.pdf"
def CMfitsFname( path , target='' ):
    return path+"CMfits%s.csv"%target
def CMBandFname( path ):
    return path+"CMparameter_Bands.csv"
def FigureFName( path ):
    return path+"cm_width_and_mean.pdf"
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

# computations
# ------------------------------------------------------------------------------- #
def Nsigma( v1 , v1Err , v2 , v2Err):
    return math.fabs( v1 - v2 )/math.sqrt( v1Err*v1Err + v2Err*v2Err )
# ------------------------------------------------------------------------------- #

# ------------------------------------------------------------------------------- #
def NsigmaScore( dataset1 , dataset2  , var   , weighting ):
    return Nsigma( dataset1[var+'_'+weighting] , dataset1[var+'err_'+weighting]  , dataset2[var+'_'+weighting] , dataset2[var+'err_'+weighting] )
# ------------------------------------------------------------------------------- #

# ------------------------------------------------------------------------------- #
def compute_Nsigma_scores( data_fits , reco_fits , weighting ):
    
    NsigSigmaX = NsigmaScore( data_fits , reco_fits  , 'SigmaX'   , weighting )
    NsigSigmaY = NsigmaScore( data_fits , reco_fits  , 'SigmaY'   , weighting )
    NsigMeanZa1 = NsigmaScore( data_fits , reco_fits  , 'MeanZa1'   , weighting )
    NsigMeanZa2 = NsigmaScore( data_fits , reco_fits  , 'MeanZa2'   , weighting )
    NsigSigmaZa1 = NsigmaScore( data_fits , reco_fits  , 'SigmaZa1'   , weighting )
    NsigSigmaZa2 = NsigmaScore( data_fits , reco_fits  , 'SigmaZa2'   , weighting )
    
    return [NsigSigmaX , NsigSigmaY , NsigMeanZa1 , NsigMeanZa2 , NsigSigmaZa1 , NsigSigmaZa2]
# ------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------- #
def Pval( dataset1 , dataset2  , var   , weighting ):
    v1 , v1Err = float(dataset1[var+'_'+weighting]) , float(dataset1[var+'err_'+weighting])
    v2 , v2Err = float(dataset2[var+'_'+weighting]) , float(dataset2[var+'err_'+weighting])
    return Pval2varsAssumeGausDist( v1 , v1Err , v2 , v2Err , flags.verbose )
# ------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------- #
def compute_Pval_parameters( data_fits , reco_fits , weighting ):

    PvalSigmaX = Pval( data_fits , reco_fits  , 'SigmaX'   , weighting )
    PvalSigmaY = Pval( data_fits , reco_fits  , 'SigmaY'   , weighting )
    PvalMeanZa1 = Pval( data_fits , reco_fits  , 'MeanZa1'   , weighting )
    PvalMeanZa2 = Pval( data_fits , reco_fits  , 'MeanZa2'   , weighting )
    PvalSigmaZa1 = Pval( data_fits , reco_fits  , 'SigmaZa1'   , weighting )
    PvalSigmaZa2 = Pval( data_fits , reco_fits  , 'SigmaZa2'   , weighting )
    
    return [PvalSigmaX , PvalSigmaY , PvalMeanZa1 , PvalMeanZa2 , PvalSigmaZa1 , PvalSigmaZa2]
# ------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------- #
def KStest( PmissBins , ana_sim , ana_data , var , cut=ROOT.TCut() , debug=2 , Nbins=20):
    # [http://docs.scipy.org/doc/scipy-0.15.1/reference/generated/scipy.stats.ks_2samp.html]
    # delete Jan-15
    #    KS_distances , Pval_KS = [] , []
    #    if debug>4 :
    #        figure = plt.figure(figsize=[60,20])
    #    for i in range(len(PmissBins)):
    #        pMiss_min , pMiss_max = PmissBins[i][0] , PmissBins[i][1]
    #        reduced_data = tree2array(ana_data.GetTree(),branches=var , selection = '%f < Pmiss3Mag && Pmiss3Mag < %f'%(pMiss_min , pMiss_max) )
    #        reduced_sim = tree2array(ana_sim.GetTree(),branches=var , selection = '%f < Pmiss3Mag && Pmiss3Mag < %f'%(pMiss_min , pMiss_max))
    #        D , Pvalue = ks_2samp( reduced_sim , reduced_data )
    #
    #        if debug>4 :
    #            ax = figure.add_subplot(len(PmissBins)/2,3,i+1)
    #            for array,col in zip([reduced_sim , reduced_data],['black','red']):
    #                g=sns.distplot( array, bins=np.linspace(-1, 2 , Nbins), ax=ax, color=col , axlabel=var )
    #            g.axes.set_title(r'%.2f < p$_{miss}$ < %.2f GeV/c'%(pMiss_min , pMiss_max), fontsize=34,color="b")
    #            print_important( "KS test of data vs. simulation for %s in p(miss) bin %d is D = %f, Pvalue = %f"%(var , i , D , Pvalue) )
    #
    #        KS_distances.append(D)
    #        Pval_KS.append(Pvalue)
    #
    #    if debug>4 :
    #        figure.savefig( path + "/cmHistos_%s.pdf"%var)
    #
    #    return KS_distances , Pval_KS

    data = tree2array( ana_data.GetTree() , branches=var )
    sim = tree2array( ana_sim.GetTree() , branches=var )
    D_KS , Pval_KS = ks_2samp( sim , data )
    if debug>4 :
        fig,ax = plt.subplots(figsize=[20,20])
        for array,col in zip([sim , data],['black','red']):
            g=sns.distplot( array, bins=np.linspace(-1, 2 , Nbins), ax=ax, color=col , axlabel=var )
        figure.savefig( path + "/cmHistos_%s.pdf"%var)
        print_important( "KS test of data vs. simulation for %s is D = %f, Pvalue = %f"%(var , D_KS , Pval_KS) )

    return D_KS , Pval_KS
# ------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------- #
def get_KS_scores( PmissBins ,ana_sim , ana_data , h3_pcm_data ):
    
    # delete Jan-15
#    # previous 1d KS tests
#    KSpCMx , KSxPval = KStest( PmissBins ,ana_sim , ana_data , "pcmX" , ROOT.TCut('') , debug)
#    KSpCMy , KSyPval = KStest( PmissBins ,ana_sim , ana_data , "pcmY" , ROOT.TCut('') , debug)
#    KSpCMt , KStPval = KStest( PmissBins ,ana_sim , ana_data , "pcmT" , ROOT.TCut('') , debug)
#    KSpCMz , KSzPval = KStest( PmissBins ,ana_sim , ana_data , "pcmZ" , ROOT.TCut('') , debug)
#    KSxPval_tot = Fisher_combination_Pvals( KSxPval )
#    KSyPval_tot = Fisher_combination_Pvals( KSyPval )
#    KStPval_tot = Fisher_combination_Pvals( KStPval )
#    KSzPval_tot = Fisher_combination_Pvals( KSzPval )
#    KSPval_tot = Fisher_combination_Pvals([KSxPval_tot , KSyPval_tot , KSzPval_tot])

    # 1d KS tests
    KSpCMx , KSxPval = KStest( PmissBins ,ana_sim , ana_data , "pcmX" , ROOT.TCut('') , debug)
    KSpCMy , KSyPval = KStest( PmissBins ,ana_sim , ana_data , "pcmY" , ROOT.TCut('') , debug)
    KSpCMt , KStPval = KStest( PmissBins ,ana_sim , ana_data , "pcmT" , ROOT.TCut('') , debug)
    KSpCMz , KSzPval = KStest( PmissBins ,ana_sim , ana_data , "pcmZ" , ROOT.TCut('') , debug)
    KSPval_tot = Fisher_combination_Pvals([ KSxPval , KSyPval , KSzPval ])
    
    # 3d KS test
    h3_pcm_sim = ana_sim.H3("pcmX","pcmY","pcmZ",ROOT.TCut(),"goff",nbins_pcm_3d,-1,1,nbins_pcm_3d,-1,1,nbins_pcm_3d,-1,1)
    KS3dHistPval = h3_pcm_sim.KolmogorovTest(h3_pcm_data)
    
    # make it a data-frame
    KS_scores = pd.DataFrame({'KSxPval':KSxPval,'KSyPval':KSyPval,'KSzPval':KSyPval,'KStPval':KSyPval,
                             #                             'KSxPval_tot':KSxPval_tot,'KSyPval_tot':KSyPval_tot,'KSzPval_tot':KSzPval_tot,'KStPval_tot':KStPval_tot, # previous
                             'KSPval_tot':KSPval_tot,
                             'KS3dHistPval':KS3dHistPval},
                             index=[0])

    if debug>1:
        print "performed KS tests"
        if debug>3:
            print "KS scores:",KS_scores

    return KS_scores
# ------------------------------------------------------------------------------- #



# ------------------------------------------------------------------------------- #
def plot_errorbar_and_fit( ax , x , y , xerr , yerr , color , marker , lstyle , label ,
                          fit_type='const' ,do_plot_fit_pars=True):
    plt.errorbar(x, y, xerr=xerr, yerr=yerr, color=color, marker=marker , linestyle=lstyle , label=None , markersize=15)
    if fit_type=='const':
        const_fit , const_fitErr = fit_as_a_function_of_pmiss( x , y , fit_type )
        if do_plot_fit_pars: label=label + "$=%.3f\pm%.3f$"%(const_fit,const_fitErr)
        ax.plot(x, np.ones(len(x))*const_fit , color=color , linestyle='--', label=label,linewidth = 2 , )
        if debug>1: print 'const fit of ' + label + " : $=%.3f\pm%.3f$"%(const_fit,const_fitErr)
        return [ const_fit , const_fitErr ]
    
    elif fit_type=='linear':
        a1 , a1err , a2 , a2err  = fit_as_a_function_of_pmiss( x , y , fit_type )
        if do_plot_fit_pars: label=label + "$=(%.3f)p_{miss}+(%.3f)$"%( a1 , a2 )
        ax.plot( x , a1 * x + a2 , color = color ,label=label )
        if debug>1: print 'linear fit of ' + label + " : $=(%.3f)p_{miss}+(%.3f)$"%( a1 , a2 )
        return [ a1 , a1err] , [ a2 , a2err ]
# ------------------------------------------------------------------------------- #

# ------------------------------------------------------------------------------- #
def fit_as_a_function_of_pmiss( x , y , fit_type='const' ): # same as plot_errorbar_and_fit without plot
    if fit_type=='const':
        p1,v1 = np.polyfit( x , y , 0 , cov=True)
        return p1[0] , sqrt(v1[0][0])
    elif fit_type=='linear':
        p2,v2 = np.polyfit( x , y , 1 , cov=True)        # fit a polynomial p2(x) = p2[0] * x + p2[1]
        return p2[0] , sqrt(v2[0][0]) , p2[1] , sqrt(v2[1][1])
# ------------------------------------------------------------------------------- #

# ------------------------------------------------------------------------------- #
def calc_cm_parameters( fana  , PmissBins , unweightedRoofitsFName = '' , weightedRoofitsFName = '' , DoSaveCanvas = False ):
    df_pMissBins = pd.DataFrame(columns=cm_pars_columns)
    
    if DoSaveCanvas:
        canvas_unweighted , canvas_weighted = fana.CreateCanvas( "RooFit plots - unweighted" , "Divide" , 4 , len(PmissBins) ) , fana.CreateCanvas( "RooFit plots - weighted" , "Divide" , 4 , len(PmissBins) )

    for i in range(len(PmissBins)):
        pMiss_min , pMiss_max = PmissBins[i][0] , PmissBins[i][1]
        if flags.verbose>1: print 'running p(miss) bin ',i
        if DoSaveCanvas:
            unweighted = fana.RooFitCM( pMiss_min , pMiss_max , False , True, flags.verbose, canvas_unweighted, 4*i + 1 )
            weighted = fana.RooFitCM( pMiss_min , pMiss_max , True , True, flags.verbose, canvas_weighted, 4*i + 1 )
        else:
            unweighted = fana.RooFitCM( pMiss_min , pMiss_max , False )
            weighted = fana.RooFitCM( pMiss_min , pMiss_max , True )

        df_pMissBin = pd.DataFrame({'pMiss_min':pMiss_min,'pMiss_max':pMiss_max
                                   ,'mean_x_unweighted':unweighted[0],'mean_xErr_unweighted':unweighted[1],'sigma_x_unweighted':unweighted[2],'sigma_xErr_unweighted':unweighted[3]
                                   ,'mean_y_unweighted':unweighted[4],'mean_yErr_unweighted':unweighted[5],'sigma_y_unweighted':unweighted[6],'sigma_yErr_unweighted':unweighted[7]
                                   ,'mean_t_unweighted':unweighted[8],'mean_tErr_unweighted':unweighted[9],'sigma_t_unweighted':unweighted[10],'sigma_tErr_unweighted':unweighted[11]
                                   ,'mean_z_unweighted':unweighted[12],'mean_zErr_unweighted':unweighted[13],'sigma_z_unweighted':unweighted[14],'sigma_zErr_unweighted':unweighted[15]
                                   ,'mean_x_weighted':weighted[0],'mean_xErr_weighted':weighted[1],'sigma_x_weighted':weighted[2],'sigma_xErr_weighted':weighted[3]
                                   ,'mean_y_weighted':weighted[4],'mean_yErr_weighted':weighted[5],'sigma_y_weighted':weighted[6],'sigma_yErr_weighted':weighted[7]
                                   ,'mean_t_weighted':weighted[8],'mean_tErr_weighted':weighted[9],'sigma_t_weighted':weighted[10],'sigma_tErr_weighted':weighted[11]
                                   ,'mean_z_weighted':weighted[12],'mean_zErr_weighted':weighted[13],'sigma_z_weighted':weighted[14],'sigma_zErr_weighted':weighted[15]}
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
        if debug>4:
            print 'df_pMissBins:',df_pMissBins

    return df_pMissBins
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
def fit_par_plot( fig , i_subplot , data , var , weight , title , do_plot_fit_pars=False): # a sub-routine to fit a single parameter

    Pmiss = (data.pMiss_max + data.pMiss_min)/2.
    pMissUpErr , pMissLowErr = data.pMiss_max - Pmiss , Pmiss - data.pMiss_min
    ax = fig.add_subplot( i_subplot )
    ax.grid(True,linestyle='-',color='0.95')
    [Xfit,XfitErr] = plot_errorbar_and_fit( ax , Pmiss, data[ var + '_x_' + weight] , [pMissLowErr,pMissUpErr] , [data[ var + '_xErr_' + weight ],data[ var + '_xErr_' + weight ]], 'black','v','none',r'$%s_{x}$'%title ,'const',do_plot_fit_pars=do_plot_fit_pars)
    [Yfit,YfitErr] = plot_errorbar_and_fit( ax , Pmiss, data[ var + '_y_' + weight] , [pMissLowErr,pMissUpErr] , [data[ var + '_yErr_' + weight ],data[ var + '_yErr_' + weight ]], 'red'  ,'o','none',r'$%s_{y}$'%title ,'const',do_plot_fit_pars=do_plot_fit_pars)
    [Tfit,TfitErr] = fit_as_a_function_of_pmiss( Pmiss, data[ var + '_t_' + weight],'const')
    #    [Tfit,TfitErr] = plot_errorbar_and_fit( ax , Pmiss, data[ var + '_t_' + weight] , [pMissLowErr,pMissUpErr] , [data[ var + '_tErr_' + weight ],data[ var + '_tErr_' + weight ]], 'green','^','none',r'$%s_{\perp}$'%title ,'const')
    #    Tfit , TfitErr = 0.5*(Xfit + Yfit) ,  math.sqrt(XfitErr*XfitErr + YfitErr*YfitErr)
    [Za1,Za1err],[Za2,Za2err] = plot_errorbar_and_fit( ax , Pmiss, data[ var + '_z_' + weight] , [pMissLowErr,pMissUpErr] , [data[ var + '_zErr_' + weight ],data[ var + '_zErr_' + weight ]], 'blue' ,'s','none',r'$%s_{\vec{p}_{miss}}$'%title ,'linear',do_plot_fit_pars=do_plot_fit_pars)
#    set_frame( ax , r'%s $%s$'%(weight,title) , r'$p_{miss}$ [GeV/c]' , r'c.m. momentum $%s$ [Gev/c]'%title , "upper left",ncol=2)
    set_frame( ax , '' , r'$p_{miss}$ [GeV/c]' , r'c.m. momentum $%s$ [Gev/c]'%title , "upper left",ncol=2)
    return [Xfit , XfitErr , Yfit , YfitErr , Tfit , TfitErr, Za1 , Za1err , Za2 , Za2err , ax]
# ------------------------------------------------------------------------------- #

# ------------------------------------------------------------------------------- #
def fit_par_noplot( data , var , weight , title ): # a sub-routine to fit a single parameter; same as fit_par_plot without a plot
    
    Pmiss = (data.pMiss_max + data.pMiss_min)/2.
    pMissUpErr , pMissLowErr = data.pMiss_max - Pmiss , Pmiss - data.pMiss_min
    Xfit,XfitErr = fit_as_a_function_of_pmiss( Pmiss, data[ var + '_x_' + weight] ,'const')
    Yfit,YfitErr = fit_as_a_function_of_pmiss( Pmiss, data[ var + '_y_' + weight] ,'const')
    Tfit,TfitErr = fit_as_a_function_of_pmiss( Pmiss, data[ var + '_t_' + weight] ,'const')
    #    Tfit , TfitErr = 0.5*(Xfit + Yfit) ,  math.sqrt(XfitErr*XfitErr + YfitErr*YfitErr)
    Za1,Za1err,Za2,Za2err = fit_as_a_function_of_pmiss( Pmiss, data[ var + '_z_' + weight] , 'linear' )
    return [Xfit , XfitErr , Yfit , YfitErr , Tfit , TfitErr, Za1 , Za1err , Za2 , Za2err , 0 ]
# ------------------------------------------------------------------------------- #



# ------------------------------------------------------------------------------- #
def fit_cm_parameters( run , data , FigureFName = '' , DoPlot = False ): # all parameters


    if DoPlot: # this means we want plots
        fig = plt.figure(figsize=(40,20)) # four plots, two unweighted and two weighted
    
    [SigmaX_unweighted  , SigmaXerr_unweighted,
     SigmaY_unweighted  , SigmaYerr_unweighted,
     sT_unweighted      , sTerr_unweighted,
     SigmaZa1_unweighted, SigmaZa1err_unweighted,
     SigmaZa2_unweighted, SigmaZa2err_unweighted, ax ] = fit_par_plot ( fig, 221, data, 'sigma', 'unweighted', '\sigma') if DoPlot else fit_par_noplot ( data,'sigma','unweighted','\sigma' )

    [MeanX_unweighted   , MeanXerr_unweighted,
     MeanY_unweighted   , MeanYerr_unweighted,
     mT_unweighted      , mTerr_unweighted,
     MeanZa1_unweighted , MeanZa1err_unweighted,
     MeanZa2_unweighted , MeanZa2err_unweighted, ax ] = fit_par_plot( fig, 222, data, 'mean', 'unweighted', 'mean') if DoPlot else fit_par_noplot( data, 'mean','unweighted','mean')

    [SigmaX_weighted  , SigmaXerr_weighted,
     SigmaY_weighted  , SigmaYerr_weighted,
     sT_weighted      , sTerr_weighted,
     SigmaZa1_weighted, SigmaZa1err_weighted,
     SigmaZa2_weighted, SigmaZa2err_weighted, ax ] = fit_par_plot ( fig, 223, data, 'sigma', 'weighted', '\sigma') if DoPlot else fit_par_noplot ( data,'sigma','weighted','\sigma')
     
    [MeanX_weighted   , MeanXerr_weighted,
     MeanY_weighted   , MeanYerr_weighted,
     mT_weighted      , mTerr_weighted,
     MeanZa1_weighted , MeanZa1err_weighted,
     MeanZa2_weighted , MeanZa2err_weighted, ax ] = fit_par_plot( fig, 224, data, 'mean', 'weighted', 'mean') if DoPlot else fit_par_noplot( data, 'mean','weighted','mean')
     

    df_fit_parameters = pd.DataFrame({ 'run':run
                                      ,'SigmaX_unweighted':SigmaX_unweighted     ,'SigmaXerr_unweighted':SigmaXerr_unweighted
                                      ,'SigmaY_unweighted':SigmaY_unweighted     ,'SigmaYerr_unweighted':SigmaYerr_unweighted
                                      ,'sT_unweighted':sT_unweighted             ,'sTerr_unweighted':sTerr_unweighted
                                      ,'SigmaZa1_unweighted':SigmaZa1_unweighted ,'SigmaZa1err_unweighted':SigmaZa1err_unweighted
                                      ,'SigmaZa2_unweighted':SigmaZa2_unweighted ,'SigmaZa2err_unweighted':SigmaZa2err_unweighted
                                      ,'MeanX_unweighted':MeanX_unweighted       ,'MeanXerr_unweighted':MeanXerr_unweighted
                                      ,'MeanY_unweighted':MeanY_unweighted       ,'MeanYerr_unweighted':MeanYerr_unweighted
                                      ,'MeanZa1_unweighted':MeanZa1_unweighted   ,'MeanZa1err_unweighted':MeanZa1err_unweighted
                                      ,'MeanZa2_unweighted':MeanZa2_unweighted   ,'MeanZa2err_unweighted':MeanZa2err_unweighted
                                      ,'SigmaX_weighted':SigmaX_weighted         ,'SigmaXerr_weighted':SigmaXerr_weighted
                                      ,'SigmaY_weighted':SigmaY_weighted         ,'SigmaYerr_weighted':SigmaYerr_weighted
                                      ,'sT_weighted':SigmaY_weighted             ,'sTerr_weighted':SigmaYerr_weighted
                                      ,'SigmaZa1_weighted':SigmaZa1_weighted     ,'SigmaZa1err_weighted':SigmaZa1err_weighted
                                      ,'SigmaZa2_weighted':SigmaZa2_weighted     ,'SigmaZa2err_weighted':SigmaZa2err_weighted
                                      ,'MeanX_weighted':MeanX_weighted           ,'MeanXerr_weighted':MeanXerr_weighted
                                      ,'MeanY_weighted':MeanY_weighted           ,'MeanYerr_weighted':MeanYerr_weighted
                                      ,'MeanZa1_weighted':MeanZa1_weighted       ,'MeanZa1err_weighted':MeanZa1err_weighted
                                      ,'MeanZa2_weighted':MeanZa2_weighted       ,'MeanZa2err_weighted':MeanZa2err_weighted }
                                      , index=[0] )

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
       plot_errorbar_and_fit( ax ,Pmiss,data[ 'sigma_z_unweighted'] ,
                             [pMissLowErr,pMissUpErr] ,
                             [data[ 'sigma_zErr_unweighted'],data[ 'sigma_zErr_unweighted']],
                             color=color ,marker='s',lstyle='none',
                             label=label ,fit_type='linear')
    set_frame( ax , r'c.m. $\sigma$ (unweighted by the cross-section)' ,
              r'$p_{miss}$ [GeV/c]' ,
              r'longitudinal c.m. momentum $\sigma$ [Gev/c]' , "upper left")
    ax.set_ylim(0.11,0.31)
    plt.savefig(FigureFName)
    print_filename( FigureFName , "longitudinal widths plot at" )
    print_line()
# ------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------- #
def fit_means_z( cm_pars_list , colors , labels , FigureFName = '' ): # all parameters
    
    Pmiss = (cm_pars_list[0].pMiss_max + cm_pars_list[0].pMiss_min)/2.
    pMissUpErr , pMissLowErr = cm_pars_list[0].pMiss_max - Pmiss , Pmiss - cm_pars_list[0].pMiss_min
    fig , ax = plt.subplots(figsize=(20,10)) # four plots, two unweighted and two weighted
    for color, label , data in zip(colors,labels,cm_pars_list):
        plot_errorbar_and_fit( ax ,Pmiss,data[ 'mean_z_unweighted'] ,
                              [pMissLowErr,pMissUpErr] ,
                              [data[ 'mean_zErr_unweighted'],data[ 'mean_zErr_unweighted']],
                              color=color ,marker='s',lstyle='none',
                              label=label ,fit_type='linear')
    set_frame( ax , r'c.m. $mean$ (unweighted by the cross-section)' ,
              r'$p_{miss}$ [GeV/c]' ,
              r'longitudinal c.m. momentum $mean$ [Gev/c]' , "upper left")
    ax.set_ylim(0,0.5)
    plt.savefig(FigureFName)
    print_filename( FigureFName , "longitudinal widths plot at" )
    print_line()
# ------------------------------------------------------------------------------- #




# ------------------------------------------------------------------------------- #
def plot_band_around_cm_parameter_fits( fig , i_subplot , data , var , weight , title  , TBandMin , TBandMax , ZBandMin , ZBandMax ):

    Pmiss = (data.pMiss_max + data.pMiss_min)/2.
    pMissUpErr , pMissLowErr = data.pMiss_max - Pmiss , Pmiss - data.pMiss_min
    [a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,ax] = fit_par_plot( fig , i_subplot , data , var , weight , title , do_plot_fit_pars=False)
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
                      MeanZa2BandRange  = None ):
 
    Pmiss = (cm_parameters.pMiss_max + cm_parameters.pMiss_min)/2.

    # ----------------------------------------------------------------------------------------------------------------------------------
    # width
    print "N: ",N

    if SigmaTBandRange is None:
        SigmaTBandMin   , SigmaTBandMax     = 0.7*np.min( [fit_pars.SigmaX_unweighted , fit_pars.SigmaY_unweighted] ) , 1.2*np.max( [fit_pars.SigmaX_unweighted,fit_pars.SigmaY_unweighted] )
    else:
        SigmaTBandMin   , SigmaTBandMax     = SigmaTBandRange[0] , SigmaTBandRange[1]

    if SigmaZa1BandRange is None:
        SigmaZa1BandMin , SigmaZa1BandMax   = fit_pars.SigmaZa1_unweighted*0.6,fit_pars.SigmaZa1_unweighted*1.3 # 0.9 , 1.1
    else:
        SigmaZa1BandMin , SigmaZa1BandMax   = SigmaZa1BandRange[0] , SigmaZa1BandRange[1]

    if SigmaZa2BandRange is None:
        SigmaZa2BandMin , SigmaZa2BandMax   = fit_pars.SigmaZa2_unweighted*0.0,fit_pars.SigmaZa2_unweighted*3
    else:
        SigmaZa2BandMin , SigmaZa2BandMax   = SigmaZa2BandRange[0] , SigmaZa2BandRange[1]

    SigmaZBandMin = float(SigmaZa1BandMin)*(Pmiss)+float(SigmaZa2BandMin)
    SigmaZBandMax = float(SigmaZa1BandMax)*(Pmiss)+float(SigmaZa2BandMax)

    # mean
    MeanTBandMin   , MeanTBandMax       = np.zeros(len(Pmiss)) , np.zeros(len(Pmiss))
    if MeanZa1BandRange is None:
        MeanZa1BandMin , MeanZa1BandMax   = fit_pars.MeanZa1_unweighted*0.5,fit_pars.MeanZa1_unweighted*1.5 # 0.7 , 1.3
    else:
        MeanZa1BandMin , MeanZa1BandMax   = MeanZa1BandRange[0] , MeanZa1BandRange[1]

    if MeanZa2BandRange is None:
        MeanZa2BandMin , MeanZa2BandMax   = np.min([fit_pars.MeanZa2_unweighted*0.2,fit_pars.MeanZa2_unweighted*2]) , np.max([fit_pars.MeanZa2_unweighted*0.2,fit_pars.MeanZa2_unweighted*2])
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
    EndRun   = StartRun + len(SigmaT)*len(SigmaZa1)*len(SigmaZa2)*len(MeanZa1)*len(MeanZa2)
    if debug>1:
        print "SigmaT:",SigmaT , "\nSigmaZa1:",SigmaZa1 , "\nSigmaZa2:",SigmaZa2 , "\nMeanZa1:",MeanZa1, "\nMeanZa2:",MeanZa2 , "\n mean(pcmZ) = %f * p(miss) + %f"%(MeanZa1 , MeanZa2  )
        print '\033[95m' + "runs ",StartRun , " to ", EndRun + '\033[0m'

    run = StartRun
    # write generated parameters to file
    for sigma_transverse in SigmaT:
        for sigma_longitudinal_a1 in SigmaZa1:
            for sigma_longitudinal_a2 in SigmaZa2:
                for mean_longitudinal_a1 in MeanZa1:
                    for mean_longitudinal_a2 in MeanZa2:
                        run = run+1
                        generated_parameters = pd.DataFrame({'run':run
                                                            ,'genMeanX':0                           ,'genSigmaX':sigma_transverse
                                                            ,'genMeanY':0                           ,'genSigmaY':sigma_transverse
                                                            ,'genMeanZa1':mean_longitudinal_a1      ,'genMeanZa2':mean_longitudinal_a2
                                                            ,'genSigmaZa1':sigma_longitudinal_a1    ,'genSigmaZa2':sigma_longitudinal_a2
                                                            },
                                                            index = [run])
                        stream_dataframe_to_file( generated_parameters, GeneParsFName  )


    bands.to_csv( CMBandFname , header=True , index = False)
    print_filename( CMBandFname , "wrote bands around cm paramters fits to" )
    print_filename( GeneParsFName , '\033[95m' + "appended " + '\033[0m' + "generation parameters to" )
    print_line()
# ------------------------------------------------------------------------------- #

# ------------------------------------------------------------------------------- #
def get_pmiss_multiples_bins( PmissBins , path , NRand ): # for pp/p analysis

    # define the bins - 4 bins in each large p(miss) bin that we have in the analysis
    pmiss_multiples_bins = []

    for i in range(len(PmissBins)):
        pmin , pmax = PmissBins[i][0] , PmissBins[i][1]
        for j in range(4):
            pmiss_multiples_bins.append( [ pmin + float(j*(pmax-pmin))/4 , pmin + float((j+1)*(pmax-pmin))/4 ])

    # get the number of generated events per bin
    evts_gen_in_pmiss_multiples_bins = []

    p1 = TPlots(path + '/DATA/SRC_e1_C.root' , 'T')
    p2 = TPlots(path + '/DATA/SRC_e2_C.root' , 'T')

    for i in range( len(pmiss_multiples_bins) ):
        pmin , pmax = pmiss_multiples_bins[i][0] , pmiss_multiples_bins[i][1]
        evts_gen_in_pmiss_multiples_bins.append( NRand * (p1.GetEntries(ROOT.TCut("%f<Pmiss_size && Pmiss_size<%f"%(pmin , pmax))) + p2.GetEntries(ROOT.TCut("%f<Pmiss_size && Pmiss_size<%f"%(pmin , pmax)))) )

    p1.Close()
    p2.Close()

    return pmiss_multiples_bins , evts_gen_in_pmiss_multiples_bins
# ------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------- #
def get_evnt_loss_in_pmiss_bins( pmiss_multiples_bins , evts_gen_in_pmiss_multiples_bins , ana_sim ):

    evnt_loss_in_pmiss_multiples_bins = []
    
    for i in range( len(pmiss_multiples_bins) ):
        pmin , pmax = pmiss_multiples_bins[i][0] , pmiss_multiples_bins[i][1]
        evts_gen = evts_gen_in_pmiss_multiples_bins[i]
        evts_acc = ana_sim.GetEntries(ROOT.TCut("%f<Pmiss3Mag && Pmiss3Mag<%f"%(pmin , pmax)))
        evnt_loss_in_pmiss_multiples_bins.append( float(evts_gen-evts_acc)/evts_gen )
    
    return evnt_loss_in_pmiss_multiples_bins
# ------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------- #
def get_Pval_scores( data_fits , reco_fits , name='' ):
    
    # No Mott/FF - weighting (un - weighted roofit results)
    [PvalSigmaX_unweighted, PvalSigmaY_unweighted ,
     PvalMeanZa1_unweighted , PvalMeanZa2_unweighted ,
     PvalSigmaZa1_unweighted , PvalSigmaZa2_unweighted ] = compute_Pval_parameters( data_fits , reco_fits , 'unweighted' )
    PvalTotal_unweighted = Fisher_combination_Pvals( [PvalSigmaX_unweighted, PvalSigmaY_unweighted ,
                                                       PvalMeanZa1_unweighted , PvalMeanZa2_unweighted ,
                                                       PvalSigmaZa1_unweighted , PvalSigmaZa2_unweighted ] )
    if debug>2: print "got unweighted P(value) results"
 
    # With Mott/FF - weighting (un - weighted roofit results)
    [PvalSigmaX_weighted, PvalSigmaY_weighted ,
     PvalMeanZa1_weighted , PvalMeanZa2_weighted ,
     PvalSigmaZa1_weighted , PvalSigmaZa2_weighted ] = compute_Pval_parameters( data_fits , reco_fits , 'weighted' )
        
    PvalTotal_weighted = Fisher_combination_Pvals( [PvalSigmaX_weighted, PvalSigmaY_weighted ,
                                                     PvalMeanZa1_weighted , PvalMeanZa2_weighted ,
                                                     PvalSigmaZa1_weighted , PvalSigmaZa2_weighted ] )
    if debug>2: print "got weighted P(value) results"

    PvalSigmaZa1SigmaZa2 = Fisher_combination_Pvals( [ PvalSigmaZa1_unweighted , PvalSigmaZa2_unweighted ] )
    PvalMeanZa1MeanZa2 = Fisher_combination_Pvals( [ PvalMeanZa1_unweighted , PvalMeanZa2_unweighted ] )
    PvalSigmaZa1MeanZa1 = Fisher_combination_Pvals( [ PvalSigmaZa1_unweighted , PvalMeanZa1_unweighted ] )
    PvalSigmaZa1MeanZa2 = Fisher_combination_Pvals( [ PvalSigmaZa1_unweighted , PvalMeanZa2_unweighted ] )
    PvalSigmaZa2MeanZa1 = Fisher_combination_Pvals( [ PvalSigmaZa2_unweighted , PvalMeanZa1_unweighted ] )
    PvalSigmaZa2MeanZa2 = Fisher_combination_Pvals( [ PvalSigmaZa2_unweighted , PvalMeanZa2_unweighted ] )
                                                                

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
                               'PvalSigmaZa2MeanZa2':PvalSigmaZa2MeanZa2},index=[0])
    
    if debug>1:
        print "got Pval scores " + name
        if debug>4:
            print "Pval_scores:",Pval_scores

    return Pval_scores
# ------------------------------------------------------------------------------- #



# ------------------------------------------------------------------------------- #
def generate_runs_with_different_parameters( option,
                                            data_fits_12C, data_fits_27Al, data_fits_56Fe, data_fits_208Pb,
                                            generated_parameters ,
                                            debug , PmissBins , buildup_resutlsFName ,
                                            reco_fitsFName , target ,
                                            N ,
                                            root_resutlsFName ,
                                            do_root_file=False, do_reco_fits_file=False, do_resutls_file=True):
    
    from definitions import *
    ana_data = TAnalysisEG2( path+"/AnaFiles" ,"Ana_ppSRCCut_DATA_%s"% target )
    h3_pcm_data = ana_data.H3("pcmX","pcmY","pcmZ",ROOT.TCut(),"goff",nbins_pcm_3d,-1,1,nbins_pcm_3d,-1,1,nbins_pcm_3d,-1,1) # for binned 3d-KS test

    pAcceptacneFile = ROOT.TFile(path+"/GSIM_DATA/PrecoilAcceptance.root")
    path = path + "/Analysis_DATA/ppSRCcm"
    if 'helion' in flags.worker:
        path = "/extra/Erez/DataMining/Analysis_DATA/ppSRCcm"

    # simulation pandas::DataFrame
    df_reco_parameters = pd.DataFrame(columns=cm_pars_columns)


    # the bands around data (around nominal values)
    if debug>2: print "generated_parameters:",generated_parameters
    if debug: print '\033[95m' + 'processing %d runs'%len(generated_parameters)+ '\033[0m'

    # multiple bins for pp/p ratio
    pmiss_multiples_bins , evts_gen_in_pmiss_multiples_bins = get_pmiss_multiples_bins( PmissBins , path , int(N.NRand) )


    '''
        recoil proton acceptances:
        (a) efficiency and acceptacne from the 'uniform' map i've generated using virtual CLAS
        (b) proton fiducial cuts (coded inside the event generator class)
    '''
    if 'generate' in option:
        h = pAcceptacneFile.Get("hRescaled")
        h.Print()
        gen_events = GenerateEvents( path , 0 , debug )
        gen_events.SetNRand( int(N.NRand) )
        gen_events.Use_protonAcceptacne( True )
        gen_events.Set_protonAcceptacne( h )
        gen_events.SetInputChain_eep()


    # event generation (and analysis) loop
    for run in generated_parameters.run.tolist():
        genMeanX    = genMeanY = 0
        genSigmaX   = genSigmaY = float(generated_parameters[generated_parameters.run==run].genSigmaX)
        genSigmaZa1 = float(generated_parameters[generated_parameters.run==run].genSigmaZa1)
        genSigmaZa2 = float(generated_parameters[generated_parameters.run==run].genSigmaZa2)
        genMeanZa1  = float(generated_parameters[generated_parameters.run==run].genMeanZa1)
        genMeanZa2  = float(generated_parameters[generated_parameters.run==run].genMeanZa2)
        if flags.verbose>2:
            print 'run:',run , genSigmaX , genSigmaZa1 , genSigmaZa2 , genMeanZa1 , genMeanZa2
            
        # (1) generate the simulated data (the 'run')
        # ----------------------------
        if 'generate' in option:
                            
            gen_events.Set_eep_Parameters( genMeanX , genSigmaX , genMeanY , genSigmaY , genMeanZa1 , genMeanZa2 , genSigmaZa1 , genSigmaZa2 )
            gen_events.DoGenerateRun_eepp( run )
                            
            # and now scheme them to our desired pp-SRC cuts
            ana_sim = TAnalysisEG2( path + '/eg_rootfiles', 'run%d'%run , ROOT.TCut('') )
            scheme.SchemeOnTCut( path + '/eg_rootfiles' , 'run%d.root'%run , "anaTree", 'run%d.root'%run , ana_sim.EGppSRCCut + ana_sim.PrecFiducial )
                            
            ana_sim.CloseFile()
            garbage_list = [ ana_sim ]
            del garbage_list
                    
                    
                    
        # (2) analyze the simulated data (the 'run') similarly to the data - reconstructed parameters
        # ----------------------------
        if 'analyze' in option or 'analyse' in option:
                            
            if debug>1: print "analyzing run %d"%run
            ana_sim = TAnalysisEG2( path + '/eg_rootfiles', 'run%d'%run , ROOT.TCut('') )
                
            evnt_loss_in_pmiss_multiples_bins = get_evnt_loss_in_pmiss_bins( pmiss_multiples_bins , evts_gen_in_pmiss_multiples_bins , ana_sim )

            if debug>4:
                reco_parameters = calc_cm_parameters( ana_sim  , PmissBins , CMRooFitsName( path + '/eg_cm_roofits/run%d_unweighted_'%run ), CMRooFitsName( path + '/eg_cm_roofits/run%d_weighted_'%run ) , True )
                fit_cm_parameters( run , reco_parameters , FigureFName( path + '/eg_cm_figures/run%d_'%run ) , True )
            
            # reconstruct c.m. parameters and fit
            reco_parameters = calc_cm_parameters( ana_sim  , PmissBins )
            reco_fits = fit_cm_parameters( run , reco_parameters )

            Pval_scores_12C  = get_Pval_scores( data_fits_12C   , reco_fits , '12C' )
            Pval_scores_27Al = get_Pval_scores( data_fits_27Al  , reco_fits , '27Al' )
            Pval_scores_56Fe = get_Pval_scores( data_fits_56Fe  , reco_fits , '56Fe' )
            Pval_scores_208Pb = get_Pval_scores( data_fits_208Pb, reco_fits , '208Pb' )

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
                                   
                                   ,'PvalSigmaX_unweighted_12C':float(Pval_scores_12C.PvalSigmaX_unweighted)               ,'PvalSigmaY_unweighted_12C':float(Pval_scores_12C.PvalSigmaY_unweighted)
                                   ,'PvalMeanZa1_unweighted_12C':float(Pval_scores_12C.PvalMeanZa1_unweighted)             ,'PvalMeanZa2_unweighted_12C':float(Pval_scores_12C.PvalMeanZa2_unweighted)
                                   ,'PvalSigmaZa1_unweighted_12C':float(Pval_scores_12C.PvalSigmaZa1_unweighted)           ,'PvalSigmaZa2_unweighted_12C':float(Pval_scores_12C.PvalSigmaZa2_unweighted)
                                   ,'PvalTotal_unweighted_12C':float(Pval_scores_12C.PvalTotal_unweighted)

                                   ,'PvalSigmaX_unweighted_27Al':float(Pval_scores_27Al.PvalSigmaX_unweighted)               ,'PvalSigmaY_unweighted_27Al':float(Pval_scores_27Al.PvalSigmaY_unweighted)
                                   ,'PvalMeanZa1_unweighted_27Al':float(Pval_scores_27Al.PvalMeanZa1_unweighted)             ,'PvalMeanZa2_unweighted_27Al':float(Pval_scores_27Al.PvalMeanZa2_unweighted)
                                   ,'PvalSigmaZa1_unweighted_27Al':float(Pval_scores_27Al.PvalSigmaZa1_unweighted)           ,'PvalSigmaZa2_unweighted_27Al':float(Pval_scores_27Al.PvalSigmaZa2_unweighted)
                                   ,'PvalTotal_unweighted_27Al':float(Pval_scores_27Al.PvalTotal_unweighted)

                                   ,'PvalSigmaX_unweighted_56Fe':float(Pval_scores_56Fe.PvalSigmaX_unweighted)               ,'PvalSigmaY_unweighted_56Fe':float(Pval_scores_56Fe.PvalSigmaY_unweighted)
                                   ,'PvalMeanZa1_unweighted_56Fe':float(Pval_scores_56Fe.PvalMeanZa1_unweighted)             ,'PvalMeanZa2_unweighted_56Fe':float(Pval_scores_56Fe.PvalMeanZa2_unweighted)
                                   ,'PvalSigmaZa1_unweighted_56Fe':float(Pval_scores_56Fe.PvalSigmaZa1_unweighted)           ,'PvalSigmaZa2_unweighted_56Fe':float(Pval_scores_56Fe.PvalSigmaZa2_unweighted)
                                   ,'PvalTotal_unweighted_56Fe':float(Pval_scores_56Fe.PvalTotal_unweighted)

                                   ,'PvalSigmaX_unweighted_208Pb':float(Pval_scores_208Pb.PvalSigmaX_unweighted)               ,'PvalSigmaY_unweighted_208Pb':float(Pval_scores_208Pb.PvalSigmaY_unweighted)
                                   ,'PvalMeanZa1_unweighted_208Pb':float(Pval_scores_208Pb.PvalMeanZa1_unweighted)             ,'PvalMeanZa2_unweighted_208Pb':float(Pval_scores_208Pb.PvalMeanZa2_unweighted)
                                   ,'PvalSigmaZa1_unweighted_208Pb':float(Pval_scores_208Pb.PvalSigmaZa1_unweighted)           ,'PvalSigmaZa2_unweighted_208Pb':float(Pval_scores_208Pb.PvalSigmaZa2_unweighted)
                                   ,'PvalTotal_unweighted_208Pb':float(Pval_scores_208Pb.PvalTotal_unweighted)

                                   # reconstructed fits - weighted by Mott+FF cross section
                                   ,'recMeanX_weighted':float(reco_fits.MeanX_weighted)         ,'recMeanY_weighted':float(reco_fits.MeanY_weighted)
                                   ,'recSigmaX_weighted':float(reco_fits.SigmaX_weighted)       ,'recSigmaY_weighted':float(reco_fits.SigmaY_weighted)
                                   ,'recMeanZa1_weighted':float(reco_fits.MeanZa1_weighted)     ,'recMeanZa2_weighted':float(reco_fits.MeanZa2_weighted)
                                   ,'recSigmaZa1_weighted':float(reco_fits.SigmaZa1_weighted)   ,'recSigmaZa2_weighted':float(reco_fits.SigmaZa2_weighted)
                                   
                                   ,'PvalSigmaX_weighted_12C':float(Pval_scores_12C.PvalSigmaX_weighted)               ,'PvalSigmaY_weighted_12C':float(Pval_scores_12C.PvalSigmaY_weighted)
                                   ,'PvalMeanZa1_weighted_12C':float(Pval_scores_12C.PvalMeanZa1_weighted)             ,'PvalMeanZa2_weighted_12C':float(Pval_scores_12C.PvalMeanZa2_weighted)
                                   ,'PvalSigmaZa1_weighted_12C':float(Pval_scores_12C.PvalSigmaZa1_weighted)           ,'PvalSigmaZa2_weighted_12C':float(Pval_scores_12C.PvalSigmaZa2_weighted)
                                   ,'PvalTotal_weighted_12C':float(Pval_scores_12C.PvalTotal_weighted)
                                   ,'PvalSigmaZa1SigmaZa2_12C':float(Pval_scores_12C.PvalSigmaZa1SigmaZa2)
                                   ,'PvalMeanZa1MeanZa2_12C':float(Pval_scores_12C.PvalMeanZa1MeanZa2)
                                   ,'PvalSigmaZa1MeanZa1_12C':float(Pval_scores_12C.PvalSigmaZa1MeanZa1)
                                   ,'PvalSigmaZa1MeanZa2_12C':float(Pval_scores_12C.PvalSigmaZa1MeanZa2)
                                   ,'PvalSigmaZa2MeanZa1_12C':float(Pval_scores_12C.PvalSigmaZa2MeanZa1)
                                   ,'PvalSigmaZa2MeanZa2_12C':float(Pval_scores_12C.PvalSigmaZa2MeanZa2)
                                   
                                   
                                   ,'PvalSigmaX_weighted_27Al':float(Pval_scores_27Al.PvalSigmaX_weighted)               ,'PvalSigmaY_weighted_27Al':float(Pval_scores_27Al.PvalSigmaY_weighted)
                                   ,'PvalMeanZa1_weighted_27Al':float(Pval_scores_27Al.PvalMeanZa1_weighted)             ,'PvalMeanZa2_weighted_27Al':float(Pval_scores_27Al.PvalMeanZa2_weighted)
                                   ,'PvalSigmaZa1_weighted_27Al':float(Pval_scores_27Al.PvalSigmaZa1_weighted)           ,'PvalSigmaZa2_weighted_27Al':float(Pval_scores_27Al.PvalSigmaZa2_weighted)
                                   ,'PvalTotal_weighted_27Al':float(Pval_scores_27Al.PvalTotal_weighted)
                                   ,'PvalSigmaZa1SigmaZa2_27Al':float(Pval_scores_27Al.PvalSigmaZa1SigmaZa2)
                                   ,'PvalMeanZa1MeanZa2_27Al':float(Pval_scores_27Al.PvalMeanZa1MeanZa2)
                                   ,'PvalSigmaZa1MeanZa1_27Al':float(Pval_scores_27Al.PvalSigmaZa1MeanZa1)
                                   ,'PvalSigmaZa1MeanZa2_27Al':float(Pval_scores_27Al.PvalSigmaZa1MeanZa2)
                                   ,'PvalSigmaZa2MeanZa1_27Al':float(Pval_scores_27Al.PvalSigmaZa2MeanZa1)
                                   ,'PvalSigmaZa2MeanZa2_27Al':float(Pval_scores_27Al.PvalSigmaZa2MeanZa2)
                                   
                                   
                                   
                                   ,'PvalSigmaX_weighted_56Fe':float(Pval_scores_56Fe.PvalSigmaX_weighted)               ,'PvalSigmaY_weighted_56Fe':float(Pval_scores_56Fe.PvalSigmaY_weighted)
                                   ,'PvalMeanZa1_weighted_56Fe':float(Pval_scores_56Fe.PvalMeanZa1_weighted)             ,'PvalMeanZa2_weighted_56Fe':float(Pval_scores_56Fe.PvalMeanZa2_weighted)
                                   ,'PvalSigmaZa1_weighted_56Fe':float(Pval_scores_56Fe.PvalSigmaZa1_weighted)           ,'PvalSigmaZa2_weighted_56Fe':float(Pval_scores_56Fe.PvalSigmaZa2_weighted)
                                   ,'PvalTotal_weighted_56Fe':float(Pval_scores_56Fe.PvalTotal_weighted)
                                   ,'PvalSigmaZa1SigmaZa2_56Fe':float(Pval_scores_56Fe.PvalSigmaZa1SigmaZa2)
                                   ,'PvalMeanZa1MeanZa2_56Fe':float(Pval_scores_56Fe.PvalMeanZa1MeanZa2)
                                   ,'PvalSigmaZa1MeanZa1_56Fe':float(Pval_scores_56Fe.PvalSigmaZa1MeanZa1)
                                   ,'PvalSigmaZa1MeanZa2_56Fe':float(Pval_scores_56Fe.PvalSigmaZa1MeanZa2)
                                   ,'PvalSigmaZa2MeanZa1_56Fe':float(Pval_scores_56Fe.PvalSigmaZa2MeanZa1)
                                   ,'PvalSigmaZa2MeanZa2_56Fe':float(Pval_scores_56Fe.PvalSigmaZa2MeanZa2)
                                   
                                   
                                   
                                   ,'PvalSigmaX_weighted_208Pb':float(Pval_scores_208Pb.PvalSigmaX_weighted)               ,'PvalSigmaY_weighted_208Pb':float(Pval_scores_208Pb.PvalSigmaY_weighted)
                                   ,'PvalMeanZa1_weighted_208Pb':float(Pval_scores_208Pb.PvalMeanZa1_weighted)             ,'PvalMeanZa2_weighted_208Pb':float(Pval_scores_208Pb.PvalMeanZa2_weighted)
                                   ,'PvalSigmaZa1_weighted_208Pb':float(Pval_scores_208Pb.PvalSigmaZa1_weighted)           ,'PvalSigmaZa2_weighted_208Pb':float(Pval_scores_208Pb.PvalSigmaZa2_weighted)
                                   ,'PvalTotal_weighted_208Pb':float(Pval_scores_208Pb.PvalTotal_weighted)
                                   ,'PvalSigmaZa1SigmaZa2_208Pb':float(Pval_scores_208Pb.PvalSigmaZa1SigmaZa2)
                                   ,'PvalMeanZa1MeanZa2_208Pb':float(Pval_scores_208Pb.PvalMeanZa1MeanZa2)
                                   ,'PvalSigmaZa1MeanZa1_208Pb':float(Pval_scores_208Pb.PvalSigmaZa1MeanZa1)
                                   ,'PvalSigmaZa1MeanZa2_208Pb':float(Pval_scores_208Pb.PvalSigmaZa1MeanZa2)
                                   ,'PvalSigmaZa2MeanZa1_208Pb':float(Pval_scores_208Pb.PvalSigmaZa2MeanZa1)
                                   ,'PvalSigmaZa2MeanZa2_208Pb':float(Pval_scores_208Pb.PvalSigmaZa2MeanZa2)
                                   
                                   
                                  
                                   # per 5 p(miss) bins
                                   
                                   ,'KSxPval':float(KS_scores.KSxPval)
                                   ,'KSyPval':float(KS_scores.KSyPval)
                                   ,'KSzPval':float(KS_scores.KSzPval)
                                   ,'KStPval':float(KS_scores.KStPval)
                                   ,'KSPval_tot':float(KS_scores.KSPval_tot)
                                   ,'KS3dHistPval':float(KS_scores.KS3dHistPval)
                                   
                                   # reconstructed parameters in p(miss) bins
                                   ,'PmissMin_PmBin0':float(reco_parameters.get_value(0,'pMiss_min')) ,'PmissMax_PmBin0':float(reco_parameters.get_value(0,'pMiss_max')) 
                                   ,'PmissMin_PmBin1':float(reco_parameters.get_value(1,'pMiss_min')) ,'PmissMax_PmBin1':float(reco_parameters.get_value(1,'pMiss_max')) 
                                   ,'PmissMin_PmBin2':float(reco_parameters.get_value(2,'pMiss_min')) ,'PmissMax_PmBin2':float(reco_parameters.get_value(2,'pMiss_max')) 
                                   ,'PmissMin_PmBin3':float(reco_parameters.get_value(3,'pMiss_min')) ,'PmissMax_PmBin3':float(reco_parameters.get_value(3,'pMiss_max')) 
                                   ,'PmissMin_PmBin4':float(reco_parameters.get_value(4,'pMiss_min')) ,'PmissMax_PmBin4':float(reco_parameters.get_value(4,'pMiss_max')) 
                                   # x
                                   ,'recMeanX_unweighted_PmBin0':float(reco_parameters.get_value(0,'mean_x_unweighted')) 
                                   ,'recSigmaX_unweighted_PmBin0':float(reco_parameters.get_value(0,'sigma_x_unweighted')) 
                                   ,'recMeanX_unweighted_PmBin1':float(reco_parameters.get_value(1,'mean_x_unweighted')) 
                                   ,'recSigmaX_unweighted_PmBin1':float(reco_parameters.get_value(1,'sigma_x_unweighted')) 
                                   ,'recMeanX_unweighted_PmBin2':float(reco_parameters.get_value(2,'mean_x_unweighted')) 
                                   ,'recSigmaX_unweighted_PmBin2':float(reco_parameters.get_value(2,'sigma_x_unweighted')) 
                                   ,'recMeanX_unweighted_PmBin3':float(reco_parameters.get_value(3,'mean_x_unweighted')) 
                                   ,'recSigmaX_unweighted_PmBin3':float(reco_parameters.get_value(3,'sigma_x_unweighted')) 
                                   ,'recMeanX_unweighted_PmBin4':float(reco_parameters.get_value(4,'mean_x_unweighted')) 
                                   ,'recSigmaX_unweighted_PmBin4':float(reco_parameters.get_value(4,'sigma_x_unweighted')) 
                                   # y
                                   ,'recMeanY_unweighted_PmBin0':float(reco_parameters.get_value(0,'mean_y_unweighted')) 
                                   ,'recSigmaY_unweighted_PmBin0':float(reco_parameters.get_value(0,'sigma_y_unweighted')) 
                                   ,'recMeanY_unweighted_PmBin1':float(reco_parameters.get_value(1,'mean_y_unweighted')) 
                                   ,'recSigmaY_unweighted_PmBin1':float(reco_parameters.get_value(1,'sigma_y_unweighted')) 
                                   ,'recMeanY_unweighted_PmBin2':float(reco_parameters.get_value(2,'mean_y_unweighted')) 
                                   ,'recSigmaY_unweighted_PmBin2':float(reco_parameters.get_value(2,'sigma_y_unweighted')) 
                                   ,'recMeanY_unweighted_PmBin3':float(reco_parameters.get_value(3,'mean_y_unweighted')) 
                                   ,'recSigmaY_unweighted_PmBin3':float(reco_parameters.get_value(3,'sigma_y_unweighted')) 
                                   ,'recMeanY_unweighted_PmBin4':float(reco_parameters.get_value(4,'mean_y_unweighted')) 
                                   ,'recSigmaY_unweighted_PmBin4':float(reco_parameters.get_value(4,'sigma_y_unweighted')) 
                                   # z
                                   ,'recMeanZ_unweighted_PmBin0':float(reco_parameters.get_value(0,'mean_z_unweighted')) 
                                   ,'recSigmaZ_unweighted_PmBin0':float(reco_parameters.get_value(0,'sigma_z_unweighted')) 
                                   ,'recMeanZ_unweighted_PmBin1':float(reco_parameters.get_value(1,'mean_z_unweighted')) 
                                   ,'recSigmaZ_unweighted_PmBin1':float(reco_parameters.get_value(1,'sigma_z_unweighted')) 
                                   ,'recMeanZ_unweighted_PmBin2':float(reco_parameters.get_value(2,'mean_z_unweighted')) 
                                   ,'recSigmaZ_unweighted_PmBin2':float(reco_parameters.get_value(2,'sigma_z_unweighted')) 
                                   ,'recMeanZ_unweighted_PmBin3':float(reco_parameters.get_value(3,'mean_z_unweighted')) 
                                   ,'recSigmaZ_unweighted_PmBin3':float(reco_parameters.get_value(3,'sigma_z_unweighted')) 
                                   ,'recMeanZ_unweighted_PmBin4':float(reco_parameters.get_value(4,'mean_z_unweighted')) 
                                   ,'recSigmaZ_unweighted_PmBin4':float(reco_parameters.get_value(4,'sigma_z_unweighted'))
                                   
                                   
                                   # events loss
                                   ,'NLostEvents':(9907*float(N.NRand) - ana_sim.GetEntries())
                                   ,'fracLostEvents':(float((9907.0*float(N.NRand)) - ana_sim.GetEntries())/(9907.0*float(N.NRand)))
                                   # events loss in 20 p(miss) bins, for pp/p analysis
                                   ,'fracLoss_pmiss_%.3f_%.3f'%(pmiss_multiples_bins[0][0],pmiss_multiples_bins[0][1]):evnt_loss_in_pmiss_multiples_bins[0]
                                   ,'fracLoss_pmiss_%.3f_%.3f'%(pmiss_multiples_bins[1][0],pmiss_multiples_bins[1][1]):evnt_loss_in_pmiss_multiples_bins[1]
                                   ,'fracLoss_pmiss_%.3f_%.3f'%(pmiss_multiples_bins[2][0],pmiss_multiples_bins[2][1]):evnt_loss_in_pmiss_multiples_bins[2]
                                   ,'fracLoss_pmiss_%.3f_%.3f'%(pmiss_multiples_bins[3][0],pmiss_multiples_bins[3][1]):evnt_loss_in_pmiss_multiples_bins[3]
                                   ,'fracLoss_pmiss_%.3f_%.3f'%(pmiss_multiples_bins[4][0],pmiss_multiples_bins[4][1]):evnt_loss_in_pmiss_multiples_bins[4]
                                   ,'fracLoss_pmiss_%.3f_%.3f'%(pmiss_multiples_bins[5][0],pmiss_multiples_bins[5][1]):evnt_loss_in_pmiss_multiples_bins[5]
                                   ,'fracLoss_pmiss_%.3f_%.3f'%(pmiss_multiples_bins[6][0],pmiss_multiples_bins[6][1]):evnt_loss_in_pmiss_multiples_bins[6]
                                   ,'fracLoss_pmiss_%.3f_%.3f'%(pmiss_multiples_bins[7][0],pmiss_multiples_bins[7][1]):evnt_loss_in_pmiss_multiples_bins[7]
                                   ,'fracLoss_pmiss_%.3f_%.3f'%(pmiss_multiples_bins[8][0],pmiss_multiples_bins[8][1]):evnt_loss_in_pmiss_multiples_bins[8]
                                   ,'fracLoss_pmiss_%.3f_%.3f'%(pmiss_multiples_bins[9][0],pmiss_multiples_bins[9][1]):evnt_loss_in_pmiss_multiples_bins[9]
                                   ,'fracLoss_pmiss_%.3f_%.3f'%(pmiss_multiples_bins[10][0],pmiss_multiples_bins[10][1]):evnt_loss_in_pmiss_multiples_bins[10]
                                   ,'fracLoss_pmiss_%.3f_%.3f'%(pmiss_multiples_bins[11][0],pmiss_multiples_bins[11][1]):evnt_loss_in_pmiss_multiples_bins[11]
                                   ,'fracLoss_pmiss_%.3f_%.3f'%(pmiss_multiples_bins[12][0],pmiss_multiples_bins[12][1]):evnt_loss_in_pmiss_multiples_bins[12]
                                   ,'fracLoss_pmiss_%.3f_%.3f'%(pmiss_multiples_bins[13][0],pmiss_multiples_bins[13][1]):evnt_loss_in_pmiss_multiples_bins[13]
                                   ,'fracLoss_pmiss_%.3f_%.3f'%(pmiss_multiples_bins[14][0],pmiss_multiples_bins[14][1]):evnt_loss_in_pmiss_multiples_bins[14]
                                   ,'fracLoss_pmiss_%.3f_%.3f'%(pmiss_multiples_bins[15][0],pmiss_multiples_bins[15][1]):evnt_loss_in_pmiss_multiples_bins[15]
                                   ,'fracLoss_pmiss_%.3f_%.3f'%(pmiss_multiples_bins[16][0],pmiss_multiples_bins[16][1]):evnt_loss_in_pmiss_multiples_bins[16]
                                   ,'fracLoss_pmiss_%.3f_%.3f'%(pmiss_multiples_bins[17][0],pmiss_multiples_bins[17][1]):evnt_loss_in_pmiss_multiples_bins[17]
                                   ,'fracLoss_pmiss_%.3f_%.3f'%(pmiss_multiples_bins[18][0],pmiss_multiples_bins[18][1]):evnt_loss_in_pmiss_multiples_bins[18]
                                   ,'fracLoss_pmiss_%.3f_%.3f'%(pmiss_multiples_bins[19][0],pmiss_multiples_bins[19][1]):evnt_loss_in_pmiss_multiples_bins[19]

                                   }
                                   , index = [int(run)])
                # ----------------------------
                


            if do_reco_fits_file:   stream_dataframe_to_file( reco_fits, reco_fitsFName  )
            if do_resutls_file:     stream_dataframe_to_file( results, buildup_resutlsFName , float_format='%.4f' )
            if do_root_file:        stream_dataframe_to_root( results, root_resutlsFName, 'ppSRCsimanaTree')

            ana_sim.CloseFile()
            if debug>1:
                print "appended into pandas.DataFrames"
                if debug>4: print "results: ",results

            garbage_list = [ ana_sim , reco_parameters , reco_fits  , results ]
            del garbage_list
                    
        print_important( "completed run %d"%run )
        print_line()



    if 'generate' in option:
        gen_events.ReleaseInputChain_eep()
    
    if 'analyze' in option:
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



