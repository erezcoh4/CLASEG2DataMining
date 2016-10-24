import time , sys , os , math , datetime , ROOT
import matplotlib , pandas as pd , numpy as np
import matplotlib as mpl , seaborn as sns; sns.set(style="white", color_codes=True , font_scale=1)
from matplotlib import pyplot as plt
from ROOT import TAnalysis, TAnalysisEG2, GenerateEvents, TSchemeDATA
from root_numpy import hist2array , tree2array
from scipy.stats import ks_2samp
from math import sqrt
sys.path.insert(0, '/Users/erezcohen/larlite/UserDev/mySoftware/MySoftwarePackage/mac')
import GeneralPlot as gp
import gc
analysis = TAnalysis()
scheme = TSchemeDATA()

# ------------------------------------------------------------------------------- #
# definitions
cm_pars_columns = ['pMiss_min','pMiss_max'
                   ,'mean_x_unweighted','mean_xErr_unweighted','sigma_x_unweighted','sigma_xErr_unweighted'
                   ,'mean_y_unweighted','mean_yErr_unweighted','sigma_y_unweighted','sigma_yErr_unweighted'
                   ,'mean_t_unweighted','mean_tErr_unweighted','sigma_t_unweighted','sigma_tErr_unweighted'
                   ,'mean_z_unweighted','mean_zErr_unweighted','sigma_z_unweighted','sigma_zErr_unweighted'
                   ,'mean_x_weighted','mean_xErr_weighted','sigma_x_weighted','sigma_xErr_weighted'
                   ,'mean_y_weighted','mean_yErr_weighted','sigma_y_weighted','sigma_yErr_weighted'
                   ,'mean_t_weighted','mean_tErr_weighted','sigma_t_weighted','sigma_tErr_weighted'
                   ,'mean_z_weighted','mean_zErr_weighted','sigma_z_weighted','sigma_zErr_weighted']

fits_columns = [ 'run'
                ,'sX_unweighted','sXerr_unweighted','sY_unweighted','sYerr_unweighted','sT_unweighted','sTerr_unweighted'
                ,'sZa1_unweighted','sZa1err_unweighted','sZa2_unweighted','sZa2err_unweighted'
                ,'mX_unweighted','mXerr_unweighted','mY_unweighted','mYerr_unweighted'
                ,'mZa1_unweighted','mZa1err_unweighted','mZa2_unweighted','mZa2err_unweighted'
                ,'sX_weighted','sXerr_weighted','sY_weighted','sYerr_weighted'
                ,'sZa1_weighted','sZa1err_weighted','sZa2_weighted','sZa2err_weighted'
                ,'mX_weighted','mXerr_weighted','mY_weighted','mYerr_weighted'
                ,'mZa1_weighted','mZa1err_weighted','mZa2_weighted','mZa2err_weighted']

bands_columns = ['sTBandMin','sTBandMax'
                 ,'sZa1Min','sZa1Max'
                 ,'sZa2Min','sZa2Max'
                 ,'mZa1Min','mZa1Max'
                 ,'mZa2Min','mZa2Max']


results_columns = ['run','time'
                   ,'genSigmaT','genSigmaL_a1','genSigmaL_a2','genShiftL_a1','genShiftL_a2'
                   ,'recSigmaT_unweighted','recSigmaTErr_unweighted'
                   ,'recSigmaL_a1_unweighted','recSigmaL_a1Err_unweighted','recSigmaL_a2_unweighted','recSigmaL_a2Err_unweighted','recShiftL_a1_unweighted','recShiftL_a1Err_unweighted','recShiftL_a2_unweighted','recShiftL_a2Err_unweighted'
                   ,'NsigST_unweighted','NsigSL_a1_unweighted','NsigSL_a2_unweighted','NsigML_a1_unweighted','NsigML_a2_unweighted','NsigAvg_unweighted'
                   ,'recSigmaT_weighted','recSigmaTErr_weighted'
                   ,'recSigmaL_a1_weighted','recSigmaL_a1Err_weighted','recSigmaL_a2_weighted','recSigmaL_a2Err_weighted','recShiftL_a1_weighted','recShiftL_a1Err_weighted','recShiftL_a2_weighted','recShiftL_a2Err_weighted'
                   ,'NsigST_weighted','NsigSL_a1_weighted','NsigSL_a2_weighted','NsigML_a1_weighted','NsigML_a2_weighted','NsigAvg_weighted'
#                   ,'KSxPval','KSyPval','KStPval','KSzPval']
                   ,'KSxPval_0','KSxPval_1','KSxPval_2','KSxPval_3','KSxPval_4','KSxPval_avg'
                   ,'KSyPval_0','KSyPval_1','KSyPval_2','KSyPval_3','KSyPval_4','KSyPval_avg'
                   ,'KStPval_0','KStPval_1','KStPval_2','KStPval_3','KStPval_4','KStPval_avg'
                   ,'KSzPval_0','KSzPval_1','KSzPval_2','KSzPval_3','KSzPval_4','KSzPval_avg']



# prints
def print_line(): print '\033[93m' + '--------------------------------------------------------------' + '\033[0m'
def print_important(string): print '\033[94m' + '\033[1m' + string + '\033[0m' ; print_line
def print_filename(filename,action_on_file=""): print action_on_file + '\n' + '\033[91m' + filename + '\033[0m'

# file names
def CMParsFname( path ):
    return path+"CMparameters.csv"
def CMRooFitsName( path ):
    return path+"CMRooFits.pdf"
def CMfitsFname( path ):
    return path+"CMfits.csv"
def CMBandFname( path ):
    return path+"CMparameter_Bands.csv"
def FigureFName( path ):
    return path+"cm_width_and_mean.pdf"
def FigureBandFName( path ):
    return path+"cm_width_and_mean_Bands.pdf"
def resutlsFName( path ):
    return path+"EG_simulated_runs_results_cm_parameters.csv"

# computations
# ------------------------------------------------------------------------------- #
def Nsigma( v1 , v1Err , v2 , v2Err):
    return math.fabs( v1 - v2 )/math.sqrt( v1Err*v1Err + v2Err*v2Err )

def NsigmaScore( dataset1 , dataset2  , var   , weighting ):
    return Nsigma( dataset1[var+'_'+weighting] , dataset1[var+'err_'+weighting]  , dataset2[var+'_'+weighting] , dataset2[var+'err_'+weighting] )


# ------------------------------------------------------------------------------- #
def KStest( PmissBins , ana_sim , ana_data , var , cut=ROOT.TCut() , debug=2 , Nbins=20):
    # [http://docs.scipy.org/doc/scipy-0.15.1/reference/generated/scipy.stats.ks_2samp.html]
    KS_distances , Pval_KS = [] , []
    figure = plt.figure(figsize=[60,20])
    for i in range(len(PmissBins)):
        pMiss_min , pMiss_max = PmissBins[i][0] , PmissBins[i][1]
        reduced_data = tree2array(ana_data.GetTree(),branches=var , selection = '%f < Pmiss3Mag && Pmiss3Mag < %f'%(pMiss_min , pMiss_max) )
        reduced_sim = tree2array(ana_sim.GetTree(),branches=var , selection = '%f < Pmiss3Mag && Pmiss3Mag < %f'%(pMiss_min , pMiss_max))
        D , Pvalue = ks_2samp( reduced_sim , reduced_data )

        if ( debug > 1 ):
            ax = figure.add_subplot(len(PmissBins)/2,3,i+1)
            for array,col in zip([reduced_sim , reduced_data],['black','red']):
                g=sns.distplot( array, bins=np.linspace(-1, 2 , Nbins), ax=ax, color=col , axlabel=var )
            g.axes.set_title(r'%.2f < p$_{miss}$ < %.2f GeV/c'%(pMiss_min , pMiss_max), fontsize=34,color="b")
            print_important( "KS test of data vs. simulation for %s in p(miss) bin %d is D = %f, Pvalue = %f"%(var , i , D , Pvalue) )
    
        KS_distances.append(D)
        Pval_KS.append(Pvalue)

    figure.savefig("/Users/erezcohen/Desktop/cmHistos_%s.pdf"%var)

    return KS_distances , Pval_KS


# ------------------------------------------------------------------------------- #
def plot_errorbar_and_fit( ax , x , y , xerr , yerr , color , marker , lstyle , label , fit_type='const' ):
    plt.errorbar(x, y, xerr=xerr, yerr=yerr, color=color, marker=marker , linestyle=lstyle , label=None , markersize=15)
    if fit_type=='const':
        const_fit , const_fitErr = fit_as_a_function_of_pmiss( x , y , fit_type )
        ax.plot(x, np.ones(len(x))*const_fit , color=color , linestyle='--', linewidth = 2 , label=label + "$=%.3f\pm%.3f$"%(const_fit,const_fitErr))
        return [ const_fit , const_fitErr ]
    
    elif fit_type=='linear':
        a1 , a1err , a2 , a2err  = fit_as_a_function_of_pmiss( x , y , fit_type )
        ax.plot( x , a1 * x + a2 , color = color , label=label + "$=(%.2f)p_{miss}+(%.2f)$"%( a1 , a2 ))
        return [ a1 , a1err] , [ a2 , a2err ]

# ------------------------------------------------------------------------------- #
def fit_as_a_function_of_pmiss( x , y , fit_type='const' ): # same as plot_errorbar_and_fit without plot
    if fit_type=='const':
        p1,v1 = np.polyfit( x , y , 0 , cov=True)
        return p1[0] , sqrt(v1[0][0])
    elif fit_type=='linear':
        p2,v2 = np.polyfit( x , y , 1 , cov=True)        # fit a polynomial p2(x) = p2[0] * x + p2[1]
        return p2[0] , sqrt(v2[0][0]) , p2[1] , sqrt(v2[1][1])

# ------------------------------------------------------------------------------- #
def calc_cm_parameters( fana  , PmissBins , unweightedRoofitsFName = '' , weightedRoofitsFName = '' , DoSaveCanvas = False ):
    df_pMissBins = pd.DataFrame(columns=cm_pars_columns)
    
    if DoSaveCanvas:
        canvas_unweighted , canvas_weighted = fana.CreateCanvas( "RooFit plots - unweighted" , "Divide" , 4 , len(PmissBins) ) , fana.CreateCanvas( "RooFit plots - weighted" , "Divide" , 4 , len(PmissBins) )

    for i in range(len(PmissBins)):
        pMiss_min , pMiss_max = PmissBins[i][0] , PmissBins[i][1]

        if DoSaveCanvas:
            unweighted = fana.RooFitCM( pMiss_min , pMiss_max , False , True, canvas_unweighted, 4*i + 1 )
            weighted = fana.RooFitCM( pMiss_min , pMiss_max , True , True, canvas_weighted, 4*i + 1 )
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
    print "computed cm parameters for "+fana.InFileName
    return df_pMissBins



# ------------------------------------------------------------------------------- #
def set_frame( ax , title , xlabel , ylabel , legend_location="upper left" ):

    plt.title( title ,fontsize=25)
    plt.xlabel( xlabel,fontsize=25)
    plt.ylabel( ylabel,fontsize=25)
    ax.tick_params(axis='both', which='major', labelsize=25)
    ax.legend(loc=legend_location,scatterpoints=1,fontsize=25)


# ------------------------------------------------------------------------------- #
def fit_par_plot( fig , i_subplot , data , var , weight , title ): # a sub-routine to fit a single parameter

    Pmiss = (data.pMiss_max + data.pMiss_min)/2.
    pMissUpErr , pMissLowErr = data.pMiss_max - Pmiss , Pmiss - data.pMiss_min
    ax = fig.add_subplot( i_subplot )
    ax.grid(True,linestyle='-',color='0.95')
    [Xfit,XfitErr] = plot_errorbar_and_fit( ax , Pmiss, data[ var + '_x_' + weight] , [pMissLowErr,pMissUpErr] , [data[ var + '_xErr_' + weight ],data[ var + '_xErr_' + weight ]], 'black','v','none',r'$%s_{x}$'%title ,'const')
    [Yfit,YfitErr] = plot_errorbar_and_fit( ax , Pmiss, data[ var + '_y_' + weight] , [pMissLowErr,pMissUpErr] , [data[ var + '_yErr_' + weight ],data[ var + '_yErr_' + weight ]], 'red'  ,'o','none',r'$%s_{y}$'%title ,'const')
    [Tfit,TfitErr] = plot_errorbar_and_fit( ax , Pmiss, data[ var + '_t_' + weight] , [pMissLowErr,pMissUpErr] , [data[ var + '_tErr_' + weight ],data[ var + '_tErr_' + weight ]], 'green','^','none',r'$%s_{\perp}$'%title ,'const')
    #    Tfit , TfitErr = 0.5*(Xfit + Yfit) ,  math.sqrt(XfitErr*XfitErr + YfitErr*YfitErr)
    [Za1,Za1err],[Za2,Za2err] = plot_errorbar_and_fit( ax , Pmiss, data[ var + '_z_' + weight] , [pMissLowErr,pMissUpErr] , [data[ var + '_zErr_' + weight ],data[ var + '_zErr_' + weight ]], 'blue' ,'s','none',r'$%s_{\vec{p}_{miss}}$'%title ,'linear')
    set_frame( ax , r'%s $%s$'%(weight,title) , r'$p_{miss}$ [GeV/c]' , r'c.m. momentum $%s$ [Gev/c]'%title , "upper left")
    return Xfit , XfitErr , Yfit , YfitErr , Tfit , TfitErr, Za1 , Za1err , Za2 , Za2err

# ------------------------------------------------------------------------------- #
def fit_par_noplot( data , var , weight , title ): # a sub-routine to fit a single parameter; same as fit_par_plot without a plot
    
    Pmiss = (data.pMiss_max + data.pMiss_min)/2.
    pMissUpErr , pMissLowErr = data.pMiss_max - Pmiss , Pmiss - data.pMiss_min
    Xfit,XfitErr = fit_as_a_function_of_pmiss( Pmiss, data[ var + '_x_' + weight] ,'const')
    Yfit,YfitErr = fit_as_a_function_of_pmiss( Pmiss, data[ var + '_y_' + weight] ,'const')
    Tfit,TfitErr = fit_as_a_function_of_pmiss( Pmiss, data[ var + '_t_' + weight] ,'const')
    #    Tfit , TfitErr = 0.5*(Xfit + Yfit) ,  math.sqrt(XfitErr*XfitErr + YfitErr*YfitErr)
    Za1,Za1err,Za2,Za2err = fit_as_a_function_of_pmiss( Pmiss, data[ var + '_z_' + weight] , 'linear' )
    return Xfit , XfitErr , Yfit , YfitErr , Tfit , TfitErr, Za1 , Za1err , Za2 , Za2err



# ------------------------------------------------------------------------------- #
def fit_cm_parameters( run , data , FigureFName = '' , DoSaveCanvas = False ): # all parameters

    if DoSaveCanvas: # this means we want plots
        fig = plt.figure(figsize=(40,20)) # four plots, two unweighted and two weighted
        sX_unweighted, sXerr_unweighted, sY_unweighted, sYerr_unweighted, sT_unweighted, sTerr_unweighted, sZa1_unweighted, sZa1err_unweighted, sZa2_unweighted, sZa2err_unweighted = fit_par_plot ( fig , 221, data , 'sigma', 'unweighted' , '\sigma' )
        mX_unweighted, mXerr_unweighted, mY_unweighted, mYerr_unweighted, mT_unweighted, mTerr_unweighted, mZa1_unweighted, mZa1err_unweighted, mZa2_unweighted, mZa2err_unweighted = fit_par_plot( fig , 222, data , 'mean' , 'unweighted' , 'mean'   )
        sX_weighted, sXerr_weighted, sY_weighted, sYerr_weighted, sT_weighted, sTerr_weighted, sZa1_weighted, sZa1err_weighted, sZa2_weighted, sZa2err_weighted = fit_par_plot( fig , 223, data , 'sigma', 'weighted' , '\sigma' )
        mX_weighted, mXerr_weighted, mY_weighted, mYerr_weighted, mT_weighted, mTerr_weighted, mZa1_weighted, mZa1err_weighted, mZa2_weighted, mZa2err_weighted = fit_par_plot( fig , 224, data , 'mean' , 'weighted' , 'mean'   )
    else:
        sX_unweighted, sXerr_unweighted, sY_unweighted, sYerr_unweighted, sT_unweighted, sTerr_unweighted, sZa1_unweighted, sZa1err_unweighted, sZa2_unweighted, sZa2err_unweighted = fit_par_noplot ( data , 'sigma', 'unweighted' , '\sigma' )
        mX_unweighted, mXerr_unweighted, mY_unweighted, mYerr_unweighted, mT_unweighted, mTerr_unweighted, mZa1_unweighted, mZa1err_unweighted, mZa2_unweighted, mZa2err_unweighted = fit_par_noplot( data , 'mean' , 'unweighted' , 'mean'    )
        sX_weighted, sXerr_weighted, sY_weighted, sYerr_weighted, sT_weighted, sTerr_weighted, sZa1_weighted, sZa1err_weighted, sZa2_weighted, sZa2err_weighted = fit_par_noplot( data , 'sigma', 'weighted' , '\sigma' )
        mX_weighted, mXerr_weighted, mY_weighted, mYerr_weighted, mT_weighted, mTerr_weighted, mZa1_weighted, mZa1err_weighted, mZa2_weighted, mZa2err_weighted = fit_par_noplot( data , 'mean' , 'weighted' , 'mean'   )

    df_fit_parameters = pd.DataFrame({ 'run':run
                                     ,'sX_unweighted':sX_unweighted,'sXerr_unweighted':sXerr_unweighted,'sY_unweighted':sY_unweighted,'sYerr_unweighted':sYerr_unweighted,'sT_unweighted':sT_unweighted,'sTerr_unweighted':sTerr_unweighted
                                     ,'sZa1_unweighted':sZa1_unweighted,'sZa1err_unweighted':sZa1err_unweighted,'sZa2_unweighted':sZa2_unweighted,'sZa2err_unweighted':sZa2err_unweighted
                                     ,'mX_unweighted':mX_unweighted,'mXerr_unweighted':mXerr_unweighted,'mY_unweighted':mY_unweighted,'mYerr_unweighted':mYerr_unweighted
                                     ,'mZa1_unweighted':mZa1_unweighted,'mZa1err_unweighted':mZa1err_unweighted,'mZa2_unweighted':mZa2_unweighted,'mZa2err_unweighted':mZa2err_unweighted
                                     ,'sX_weighted':sX_weighted,'sXerr_weighted':sXerr_weighted,'sY_weighted':sY_weighted,'sYerr_weighted':sYerr_weighted,'sT_weighted':sY_weighted,'sTerr_weighted':sYerr_weighted
                                     ,'sZa1_weighted':sZa1_weighted,'sZa1err_weighted':sZa1err_weighted,'sZa2_weighted':sZa2_weighted,'sZa2err_weighted':sZa2err_weighted
                                     ,'mX_weighted':mX_weighted,'mXerr_weighted':mXerr_weighted,'mY_weighted':mY_weighted,'mYerr_weighted':mYerr_weighted
                                     ,'mZa1_weighted':mZa1_weighted,'mZa1err_weighted':mZa1err_weighted,'mZa2_weighted':mZa2_weighted,'mZa2err_weighted':mZa2err_weighted } , index=[0] )
    if DoSaveCanvas:
        plt.savefig(FigureFName)
        print_filename( FigureFName , "and plot can be found at" )
    print "computed fit parameters for ",run 
    return df_fit_parameters


# ------------------------------------------------------------------------------- #
def plot_band_around_cm_parameter_fits( fig , i_subplot , data , var , weight , title  , TBandMin , TBandMax , ZBandMin , ZBandMax ):

    Pmiss = (data.pMiss_max + data.pMiss_min)/2.
    pMissUpErr , pMissLowErr = data.pMiss_max - Pmiss , Pmiss - data.pMiss_min

    fit_par_plot( fig , i_subplot , data , var , weight , title )
    plt.fill_between(Pmiss, TBandMin , TBandMax ,alpha=0.5, edgecolor='#CC4F1B', facecolor='#FF9848')
    plt.fill_between(Pmiss, ZBandMin , ZBandMax ,alpha=0.5, edgecolor='#C14F1B', facecolor='#1122CC')


# ------------------------------------------------------------------------------- #
def generate_cm_bands( cm_parameters , fit_pars , CMBandFname , FigureBandFName , DoSaveCanvas = False ):
 
    df = pd.DataFrame(columns=bands_columns)
    Pmiss = (cm_parameters.pMiss_max + cm_parameters.pMiss_min)/2.

    #    sTBand = np.ones(len(Pmiss))*[fit_pars.sT_unweighted*0.9,fit_pars.sT_unweighted*1.1]
    min_sXY , max_sXY = 0.9*np.min( [fit_pars.sX_unweighted , fit_pars.sY_unweighted] ) , 1.1*np.max( [fit_pars.sX_unweighted,fit_pars.sY_unweighted] )
    sTBandMin   , sTBandMax     = min_sXY , max_sXY
    sZa1BandMin , sZa1BandMax   = fit_pars.sZa1_unweighted*0.9,fit_pars.sZa1_unweighted*1.1
    sZa2BandMin , sZa2BandMax   = fit_pars.sZa2_unweighted*0.9,fit_pars.sZa2_unweighted*1.1
    sZBandMax = float(sZa1BandMax)*(Pmiss)+float(sZa2BandMax)
    sZBandMin = float(sZa1BandMin)*(Pmiss)+float(sZa2BandMin)

    mTBandMin   , mTBandMax     = np.zeros(len(Pmiss)) , np.zeros(len(Pmiss))
    mZa1BandMin , mZa1BandMax   = fit_pars.mZa1_unweighted*0.7,fit_pars.mZa1_unweighted*1.3
    mZa2BandMin , mZa2BandMax   = fit_pars.mZa2_unweighted*0.7,fit_pars.mZa2_unweighted*1.3
    mZBandMax = float(mZa1BandMax)*(Pmiss)+float(mZa2BandMax)
    mZBandMin = float(mZa1BandMin)*(Pmiss)+float(mZa2BandMin)

    if DoSaveCanvas:
        fig = plt.figure(figsize=(40,10))
        plot_band_around_cm_parameter_fits( fig , 121, cm_parameters , 'sigma', 'unweighted' , '\sigma' , sTBandMin , sTBandMax , sZBandMin , sZBandMax  )
        plot_band_around_cm_parameter_fits( fig , 122, cm_parameters , 'mean', 'unweighted' , 'mean' , mTBandMin , mTBandMax , mZBandMin , mZBandMax  )
        plt.savefig(FigureBandFName)
        print_filename( FigureBandFName , "plots to file" )

    df_bands = pd.DataFrame({'sTBandMin':sTBandMin,'sTBandMax':sTBandMax
                            ,'sZa1Min':sZa1BandMin,'sZa1Max':sZa1BandMax
                            ,'sZa2Min':sZa2BandMin,'sZa2Max':sZa2BandMax
                            ,'mZa1Min':mZa1BandMin,'mZa1Max':mZa1BandMax
                            ,'mZa2Min':mZa2BandMin,'mZa2Max':mZa2BandMax},index=[0])
    df = df.append(df_bands)
    df.to_csv( CMBandFname , header=True , index = False)
    print_filename( CMBandFname , "wrote bands around cm paramters fits to" )
    print_line()


# ------------------------------------------------------------------------------- #
# deprecated....
#def linspace_single_core( band_min  , band_max  , NptsBand , Ncores , i_core ):
#    tmp_min = np.min( [band_min , band_max] )
#    band_max = np.max( [band_min , band_max] )
#    band_min = tmp_min
#    step = math.fabs(band_max - band_min)/NptsBand#Ncores
#    min = band_min + (float(i_core)/Ncores)*(band_max - band_min)
#    max = min + float(band_max - band_min)/Ncores
#    print min , max , step
#    res = np.arange( min , max , step )
#    return res




# ------------------------------------------------------------------------------- #
#def generate_runs_with_different_parameters( cm_fits_parameters , cm_pars_bands ,
def generate_runs_with_different_parameters( option,
                                            data_fits , bands , NRand ,
                                            start_run , debug , PmissBins , resutlsFName , reco_fitsFName , target ,
                                            NptsBand , Ncores = 1 , i_core = 0 ):
    
    # the data (nominal values)
    ana_data = TAnalysisEG2( "ppSRCCut_DATA_%s"% target )
    path = "/Users/erezcohen/Desktop/DataMining/Analysis_DATA/ppSRCcm"


    # simulation pandas::DataFrame
    df_reco_parameters = pd.DataFrame(columns=cm_pars_columns)
    df_reco_fits = pd.DataFrame(columns=fits_columns)
    df_results = pd.DataFrame(columns=results_columns)


    # the bands around data (around nominal values)
#    sigT    = linspace_single_core( bands.sTBandMin[0],bands.sTBandMax[0] , NptsBand , Ncores , i_core )
#    sigLa1  = linspace_single_core( bands.sZa1Min[0]  ,bands.sZa1Max[0]   , NptsBand , Ncores , i_core )
#    sigLa2  = linspace_single_core( bands.sZa2Min[0]  ,bands.sZa2Max[0]   , NptsBand , Ncores , i_core )
#    meanLa1 = linspace_single_core( bands.mZa1Min[0]  ,bands.mZa1Max[0]   , NptsBand , Ncores , i_core )
#    meanLa2 = linspace_single_core( bands.mZa2Min[0]  ,bands.mZa2Max[0]   , NptsBand , Ncores , i_core )
    sigT    = np.linspace( bands.sTBandMin[0]   + (bands.sTBandMax[0] - bands.sTBandMin[0]) / (NptsBand+1)  , bands.sTBandMax[0] , NptsBand , endpoint=False)
    sigLa1  = np.linspace( bands.sZa1Min[0]     + (bands.sZa1Max[0] - bands.sZa1Min[0]) / (NptsBand+1)      , bands.sZa1Max[0]   , NptsBand , endpoint=False)
    sigLa2  = np.linspace( bands.sZa2Min[0]     + (bands.sZa2Max[0] - bands.sZa2Min[0]) / (NptsBand+1)      , bands.sZa2Max[0]   , NptsBand , endpoint=False)
    meanLa1 = np.linspace( bands.mZa1Min[0]     + (bands.mZa1Max[0] - bands.mZa1Min[0]) / (NptsBand+1)      , bands.mZa1Max[0]   , NptsBand , endpoint=False)
    meanLa2 = np.linspace( bands.mZa2Min[0]     + (bands.mZa2Max[0] - bands.mZa2Min[0]) / (NptsBand+1)      , bands.mZa2Max[0]   , NptsBand , endpoint=False)
    if debug>1: print "sigT:",sigT , "\nsigLa1:",sigLa1 , "\nsigLa2:",sigLa2 , "\nmeanLa1:",meanLa1, "\nmeanLa2:",meanLa2 , "\n mean(pcmZ) = %f * p(miss) + %f"%(meanLa1 , meanLa2  )
    
    NrunsThisCore , NrunsTotal = len(sigT)*len(sigLa1)*len(sigLa2)*len(meanLa1)*len(meanLa2) , NptsBand*NptsBand*NptsBand*NptsBand*NptsBand
    if (debug>0): print '\033[95m' + 'Core %d (out of %d) will procees %d runs (total %d runs)'%(i_core,Ncores,NrunsThisCore,NrunsTotal) + '\033[0m'
    
    run = start_run + (i_core+1)*1000
    
    '''
        recoil proton acceptances:
        (a) efficiency and acceptacne from the 'uniform' map i've generated using virtual CLAS
        (b) proton fiducial cuts (coded inside the event generator class)
    '''
    if 'generate' in option:
        pAcceptacneFile = ROOT.TFile("/Users/erezcohen/Desktop/DataMining/GSIM_DATA/PrecoilAcceptance.root")
        h = pAcceptacneFile.Get("hRescaled")
        gen_events = GenerateEvents( path , run , debug )
        gen_events.SetNRand( NRand )
        gen_events.Use_protonAcceptacne( True )
        gen_events.Set_protonAcceptacne( h )
        gen_events.SetInputChain_eep()
    

    # event generation (and analysis) loop
    for sT in sigT:
        for sLa1 in sigLa1:
            for sLa2 in sigLa1:
                for mLa1 in meanLa1:
                    for mLa2 in meanLa2:
                        run = run+1
                        
                        if 'generate' in option:

                            # (1) generate the simulated data (the 'run')
                            # ----------------------------
                            gen_events.Set_eep_Parameters( data_fits.mX_unweighted , data_fits.mY_unweighted , sT , sLa1 , sLa2 , mLa1 , mLa2 )
                            gen_events.DoGenerateRun_eep( run )
                            
                            # and now scheme them to our desired pp-SRC cuts
                            ana_sim = TAnalysisEG2( path + '/eg_rootfiles', 'run%d'%run , ROOT.TCut('') )
                            scheme.SchemeOnTCut( path + '/eg_rootfiles' , 'run%d.root'%run , "anaTree", 'run%d.root'%run , ana_sim.EGppSRCCut + ana_sim.PrecFiducial )

                            ana_sim.CloseFile()
                            garbage_list = [ ana_sim ]
                            del garbage_list



                        if 'analyze' in option or 'analyse' in option:
                        
                            if (debug>1): print "analyzing run %d"%run
                            # (2) analyze the simulated data (the 'run') similarly to the data - reconstructed parameters
                            # ----------------------------
                            ana_sim = TAnalysisEG2( path + '/eg_rootfiles', 'run%d'%run , ROOT.TCut('') )
                            reco_parameters = calc_cm_parameters( ana_sim  , PmissBins ) # , CMRooFitsName( path + '/eg_cm_roofits/run%d_unweighted_'%run ), CMRooFitsName( path + '/eg_cm_roofits/run%d_weighted_'%run ) )
                            if (debug>1): print "reconstructed cm parameters"
                            if (debug>4): print "reco_parameters: ",reco_parameters
                            reco_fits = fit_cm_parameters( run , reco_parameters ) # , FigureFName( path + '/eg_cm_figures/run%d_'%run ) )
                            if (debug>1): print "completed fiting processes"
                            if (debug>4): print "reco_fits: ",reco_fits


                            # No Mott/FF - weighting
                            # un - weighted roofit results
                            NsigST_unweighted    = NsigmaScore( data_fits , reco_fits  , 'sT'   , 'unweighted' )
                            NsigSL_a1_unweighted = NsigmaScore( data_fits , reco_fits  , 'sZa1' , 'unweighted' )
                            NsigSL_a2_unweighted = NsigmaScore( data_fits , reco_fits  , 'sZa2' , 'unweighted' )
                            NsigML_a1_unweighted = NsigmaScore( data_fits , reco_fits  , 'mZa1' , 'unweighted' )
                            NsigML_a2_unweighted = NsigmaScore( data_fits , reco_fits  , 'mZa2' , 'unweighted' )
                            NsigAvg_unweighted = (NsigST_unweighted + NsigSL_a1_unweighted + NsigSL_a2_unweighted + NsigML_a1_unweighted + NsigML_a2_unweighted)/5.
                            if (debug>1): print "got unweighted roofit results"
                        
                            # With Mott/FF - weighting
                            # weighted roofit results
                            NsigST_weighted    = NsigmaScore( data_fits , reco_fits  , 'sT'   , 'weighted' )
                            NsigSL_a1_weighted = NsigmaScore( data_fits , reco_fits  , 'sZa1' , 'weighted' )
                            NsigSL_a2_weighted = NsigmaScore( data_fits , reco_fits  , 'sZa2' , 'weighted' )
                            NsigML_a1_weighted = NsigmaScore( data_fits , reco_fits  , 'mZa1' , 'weighted' )
                            NsigML_a2_weighted = NsigmaScore( data_fits , reco_fits  , 'mZa2' , 'weighted' )
                            NsigAvg_weighted = (NsigST_weighted + NsigSL_a1_weighted + NsigSL_a2_weighted + NsigML_a1_weighted + NsigML_a2_weighted)/5.
                            if (debug>1): print "got weighted roofit results"

                            # KS test for the c.m. distributions in x,y,z directions
                            KSpCMx , KSxPval = KStest( PmissBins ,ana_sim , ana_data , "pcmX" , ROOT.TCut('') , debug) # maybe make it 2D, with adding the pmiss magnitude as a second variable?
                            KSpCMy , KSyPval = KStest( PmissBins ,ana_sim , ana_data , "pcmY" , ROOT.TCut('') , debug)
                            KSpCMt , KStPval = KStest( PmissBins ,ana_sim , ana_data , "pcmT" , ROOT.TCut('') , debug)
                            KSpCMz , KSzPval = KStest( PmissBins ,ana_sim , ana_data , "pcmZ" , ROOT.TCut('') , debug)
                            if (debug>1): print "performed KS tests"
                            if debug>3: print "KSxPval[0]:",KSxPval[0]


                            # (3) stream into file
                            # ----------------------------
                            results = pd.DataFrame({'run':int(run), 'time':str(datetime.datetime.now().strftime("%Y%B%d")),
                                                   'genSigmaT':sT    , 'genSigmaL_a1':sLa1   ,'genSigmaL_a2':sLa2 ,'genShiftL_a1':mLa1    ,'genShiftL_a2':mLa2       ,
                                                   'recSigmaT_unweighted':      float(reco_fits.sT_unweighted)    ,'recSigmaTErr_unweighted':     float(reco_fits.sTerr_unweighted)  ,
                                                   'recSigmaL_a1_unweighted':   float(reco_fits.sZa1_unweighted)   ,'recSigmaL_a1Err_unweighted':  float(reco_fits.sZa1err_unweighted),
                                                   'recSigmaL_a2_unweighted':   float(reco_fits.sZa2_unweighted)   ,'recSigmaL_a2Err_unweighted':  float(reco_fits.sZa2err_unweighted),
                                                   'recShiftL_a1_unweighted':   float(reco_fits.mZa1_unweighted)   ,'recShiftL_a1Err_unweighted':  float(reco_fits.mZa1err_unweighted),
                                                   'recShiftL_a2_unweighted':   float(reco_fits.mZa2_unweighted)   ,'recShiftL_a2Err_unweighted':  float(reco_fits.mZa2err_unweighted),
                                                   'NsigST_unweighted':         NsigST_unweighted           ,'NsigSL_a1_unweighted':        NsigSL_a1_unweighted        ,'NsigSL_a2_unweighted':    NsigSL_a2_unweighted,
                                                   'NsigML_a1_unweighted':      NsigML_a1_unweighted        ,'NsigML_a2_unweighted':        NsigML_a2_unweighted        ,
                                                   'NsigAvg_unweighted':        NsigAvg_unweighted          ,
                                                   'recSigmaT_weighted':        float(reco_fits.sT_weighted)       ,'recSigmaTErr_weighted':       float(reco_fits.sTerr_weighted)    ,
                                                   'recSigmaL_a1_weighted':     float(reco_fits.sZa1_weighted)     ,'recSigmaL_a1Err_weighted':    float(reco_fits.sZa1err_weighted)  ,
                                                   'recSigmaL_a2_weighted':     float(reco_fits.sZa2_weighted)     ,'recSigmaL_a2Err_weighted':    float(reco_fits.sZa2err_weighted)  ,
                                                   'recShiftL_a1_weighted':     float(reco_fits.mZa1_weighted)     ,'recShiftL_a1Err_weighted':    float(reco_fits.mZa1err_weighted)  ,
                                                   'recShiftL_a2_weighted':     float(reco_fits.mZa2_weighted)     ,'recShiftL_a2Err_weighted':    float(reco_fits.mZa2err_weighted)  ,
                                                   'NsigST_weighted':           NsigST_weighted             ,'NsigSL_a1_weighted':          NsigSL_a1_weighted          ,'NsigSL_a2_weighted':      NsigSL_a2_weighted,
                                                   'NsigML_a1_weighted':        NsigML_a1_weighted          ,'NsigML_a2_weighted':          NsigML_a2_weighted          ,
                                                   'NsigAvg_weighted':          NsigAvg_weighted            ,
                                                   'KSxPval_0':KSxPval[0]    , 'KSxPval_1':KSxPval[1] , 'KSxPval_2':KSxPval[2] , 'KSxPval_3':KSxPval[3] , 'KSxPval_4':KSxPval[4],'KSxPval_avg':np.average(KSxPval),
                                                   'KSyPval_0':KSyPval[0]    , 'KSyPval_1':KSyPval[1] , 'KSyPval_2':KSyPval[2] , 'KSyPval_3':KSxPval[3] , 'KSyPval_4':KSyPval[4],'KSxPval_avg':np.average(KSyPval),
                                                   'KStPval_0':KStPval[0]    , 'KStPval_1':KStPval[1] , 'KStPval_2':KStPval[2] , 'KStPval_3':KSxPval[3] , 'KStPval_4':KStPval[4],'KSxPval_avg':np.average(KStPval),
                                                   'KSzPval_0':KSzPval[0]    , 'KSzPval_1':KSzPval[1] , 'KSzPval_2':KSzPval[2] , 'KSzPval_3':KSxPval[3] , 'KSzPval_4':KSzPval[4],'KSxPval_avg':np.average(KSzPval) } ,
                                                   index = [int(run)])


                            if (debug>4): print "results: ",results
                            df_reco_parameters = df_reco_parameters.append( reco_parameters )
                            df_reco_fits = df_reco_fits.append( reco_fits )
                            df_results = df_results.append( results )
                            ana_sim.CloseFile()
                            if (debug>1): print "appended into pandas.DataFrames"
                            if (debug>2): print "resutls: ",df_results
                            garbage_list = [ ana_sim , reco_parameters , reco_fits  , results ]
                            del garbage_list

                        print_important( "completed run %d"%run ) ; print_line()
    


    if 'generate' in option:
        gen_events.ReleaseInputChain_eep()

    if 'analyze' in option:
        stream_dataframe_to_file( df_reco_fits, reco_fitsFName  )
        print_filename( reco_fitsFName , "reconstructed parameters fits wrote to" )
        stream_dataframe_to_file( df_results, resutlsFName  )
        print_filename( resutlsFName , "results wrote to " )
    print_important("done...") ; print_line


# ------------------------------------------------------------------------------- #
def plot( simulation_results , x , y , xlabel = '' , ylabel = '' ):
    sr = simulation_results
    cmap = mpl.cm.hot
    my_hot_cmap = gp.reverse_colourmap(cmap)
    
    with sns.axes_style("white"):
        g = sns.jointplot(x=sr[x], y=sr[y] , cmap=my_hot_cmap, kind="hex", stat_func=None, marginal_kws={'color': 'green'})
    g.set_axis_labels(xlabel,ylabel)
    plt.colorbar()
    plt.show()


# ------------------------------------------------------------------------------- #
def find_best_parameters( simulation_results ):
    sr = simulation_results
    gp.sns2d_with_projections( sr.genSigmaT , sr.recSigmaT_unweighted , axes_labels=[r'generated $\sigma_{T}$ [GeV/c]',r'un-weighted reconstructed $\sigma_{T}$ [GeV/c]'] , kind="hex")





# ------------------------------------------------------------------------------- #
def stream_dataframe_to_file( df , finename ):
    # if file does not exist write header
    if not os.path.isfile(finename):
        df.to_csv(finename,header ='column_names' , index = False)
    else: # else it exists so append without writing the header
        df.to_csv(finename,mode = 'a', header=False , index = False)










