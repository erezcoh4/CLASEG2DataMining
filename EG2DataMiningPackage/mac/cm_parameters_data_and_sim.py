from definitions import *
from cm_tools import *
'''
    usage:
    ---------
    python mac/cm_parameters_data_and_sim.py --option=generate
    
    options (can be ran simultaneously):
    acceptance  {"recoil proton acceptance"}
    calc        {"calc. phys. vars."}
    scheme      {"scheme pp-SRC"}
    extract     {"extract data cm-parameters"}
    bends       {"create bands for EG"}
    generate    {"generate and analyze runs"}
    
'''


PmissBins = [[0.3,0.45]  , [0.45,0.55] , [0.55,0.65] , [0.65,0.75] , [0.75,1.0]]
#PmissBins = [[0.3,0.5]  , [0.5,0.7] , [0.7,1.0]] # 3 bins, irrelevant


# proton acceptance plot
# ----------------------------------------
if 'recoil proton acceptance' in flags.option or 'acceptance' in flags.option:
    print_important("ipynb notebooks/recoil_proton_acceptance.ipynb")


# (1) calculate physical variables
# ----------------------------------------
if 'calc. phys. vars.' in flags.option or 'calc' in flags.option:
    print_important("python mac/calc_phys_vars.py -A12 -werez --option=ppSRC --DataType=DATA -evf=1 -p1000 -v2")


# (2) scheme for pp-src
# ----------------------------------------
if 'scheme pp-SRC' in flags.option or 'scheme' in flags.option: # scheme to pp-SRC

    DataName    = "DATA_%s"% dm.Target(flags.atomic_mass)
    SchemedName = "ppSRCCut_%s"% DataName
    ana     = TAnalysisEG2( path+"/AnaFiles" , "Ana_SRCPmissXb_"+DataName , flags.cut )
    scheme  = TSchemeDATA()
    scheme.SchemeOnTCut( path+"/AnaFiles" , "Ana_SRCPmissXb_"+DataName+".root", "anaTree", "Ana_"+SchemedName+".root", ana.ppSRCCut + ana.PrecFiducial)
    print 'schemed to %s'%SchemedName


# (3) extract cm-parameters from data (no acc. correction)
# ----------------------------------------------------------
if 'extract data cm-parameters' in flags.option or 'extract' in flags.option: # DATA

    # (A) calc cm parameters of data
    ana_data = TAnalysisEG2( "ppSRCCut_DATA_%s"% dm.Target(A) )
    cm_parameters = calc_cm_parameters( ana_data  , PmissBins , CMRooFitsName( ppPath + '/DATA/unweighted' ) , CMRooFitsName( ppPath + '/DATA/weighted' ) , DoSaveCanvas = True )
    cm_parameters.to_csv( CMParsFname(ppPath+'/DATA/data') , header=True , index = False)
    print_filename( CMParsFname(ppPath+'/DATA/data')  ,"data c.m. parameters for different p(miss) bins at")
    print_line()

    # (B) plot cm parameters
    fits = fit_cm_parameters( 'data' , cm_parameters , FigureFName(ppPath+'/DATA/data') , DoPlot = True )
    fits.to_csv( CMfitsFname(ppPath+'/DATA/data') , header=True , index = False)
    print_filename( CMfitsFname(ppPath+'/DATA/data')  ,"data c.m. fits at")
    print_line()


# (4) create bands for Event-Generation
# ----------------------------------------------------------
if 'create bands for EG' in flags.option or 'bands' in flags.option:

    cm_parameters = pd.read_csv( CMParsFname(ppPath+'/DATA/data') )
    fits = pd.read_csv( CMfitsFname( ppPath+'/DATA/data' ) )
    generate_cm_bands( cm_parameters , fits , CMBandFname( ppPath+'/DATA/data' ) , FigureBandFName( ppPath+'/DATA/data' ) , DoSaveCanvas = True)


# (5) generate runs with different parameters
# ----------------------------------------------------------
# ToDo: Continue here! make
# (1) add to the CSV the mean and width in x,y,z in each Pmiss Bin!
# (2) convert the CSV to a ROOT file as well
# (3) re-run all the runs from scratch? if yes, with test_name changing .....
if 'generate and analyze runs' in flags.option or 'generate' in flags.option or 'analyze' in flags.option or 'analyse' in flags.option:
    
    cm_pars_bands = pd.read_csv( CMBandFname(ppPath+'/DATA/data') )
    cm_fits_parameters = pd.read_csv( CMfitsFname( ppPath+'/DATA/data' ) )
    
    test_name , start_run = 'debug_test' , 0
    N = pd.DataFrame({'SigmaT':1,'SigmaZa1':1 ,'SigmaZa2':1 ,'MeanZa1':1 ,'MeanZa2':1 , 'NRand':1}, index=[0])
    full_path = ppPath+'/simulation/'+test_name+'_simulation'
    generate_runs_with_different_parameters( flags.option ,
                                                  cm_fits_parameters , cm_pars_bands ,
                                                  start_run , flags.verbose , PmissBins ,
                                                  buildup_resutlsFName( full_path ) , CMfitsFname( full_path ) , dm.Target(A)  , N )





# (6) find the best-correspondance from the generated runs, to estimate nature's parameteres
# ----------------------------------------------------------
if 'find the best paramteres' in flags.option:

    print_filename(SimParametersFileName( ppPath+'/simulation/' ),'reading file ')
    simulation_results = pd.read_csv( SimParametersFileName( ppPath+'/simulation/' ) )
    plot( simulation_results , 'genSigmaL_a1' , 'NsigSL_a1_unweighted' , 'generated a$_1$ ($\sigma_z$) [GeV/c]' , 'unweighted N$\sigma$ (a$_1$ ($\sigma_z$))' )





