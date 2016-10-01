import time , sys , os , math , datetime , ROOT
import matplotlib , pandas as pd , numpy as np
from matplotlib import pyplot as plt
from ROOT import TAnalysisEG2,GenerateEvents

# ------------------------------------------------------------------------------- #
# file names
def CMParsFname( path ):
    return path+"CMparameters.csv"
def CMRooFitsName( path ):
    return path+"CMRooFits.pdf"
def CMFitsFname( path ):
    return path+"CMparameter_Fits.csv"
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
    try:
        if os.stat(SimParametersFileName).st_size > 0:
            SimParametersFile = open(SimParametersFileName,'a')
        else:
            SimParametersFile = open(SimParametersFileName,'wb')
            SimParametersFile.write( "run,time,genSigmaT,genSigmaL_a1,genSigmaL_a2,genShiftL_a1,genShiftL_a2,recSigmaT,recSigmaL_a1,recSigmaL_a2,recShiftL_a1,recShiftL_a2\n" )
    except OSError:
        SimParametersFile = open(SimParametersFileName,'wb')
        SimParametersFile.write( "run,time,genSigmaT,genSigmaL_a1,genSigmaL_a2,genShiftL_a1,genShiftL_a2,recSigmaT,recSigmaL_a1,recSigmaL_a2,recShiftL_a1,recShiftL_a2\n" )
    return SimParametersFile

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
# ToDo: add cross-section weighting to the fits
def calc_cm_parameters( fana  , PmissBins , outFileName , plotsFileName):
    outfile = open( outFileName , "wb")
    outfile.write('\n\n')
    outfile.write("pMiss_min,pMiss_max,mean_x,mean_xErr,sigma_x,sigma_xErr,mean_y,mean_yErr,sigma_y,sigma_yErr,mean_z,mean_zErr,sigma_z,sigma_zErr\n")
    canvas = fana.CreateCanvas( "RooFit plots" , "Divide" , 3 , len(PmissBins) )
    for i in range(len(PmissBins)):
        print "p(miss) bin %d\n"%i
        x = fana.RooFitCM(PmissBins[i][0],PmissBins[i][1] , True, canvas, 3*i + 1) # RooFitCM return a parameter vector
        outfile.write("%.2f,%.2f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f\n" % ( PmissBins[i][0],PmissBins[i][1] ,x(0,0) ,x(0,1) ,x(1,0) ,x(1,1) , x(2,0) ,x(2,1) ,x(3,0), x(3,1) , x(4,0), x(4,1) , x(5,0), x(5,1)))
    outfile.write('\n\n')
    outfile.close()
    print "from \n"+fana.GetFile().GetName()
    print "done calculating parameters, output can be found in the file:\n", outfile.name
    canvas.SaveAs(plotsFileName)
    print "see plots at \n"+plotsFileName




# ------------------------------------------------------------------------------- #
def plot_cm_parameters( data , CMFitsFname , FigureFName ):

    Pmiss = (data.pMiss_max + data.pMiss_min)/2.
    pMissUpErr , pMissLowErr = data.pMiss_max - Pmiss , Pmiss - data.pMiss_min

    fig = plt.figure(figsize=(40,10))
    ax = fig.add_subplot(121)
    ax.text( 0.3 , 0.2 , "no acc. corr." , fontsize=80 , color='red' , alpha = 0.15 )
    ax.grid(True,linestyle='-',color='0.95')
    [sXfit,sXfiterr] = plot_errorbar_and_fit( ax , Pmiss, data.sigma_x ,
                                             [pMissLowErr,pMissUpErr] , [data.sigma_xErr,data.sigma_xErr],
                                             'black'  ,'v','none',r'$\sigma_{x}$' ,'const')
    [sYfit,sYfiterr] = plot_errorbar_and_fit( ax , Pmiss, data.sigma_y ,
                                             [pMissLowErr,pMissUpErr] , [data.sigma_yErr,data.sigma_yErr],
                                             'red'    ,'o','none',r'$\sigma_{y}$' ,'const')
    [sZa1,sZa1err],[sZa2,sZa2err] = plot_errorbar_and_fit( ax , Pmiss, data.sigma_z ,
                                                          [pMissLowErr,pMissUpErr] , [data.sigma_zErr,data.sigma_zErr],
                                                          'blue'   ,'s','none',r'$\sigma_{\vec{p}_{miss}}$' ,'linear', 0.5)
    plt.xlabel( r'$p_{miss}$ [GeV/c]',fontsize=25)
    plt.ylabel( r'c.m. momentum width [Gev/c]',fontsize=25)
    ax.legend(loc="upper left",scatterpoints=1)

    ax = fig.add_subplot(122)
    ax.text( 0.3 , 0.15 , "no acc. corr." , fontsize=80 , color='red' , alpha = 0.15 )
    ax.grid(True,linestyle='-',color='0.95')
    [mXfit,mXfiterr] = plot_errorbar_and_fit( ax , Pmiss, data.mean_x ,
                                             [pMissLowErr,pMissUpErr] , [data.mean_xErr,data.mean_xErr],
                                             'black' ,'v','none',r'$mean_{x}$' ,'const')
    [mYfit,mYfiterr] = plot_errorbar_and_fit( ax , Pmiss, data.mean_y ,
                                             [pMissLowErr,pMissUpErr] , [data.mean_yErr,data.mean_yErr],
                                             'red'   ,'v','none',r'$mean_{y}$' ,'const')
    [mZa1,mZa1err],[mZa2,mZa2err] = plot_errorbar_and_fit( ax , Pmiss, data.mean_z ,
                                                          [pMissLowErr,pMissUpErr] , [data.mean_zErr,data.mean_zErr],
                                                          'blue'  ,'v','none',r'$mean_{\vec{p}_{miss}}$' ,'linear', 0.3)

    plt.xlabel( r'$p_{miss}$ [GeV/c]',fontsize=25)
    plt.ylabel( r'c.m. momentum mean [Gev/c]',fontsize=25)
    ax.legend(loc="upper left",scatterpoints=1)
    plt.savefig(FigureFName)
    
    outfile = open(CMFitsFname, "wb")
    outfile.write("sXfit,sXfiterr,sYfit,sYfiterr,sZa1,sZa1err,sZa2,sZa2err,mXfit,mXfiterr,mYfit,mYfiterr,mZa1,mZa1err,mZa2,mZa2err\n")
    outfile_str = "%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f"%(sXfit,sXfiterr,sYfit,sYfiterr,
                                                                     sZa1,sZa1err,sZa2,sZa2err,
                                                                     mXfit,mXfiterr,mYfit,mYfiterr,
                                                                     mZa1,mZa1err,mZa2,mZa2err)
    outfile.write(outfile_str)
    outfile.close()
    print "wrote fit parameters to\n"+CMFitsFname
    print "and plot can be found at\n"+FigureFName




# ------------------------------------------------------------------------------- #
def generate_cm_bands( cm_parameters , run , CMFitsFname , CMBandFname , RunsInfoFileName , FigureBandFName ):
    
    data = cm_parameters
    Pmiss = (data.pMiss_max + data.pMiss_min)/2.
    pMissUpErr , pMissLowErr = data.pMiss_max - Pmiss , Pmiss - data.pMiss_min
    
    RunsInfoFile = append2RunsInfoFile(RunsInfoFileName)
    cm_fits_parameters = pd.read_csv(CMFitsFname)

    sXfit , sXfiterr = cm_fits_parameters.sXfit , cm_fits_parameters.sXfiterr
    sYfit , sYfiterr = cm_fits_parameters.sYfit , cm_fits_parameters.sYfiterr
    sZa1  , sZa1err  = cm_fits_parameters.sZa1 , cm_fits_parameters.sZa1err
    sZa2  , sZa2err  = cm_fits_parameters.sZa2 , cm_fits_parameters.sZa2err
    mXfit , mXfiterr = cm_fits_parameters.mXfit , cm_fits_parameters.mXfiterr
    mYfit , mYfiterr = cm_fits_parameters.mYfit , cm_fits_parameters.mYfiterr
    mZa1  , mZa1err  = cm_fits_parameters.mZa1 , cm_fits_parameters.mZa1err
    mZa2  , mZa2err  = cm_fits_parameters.mZa2 , cm_fits_parameters.mZa2err
    sTfit , sTfiterr = 0.5*(sXfit+sYfit) , math.sqrt(sXfit*sXfit+sYfit*sYfit)


    sTBand = np.ones(len(Pmiss))*[sTfit*0.9,sTfit*1.1]
    sZa1BandMin , sZa1BandMax = sZa1*0.9,sZa1*1.1
    sZa2BandMin , sZa2BandMax = sZa2*0.9,sZa2*1.1
    sZBandMax = float(sZa1BandMax)*(Pmiss-0.5)+float(sZa2BandMax)
    sZBandMin = float(sZa1BandMin)*(Pmiss-0.5)+float(sZa2BandMin)

    fig = plt.figure(figsize=(40,10))
    ax = fig.add_subplot(121)
    plt.errorbar(Pmiss, data.sigma_x, xerr=[pMissLowErr,pMissUpErr], yerr=[data.sigma_xErr,data.sigma_xErr]
                 , color='black', marker='v' , linestyle='none' , label=None)
    plt.errorbar(Pmiss, data.sigma_y, xerr=[pMissLowErr,pMissUpErr], yerr=[data.sigma_yErr,data.sigma_yErr]
                 , color='red', marker='o' , linestyle='none' , label=None)
    ax.plot(Pmiss, float(sTfit)*np.ones(len(Pmiss)) , color='0.65' )

    plt.fill_between(Pmiss, sTBand[0] , sTBand[1] ,alpha=0.5, edgecolor='#CC4F1B', facecolor='#FF9848')


    plt.errorbar(Pmiss, data.sigma_z, xerr=[pMissLowErr,pMissUpErr], yerr=[data.sigma_zErr,data.sigma_zErr]
                 , color='blue', marker='s' , linestyle='none' , label=None)
    ax.plot(Pmiss, float(sZa1)*(Pmiss-0.5) + float(sZa2), color='0.65' )
    plt.fill_between(Pmiss, sZBandMin , sZBandMax ,alpha=0.5, edgecolor='#C14F1B', facecolor='#1122CC')
    plt.xlabel( r'$p_{miss}$ [GeV/c]' ,fontsize=25)
    plt.ylabel( r'c.m. momentum width [Gev/c]',fontsize=25)


    mTBand = np.zeros(len(Pmiss))
    mZa1BandMin , mZa1BandMax = mZa1*0.8,mZa1*1.2
    mZa2BandMin , mZa2BandMax = mZa2*0.8,mZa2*1.2
    mZBandMax = float(mZa1BandMax)*(Pmiss-0.3)+float(mZa2BandMax)
    mZBandMin = float(mZa1BandMin)*(Pmiss-0.3)+float(mZa2BandMin)

    ax = fig.add_subplot(122)
    plt.errorbar(Pmiss, data.mean_x, xerr=[pMissLowErr,pMissUpErr], yerr=[data.mean_xErr,data.mean_xErr]
                 , color='black', marker='v' , linestyle='none' , label=None)
    plt.errorbar(Pmiss, data.mean_y, xerr=[pMissLowErr,pMissUpErr], yerr=[data.mean_yErr,data.mean_yErr]
                 , color='red', marker='o' , linestyle='none' , label=None)
    ax.plot(Pmiss, np.zeros(len(Pmiss)) , color='0.65' )

    plt.errorbar(Pmiss, data.mean_z, xerr=[pMissLowErr,pMissUpErr], yerr=[data.mean_zErr,data.mean_zErr]
                 , color='blue', marker='s' , linestyle='none' , label=None)
    ax.plot(Pmiss, float(mZa1)*(Pmiss-0.3) + float(mZa2), color='0.65' )
    plt.fill_between(Pmiss, mZBandMin , mZBandMax ,alpha=0.5, edgecolor='#C14F1B', facecolor='#1122CC')

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





# ------------------------------------------------------------------------------- #
def generate_runs_with_different_parameters( cm_pars_bands , start_run , RunsInfoFileName , path , debug , PmissBins , SimParametersFileName ):
    # returns the generated run numbers

    RunsInfoFile = append2RunsInfoFile(RunsInfoFileName)
    SimParametersFile = append2SimParametersFile(SimParametersFileName)
    run = start_run
    generated_runs = []
    print 'cm_pars_bands:',cm_pars_bands
    sigT = np.linspace(cm_pars_bands.sTBandMin[0]  ,cm_pars_bands.sTBandMax[0]  ,1)
    sigLa1 = np.linspace(cm_pars_bands.sZa1Min[0]  ,cm_pars_bands.sZa1Max[0]    ,1)
    sigLa2 = np.linspace(cm_pars_bands.sZa2Min[0]  ,cm_pars_bands.sZa2Max[0]    ,1)
    meanLa1 = np.linspace(cm_pars_bands.mZa1Min[0] ,cm_pars_bands.mZa1Max[0]    ,1)
    meanLa2 = np.linspace(cm_pars_bands.mZa2Min[0] ,cm_pars_bands.mZa2Max[0]    ,1)


    for sT in sigT:
        for sLa1 in sigLa1:
            for sLa2 in sigLa1:
                for mLa1 in meanLa1:
                    for mLa2 in meanLa2:
                        run = run+1
                        generated_runs.append(run)
                        par_str = "%d"%run+","+str(datetime.datetime.now().strftime("%Y%B%d"))
                        par_str += ",%f"%sT+",%f"%sLa1+",%f"%sLa2+",%f"%mLa1+",%f"%mLa2
                        RunsInfoFile.write( par_str + '\n' )
                        
                        # (1) generate the simulated data (the 'run')
                        gen_events = GenerateEvents( path , run , debug )
                        gen_events.SetNRand( 10 )
                        gen_events.Set_eep_Parameters( sT , sLa1 , sLa2 , mLa1 , mLa2 )
                        pAcceptacneFile = ROOT.TFile("/Users/erezcohen/Desktop/DataMining/GSIM_DATA/PrecoilAcceptance.root")
                        h = pAcceptacneFile.Get("hRescaled")
                        gen_events.Set_protonAcceptacne( h )
                        # ToDo: add proton fiducial cuts acceptance
                        gen_events.DoGenerate( "(e,e'pp)" , True , False )
                        
                        # (2) analyze the simulated data (the 'run') similarly to the data - reconstructed parameters
                        path = "/Users/erezcohen/Desktop/DataMining/Analysis_DATA/ppSRCcm"
                        ana_sim = TAnalysisEG2( path + '/eg_rootfiles', 'run%d'%run , ROOT.TCut('') )
                        calc_cm_parameters( ana_sim  , PmissBins , CMParsFname( path + '/eg_cm_parameters/run%d_'%run ) , CMRooFitsName( path + '/eg_cm_roofits/run%d_'%run ) )
                        cm_parameters = pd.read_csv( CMParsFname( path + '/eg_cm_parameters/run%d_'%run ) )
                        plot_cm_parameters( cm_parameters , CMFitsFname( path + '/eg_cm_fits/run%d_'%run ) , FigureFName( path + '/eg_cm_figures/run%d_'%run ) )
                        cm_fits_parameters = pd.read_csv( CMFitsFname( path + '/eg_cm_fits/run%d_'%run ) )
                        sXfit   , sXfiterr      = cm_fits_parameters.sXfit , cm_fits_parameters.sXfiterr
                        sYfit   , sYfiterr      = cm_fits_parameters.sYfit , cm_fits_parameters.sYfiterr
                        sLa1rec , sLa1recErr    = cm_fits_parameters.sZa1 , cm_fits_parameters.sZa1err
                        sLa2rec , sLa2recErr    = cm_fits_parameters.sZa2 , cm_fits_parameters.sZa2err
                        mXfit   , mXfiterr      = cm_fits_parameters.mXfit , cm_fits_parameters.mXfiterr
                        mYfit   , mYfiterr      = cm_fits_parameters.mYfit , cm_fits_parameters.mYfiterr
                        mLa1rec , mLa1recErr    = cm_fits_parameters.mZa1 , cm_fits_parameters.mZa1err
                        mLa2rec , mLa2recErr    = cm_fits_parameters.mZa2 , cm_fits_parameters.mZa2err
                        sTrec   , sTrecErr      = 0.5*(sXfit+sYfit) , math.sqrt(sXfit*sXfit+sYfit*sYfit)
                        par_str += ",%f"%sTrec+",%f"%sLa1rec+",%f"%sLa2rec+",%f"%mLa1rec+",%f"%mLa2rec
                        SimParametersFile.write( par_str + '\n' )
                        # ToDo: Add rooFit plots to monitor what the fuck is wrong with these not happening







    RunsInfoFile.close()
    SimParametersFile.close()
    print "done... see \n"+RunsInfoFileName+"\n"+SimParametersFileName
    return generated_runs
