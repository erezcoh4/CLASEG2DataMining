from definitions import *
from cm_tools import *
'''
    usage:
    ---------
    python mac/cm_parameters_data_and_sim.py --option=scheme
    
    options (can be ran simultaneously):
    ------------------------------------
    acceptance  {"recoil proton acceptance"}
    calc        {"calc. phys. vars."}
    scheme      {"scheme pp-SRC"}
    extract     {"extract data cm-parameters"}
    bends       {"create bands for EG"}
    generate    {"generate and analyze runs"}
    
'''


splitjobs_runs = 2
start_run , Nruns = 100000 , 2
if flags.run!=0
    start_run = flags.run


PmissBins = [[0.3,0.45]  , [0.45,0.55] , [0.55,0.65] , [0.65,0.75] , [0.75,1.0]]
N = pd.DataFrame({'SigmaT':30,'SigmaZa1':15 ,'SigmaZa2':15 ,'MeanZa1':15 ,'MeanZa2':15 ,'StartRun':100000 , 'NRand':10 }, index=[0])
#N = pd.DataFrame({'SigmaT':1,'SigmaZa1':100,'SigmaZa2':2 ,'MeanZa1':2 ,'MeanZa2':2 ,'StartRun':1000 , 'NRand':10 }, index=[0])
#N = pd.DataFrame({'SigmaT':1,'SigmaZa1':1 ,'SigmaZa2':1 ,'MeanZa1':1 ,'MeanZa2':1 ,'StartRun':0 , 'NRand':1}, index=[0]) # for debugging



# proton acceptance plot
# ----------------------------------------
if 'recoil proton acceptance' in flags.option or 'acceptance' in flags.option:
    print_important("ipynb notebooks/recoil_proton_acceptance.ipynb")


# (1) calculate physical variables
# ----------------------------------------
if 'calc. phys. vars.' in flags.option or 'calc' in flags.option:
    print_important("python mac/calc_phys_vars.py -A12 -w%s --option=ppSRC --DataType=DATA -evf=1 -p10000"%flags.worker)


# (2) scheme for pp-src
# ----------------------------------------
if 'scheme pp-SRC' in flags.option or 'scheme' in flags.option: # scheme to pp-SRC

    DataName    = "DATA_%s"% dm.Target(flags.atomic_mass)
    ana     = TAnalysisEG2( path+"/AnaFiles" , "Ana_SRCPmissXb_"+DataName , flags.cut )
    scheme  = TSchemeDATA()
    SchemedName = "ppSRCCut_%s"% DataName
    scheme.SchemeOnTCut( path+"/AnaFiles" , "Ana_SRCPmissXb_"+DataName+".root", "anaTree", "Ana_"+SchemedName+".root", ROOT.TCut("ppSRCcutFiducial") )
    SchemedName = "eep_in_ppSRCCut_%s"% DataName
    scheme.SchemeOnTCut( path+"/AnaFiles" , "Ana_SRCPmissXb_"+DataName+".root", "anaTree", "Ana_"+SchemedName+".root", ROOT.TCut("eep_in_ppSRCcut") )
    print 'schemed to %s'%SchemedName


# (3) extract cm-parameters from data (no acc. correction)
# ----------------------------------------------------------
if 'extract data cm-parameters' in flags.option or 'extract' in flags.option: # DATA

    # (A) calc cm parameters of data
    ana_data = TAnalysisEG2( path+"/AnaFiles" , "Ana_ppSRCCut_DATA_%s"% dm.Target(A) )
    cm_parameters = calc_cm_parameters( ana_data  , PmissBins , CMRooFitsName( ppPath + '/DATA/unweighted' ) , CMRooFitsName( ppPath + '/DATA/weighted' ) , DoSaveCanvas = True )
    cm_parameters.to_csv( CMParsFname(ppPath+'/DATA/data') , header=True , index = False)
    print_filename( CMParsFname(ppPath+'/DATA/data')  ,"data c.m. parameters for different p(miss) bins at")
    print_line()

    # (B) plot cm parameters
    fits = fit_cm_parameters( 'data' , cm_parameters , FigureFName(ppPath+'/DATA/data') , DoPlot = True )
    fits.to_csv( CMfitsFname(ppPath+'/DATA/data') , header=True , index = False)
    print_filename( CMfitsFname(ppPath+'/DATA/data')  ,"data c.m. fits at")
    print_line()




# (3).1 plot all parameters together
# ----------------------------------------------------------
if 'plot all parameters for all targets' in flags.option or 'AllTragets' in flags.option: # DATA
    
    # (A) compute width and mean for all nuclei
    targets = ['C12'        , 'Al27'        , 'Fe56'        , 'Pb208'       ]
    colors  = ['black'      , 'red'         , 'green'       , 'blue'        ]
    labels  = ['$^{12}$C'   , '$^{27}$Al'   , '$^{56}$Fe'   , '$^{208}$Pb'  ]
    
    ana , cm_pars = [] , []
    if 'extraction' in flags.option:
        for target in targets:
            ana.append( TAnalysisEG2( "ppSRCCut_DATA_%s"%target ) )
            cm_parameters = calc_cm_parameters( ana[-1]  , PmissBins ,
                                               CMRooFitsName( ppPath + '/DATA/%s_unweighted'%target ) ,
                                               CMRooFitsName( ppPath + '/DATA/%s_weighted'%target ) ,
                                               DoSaveCanvas = True )
            cm_parameters.to_csv( CMParsFname(ppPath+'/DATA/%s_data'%target) , header=True , index = False)
            cm_pars.append( cm_parameters )
    else:
        for target in targets:
            cm_parameters = pd.read_csv( CMParsFname(ppPath+'/DATA/%s_data'%target) )
            print 'read ',ppPath+'/DATA/%s_data'%target
            cm_pars.append( cm_parameters )



    # (B) plot longitudinal width and mean for all nuclei
    widths_z = fit_widths_z( cm_pars , colors=colors , labels=labels ,
                            FigureFName = FigureFName(ppPath+'/DATA/widths_z_all_nuclei') )
    mean_z = fit_means_z( cm_pars , colors=colors , labels=labels ,
                         FigureFName = FigureFName(ppPath+'/DATA/means_z_all_nuclei') )
    print_line()





# (4) create bands for Event-Generation
# ----------------------------------------------------------
if 'create bands for EG' in flags.option or 'bands' in flags.option:

    cm_parameters = pd.read_csv( CMParsFname(ppPath+'/DATA/data') )
    fits = pd.read_csv( CMfitsFname( ppPath+'/DATA/data' ) )

    generate_cm_bands( cm_parameters , fits , N ,
                      flags.verbose ,
                      CMBandFname( ppPath+'/DATA/data' ) , FigureBandFName( ppPath+'/DATA/data' ) , GeneParsFName ( ppPath+'/simulation/' ) ,
                      DoSaveCanvas = True,
                      SigmaTBandRange = [0.1,0.22],
                      SigmaZa1BandRange = [-0.9,2.4],
                      SigmaZa2BandRange = [-0.3,0.2],
                      MeanZa2BandRange  = [-0.3,1.2],
                      MeanZa2BandRange = [-0.5,0.2],
                      )




# (5) generate runs with different parameters
# ----------------------------------------------------------
if 'generate and analyze runs' in flags.option or 'generate' in flags.option or 'analyze' in flags.option or 'analyse' in flags.option:


    fits = pd.read_csv( CMfitsFname( ppPath+'/DATA/data' ) )
    generated_parameters = pd.read_csv( GeneParsFName ( ppPath+'/simulation/' ) )
    generated_parameters = generated_parameters[(start_run <= generated_parameters.run) & (generated_parameters.run <= start_run + Nruns)]
    print 'running on: ',generated_parameters.run.tolist()

    test_name = 'runs%dto%d_NsigmaT_%d_NSigmaZa1_%d_NSigmaZa2_%d_NMeanZa1_%d_NMeanZa2_%d_NRand_%d'%( start_run , start_run+Nruns , N.SigmaT , N.SigmaZa1 , N.SigmaZa2 , N.MeanZa1 , N.MeanZa2 , N.NRand )
    full_path = ppPath+'/simulation/'+test_name+'_simulation'
    generate_runs_with_different_parameters( flags.option ,
                                            fits,
                                            generated_parameters ,
                                            flags.verbose , PmissBins ,
                                            buildup_resutlsFName( full_path ) ,
                                            CMfitsFname( full_path ) ,
                                            dm.Target(A) ,
                                            N ,
                                            root_resutlsFName( full_path ) )





# (6) find the best-correspondance from the generated runs, to estimate nature's parameteres
# ----------------------------------------------------------
if 'find the best paramteres' in flags.option:

    print_filename(SimParametersFileName( ppPath+'/simulation/' ),'reading file ')
    simulation_results = pd.read_csv( SimParametersFileName( ppPath+'/simulation/' ) )
    plot( simulation_results , 'genSigmaL_a1' , 'NsigSL_a1_unweighted' , 'generated a$_1$ ($\sigma_z$) [GeV/c]' , 'unweighted N$\sigma$ (a$_1$ ($\sigma_z$))' )





