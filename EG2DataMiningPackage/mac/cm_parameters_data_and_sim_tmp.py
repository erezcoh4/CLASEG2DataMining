'''
    usage:
    ---------
    python mac/cm_parameters_data_and_sim.py --option=generate
    
    options (can be ran simultaneously):
            acceptance  {"recoil proton acceptance"}
            scheme      {"scheme pp-SRC"}
            extract     {"extract data cm-parameters"}
            bends       {"create bands for EG"}
            generate    {"generate and analyze runs"}
    
'''

from definitions import *
import cm_tools as tools

PmissBins = [[0.3,0.45]  , [0.45,0.55] , [0.55,0.65] , [0.65,0.75] , [0.75,1.0]]
#PmissBins = [[0.3,0.5]  , [0.5,0.7] , [0.7,1.0]]
A = 12
start_run  = flags.run
dm = TEG2dm()


if 'recoil proton acceptance' in flags.option or 'acceptance' in flags.option:
    pAcceptacneFile = ROOT.TFile("/Users/erezcohen/Desktop/DataMining/GSIM_DATA/PrecoilAcceptance.root")
    hAcceptance = pAcceptacneFile.Get("hRescaled")
    hAcceptance.Draw()
#    hThetaPhi = hAcceptance.Project3D("xy")




if 'scheme pp-SRC' in flags.option or 'scheme' in flags.option: # scheme to pp-SRC

    DataName    = "DATA_%s"% dm.Target(flags.atomic_mass)
    SchemedName = "ppSRCCut_%s"% DataName
    ana     = TAnalysisEG2( path+"/AnaFiles" , "Ana_SRCPmissXb_"+DataName , flags.cut )
    scheme  = TSchemeDATA()
    scheme.SchemeOnTCut( path+"/AnaFiles" , "Ana_SRCPmissXb_"+DataName+".root", "anaTree", "Ana_"+SchemedName+".root", ana.ppSRCCut + ana.PrecFiducial)
    print 'schemed to %s'%SchemedName


if 'extract data cm-parameters' in flags.option or 'extract' in flags.option: # DATA

    # (1) calc cm parameters of data
    ana_data = TAnalysisEG2( "ppSRCCut_DATA_%s"% dm.Target(A) )
    cm_parameters = tools.calc_cm_parameters( ana_data  , PmissBins , tools.CMRooFitsName( ppPath + '/DATA/unweighted' ) , tools.CMRooFitsName( ppPath + '/DATA/weighted' ) , DoSaveCanvas = True )
    cm_parameters.to_csv( tools.CMParsFname(ppPath+'/DATA/data') , header=True , index = False)
    tools.print_filename( tools.CMParsFname(ppPath+'/DATA/data')  ,"data c.m. parameters for different p(miss) bins at")
    tools.print_line()

    # (2) plot cm parameters
    fits = tools.fit_cm_parameters( 'data' , cm_parameters , tools.FigureFName(ppPath+'/DATA/data') , DoPlot = True )
    fits.to_csv( tools.CMfitsFname(ppPath+'/DATA/data') , header=True , index = False)
    tools.print_filename( tools.CMfitsFname(ppPath+'/DATA/data')  ,"data c.m. fits at")
    tools.print_line()


if 'create bands for EG' in flags.option or 'bands' in flags.option:

    # (3) create bands for event generation
    cm_parameters = pd.read_csv( tools.CMParsFname(ppPath+'/DATA/data') )
    fits = pd.read_csv( tools.CMfitsFname( ppPath+'/DATA/data' ) )
    tools.generate_cm_bands( cm_parameters , fits , tools.CMBandFname( ppPath+'/DATA/data' ) , tools.FigureBandFName( ppPath+'/DATA/data' ) , DoSaveCanvas = True)


if 'generate and analyze runs' in flags.option or 'generate' in flags.option or 'analyze' in flags.option or 'analyse' in flags.option:
    
    # (4) generate runs with different parameters
    cm_pars_bands = pd.read_csv( tools.CMBandFname(ppPath+'/DATA/data') )
    cm_fits_parameters = pd.read_csv( tools.CMfitsFname( ppPath+'/DATA/data' ) )
    NRand = 10
    NptsBand = 10 # if flags.files_frac<1 else flags.files_frac
    start_run = 10000
    tools.generate_runs_with_different_parameters( flags.option ,
                                                  cm_fits_parameters , cm_pars_bands , NRand ,
                                                  start_run , flags.verbose , PmissBins ,
                                                  tools.resutlsFName( ppPath+'/simulation/simulation' ) , tools.buildup_resutlsFName( ppPath+'/simulation/simulation' ) , tools.CMfitsFname( ppPath + '/simulation/simulation' ) , dm.Target(A)  ,
                                                  NptsBand )





if 'find the best paramteres' in flags.option:

    # (5) find the best-correspondance from the generated runs, to estimate nature's parameteres
    tools.print_filename(tools.SimParametersFileName( ppPath+'/simulation/' ),'reading file ')
    simulation_results = pd.read_csv( tools.SimParametersFileName( ppPath+'/simulation/' ) )
#    tools.plot( simulation_results , 'genSigmaT' , 'recSigmaT_unweighted' )
#    tools.plot( simulation_results , 'KSpCMx' , 'KSpCMy' )
#    tools.plot( simulation_results , 'genSigmaT' , 'NsigST_unweighted' , 'generated $\sigma_T$ [GeV/c]' , 'unweighted N$\sigma$ ($\sigma_T$)' )
    tools.plot( simulation_results , 'genSigmaL_a1' , 'NsigSL_a1_unweighted' , 'generated a$_1$ ($\sigma_z$) [GeV/c]' , 'unweighted N$\sigma$ (a$_1$ ($\sigma_z$))' )
#    tools.find_best_parameters( simulation_results )



