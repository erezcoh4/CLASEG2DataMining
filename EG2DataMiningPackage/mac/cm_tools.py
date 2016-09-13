import time , sys , os , math , datetime
import matplotlib , pandas as pd , numpy as np
from matplotlib import pyplot as plt

# ------------------------------------------------------------------------------- #
# file names
def CMParsFname( path ):
    return path+"/CMparameters.csv"
def CMFitsFname( path ):
    return path+"/CMparameter_Fits.csv"
def CMBandFname( path ):
    return path+"/CMparameter_Bands.csv"
def FigureFName( path ):
    return path+"/cm_width_and_mean.pdf"
def FigureBandFName( path ):
    return path+"/cm_width_and_mean_Bands.pdf"
def RunsInfoFileName( path ):
    return path+"/EG_simulated_runs_Info.csv"

# ------------------------------------------------------------------------------- #
def append2RunsInfoFile(RunsInfoFileName):
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
def calc_cm_parameters( fana  , PmissBins , outFileName ):
    outfile = open( outFileName , "wb")
    outfile.write('\n\n')
    outfile.write("pMiss_min,pMiss_max,mean_x,mean_xErr,sigma_x,sigma_xErr,mean_y,mean_yErr,sigma_y,sigma_yErr,mean_z,mean_zErr,sigma_z,sigma_zErr\n")
    for i in range(len(PmissBins)):
        print "p(miss) bin %d\n"%i
        x = fana.RooFitCM(PmissBins[i][0],PmissBins[i][1]) # RooFitCM return a parameter vector
        outfile.write("%.2f,%.2f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f\n" % ( PmissBins[i][0],PmissBins[i][1] ,x(0,0) ,x(0,1) ,x(1,0) ,x(1,1) , x(2,0) ,x(2,1) ,x(3,0), x(3,1) , x(4,0), x(4,1) , x(5,0), x(5,1)))
    outfile.write('\n\n')
    outfile.close()
    print "from \n/Users/erezcohen/Desktop/DataMining/AnaFiles/Ana_"+outFileName+".root"
    print "done calculating parameters, output can be found in the file:\n", outfile.name


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
def generate_cm_bands( data , run , CMFitsFname , CMBandFname , RunsInfoFileName , FigureBandFName ):
    
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
    ax.grid(True,linestyle='-',color='0.95')
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
    ax.grid(True,linestyle='-',color='0.95')
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






def generate_runs_with_different_parameters( data , run , RunsInfoFile ):

    RunsInfoFile = append2RunsInfoFile(RunsInfoFileName)

    for sT in sigT:
        for sLa1 in sigLa1:
            for sLa2 in sigLa1:
                for mLa1 in meanLa1:
                    for mLa2 in meanLa2:
                        run = run+1
                        par_str = "%d"%run+","+str(datetime.datetime.now().strftime("%Y%B%d"))
                        par_str += ",%f"%sT+",%f"%sLa1+",%f"%sLa2+",%f"%mLa1+",%f"%mLa2+"\n"
                        RunsInfoFile.write( par_str )
                        # generate the simulated data (the 'run')
                        gen_events = GenerateEvents( path , run , debug )
                        gen_events.SetNRand( 1 )
                        gen_events.Set_eep_Parameters( sT , sLa1 , sLa2 , mLa1 , mLa2 )
                        gen_events.Set_protonAcceptacne( ROOT.TFile("/Users/erezcohen/Desktop/DataMining/GSIM_DATA/").Get("PrecoilAcceptance.root") )
                        # ToDo: implement this method in GenerateEvents::Set_protonAcceptacne(TH3F * h) that accepts or doesn't accept the recoil proton by generating a random number and asking if it is smaller than
                        # ( h -> Interpolate(Double_t Pmag, Double_t theta , Double_t phi); in % )
                        # and thus deciding weather or not to accept this event....
                        gen_events.DoGenerate( "(e,e'pp)" , True , False )

                        # analyze the simulated data (the 'run') similarly to the data,
                        # to get the parameters after CLAS acceptance and the cut



    RunsInfoFile.close()
    print "done... see \n",RunsInfoFileName

