import time , sys , os , math , datetime , ROOT
import matplotlib , pandas as pd , numpy as np
import matplotlib as mpl , seaborn as sns; sns.set(style="white", color_codes=True , font_scale=3)
from matplotlib import pyplot as plt
from ROOT import TAnalysisEG2,GenerateEvents
from root_numpy import hist2array
from scipy.stats import ks_2samp
sys.path.insert(0, '/Users/erezcohen/larlite/UserDev/mySoftware/MySoftwarePackage/mac')
import GeneralPlot as gp
import gc

# ------------------------------------------------------------------------------- #
# definitions
cm_pars_columns = ['pMiss_min','pMiss_max'
                   ,'mean_x_unweighted','mean_xErr_unweighted','sigma_x_unweighted','sigma_xErr_unweighted'
                   ,'mean_y_unweighted','mean_yErr_unweighted','sigma_y_unweighted','sigma_yErr_unweighted'
                   ,'mean_z_unweighted','mean_zErr_unweighted','sigma_z_unweighted','sigma_zErr_unweighted'
                   ,'mean_x_weighted','mean_xErr_weighted','sigma_x_weighted','sigma_xErr_weighted'
                   ,'mean_y_weighted','mean_yErr_weighted','sigma_y_weighted','sigma_yErr_weighted'
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
                   ,'KSpCMx','KSpCMy','KSpCMz','KSavg']



# prints
def print_line(): print '\033[93m' + '--------------------------------------------------------------' + '\033[0m'
def print_important(string): print '\033[94m' + '\033[1m' + string + '\033[0m' ; print_line
def print_filename(filename,action_on_file=""): print action_on_file + ' ' + '\033[91m' + filename + '\033[0m'

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
def KStest( ana1 , ana2 , var , cut=ROOT.TCut() , Nbins=50, xmin=0 , xmax=2 ):
    # [http://docs.scipy.org/doc/scipy-0.15.1/reference/generated/scipy.stats.ks_2samp.html]
    h1 = ana1.H1( var, cut,"goff", Nbins, xmin, xmax)
    h2 = ana2.H1( var, cut,"goff", Nbins, xmin, xmax)
    array1 , array2 = hist2array(h1) , hist2array(h2)
    D , Pvalue = ks_2samp( array1 , array2 )
    return D


# ------------------------------------------------------------------------------- #
def plot_errorbar_and_fit( ax , x , y , xerr , yerr , color , marker , lstyle , label , fit_type='const',offset=0.3):
    plt.errorbar(x, y, xerr=xerr, yerr=yerr, color=color, marker=marker , linestyle=lstyle , label=None)
    if fit_type=='const':
        p1,v1 = np.polyfit( x , y , 0 , cov=True)
        ax.plot(x, np.ones(len(x))*p1[0] , color=color , label=label + "$=%.3f\pm%.3f$"%(p1[0],math.sqrt(v1[0][0])))
        # return a 2D variable - the const. fit + its error
        return [p1[0],math.sqrt(v1[0][0])]
    elif fit_type=='linear':
        p2,v2 = np.polyfit( x , y , 1, cov=True)
        ax.plot(x, p2[0] * (x-offset) + p2[0]*offset + p2[1], color=color ,
                label=label + "$=%.2f(p_{miss}-%.1f)+(%.2f)$"%(p2[0],offset,p2[0]*offset + p2[1]))
                # return a set of 2D variables - the fit parameters + their errors
        return [p2[0],math.sqrt(v2[0][0])] , [p2[0]*offset + p2[1],math.sqrt(v2[0][0]*offset+v2[1][1])]

# ------------------------------------------------------------------------------- #
def errorbar_and_fit( x , y , fit_type='const' , offset=0.3): # same as plot_errorbar_and_fit without plot
    if fit_type=='const':
        p1,v1 = np.polyfit( x , y , 0 , cov=True)
        return [p1[0],math.sqrt(v1[0][0])]
    elif fit_type=='linear':
        p2,v2 = np.polyfit( x , y , 1, cov=True)
        return [p2[0],math.sqrt(v2[0][0])] , [p2[0]*offset + p2[1],math.sqrt(v2[0][0]*offset+v2[1][1])]

# ------------------------------------------------------------------------------- #
def calc_cm_parameters( fana  , PmissBins , unweightedRoofitsFName = '' , weightedRoofitsFName = '' , DoSaveCanvas = False ):
    df_pMissBins = pd.DataFrame(columns=cm_pars_columns)
    
    if DoSaveCanvas:
        canvas_unweighted , canvas_weighted = fana.CreateCanvas( "RooFit plots - unweighted" , "Divide" , 3 , len(PmissBins) ) , fana.CreateCanvas( "RooFit plots - weighted" , "Divide" , 3 , len(PmissBins) )

    for i in range(len(PmissBins)):
        pMiss_min , pMiss_max = PmissBins[i][0] , PmissBins[i][1]

        if DoSaveCanvas:
            unweighted = fana.RooFitCM( pMiss_min , pMiss_max , False , True, canvas_unweighted, 3*i + 1 )
            weighted = fana.RooFitCM( pMiss_min , pMiss_max , True , True, canvas_weighted, 3*i + 1 )
        else:
            unweighted = fana.RooFitCM( pMiss_min , pMiss_max , False )
            weighted = fana.RooFitCM( pMiss_min , pMiss_max , True )

        df_pMissBin = pd.DataFrame({'pMiss_min':pMiss_min,'pMiss_max':pMiss_max
                                   ,'mean_x_unweighted':unweighted[0],'mean_xErr_unweighted':unweighted[1],'sigma_x_unweighted':unweighted[2],'sigma_xErr_unweighted':unweighted[3]
                                   ,'mean_y_unweighted':unweighted[4],'mean_yErr_unweighted':unweighted[5],'sigma_y_unweighted':unweighted[6],'sigma_yErr_unweighted':unweighted[7]
                                   ,'mean_z_unweighted':unweighted[8],'mean_zErr_unweighted':unweighted[9],'sigma_z_unweighted':unweighted[10],'sigma_zErr_unweighted':unweighted[11]
                                   ,'mean_x_weighted':weighted[0],'mean_xErr_weighted':weighted[1],'sigma_x_weighted':weighted[2],'sigma_xErr_weighted':weighted[3]
                                   ,'mean_y_weighted':weighted[4],'mean_yErr_weighted':weighted[5],'sigma_y_weighted':weighted[6],'sigma_yErr_weighted':weighted[7]
                                   ,'mean_z_weighted':weighted[8],'mean_zErr_weighted':weighted[9],'sigma_z_weighted':weighted[10],'sigma_zErr_weighted':weighted[11]}
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
def fit_par_plot( fig , i_subplot , data , var , weight , title , zOffset): # a sub-routine to fit a single parameter

    Pmiss = (data.pMiss_max + data.pMiss_min)/2.
    pMissUpErr , pMissLowErr = data.pMiss_max - Pmiss , Pmiss - data.pMiss_min
    ax = fig.add_subplot( i_subplot )
    #     ax.text( 0.3 , 0.2 , "no acc. corr." , fontsize=80 , color='red' , alpha = 0.15 ) # keep for future
    ax.grid(True,linestyle='-',color='0.95')
    [Xfit,XfitErr] = plot_errorbar_and_fit( ax , Pmiss, data[ var + '_x_' + weight] , [pMissLowErr,pMissUpErr] , [data[ var + '_xErr_' + weight ],data[ var + '_xErr_' + weight ]], 'black','v','none',r'$%s_{x}$'%title ,'const')
    [Yfit,YfitErr] = plot_errorbar_and_fit( ax , Pmiss, data[ var + '_y_' + weight] , [pMissLowErr,pMissUpErr] , [data[ var + '_yErr_' + weight ],data[ var + '_yErr_' + weight ]], 'red'  ,'o','none',r'$%s_{y}$'%title ,'const')
    Tfit , TfitErr = 0.5*(Xfit + Yfit) ,  math.sqrt(XfitErr*XfitErr + YfitErr*YfitErr)
    [Za1,Za1err],[Za2,Za2err] = plot_errorbar_and_fit( ax , Pmiss, data[ var + '_z_' + weight] , [pMissLowErr,pMissUpErr] , [data[ var + '_zErr_' + weight ],data[ var + '_zErr_' + weight ]], 'blue' ,'s','none',r'$%s_{\vec{p}_{miss}}$'%title ,'linear', zOffset)
    set_frame( ax , r'%s $%s$'%(weight,title) , r'$p_{miss}$ [GeV/c]' , r'c.m. momentum $%s$ [Gev/c]'%title , "upper left")
    return Xfit , XfitErr , Yfit , YfitErr , Tfit , TfitErr, Za1 , Za1err , Za2 , Za2err

# ------------------------------------------------------------------------------- #
def fit_par_noplot( data , var , weight , title , zOffset): # a sub-routine to fit a single parameter; same as fit_par_plot without a plot
    
    Pmiss = (data.pMiss_max + data.pMiss_min)/2.
    pMissUpErr , pMissLowErr = data.pMiss_max - Pmiss , Pmiss - data.pMiss_min
    [Xfit,XfitErr] = errorbar_and_fit( Pmiss, data[ var + '_x_' + weight] ,'const')
    [Yfit,YfitErr] = errorbar_and_fit( Pmiss, data[ var + '_y_' + weight] ,'const')
    Tfit , TfitErr = 0.5*(Xfit + Yfit) ,  math.sqrt(XfitErr*XfitErr + YfitErr*YfitErr)
    [Za1,Za1err],[Za2,Za2err] = errorbar_and_fit( Pmiss, data[ var + '_z_' + weight] , 'linear' , zOffset)
    return Xfit , XfitErr , Yfit , YfitErr , Tfit , TfitErr, Za1 , Za1err , Za2 , Za2err



# ------------------------------------------------------------------------------- #
def fit_cm_parameters( run , data , FigureFName = '' , DoSaveCanvas = False ): # all parameters

    if DoSaveCanvas: # this means we want plots
        fig = plt.figure(figsize=(40,20)) # four plots, two unweighted and two weighted
        sX_unweighted, sXerr_unweighted, sY_unweighted, sYerr_unweighted, sT_unweighted, sTerr_unweighted, sZa1_unweighted, sZa1err_unweighted, sZa2_unweighted, sZa2err_unweighted = fit_par_plot ( fig , 221, data , 'sigma', 'unweighted' , '\sigma' , 0.5 )
        mX_unweighted, mXerr_unweighted, mY_unweighted, mYerr_unweighted, mT_unweighted, mTerr_unweighted, mZa1_unweighted, mZa1err_unweighted, mZa2_unweighted, mZa2err_unweighted = fit_par_plot( fig , 222, data , 'mean' , 'unweighted' , 'mean'   , 0.3 )
        sX_weighted, sXerr_weighted, sY_weighted, sYerr_weighted, sT_weighted, sTerr_weighted, sZa1_weighted, sZa1err_weighted, sZa2_weighted, sZa2err_weighted = fit_par_plot( fig , 223, data , 'sigma', 'weighted' , '\sigma' , 0.5 )
        mX_weighted, mXerr_weighted, mY_weighted, mYerr_weighted, mT_weighted, mTerr_weighted, mZa1_weighted, mZa1err_weighted, mZa2_weighted, mZa2err_weighted = fit_par_plot( fig , 224, data , 'mean' , 'weighted' , 'mean'   , 0.3 )
    else:
        sX_unweighted, sXerr_unweighted, sY_unweighted, sYerr_unweighted, sT_unweighted, sTerr_unweighted, sZa1_unweighted, sZa1err_unweighted, sZa2_unweighted, sZa2err_unweighted = fit_par_noplot ( data , 'sigma', 'unweighted' , '\sigma' , 0.5 )
        mX_unweighted, mXerr_unweighted, mY_unweighted, mYerr_unweighted, mT_unweighted, mTerr_unweighted, mZa1_unweighted, mZa1err_unweighted, mZa2_unweighted, mZa2err_unweighted = fit_par_noplot( data , 'mean' , 'unweighted' , 'mean'   , 0.3 )
        sX_weighted, sXerr_weighted, sY_weighted, sYerr_weighted, sT_weighted, sTerr_weighted, sZa1_weighted, sZa1err_weighted, sZa2_weighted, sZa2err_weighted = fit_par_noplot( data , 'sigma', 'weighted' , '\sigma' , 0.5 )
        mX_weighted, mXerr_weighted, mY_weighted, mYerr_weighted, mT_weighted, mTerr_weighted, mZa1_weighted, mZa1err_weighted, mZa2_weighted, mZa2err_weighted = fit_par_noplot( data , 'mean' , 'weighted' , 'mean'   , 0.3 )

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
def plot_band_around_cm_parameter_fits( fig , i_subplot , data , var , weight , title , zOffset , TBand , ZBandMin , ZBandMax ):

    Pmiss = (data.pMiss_max + data.pMiss_min)/2.
    pMissUpErr , pMissLowErr = data.pMiss_max - Pmiss , Pmiss - data.pMiss_min

    fit_par_plot( fig , i_subplot , data , var , weight , title , zOffset)
    plt.fill_between(Pmiss, TBand[0] , TBand[1] ,alpha=0.5, edgecolor='#CC4F1B', facecolor='#FF9848')
    plt.fill_between(Pmiss, ZBandMin , ZBandMax ,alpha=0.5, edgecolor='#C14F1B', facecolor='#1122CC')


# ------------------------------------------------------------------------------- #
def generate_cm_bands( cm_parameters , fit_pars , CMBandFname , FigureBandFName , DoSaveCanvas = False ):
 
    df = pd.DataFrame(columns=bands_columns)
    Pmiss = (cm_parameters.pMiss_max + cm_parameters.pMiss_min)/2.

    sTBand = np.ones(len(Pmiss))*[fit_pars.sT_unweighted*0.9,fit_pars.sT_unweighted*1.1]
    sZa1BandMin , sZa1BandMax = fit_pars.sZa1_unweighted*0.9,fit_pars.sZa1_unweighted*1.1
    sZa2BandMin , sZa2BandMax = fit_pars.sZa2_unweighted*0.9,fit_pars.sZa2_unweighted*1.1
    sZBandMax = float(sZa1BandMax)*(Pmiss-0.5)+float(sZa2BandMax)
    sZBandMin = float(sZa1BandMin)*(Pmiss-0.5)+float(sZa2BandMin)

    mTBand = np.zeros(len(Pmiss))
    mZa1BandMin , mZa1BandMax = fit_pars.mZa1_unweighted*0.8,fit_pars.mZa1_unweighted*1.2
    mZa2BandMin , mZa2BandMax = fit_pars.mZa2_unweighted*0.8,fit_pars.mZa2_unweighted*1.2
    mZBandMax = float(mZa1BandMax)*(Pmiss-0.3)+float(mZa2BandMax)
    mZBandMin = float(mZa1BandMin)*(Pmiss-0.3)+float(mZa2BandMin)

    if DoSaveCanvas:
        fig = plt.figure(figsize=(40,10))
        plot_band_around_cm_parameter_fits( fig , 121, cm_parameters , 'sigma', 'unweighted' , '\sigma' , 0.5 , sTBand , sZBandMin , sZBandMax  )
        plot_band_around_cm_parameter_fits( fig , 122, cm_parameters , 'mean', 'unweighted' , 'mean' , 0.3 , mTBand , mZBandMin , mZBandMax  )
        plt.savefig(FigureBandFName)
        print_filename( FigureBandFName , "plots to file" )

    df_bands = pd.DataFrame({'sTBandMin':np.amin(sTBand),'sTBandMax':np.amax(sTBand)
                            ,'sZa1Min':sZa1BandMin,'sZa1Max':sZa1BandMax
                            ,'sZa2Min':sZa2BandMin,'sZa2Max':sZa2BandMax
                            ,'mZa1Min':mZa1BandMin,'mZa1Max':mZa1BandMax
                            ,'mZa2Min':mZa2BandMin,'mZa2Max':mZa2BandMax},index=[0])
    df = df.append(df_bands)
    df.to_csv( CMBandFname , header=True , index = False)
    print_filename( CMBandFname , "wrote bands around cm paramters fits to" )
    print_line()


# ------------------------------------------------------------------------------- #
def linspace_single_core( band_min  , band_max  , NptsBand , Ncores , i_core ):
    tmp_min = np.min( [band_min , band_max] )
    band_max = np.max( [band_min , band_max] )
    band_min = tmp_min
    step = math.fabs(band_max - band_min)/NptsBand#Ncores
    min = band_min + (float(i_core)/Ncores)*(band_max - band_min)
    max = min + float(band_max - band_min)/Ncores
    print min , max , step
    res = np.arange( min , max , step )
    return res




# ------------------------------------------------------------------------------- #
#def generate_runs_with_different_parameters( cm_fits_parameters , cm_pars_bands ,
def generate_runs_with_different_parameters( option,
                                            data_fits , bands , NRand ,
                                            start_run , debug , PmissBins , resutlsFName , reco_fitsFName , target ,
                                            NptsBand , Ncores , i_core ):
    
    # the data (nominal values)
    ana_data = TAnalysisEG2( "ppSRCCut_DATA_%s"% target )
    path = "/Users/erezcohen/Desktop/DataMining/Analysis_DATA/ppSRCcm"


    # simulation pandas::DataFrame
    df_reco_parameters = pd.DataFrame(columns=cm_pars_columns)
    df_reco_fits = pd.DataFrame(columns=fits_columns)
    df_results = pd.DataFrame(columns=results_columns)


    # the bands around data (around nominal values)
    sigT    = linspace_single_core( bands.sTBandMin[0]  ,bands.sTBandMax[0]    , NptsBand , Ncores , i_core )
    sigLa1  = linspace_single_core( bands.sZa1Min[0]  ,bands.sZa1Max[0]      , NptsBand , Ncores , i_core )
    sigLa2  = linspace_single_core( bands.sZa2Min[0]  ,bands.sZa2Max[0]      , NptsBand , Ncores , i_core )
    meanLa1 = linspace_single_core( bands.mZa1Min[0]  ,bands.mZa1Max[0]     , NptsBand , Ncores , i_core )
    meanLa2 = linspace_single_core( bands.mZa2Min[0]  ,bands.mZa2Max[0]     , NptsBand , Ncores , i_core )
    
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
                            gen_events.Set_eep_Parameters( sT , sLa1 , sLa2 , mLa1 , mLa2 )
                            gen_events.DoGenerateRun_eep( run )


                        if 'analyze' in option or 'analyse' in option:
                        
                            if (debug>1): print "analyzing run %d"%run
                            # (2) analyze the simulated data (the 'run') similarly to the data - reconstructed parameters
                            # ----------------------------
                            ana_sim = TAnalysisEG2( path + '/eg_rootfiles', 'run%d'%run , ROOT.TCut('') )
                            reco_parameters = calc_cm_parameters( ana_sim  , PmissBins ) # , CMRooFitsName( path + '/eg_cm_roofits/run%d_unweighted_'%run ), CMRooFitsName( path + '/eg_cm_roofits/run%d_weighted_'%run ) )
                            if (debug>1): print "reconstructed cm parameters"
                            reco_fits = fit_cm_parameters( run , reco_parameters ) # , FigureFName( path + '/eg_cm_figures/run%d_'%run ) )
                            if (debug>1): print "completed fiting processes"


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
                            KSpCMx = KStest( ana_sim , ana_data , "pcmX" ) # maybe make it 2D, with adding the pmiss magnitude as a second variable?
                            KSpCMy = KStest( ana_sim , ana_data , "pcmY" )
                            KSpCMz = KStest( ana_sim , ana_data , "pcmZ" )
                            KSavg = (KSpCMx + KSpCMy + KSpCMz)/3.
                            ana_sim.CloseFile()
                            if (debug>1): print "performed KS tests"


                            # (3) stream into file
                            # ----------------------------
                            results = pd.DataFrame({'run':int(run), 'time':str(datetime.datetime.now().strftime("%Y%B%d")),
                                                   'genSigmaT':sT    , 'genSigmaL_a1':sLa1   ,'genSigmaL_a2':sLa2    ,'genShiftL_a1':mLa1    ,'genShiftL_a2':mLa2       ,
                                                   'recSigmaT_unweighted':      reco_fits.sT_unweighted     ,'recSigmaTErr_unweighted':     reco_fits.sTerr_unweighted  ,
                                                   'recSigmaL_a1_unweighted':   reco_fits.sZa1_unweighted   ,'recSigmaL_a1Err_unweighted':  reco_fits.sZa1err_unweighted,
                                                   'recSigmaL_a2_unweighted':   reco_fits.sZa2_unweighted   ,'recSigmaL_a2Err_unweighted':  reco_fits.sZa2err_unweighted,
                                                   'recShiftL_a1_unweighted':   reco_fits.mZa1_unweighted   ,'recShiftL_a1Err_unweighted':  reco_fits.mZa1err_unweighted,
                                                   'recShiftL_a2_unweighted':   reco_fits.mZa2_unweighted   ,'recShiftL_a2Err_unweighted':  reco_fits.mZa2err_unweighted,
                                                   'NsigST_unweighted':         NsigST_unweighted           ,'NsigSL_a1_unweighted':        NsigSL_a1_unweighted        ,'NsigSL_a2_unweighted':    NsigSL_a2_unweighted,
                                                   'NsigML_a1_unweighted':      NsigML_a1_unweighted        ,'NsigML_a2_unweighted':        NsigML_a2_unweighted        ,
                                                   'NsigAvg_unweighted':        NsigAvg_unweighted          ,
                                                   'recSigmaT_weighted':        reco_fits.sT_weighted       ,'recSigmaTErr_weighted':       reco_fits.sTerr_weighted    ,
                                                   'recSigmaL_a1_weighted':     reco_fits.sZa1_weighted     ,'recSigmaL_a1Err_weighted':    reco_fits.sZa1err_weighted  ,
                                                   'recSigmaL_a2_weighted':     reco_fits.sZa2_weighted     ,'recSigmaL_a2Err_weighted':    reco_fits.sZa2err_weighted  ,
                                                   'recShiftL_a1_weighted':     reco_fits.mZa1_weighted     ,'recShiftL_a1Err_weighted':    reco_fits.mZa1err_weighted  ,
                                                   'recShiftL_a2_weighted':     reco_fits.mZa2_weighted     ,'recShiftL_a2Err_weighted':    reco_fits.mZa2err_weighted  ,
                                                   'NsigST_weighted':           NsigST_weighted             ,'NsigSL_a1_weighted':          NsigSL_a1_weighted          ,'NsigSL_a2_weighted':      NsigSL_a2_weighted,
                                                   'NsigML_a1_weighted':        NsigML_a1_weighted          ,'NsigML_a2_weighted':          NsigML_a2_weighted          ,
                                                   'NsigAvg_weighted':          NsigAvg_weighted            ,
                                                   'KSpCMx':KSpCMx   ,'KSpCMy':KSpCMy    ,'KSpCMz':KSpCMz    ,'KSavg':KSavg  } , index = [int(run)])

                            df_reco_parameters = df_reco_parameters.append( reco_parameters )
                            df_reco_fits = df_reco_fits.append( reco_fits )
                            df_results = df_results.append( results )
                            if (debug>1): print "appended into pandas.DataFrames"
                            if (debug>2): print "resutls: ",df_results
                            garbage_list = [ ana_sim , reco_parameters , reco_fits  , results ]
                            del garbage_list
                                
                        print_important( "completed run %d"%run ) ; print_line
    


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










