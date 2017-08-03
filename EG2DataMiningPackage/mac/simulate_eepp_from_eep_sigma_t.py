from definitions import *
from cm_tools import *
'''
    usage:
    ---------------
    python mac/simulate_eepp_from_eep_sigma_t.py --option=generate_analyze_delete -nruns=100 -v1
    python mac/simulate_eepp_from_eep_sigma_t.py --option=extract_all_targets --DataType=NoFiducials_300Pmiss600 -v2
    python mac/simulate_eepp_from_eep_sigma_t.py --option=extract_all_targets --DataType=NoFiducials_allPmiss -v2
    python mac/simulate_eepp_from_eep_sigma_t.py --option=extract_all_targets --DataType=allPmiss -v2
    python mac/simulate_eepp_from_eep_sigma_t.py --option=extract_all_targets --DataType=300Pmiss600 -v2
    python mac/simulate_eepp_from_eep_sigma_t.py --option=extractOnly_C12 --DataType=NoFiducials_allPmiss -v6
    python mac/simulate_eepp_from_eep_sigma_t.py --option=generate_analyze -nruns=1 -v1
'''
    



# extract cm-parameters from data for all targets (no acc. correction)
# ----------------------------------------------------------
if 'extract' in flags.option: #{
    
    cm_pars = pd.DataFrame()
    ana = dict()
    if 'Only' in flags.option or 'only' in flags.option: targets = [flags.option[12:]]
    
    for target,label,A in zip(targets,labels,[12,27,56,208]):#{
        if 'NoFiducials' in flags.DataType and '300Pmiss600' in flags.DataType: #{
            directory_name = '300Pmiss600'
            pMiss_max = 0.6
            ana[target] = TAnalysisEG2( path + "/OrAnalysisTrees/AdjustedTrees" , "SRC_e2p_adjusted_300Pmiss600_%s_noFiducials"%target )
        #}
        elif 'NoFiducials' not in flags.DataType and '300Pmiss600' in flags.DataType: #{
            directory_name = '300Pmiss600'
            pMiss_max = 0.6
            ana[target] = TAnalysisEG2( path + "/OrAnalysisTrees/AdjustedTrees" , "SRC_e2p_adjusted_300Pmiss600_%s"%target )
        #}
        elif 'NoFiducials' in flags.DataType and 'allPmiss' in flags.DataType:#{
            directory_name = 'OrDataTrees'
            pMiss_max = 1.0
            ana[target] = TAnalysisEG2( path + "/OrAnalysisTrees/AdjustedTrees" , "SRC_e2p_adjusted_%s_noFiducials"%target )
        #}
        elif 'NoFiducials' not in flags.DataType and 'allPmiss' in flags.DataType: #{
            directory_name = 'OrDataTrees'
            pMiss_max = 1.0
            ana[target] = TAnalysisEG2( path + "/OrAnalysisTrees/AdjustedTrees" , "SRC_e2p_adjusted_%s"%target )
        #}
        cm_parameters = calc_cm_pars_sigma(ana[target],
                                           CMRooFitsName( ppPath + '/'+directory_name+'/%s_unweighted'%target ) ,
                                           CMRooFitsName( ppPath + '/'+directory_name+'/%s_weighted'%target ) ,
                                           DoSaveCanvas = True ,
                                           pMiss_max = pMiss_max )
        cm_parameters['target'] = label
        cm_parameters['A'] = A
        cm_pars = cm_pars.append( cm_parameters )
    #}
    cm_pars.to_csv( CMParsFname(ppPath+'/'+directory_name+'/alltargets_data') , header=True , index=False )
    print_filename( CMParsFname(ppPath+'/'+directory_name+'/alltargets_data') , "c.m. parameters" )
    print 'done extractCMparsAllNuclei'; print_line()
#}




# generate runs with different \sigma (for acceptance correction)
# ----------------------------------------------------------
if 'generate' in flags.option: #{
    
    
    
    hyperparameters = dict({'start_run':flags.run,
                           'Nruns':flags.NumberOfRuns,
                           'range_sigma_t':(0.0,0.3),       # around 0.160 (0,0.3)
                           'NRand':20,
                           'Ntimes':50,                     # wanted number of events, multiplied by the number of data events in 12C
                           'NgenMax':100000,                # maximal number of attempts
                           'do proton acceptance':True,
                           'do p(rec)>0.35 cut':True,
                           'do p(rec) FV cuts':True,
                           'do p(rec) resolution smearing':True,
                           'p(rec) resolution smearing':0.020, # [GeV/c] momentum resolution
                           'generated mean(x)':0.0,
                           'generated mean(y)':0.0,
                           # take the longitudinal parameters as variable input to the simulation,
                           # distributed as a Gaussian around their measured value
                           # with a width that is N(uncertainties) times the uncertainty in the measured value
                           'N(uncertainties) in generation': 5,
                           })
        
    ana_data = dict()
    for target in targets:#{
        ana_data[target] = TAnalysisEG2( path + "/OrAnalysisTrees/AdjustedTrees" , "SRC_e2p_adjusted_300Pmiss600_%s_noFiducials"%target )
    #}

    for target_name,mean_z,mean_z_err,sigma_z,sigma_z_err in zip(['C','Al','Fe','Pb']
                                                                 # measured \mu(miss)
                                                                 ,[0.100,0.119,0.147,0.166]
                                                                 ,[0.008,0.015,0.010,0.023]
                                                                 # measured \sigma(miss)
                                                                 ,[0.146,0.143,0.153,0.167]
                                                                 ,[0.006,0.010,0.007,0.017]
                                                                 ):#{
        hyperparameters['target name'] = target_name
        hyperparameters['measured mean(z)'] = mean_z
        hyperparameters['measured mean(z) err'] = mean_z_err
        hyperparameters['measured sigma(z)'] = sigma_z
        hyperparameters['measured sigma(z) err'] = sigma_z_err
        
        print_important( "grabbing "+target_name+"(e,e'p) and simulating" )
            
        test_name = 'simulation_300Pmiss600_%s_runs_%d_%d'%( hyperparameters['target name']
                                                            , hyperparameters['start_run']
                                                            , hyperparameters['start_run'] + hyperparameters['Nruns']
                                                            )
        full_path = ppPath+'/simulation_300Pmiss600/'+test_name
    
        generate_runs_with_random_sigma( option=flags.option,
                                        hyperparameters=hyperparameters,
                                        ana_data=ana_data,
                                        debug=flags.verbose,
                                        buildup_resultsFName=buildup_resultsFName( full_path ),
                                        do_results_file=True
                                        )
        print_important( "done "+target_name+"(e,e'p) simulations ")
        print_xline()
    #}
    print 'done '+flags.option; print_line()
#}

print_important( 'done simulate_eepp_from_eep_sigma_t.py' )
print



# older version: generate 9 times for acceptance correction,
# in each time - for different (fixed) longitudinal input

## generate runs with different \sigma (for acceptance correction)
## ----------------------------------------------------------
#if 'generate' in flags.option: #{
#    
#    
#    
#    hyperparameters = dict({'start_run':flags.run,
#                           'Nruns':flags.NumberOfRuns,
#                           'range_sigma_t':(0.0,0.3),       # around 0.160 (0,0.3)
#                           'NRand':20,
#                           'Ntimes':50,                     # wanted number of events, multiplied by the number of data events in 12C
#                           'NgenMax':100000,                # maximal number of attempts
#                           'do proton acceptance':True,
#                           'do p(rec)>0.35 cut':True,
#                           'do p(rec) FV cuts':False,
#                           'do p(rec) resolution smearing':True,
#                           'p(rec) resolution smearing':0.020, # [GeV/c] momentum resolution
#                           'generated mean(x)':0.0,
#                           'generated mean(y)':0.0,
#                           
#                           # variables
#                           'target name':'',
#                           'generated mean(z)':0, # C: 0.100(8), Al: 0.119(15), Fe: 0.147(10), Pb: 0.166(23)
#                           'generated sigma(z)':0, # C: 0.146(6), Al: 0.143(10), Fe:  0.153(7), Pb: 0.167(17)
#                           })
#        
#                           ana_data = dict()
#                           for target in targets:#{
#                               ana_data[target] = TAnalysisEG2( path + "/OrAnalysisTrees/AdjustedTrees" , "SRC_e2p_adjusted_300Pmiss600_%s_noFiducials"%target )
#                           #}
#
#for target_name,mean_z,mean_z_err,sigma_z,sigma_z_err in zip(['C','Al','Fe','Pb']
#                                                             # measured \mu(miss)
#                                                             ,[0.100,0.119,0.147,0.166]
#                                                             ,[0.008,0.015,0.010,0.023]
#                                                             # measured \sigma(miss)
#                                                             ,[0.146,0.143,0.153,0.167]
#                                                             ,[0.006,0.010,0.007,0.017]
#                                                             ):#{
#    hyperparameters['target name'] = target_name
#        
#        for gen_mean_z in [ mean_z-mean_z_err , mean_z , mean_z+mean_z_err ]:#{
#            
#            hyperparameters['generated mean(z)'] = gen_mean_z
#            
#            for gen_sigma_z in [ sigma_z-sigma_z_err , sigma_z , sigma_z+sigma_z_err ]:#{
#                
#                hyperparameters['generated sigma(z)'] = gen_sigma_z
#                print_important( "grabbing "+target_name+"(e,e'p) and simulating with mean(z)=%.3f"%gen_mean_z+" and sigma(z)=%.3f"%    gen_sigma_z )
#                
#                test_name = 'simulation_300Pmiss600_%s_genMeanZ_%.3f_genSigmaZ_%.3f_%d_%d'%( hyperparameters['target name']
#                                                                                            , hyperparameters['generated mean(z)']
#                                                                                            , hyperparameters['generated sigma(z)']
#                                                                                            , hyperparameters['start_run']
#                                                                                            , hyperparameters['start_run']
#                                                                                            + hyperparameters['Nruns']
#                                                                                            )
#                                                                                            full_path = ppPath+'/simulation_300Pmiss600/'+test_name
#                                                                                            
#                                                                                            generate_runs_with_random_sigma( option=flags.option,
#                                                                                                                            hyperparameters=hyperparameters,
#                                                                                                                            ana_data=ana_data,
#                                                                                                                            debug=flags.verbose,
#                                                                                                                            buildup_resultsFName=buildup_resultsFName( full_path ),
#                                                                                                                            do_results_file=True
#                                                                                                                            )
#                                                                                            print_important( "done "+target_name+"(e,e'p) simulating with mean(z)=%.3f"%gen_mean_z+" and sigma(z)=%.3f"%gen_sigma_z )
#                                                                                            print_xline()
#    #}
##}
##}
#print 'done '+flags.option; print_line()
##}