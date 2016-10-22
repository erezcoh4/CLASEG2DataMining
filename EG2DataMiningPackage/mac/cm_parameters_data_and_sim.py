'''
    usage:
    ---------
    python mac/cm_parameters_data_and_sim.py --option="generate runs"
    
    options (can be ran simultaneously):
            "scheme pp-SRC"
            "extract data cm-parameters"
            "create bands for EG"
            "generate runs" -core=0
            "find the best paramteres"
    
'''



import ROOT , time , sys , math , datetime ,  matplotlib , pandas as pd , numpy as np
from ROOT import TPlots, TAnalysisEG2 , TEG2dm , TSchemeDATA ,GenerateEvents
sys.path.append('../mac') ; sys.path.append('../../mySoftware/MySoftwarePackage/mac')
import input_flags, cm_tools as tools
flags = input_flags.get_args()

PmissBins = [[0.3,0.45]  , [0.45,0.55] , [0.55,0.65] , [0.65,0.75] , [0.75,1.0]]
path = "/Users/erezcohen/Desktop/DataMining/Analysis_DATA/ppSRCcm"
A = 12
start_run  = flags.run
dm = TEG2dm()



if 'scheme pp-SRC' in flags.option: # scheme to pp-SRC

    DataName    = "DATA_%s"% dm.Target(flags.atomic_mass)
    SchemedName = "ppSRCCut_%s"% DataName
    ana     = TAnalysisEG2( "SRCPmissXb_"+DataName , flags.cut )
    scheme  = TSchemeDATA()
    scheme.SchemeOnTCut( "/Users/erezcohen/Desktop/DataMining/AnaFiles" , "Ana_SRCPmissXb_"+DataName+".root", "anaTree", "Ana_"+SchemedName+".root", ana.ppSRCCut + ana.PrecFiducial)
    print 'schemed to %s'%SchemedName


if 'extract data cm-parameters' in flags.option: # DATA

    # (1) calc cm parameters of data
    ana_data = TAnalysisEG2( "ppSRCCut_DATA_%s"% dm.Target(A) )
    cm_parameters = tools.calc_cm_parameters( ana_data  , PmissBins , tools.CMRooFitsName( path + '/DATA/unweighted' ) , tools.CMRooFitsName( path + '/DATA/weighted' ) , DoSaveCanvas = True )
    cm_parameters.to_csv( tools.CMParsFname(path+'/DATA/') , header=True , index = False)
    tools.print_filename( tools.CMParsFname(path+'/DATA/')  ,"data c.m. parameters for different p(miss) bins at"); tools.print_line

    # (2) plot cm parameters
    fits = tools.fit_cm_parameters( 'data' , cm_parameters , tools.FigureFName(path+'/DATA/') , DoSaveCanvas = True )
    fits.to_csv( tools.CMfitsFname(path+'/DATA/') , header=True , index = False)
    tools.print_filename( tools.CMfitsFname(path+'/DATA/')  ,"data c.m. fits at"); tools.print_line




if 'create bands for EG' in flags.option:

    # (3) create bands for event generation
    cm_parameters = pd.read_csv( tools.CMParsFname(path+'/DATA/') )
    fits = pd.read_csv( tools.CMfitsFname( path+'/DATA/' ) )
    tools.generate_cm_bands( cm_parameters , fits , tools.CMBandFname( path+'/DATA/' ) , tools.FigureBandFName( path+'/DATA/' ) , DoSaveCanvas = True)


if 'generate runs' in flags.option:
    
    # (4) generate runs with different parameters
    cm_pars_bands = pd.read_csv( tools.CMBandFname(path+'/DATA/') )
    cm_fits_parameters = pd.read_csv( tools.CMfitsFname( path+'/DATA/' ) )
    
    NptsBand = 4
    Ncores = 1 if flags.worker == "erez" else 50 if flags.worker == "helion" else 1
    if flags.i_core > Ncores:
        print 'error: i_core > Ncores!'
        exit(1)
    tools.generate_runs_with_different_parameters( cm_fits_parameters , cm_pars_bands , NRand = 10 ,
                                                  start_run , flags.verbose , PmissBins , tools.resutlsFName( path+'/simulation/' ) , tools.CMfitsFname( path + '/simulation/' ) , dm.Target(A)  ,
                                                  NptsBand , Ncores , flags.i_core )




if 'find the best paramteres' in flags.option:

    # (5) find the best-correspondance from the generated runs, to estimate nature's parameteres
    tools.print_filename(tools.SimParametersFileName( path+'/simulation/' ),'reading file ')
    simulation_results = pd.read_csv( tools.SimParametersFileName( path+'/simulation/' ) )
#    tools.plot( simulation_results , 'genSigmaT' , 'recSigmaT_unweighted' )
#    tools.plot( simulation_results , 'KSpCMx' , 'KSpCMy' )
#    tools.plot( simulation_results , 'genSigmaT' , 'NsigST_unweighted' , 'generated $\sigma_T$ [GeV/c]' , 'unweighted N$\sigma$ ($\sigma_T$)' )
    tools.plot( simulation_results , 'genSigmaL_a1' , 'NsigSL_a1_unweighted' , 'generated a$_1$ ($\sigma_z$) [GeV/c]' , 'unweighted N$\sigma$ (a$_1$ ($\sigma_z$))' )
#    tools.find_best_parameters( simulation_results )



