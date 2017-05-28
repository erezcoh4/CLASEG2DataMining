from definitions import *
from cm_tools import *
'''
    usage:
    ---------------
    python mac/simulate_eepp_from_eep_sigma_t.py --option=extract_all_targets --DataType=NoFiducials -v2
    python mac/simulate_eepp_from_eep_sigma_t.py --option=generate_analyze_delete -nruns=10 -v1
    python mac/simulate_eepp_from_eep_sigma_t.py --option=extractOnly_C12 --DataType=NoFiducials -v2
'''
    



# extract cm-parameters from data for all targets (no acc. correction)
# ----------------------------------------------------------
if 'extract' in flags.option: #{
    
    cm_pars = pd.DataFrame()
    ana = dict()
    if 'Only' in flags.option or 'only' in flags.option: targets = [flags.option[12:]]
    
    for target,label,A in zip(targets,labels,[12,27,56,208]):#{
        if flags.DataType=='NoFiducials': #{
            ana[target] = TAnalysisEG2( path + "/OrAnalysisTrees/AdjustedTrees" , "SRC_e2p_adjusted_300Pmiss600_%s_noFiducials"%target )
        #}
        else: #{
            ana[target] = TAnalysisEG2( path + "/OrAnalysisTrees/AdjustedTrees" , "SRC_e2p_adjusted_300Pmiss600_%s"%target )
        #}
        cm_parameters = calc_cm_pars_sigma(ana[target],
                                           CMRooFitsName( ppPath + '/300Pmiss600/%s_unweighted'%target ) ,
                                           CMRooFitsName( ppPath + '/300Pmiss600/%s_weighted'%target ) ,
                                           DoSaveCanvas = True )
        cm_parameters['target'] = label
        cm_parameters['A'] = A
        cm_pars = cm_pars.append( cm_parameters )
    #}
    cm_pars.to_csv( CMParsFname(ppPath+'/300Pmiss600/alltargets_data') , header=True , index=False )
    print_filename( CMParsFname(ppPath+'/300Pmiss600/alltargets_data') , "c.m. parameters for %s "%target )
    print 'done extractCMparsAllNuclei'; print_line()
#}




# generate runs with different \sigma (for acceptance correction)
# ----------------------------------------------------------
if 'generate' in flags.option: #{
    
    hyperparameters = dict({'start_run':flags.run,
                           'Nruns':flags.NumberOfRuns,
                           'range_sigma_t':(0.144,0.146),       # around 0.160 (0,0.3)
                           'NRand':20,
                           'Ntimes':50,                     # wanted number of events, multiplied by the number of data events in 12C
                           'NgenMax':100000,                # maximal number of attempts
                           'do proton acceptance':True,
                           'do p(rec)>0.35 cut':True,
                           'do p(rec) FV cuts':False,
                           'do p(rec) resolution smearing':True,
                           'p(rec) resolution smearing':0.020 # [GeV/c] momentum resolution
                           })
        
    ana_data = dict()
    for target in targets:#{
        ana_data[target] = TAnalysisEG2( path + "/OrAnalysisTrees/AdjustedTrees" , "SRC_e2p_adjusted_300Pmiss600_%s_noFiducials"%target )
    #}


    test_name = 'results_300Pmiss600_simulation_%d_%d'%( hyperparameters['start_run'] , hyperparameters['start_run'] + hyperparameters['Nruns'] )
    full_path = ppPath+'/simulation_300Pmiss600/'+test_name+'_simulation'
    
    generate_runs_with_random_sigma( option=flags.option,
                                    hyperparameters=hyperparameters,
                                    ana_data=ana_data,
                                    debug=flags.verbose,
                                    buildup_resultsFName=buildup_resultsFName( full_path ),
                                    do_results_file=True
                                    )
    print 'done '+flags.option; print_line()
#}

print_important( 'done simulate_eepp_from_eep_sigma_t.py' )
print
