from definitions import *
from cm_tools import *
'''
    usage:
    ---------------
    python mac/simulate_eepp_from_eep.py --option=extract_all --DataType=PrecFiducials
    python mac/simulate_eepp_from_eep.py --option=extract_all --DataType=PrecFiducials -whelion
    python mac/simulate_eepp_from_eep.py --option=extractCMparsAllNuclei --DataType=NoFiducials
    python mac/simulate_eepp_from_eep.py --option=extractOnly_C12 --DataType=PrecFiducials
    python mac/simulate_eepp_from_eep.py --option=extractOnly_C12 --DataType=NoFiducials -v2
    python mac/simulate_eepp_from_eep.py --option=generate_analyse_delete -nruns=10
'''
    



# extract cm-parameters from data for all targets (no acc. correction)
# ----------------------------------------------------------
if 'extract' in flags.option: #{
    
    cm_pars = []
    cm_fits = pd.DataFrame()
    
    ana = dict()
    if 'Only' in flags.option or 'only' in flags.option: targets = [flags.option[12:]]
    
    for target,label,A in zip(targets,labels,[12,27,56,208]):#{
        if flags.DataType=='NoFiducials': #{
            ana[target] = TAnalysisEG2( path + "/OrAnalysisTrees/AdjustedTrees" , "SRC_e2p_adjusted_%s_noFiducials"%target )
        #}
        else: #{
            ana[target] = TAnalysisEG2( path + "/OrAnalysisTrees/AdjustedTrees" , "SRC_e2p_adjusted_%s"%target )
        #}
        cm_parameters , _ = calc_cm_parameters(ana[target] , PmissBinsPerTarget[target] ,
                                               CMRooFitsName( ppPath + '/DATA/%s_unweighted'%target ) ,
                                               CMRooFitsName( ppPath + '/DATA/%s_weighted'%target ) ,
                                               DoSaveCanvas = True )

        cm_parameters.to_csv( CMParsFname(ppPath+'/DATA/%s_data'%target) , header=True , index=False )
        cm_pars.append( cm_parameters )
        fits = fit_cm_parameters( run=target+' data', data=cm_parameters, FigureFName=FigureFName(ppPath+'/DATA/data', target) , DoPlot=True )
        fits.to_csv( CMfitsFname( ppPath+'/DATA/data' , target ) , header=True , index=False )
        print_filename( CMfitsFname(ppPath+'/DATA/data' , target )  , target + " data c.m. fits at" )
        
        
        fits['target'] = label
        fits['A'] = A
        cm_fits = cm_fits.append( fits )

    #}
    cm_fits.to_csv( ppPath+'/DATA/alltargets_dataCMfits.csv' , header=True , index=False )
    print_filename( ppPath+'/DATA/alltargets_dataCMfits.csv' , "c.m. fits" )
    print 'done extractCMparsAllNuclei'; print_line()
#}





# generate and analyse runs
# ----------------------------------------------------------
if 'generate' in flags.option or 'analyse' in flags.option:#{
    
    hyperparameters = dict({'start_run':flags.run,
                           'Nruns':flags.NumberOfRuns,
                           'range_sigma_t':(0.1  , 0.3),    # 0.160
                           'range_a1':(-0.4 , 1.0),         # 0.143
                           'range_a2':(0.0  , 0.5),         # 0.158
                           'range_b1':(-0.2 , 1.4),         # 0.569
                           'range_b2':(-0.1 , 0.6),         # 0.159
                           'NRand':20,
                           'Ntimes':10,                     # wanted number of events in each Pmiss bin
                           'NgenMax':100000,                # maximal number of attempts
                           'do_ks_plots':False,
                           'do proton acceptance':True,
                           'do p(rec)>0.35 cut':True,
                           'do p(rec) FV cuts':True,
                           'do p(rec) resolution smearing':True,
                           'p(rec) resolution smearing':0.020, # [GeV/c] momentum resolution
                           'binom_p':0.33 # average approximate acceptance
                           })
    
    cm_pars , cm_fits , ana_data = dict() , dict() , dict()
    for target in targets:#{
        ana_data[target] = TAnalysisEG2( path + "/OrAnalysisTrees/AdjustedTrees" , "SRC_e2p_adjusted_%s"%target )
    #}
    

    test_name = 'runs_%d_%d'%( hyperparameters['start_run'] , hyperparameters['start_run'] + hyperparameters['Nruns'] )
    full_path = ppPath+'/simulation/'+test_name+'_simulation'

    generate_runs_with_random_parameters( option=flags.option, hyperparameters=hyperparameters,
                                         ana_data=ana_data,
                                         debug=flags.verbose , Q2Bins=Q2Bins , thetapmqBins=thetapmqBins ,
                                         buildup_resultsFName=buildup_resultsFName( full_path ),
                                         reco_fitsFName=CMfitsFname( full_path ),
                                         root_resutlsFName=root_resutlsFName( full_path ),
                                         do_root_file=False, do_reco_fits_file=False, do_resutls_file=True, do_add_plots=False
                                         )
    

    print 'done '+flags.option; print_line()
    #}



print_important( 'done simulate_eepp_from_eep.py' )
print
