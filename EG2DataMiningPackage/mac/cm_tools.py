import time , sys , os , math , datetime , ROOT
import matplotlib , pandas as pd , numpy as np
from matplotlib import pyplot as plt
from ROOT import TAnalysisEG2,GenerateEvents
from root_numpy import hist2array
from scipy.stats import ks_2samp

# ------------------------------------------------------------------------------- #
# file names
def print_important(string): print '\033[94m' + '\033[1m' + string + '\033[0m'
def print_line(): print '\033[93m' + '--------------------------------------------------------------' + '\033[0m'
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
def RunsInfoFileName( path ):
    return path+"EG_simulated_runs_Info.csv"
def SimParametersFileName( path ):
    return path+"EG_simulated_runs_results_cm_parameters.csv"

# ------------------------------------------------------------------------------- #
def Nsigma( v1 , v1Err , v2 , v2Err):
    return math.fabs( v1 - v2 )/math.sqrt( v1Err*v1Err + v2Err*v2Err )

# ------------------------------------------------------------------------------- #
def append2RunsInfoFile(RunsInfoFileName):
    print "appending into Runs Info File Name:\n"+RunsInfoFileName
    try:
        if os.stat(RunsInfoFileName).st_size > 0:
            RunsInfoFile = open(RunsInfoFileName,'a')
        else:
            RunsInfoFile = open(RunsInfoFileName,'wb')
            RunsInfoFile.write( "run,time,SigmaT,SigmaL_a1,SigmaL_a2,ShiftL_a1,ShiftL_a2\n" )
    except OSError:
        RunsInfoFile = open(RunsInfoFileName,'wb')
        RunsInfoFile.write( "run,time,SigmaT,SigmaL_a1,SigmaL_a2,ShiftL_a1,ShiftL_a2\n" )
    return RunsInfoFile

# ------------------------------------------------------------------------------- #
def append2SimParametersFile(SimParametersFileName):

    print "appending into simulated-parameters File Name:\n"+SimParametersFileName
    string = "run,time"
    string += ",genSigmaT,genSigmaL_a1,genSigmaL_a2,genShiftL_a1,genShiftL_a2"
    string += ",recSigmaT_unweighted,recSigmaTErr_unweighted"
    string += ",recSigmaL_a1_unweighted,recSigmaL_a1Err_unweighted,recSigmaL_a2_unweighted,recSigmaL_a2Err_unweighted"
    string += ",recShiftL_a1_unweighted,recShiftL_a1Err_unweighted,recShiftL_a2_unweighted,recShiftL_a2Err_unweighted"
    string += ",NsigST_unweighted,NsigSL_a1_unweighted,NsigSL_a2_unweighted,NsigML_a1_unweighted,NsigML_a2_unweighted,NsigAvg_unweighted" # Nsig = N(sigma), the distance of the recosntructed parameter from the data-fit parameter
    string += ",recSigmaT_weighted,recSigmaTErr_weighted"
    string += ",recSigmaL_a1_weighted,recSigmaL_a1Err_weighted,recSigmaL_a2_weighted,recSigmaL_a2Err_weighted"
    string += ",recShiftL_a1_weighted,recShiftL_a1Err_weighted,recShiftL_a2_weighted,recShiftL_a2Err_weighted"
    string += ",NsigST_weighted,NsigSL_a1_weighted,NsigSL_a2_weighted,NsigML_a1_weighted,NsigML_a2_weighted,NsigAvg_weighted" # Nsig = N(sigma), the distance of the recosntructed parameter from the data-fit parameter
    string += ",KSpCMx,KSpCMy,KSpCMz,KSavg" # Kolomogorov-Smirnov test results for pCM distributions in x,y,z directions
    
    try:
        if os.stat(SimParametersFileName).st_size > 0:
            SimParametersFile = open(SimParametersFileName,'a')
        else:
            SimParametersFile = open(SimParametersFileName,'wb')
            SimParametersFile.write( string + "\n" )
    except OSError:
        SimParametersFile = open(SimParametersFileName,'wb')
        SimParametersFile.write( string + "\n" )
    return SimParametersFile


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
# calculate the  C.M. parameters
def calc_cm_parameters( fana  , PmissBins , outFileName , plotsFileName ):
    outfile = open( outFileName , 'wb' )
    out_string = "pMiss_min,pMiss_max"
    out_string += ",mean_x_unweighted,mean_xErr_unweighted,sigma_x_unweighted,sigma_xErr_unweighted,mean_y_unweighted,mean_yErr_unweighted,sigma_y_unweighted,sigma_yErr_unweighted,mean_z_unweighted,mean_zErr_unweighted,sigma_z_unweighted,sigma_zErr_unweighted"
    out_string += ",mean_x_weighted,mean_xErr_weighted,sigma_x_weighted,sigma_xErr_weighted,mean_y_weighted,mean_yErr_weighted,sigma_y_weighted,sigma_yErr_weighted,mean_z_weighted,mean_zErr_weighted,sigma_z_weighted,sigma_zErr_weighted"
    outfile.write(out_string + "\n")
    canvas = fana.CreateCanvas( "RooFit plots" , "Divide" , 3 , len(PmissBins) )
    for i in range(len(PmissBins)):
        out_string = "%.2f,%.2f" % (PmissBins[i][0],PmissBins[i][1])
        cmParsUnWeighted = fana.RooFitCM(PmissBins[i][0],PmissBins[i][1] , True, canvas, 3*i + 1 , False ) # RooFitCM return a parameter vector
        for j in range(len(cmParsUnWeighted)):
            out_string += ",%f" % cmParsUnWeighted.at(j)
        cmParsWeighted = fana.RooFitCM(PmissBins[i][0],PmissBins[i][1] , True, canvas, 3*i + 1 , True ) # RooFitCM return a parameter vector
        for j in range(len(cmParsWeighted)):
            out_string += ",%f" % cmParsWeighted.at(j)
        outfile.write(out_string + "\n")
    outfile.close()
    print "from \n"+fana.GetFile().GetName()
    print "done calculating parameters, output can be found in the file:\n", outfile.name
    canvas.SaveAs(plotsFileName)
    print "see plots at \n"+plotsFileName
    print_line()



# ------------------------------------------------------------------------------- #
def plot_cm_parameters( data , CMFitsFname , FigureFName ):

    Pmiss = (data.pMiss_max + data.pMiss_min)/2.
    pMissUpErr , pMissLowErr = data.pMiss_max - Pmiss , Pmiss - data.pMiss_min
    outfile = open(CMFitsFname, "wb")
    out_string = "sXfit_unweighted,sXfiterr_unweighted,sYfit_unweighted,sYfiterr_unweighted"
    out_string += ",sZa1_unweighted,sZa1err_unweighted,sZa2_unweighted,sZa2err_unweighted"
    out_string += ",mXfit_unweighted,mXfiterr_unweighted,mYfit_unweighted,mYfiterr_unweighted"
    out_string += ",mZa1_unweighted,mZa1err_unweighted,mZa2_unweighted,mZa2err_unweighted"
    out_string += ",sXfit_weighted,sXfiterr_weighted,sYfit_weighted,sYfiterr_weighted"
    out_string += ",sZa1_weighted,sZa1err_weighted,sZa2_weighted,sZa2err_weighted"
    out_string += ",mXfit_weighted,mXfiterr_weighted,mYfit_weighted,mYfiterr_weighted"
    out_string += ",mZa1_weighted,mZa1err_weighted,mZa2_weighted,mZa2err_weighted"
    outfile.write(out_string + "\n")
    out_string = ""
    
    fig = plt.figure(figsize=(40,20)) # four plots, two unweighted and two weighted
    
    ax = fig.add_subplot(221)
    ax.text( 0.3 , 0.2 , "no acc. corr." , fontsize=80 , color='red' , alpha = 0.15 )
    ax.grid(True,linestyle='-',color='0.95')
    [sXfit,sXfiterr] = plot_errorbar_and_fit( ax , Pmiss, data.sigma_x_unweighted ,
                                             [pMissLowErr,pMissUpErr] , [data.sigma_xErr_unweighted,data.sigma_xErr_unweighted],
                                             'black'  ,'v','none',r'$\sigma_{x}$' ,'const')
    [sYfit,sYfiterr] = plot_errorbar_and_fit( ax , Pmiss, data.sigma_y_unweighted ,
                                             [pMissLowErr,pMissUpErr] , [data.sigma_yErr_unweighted,data.sigma_yErr_unweighted],
                                             'red'    ,'o','none',r'$\sigma_{y}$' ,'const')
    [sZa1,sZa1err],[sZa2,sZa2err] = plot_errorbar_and_fit( ax , Pmiss, data.sigma_z_unweighted ,
                                                          [pMissLowErr,pMissUpErr] , [data.sigma_zErr_unweighted,data.sigma_zErr_unweighted],
                                                          'blue'   ,'s','none',r'$\sigma_{\vec{p}_{miss}}$' ,'linear', 0.5)
    plt.title( r'un-weighted width',fontsize=25)
    plt.xlabel( r'$p_{miss}$ [GeV/c]',fontsize=25)
    ax.tick_params(axis='both', which='major', labelsize=25)
    plt.ylabel( r'c.m. momentum width [Gev/c]',fontsize=25)
    ax.legend(loc="upper left",scatterpoints=1,fontsize=25)

    ax = fig.add_subplot(222)
    ax.text( 0.3 , 0.15 , "no acc. corr." , fontsize=80 , color='red' , alpha = 0.15 )
    ax.grid(True,linestyle='-',color='0.95')
    [mXfit,mXfiterr] = plot_errorbar_and_fit( ax , Pmiss, data.mean_x_unweighted ,
                                             [pMissLowErr,pMissUpErr] , [data.mean_xErr_unweighted,data.mean_xErr_unweighted],
                                             'black' ,'v','none',r'$mean_{x}$' ,'const')
    [mYfit,mYfiterr] = plot_errorbar_and_fit( ax , Pmiss, data.mean_y_unweighted ,
                                             [pMissLowErr,pMissUpErr] , [data.mean_yErr_unweighted,data.mean_yErr_unweighted],
                                             'red'   ,'v','none',r'$mean_{y}$' ,'const')
    [mZa1,mZa1err],[mZa2,mZa2err] = plot_errorbar_and_fit( ax , Pmiss, data.mean_z_unweighted ,
                                                          [pMissLowErr,pMissUpErr] , [data.mean_zErr_unweighted,data.mean_zErr_unweighted],
                                                          'blue'  ,'v','none',r'$mean_{\vec{p}_{miss}}$' ,'linear', 0.3)

    plt.title( r'un-weighted mean',fontsize=25)
    plt.xlabel( r'$p_{miss}$ [GeV/c]',fontsize=25)
    plt.ylabel( r'c.m. momentum mean [Gev/c]',fontsize=25)
    ax.tick_params(axis='both', which='major', labelsize=25)

    ax.legend(loc="upper left",scatterpoints=1,fontsize=25)

    out_string += "%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f"%(sXfit,sXfiterr,sYfit,sYfiterr,
                                                                     sZa1,sZa1err,sZa2,sZa2err,
                                                                     mXfit,mXfiterr,mYfit,mYfiterr,
                                                                     mZa1,mZa1err,mZa2,mZa2err)

    ax = fig.add_subplot(223)
    ax.text( 0.3 , 0.2 , "no acc. corr." , fontsize=80 , color='red' , alpha = 0.15 )
    ax.grid(True,linestyle='-',color='0.95')
    [sXfit,sXfiterr] = plot_errorbar_and_fit( ax , Pmiss, data.sigma_x_weighted ,
    [pMissLowErr,pMissUpErr] , [data.sigma_xErr_weighted,data.sigma_xErr_weighted],
                                             'black'  ,'v','none',r'$\sigma_{x}$' ,'const')
    [sYfit,sYfiterr] = plot_errorbar_and_fit( ax , Pmiss, data.sigma_y_weighted ,
                                             [pMissLowErr,pMissUpErr] , [data.sigma_yErr_weighted,data.sigma_yErr_weighted],
                                             'red'    ,'o','none',r'$\sigma_{y}$' ,'const')
    [sZa1,sZa1err],[sZa2,sZa2err] = plot_errorbar_and_fit( ax , Pmiss, data.sigma_z_weighted ,
                                                          [pMissLowErr,pMissUpErr] , [data.sigma_zErr_weighted,data.sigma_zErr_weighted],
                                                          'blue'   ,'s','none',r'$\sigma_{\vec{p}_{miss}}$' ,'linear', 0.5)
    plt.title( r'weighted width',fontsize=25)
    plt.xlabel( r'$p_{miss}$ [GeV/c]',fontsize=25)
    plt.ylabel( r'c.m. momentum width [Gev/c]',fontsize=25)
    ax.tick_params(axis='both', which='major', labelsize=25)

    ax.legend(loc="upper left",scatterpoints=1,fontsize=25)
                                             
    ax = fig.add_subplot(224)
    ax.text( 0.3 , 0.15 , "no acc. corr." , fontsize=80 , color='red' , alpha = 0.15 )
    ax.grid(True,linestyle='-',color='0.95')
    [mXfit,mXfiterr] = plot_errorbar_and_fit( ax , Pmiss, data.mean_x_weighted ,
                                             [pMissLowErr,pMissUpErr] , [data.mean_xErr_weighted,data.mean_xErr_weighted],
                                             'black' ,'v','none',r'$mean_{x}$' ,'const')
    [mYfit,mYfiterr] = plot_errorbar_and_fit( ax , Pmiss, data.mean_y_weighted ,
                                             [pMissLowErr,pMissUpErr] , [data.mean_yErr_weighted,data.mean_yErr_weighted],
                                             'red'   ,'v','none',r'$mean_{y}$' ,'const')
    [mZa1,mZa1err],[mZa2,mZa2err] = plot_errorbar_and_fit( ax , Pmiss, data.mean_z_weighted ,
                                                          [pMissLowErr,pMissUpErr] , [data.mean_zErr_weighted,data.mean_zErr_weighted],
                                                          'blue'  ,'v','none',r'$mean_{\vec{p}_{miss}}$' ,'linear', 0.3)
    plt.title( r'weighted mean',fontsize=25)
    plt.xlabel( r'$p_{miss}$ [GeV/c]',fontsize=25)
    plt.ylabel( r'c.m. momentum mean [Gev/c]',fontsize=25)
    ax.tick_params(axis='both', which='major', labelsize=25)

    ax.legend(loc="upper left",scatterpoints=1,fontsize=25)

    out_string += ",%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f"%(sXfit,sXfiterr,sYfit,sYfiterr,
                                                                     sZa1,sZa1err,sZa2,sZa2err,
                                                                     mXfit,mXfiterr,mYfit,mYfiterr,
                                                                     mZa1,mZa1err,mZa2,mZa2err)

    plt.savefig(FigureFName)
    
    outfile.write(out_string + "\n")
    outfile.close()
    print "wrote fit parameters to\n"+CMFitsFname
    print "and plot can be found at\n"+FigureFName
    print_line()




# ------------------------------------------------------------------------------- #
def generate_cm_bands( cm_parameters , cm_fits_parameters , CMBandFname , RunsInfoFileName , FigureBandFName ):
    
    data = cm_parameters
    Pmiss = (data.pMiss_max + data.pMiss_min)/2.
    pMissUpErr , pMissLowErr = data.pMiss_max - Pmiss , Pmiss - data.pMiss_min
    
    RunsInfoFile = append2RunsInfoFile(RunsInfoFileName)

    sXfit , sXfiterr = cm_fits_parameters.sXfit_unweighted , cm_fits_parameters.sXfiterr_unweighted
    sYfit , sYfiterr = cm_fits_parameters.sYfit_unweighted , cm_fits_parameters.sYfiterr_unweighted
    sZa1  , sZa1err  = cm_fits_parameters.sZa1_unweighted , cm_fits_parameters.sZa1err_unweighted
    sZa2  , sZa2err  = cm_fits_parameters.sZa2_unweighted , cm_fits_parameters.sZa2err_unweighted
    mXfit , mXfiterr = cm_fits_parameters.mXfit_unweighted , cm_fits_parameters.mXfiterr_unweighted
    mYfit , mYfiterr = cm_fits_parameters.mYfit_unweighted , cm_fits_parameters.mYfiterr_unweighted
    mZa1  , mZa1err  = cm_fits_parameters.mZa1_unweighted , cm_fits_parameters.mZa1err_unweighted
    mZa2  , mZa2err  = cm_fits_parameters.mZa2_unweighted , cm_fits_parameters.mZa2err_unweighted
    sTfit , sTfiterr = 0.5*(sXfit+sYfit) , math.sqrt(sXfit*sXfit+sYfit*sYfit)


    sTBand = np.ones(len(Pmiss))*[sTfit*0.9,sTfit*1.1]
    sZa1BandMin , sZa1BandMax = sZa1*0.9,sZa1*1.1
    sZa2BandMin , sZa2BandMax = sZa2*0.9,sZa2*1.1
    sZBandMax = float(sZa1BandMax)*(Pmiss-0.5)+float(sZa2BandMax)
    sZBandMin = float(sZa1BandMin)*(Pmiss-0.5)+float(sZa2BandMin)

    fig = plt.figure(figsize=(40,10))
    ax = fig.add_subplot(121)
    plt.errorbar(Pmiss, data.sigma_x_unweighted, xerr=[pMissLowErr,pMissUpErr], yerr=[data.sigma_xErr_unweighted,data.sigma_xErr_unweighted]
                 , color='black', marker='v' , linestyle='none' , label=None)
    plt.errorbar(Pmiss, data.sigma_y_unweighted, xerr=[pMissLowErr,pMissUpErr], yerr=[data.sigma_yErr_unweighted,data.sigma_yErr_unweighted]
                 , color='red', marker='o' , linestyle='none' , label=None)
    ax.plot(Pmiss, float(sTfit)*np.ones(len(Pmiss)) , color='0.65' )

    plt.fill_between(Pmiss, sTBand[0] , sTBand[1] ,alpha=0.5, edgecolor='#CC4F1B', facecolor='#FF9848')


    plt.errorbar(Pmiss, data.sigma_z_unweighted, xerr=[pMissLowErr,pMissUpErr], yerr=[data.sigma_zErr_unweighted,data.sigma_zErr_unweighted]
                 , color='blue', marker='s' , linestyle='none' , label=None)
    ax.plot(Pmiss, float(sZa1)*(Pmiss-0.5) + float(sZa2), color='0.65' )
    plt.fill_between(Pmiss, sZBandMin , sZBandMax ,alpha=0.5, edgecolor='#C14F1B', facecolor='#1122CC')
    plt.title( r'un-weighted width',fontsize=25)
    plt.xlabel( r'$p_{miss}$ [GeV/c]' ,fontsize=25)
    plt.ylabel( r'c.m. momentum width [Gev/c]',fontsize=25)


    mTBand = np.zeros(len(Pmiss))
    mZa1BandMin , mZa1BandMax = mZa1*0.8,mZa1*1.2
    mZa2BandMin , mZa2BandMax = mZa2*0.8,mZa2*1.2
    mZBandMax = float(mZa1BandMax)*(Pmiss-0.3)+float(mZa2BandMax)
    mZBandMin = float(mZa1BandMin)*(Pmiss-0.3)+float(mZa2BandMin)

    ax = fig.add_subplot(122)
    plt.errorbar(Pmiss, data.mean_x_unweighted, xerr=[pMissLowErr,pMissUpErr], yerr=[data.mean_xErr_unweighted,data.mean_xErr_unweighted]
                 , color='black', marker='v' , linestyle='none' , label=None)
    plt.errorbar(Pmiss, data.mean_y_unweighted, xerr=[pMissLowErr,pMissUpErr], yerr=[data.mean_yErr_unweighted,data.mean_yErr_unweighted]
                 , color='red', marker='o' , linestyle='none' , label=None)
    ax.plot(Pmiss, np.zeros(len(Pmiss)) , color='0.65' )

    plt.errorbar(Pmiss, data.mean_z_unweighted, xerr=[pMissLowErr,pMissUpErr], yerr=[data.mean_zErr_unweighted,data.mean_zErr_unweighted]
                 , color='blue', marker='s' , linestyle='none' , label=None)
    ax.plot(Pmiss, float(mZa1)*(Pmiss-0.3) + float(mZa2), color='0.65' )
    plt.fill_between(Pmiss, mZBandMin , mZBandMax ,alpha=0.5, edgecolor='#C14F1B', facecolor='#1122CC')

    plt.title( r'un-weighted mean',fontsize=25)
    plt.xlabel( r'$p_{miss}$ [GeV/c]' ,fontsize=25)
    plt.ylabel( r'c.m. momentum mean [Gev/c]',fontsize=25)

    plt.savefig(FigureBandFName)

    outfile = open(CMBandFname, "wb")
    outfile.write("sTBandMin,sTBandMax,sZa1Min,sZa1Max,sZa2Min,sZa2Max,mZa1Min,mZa1Max,mZa2Min,mZa2Max\n")
    outfile_str = "%f,%f,%f,%f,%f,%f,%f,%f,%f,%f\n"%(np.amin(sTBand),np.amax(sTBand),
                                                     sZa1BandMin,sZa1BandMax,sZa2BandMin,sZa2BandMax,
                                                     mZa1BandMin,mZa1BandMax,mZa2BandMin,mZa2BandMax)
    outfile.write(outfile_str)
    outfile.close()
    print "wrote fit bands to\n"+CMBandFname
    print "plots to file\n"+FigureBandFName
    print_line()


# ------------------------------------------------------------------------------- #
def linspace_single_core( band_min  , band_max  , NptsBand , Ncores , i_core ):
    tmp_min = np.min( [band_min , band_max] )
    band_max = np.max( [band_min , band_max] )
    band_min = tmp_min
    step = math.fabs(band_max - band_min)/Ncores
    min = band_min + (float(i_core)/Ncores)*(band_max - band_min)
    max = min + float(band_max - band_min)/Ncores
    res = np.arange( min , max , step )
    return res




# ------------------------------------------------------------------------------- #
def generate_runs_with_different_parameters( cm_fits_parameters , cm_pars_bands ,
                                             start_run , RunsInfoFileName , debug , PmissBins , SimParametersFileName , target ,
                                             NptsBand , Ncores , i_core ):
    # returns the generated run numbers
    
    # the data (nominal values)
    ana_data = TAnalysisEG2( "ppSRCCut_DATA_%s"% target )
    path = "/Users/erezcohen/Desktop/DataMining/Analysis_DATA/ppSRCcm"
    
    DATAsXfit_unweighted , DATAsXfiterr_unweighted = cm_fits_parameters.sXfit_unweighted , cm_fits_parameters.sXfiterr_unweighted
    DATAsYfit_unweighted , DATAsYfiterr_unweighted = cm_fits_parameters.sYfit_unweighted , cm_fits_parameters.sYfiterr_unweighted
    DATAsZa1_unweighted  , DATAsZa1err_unweighted  = cm_fits_parameters.sZa1_unweighted  , cm_fits_parameters.sZa1err_unweighted
    DATAsZa2_unweighted  , DATAsZa2err_unweighted  = cm_fits_parameters.sZa2_unweighted  , cm_fits_parameters.sZa2err_unweighted
    DATAmXfit_unweighted , DATAmXfiterr_unweighted = cm_fits_parameters.mXfit_unweighted , cm_fits_parameters.mXfiterr_unweighted
    DATAmYfit_unweighted , DATAmYfiterr_unweighted = cm_fits_parameters.mYfit_unweighted , cm_fits_parameters.mYfiterr_unweighted
    DATAmZa1_unweighted  , DATAmZa1err_unweighted  = cm_fits_parameters.mZa1_unweighted  , cm_fits_parameters.mZa1err_unweighted
    DATAmZa2_unweighted  , DATAmZa2err_unweighted  = cm_fits_parameters.mZa2_unweighted  , cm_fits_parameters.mZa2err_unweighted
    DATA_ST_unweighted   , DATA_STErr_unweighted = 0.5*(DATAsXfit_unweighted+DATAsYfit_unweighted)  , math.sqrt(DATAsXfiterr_unweighted*DATAsXfiterr_unweighted + DATAsYfiterr_unweighted*DATAsYfiterr_unweighted)

    DATAsXfit_weighted , DATAsXfiterr_weighted = cm_fits_parameters.sXfit_weighted , cm_fits_parameters.sXfiterr_weighted
    DATAsYfit_weighted , DATAsYfiterr_weighted = cm_fits_parameters.sYfit_weighted , cm_fits_parameters.sYfiterr_weighted
    DATAsZa1_weighted  , DATAsZa1err_weighted  = cm_fits_parameters.sZa1_weighted  , cm_fits_parameters.sZa1err_weighted
    DATAsZa2_weighted  , DATAsZa2err_weighted  = cm_fits_parameters.sZa2_weighted  , cm_fits_parameters.sZa2err_weighted
    DATAmXfit_weighted , DATAmXfiterr_weighted = cm_fits_parameters.mXfit_weighted , cm_fits_parameters.mXfiterr_weighted
    DATAmYfit_weighted , DATAmYfiterr_weighted = cm_fits_parameters.mYfit_weighted , cm_fits_parameters.mYfiterr_weighted
    DATAmZa1_weighted  , DATAmZa1err_weighted  = cm_fits_parameters.mZa1_weighted  , cm_fits_parameters.mZa1err_weighted
    DATAmZa2_weighted  , DATAmZa2err_weighted  = cm_fits_parameters.mZa2_weighted  , cm_fits_parameters.mZa2err_weighted
    DATA_ST_weighted   , DATA_STErr_weighted = 0.5*(DATAsXfit_weighted+DATAsYfit_weighted)  , math.sqrt(DATAsXfiterr_weighted*DATAsXfiterr_weighted + DATAsYfiterr_weighted*DATAsYfiterr_weighted)


    RunsInfoFile = append2RunsInfoFile(RunsInfoFileName)
    SimParametersFile = append2SimParametersFile(SimParametersFileName)
    generated_runs = []
    # the bands around data (around nominal values)
    sigT = linspace_single_core( cm_pars_bands.sTBandMin[0]  ,cm_pars_bands.sTBandMax[0]    , NptsBand , Ncores , i_core )
    sigLa1 = linspace_single_core( cm_pars_bands.sZa1Min[0]  ,cm_pars_bands.sZa1Max[0]      , NptsBand , Ncores , i_core )
    sigLa2 = linspace_single_core( cm_pars_bands.sZa2Min[0]  ,cm_pars_bands.sZa2Max[0]      , NptsBand , 1 , 0 ) # ToDo: change this to Ncores , i_core
    meanLa1 = linspace_single_core( cm_pars_bands.mZa1Min[0]  ,cm_pars_bands.mZa1Max[0]     , NptsBand , 1 , 0 ) # ToDo: change this to Ncores , i_core
    meanLa2 = linspace_single_core( cm_pars_bands.mZa2Min[0]  ,cm_pars_bands.mZa2Max[0]     , NptsBand , 1 , 0 ) # ToDo: change this to Ncores , i_core
    
    NrunsThisCore , NrunsTotal = len(sigT)*len(sigLa1)*len(sigLa2)*len(meanLa1)*len(meanLa2) , NptsBand*NptsBand*1*1*1
    if (debug>0): print '\033[95m' + 'Core %d (out of %d) will procees %d runs (total %d runs)'%(i_core,Ncores,NrunsThisCore,NrunsTotal) + '\033[0m'
    print_line
    run = start_run + (i_core+1)*1000


    # event generation (and analysis) loop
    for sT in sigT:
        for sLa1 in sigLa1:
            for sLa2 in sigLa1:
                for mLa1 in meanLa1:
                    for mLa2 in meanLa2:
                        run = run+1
                        generated_runs.append(run)
                        out_string = "%d"%run+","+str(datetime.datetime.now().strftime("%Y%B%d"))
                        out_string += ",%f"%sT+",%f"%sLa1+",%f"%sLa2+",%f"%mLa1+",%f"%mLa2
                        RunsInfoFile.write( out_string + "\n" )
                        
                        # (1) generate the simulated data (the 'run')
                        gen_events = GenerateEvents( path , run , debug )
                        gen_events.SetNRand( 1 )
                        gen_events.Set_eep_Parameters( sT , sLa1 , sLa2 , mLa1 , mLa2 )
                        pAcceptacneFile = ROOT.TFile("/Users/erezcohen/Desktop/DataMining/GSIM_DATA/PrecoilAcceptance.root")
                        '''
                            recoil proton acceptances:
                            (a) efficiency and acceptacne from the 'uniform' map i've generated using virtual CLAS
                            (b) proton fiducial cuts (coded inside the event generator class)
                        '''
                        gen_events.Use_protonAcceptacne( True )
                        h = pAcceptacneFile.Get("hRescaled")
                        gen_events.Set_protonAcceptacne( h )
                        gen_events.DoGenerate( "(e,e'pp)" , True , False )


                        # (2) analyze the simulated data (the 'run') similarly to the data - reconstructed parameters
                        ana_sim = TAnalysisEG2( path + '/eg_rootfiles', 'run%d'%run , ROOT.TCut('') )
                        calc_cm_parameters( ana_sim  , PmissBins , CMParsFname( path + '/eg_cm_parameters/run%d_'%run ) , CMRooFitsName( path + '/eg_cm_roofits/run%d_'%run ) )
                        cm_parameters = pd.read_csv( CMParsFname( path + '/eg_cm_parameters/run%d_'%run ) )
                        plot_cm_parameters( cm_parameters , CMfitsFname( path + '/eg_cm_fits/run%d_'%run ) , FigureFName( path + '/eg_cm_figures/run%d_'%run ) )
                        cm_fits_parameters = pd.read_csv( CMfitsFname( path + '/eg_cm_fits/run%d_'%run ) )

                        # No Mott/FF - weighting
                        # un - weighted roofit results
                        # ----------------------------
                        sXfit_unweighted   , sXfiterr_unweighted      = cm_fits_parameters.sXfit_unweighted , cm_fits_parameters.sXfiterr_unweighted
                        sYfit_unweighted   , sYfiterr_unweighted      = cm_fits_parameters.sYfit_unweighted , cm_fits_parameters.sYfiterr_unweighted
                        sLa1rec_unweighted , sLa1recErr_unweighted    = cm_fits_parameters.sZa1_unweighted , cm_fits_parameters.sZa1err_unweighted
                        sLa2rec_unweighted , sLa2recErr_unweighted    = cm_fits_parameters.sZa2_unweighted , cm_fits_parameters.sZa2err_unweighted
                        mXfit_unweighted   , mXfiterr_unweighted      = cm_fits_parameters.mXfit_unweighted , cm_fits_parameters.mXfiterr_unweighted
                        mYfit_unweighted   , mYfiterr_unweighted      = cm_fits_parameters.mYfit_unweighted , cm_fits_parameters.mYfiterr_unweighted
                        mLa1rec_unweighted , mLa1recErr_unweighted    = cm_fits_parameters.mZa1_unweighted , cm_fits_parameters.mZa1err_unweighted
                        mLa2rec_unweighted , mLa2recErr_unweighted    = cm_fits_parameters.mZa2_unweighted , cm_fits_parameters.mZa2err_unweighted
                        sTrec_unweighted   , sTrecErr_unweighted      = 0.5*(sXfit_unweighted+sYfit_unweighted) , math.sqrt(sXfit_unweighted*sXfit_unweighted+sYfit_unweighted*sYfit_unweighted)
                        
                        # write the results into file
                        out_string += ",%f"%sTrec_unweighted+",%f"%sTrecErr_unweighted
                        out_string += ",%f"%sLa1rec_unweighted+",%f"%sLa1recErr_unweighted+",%f"%sLa2rec_unweighted+",%f"%sLa2recErr_unweighted
                        out_string += ",%f"%mLa1rec_unweighted+",%f"%mLa1recErr_unweighted+",%f"%mLa2rec_unweighted+",%f"%mLa2recErr_unweighted

                        # compute N(sigma), the distance of the recosntructed parameter from the data-fit parameter
                        NsigST_unweighted = Nsigma( sTrec_unweighted , sTrecErr_unweighted  , DATA_ST_unweighted , DATA_STErr_unweighted )
                        NsigSL_a1_unweighted = Nsigma( sLa1rec_unweighted , sLa1recErr_unweighted , DATAsZa1_unweighted , DATAsZa1err_unweighted )
                        NsigSL_a2_unweighted = Nsigma( sLa2rec_unweighted , sLa2recErr_unweighted , DATAsZa2_unweighted , DATAsZa2err_unweighted )
                        NsigML_a1_unweighted = Nsigma( mLa1rec_unweighted , mLa1recErr_unweighted , DATAmZa1_unweighted , DATAmZa1err_unweighted )
                        NsigML_a2_unweighted = Nsigma( mLa2rec_unweighted , mLa2recErr_unweighted , DATAmZa2_unweighted , DATAmZa2err_unweighted )
                        NsigAvg_unweighted = (NsigST_unweighted + NsigSL_a1_unweighted + NsigSL_a2_unweighted + NsigML_a1_unweighted + NsigML_a2_unweighted)/5.
                        out_string += ",%f"%NsigST_unweighted+",%f"%NsigSL_a1_unweighted+",%f"%NsigSL_a2_unweighted+",%f"%NsigML_a1_unweighted+",%f"%NsigML_a2_unweighted+",%f"%NsigAvg_unweighted
                        # ----------------------------


                        # With Mott/FF - weighting
                        # weighted roofit results
                        # ----------------------------
                        sXfit_weighted   , sXfiterr_weighted      = cm_fits_parameters.sXfit_weighted , cm_fits_parameters.sXfiterr_weighted
                        sYfit_weighted   , sYfiterr_weighted      = cm_fits_parameters.sYfit_weighted , cm_fits_parameters.sYfiterr_weighted
                        sLa1rec_weighted , sLa1recErr_weighted    = cm_fits_parameters.sZa1_weighted , cm_fits_parameters.sZa1err_weighted
                        sLa2rec_weighted , sLa2recErr_weighted    = cm_fits_parameters.sZa2_weighted , cm_fits_parameters.sZa2err_weighted
                        mXfit_weighted   , mXfiterr_weighted      = cm_fits_parameters.mXfit_weighted , cm_fits_parameters.mXfiterr_weighted
                        mYfit_weighted   , mYfiterr_weighted      = cm_fits_parameters.mYfit_weighted , cm_fits_parameters.mYfiterr_weighted
                        mLa1rec_weighted , mLa1recErr_weighted    = cm_fits_parameters.mZa1_weighted , cm_fits_parameters.mZa1err_weighted
                        mLa2rec_weighted , mLa2recErr_weighted    = cm_fits_parameters.mZa2_weighted , cm_fits_parameters.mZa2err_weighted
                        sTrec_weighted   , sTrecErr_weighted      = 0.5*(sXfit_weighted+sYfit_weighted) , math.sqrt(sXfit_weighted*sXfit_weighted+sYfit_weighted*sYfit_weighted)
                        
                        
                        
                        # write the results into file
                        out_string += ",%f"%sTrec_weighted+",%f"%sTrecErr_weighted
                        out_string += ",%f"%sLa1rec_weighted+",%f"%sLa1recErr_weighted+",%f"%sLa2rec_weighted+",%f"%sLa2recErr_weighted
                        out_string += ",%f"%mLa1rec_weighted+",%f"%mLa1recErr_weighted+",%f"%mLa2rec_weighted+",%f"%mLa2recErr_weighted

                        # compute N(sigma), the distance of the recosntructed parameter from the data-fit parameter
                        NsigST_weighted = Nsigma( sTrec_weighted , sTrecErr_weighted  , DATA_ST_weighted , DATA_STErr_weighted )
                        NsigSL_a1_weighted = Nsigma( sLa1rec_weighted , sLa1recErr_weighted , DATAsZa1_weighted , DATAsZa1err_weighted )
                        NsigSL_a2_weighted = Nsigma( sLa2rec_weighted , sLa2recErr_weighted , DATAsZa2_weighted , DATAsZa2err_weighted )
                        NsigML_a1_weighted = Nsigma( mLa1rec_weighted , mLa1recErr_weighted , DATAmZa1_weighted , DATAmZa1err_weighted )
                        NsigML_a2_weighted = Nsigma( mLa2rec_weighted , mLa2recErr_weighted , DATAmZa2_weighted , DATAmZa2err_weighted )
                        NsigAvg_weighted = (NsigST_weighted + NsigSL_a1_weighted + NsigSL_a2_weighted + NsigML_a1_weighted + NsigML_a2_weighted)/5.
                        out_string += ",%f"%NsigST_weighted+",%f"%NsigSL_a1_weighted+",%f"%NsigSL_a2_weighted+",%f"%NsigML_a1_weighted+",%f"%NsigML_a2_weighted+",%f"%NsigAvg_weighted
                        # ----------------------------
                        
                        # KS test for the c.m. distributions in x,y,z directions
                        KSpCMx = KStest( ana_sim , ana_data , "pcmX" ) # maybe make it 2D, with adding the pmiss magnitude as a second variable?
                        KSpCMy = KStest( ana_sim , ana_data , "pcmY" )
                        KSpCMz = KStest( ana_sim , ana_data , "pcmZ" )
                        KSavg = (KSpCMx + KSpCMy + KSpCMz)/3.
                        out_string += ",%f"%KSpCMx+",%f"%KSpCMy+",%f"%KSpCMz+",%f"%KSavg

                        SimParametersFile.write( out_string + '\n' )
                        print_important( "completed run %d"%run )
                        print_line()







    RunsInfoFile.close()
    SimParametersFile.close()
    print "done... see \n"+RunsInfoFileName+"\n"+SimParametersFileName
    print_line()
    return generated_runs
