from definitions import *
from cm_tools import *
'''
    usage:
    ---------------
    python mac/simulate_eepp_from_eep_sigma_t.py --option=generate_analyze -nruns=1 -v1
    python mac/simulate_eepp_from_eep_sigma_t.py --option=extract_all_targets --DataType=PrecFiducials_300Pmiss600 -v2
    python mac/simulate_eepp_from_eep_sigma_t.py --option=extractOnly_C12 --DataType=PrecFiducials_300Pmiss600 -v2
    python mac/simulate_eepp_from_eep_sigma_t.py --option=extract_all_targets --DataType=NoPrecFiducials_300Pmiss600 -v2
    python mac/simulate_eepp_from_eep_sigma_t.py --option=extract_all_targets --DataType=NoFiducials_allPmiss -v2
    python mac/simulate_eepp_from_eep_sigma_t.py --option=extract_all_targets --DataType=allPmiss -v2
    python mac/simulate_eepp_from_eep_sigma_t.py --option=extract_all_targets --DataType=300Pmiss600 -v2
    python mac/simulate_eepp_from_eep_sigma_t.py --option=generate_analyze -nruns=1 -v1
'''
    



# extract cm-parameters from data for all targets (no acc. correction)
# ----------------------------------------------------------
if 'extract' in flags.option: #{
    
    cm_pars = pd.DataFrame()
    ana = dict()
    if 'Only' in flags.option or 'only' in flags.option: targets = [flags.option[12:]]
    
    for target,label,A in zip(targets,labels,[12,27,56,208]):#{
        if 'NoPrecFiducials' in flags.DataType and '300Pmiss600' in flags.DataType: #{
            Fiducials = 'NoPrecFiducials'
            directory_name = '300Pmiss600'
            print 'running ',Fiducials,'at',directory_name
            pMiss_max = 0.6
            ana[target] = TAnalysisEG2( path + "/OrAnalysisTrees/AdjustedTrees" , "SRC_e2p_adjusted_300Pmiss600_%s_NoPrecFiducials"%target )
        #}
        elif '300Pmiss600' in flags.DataType: #{
            Fiducials = 'PrecFiducials'
            directory_name = '300Pmiss600'
            print 'running ',Fiducials,'at',directory_name
            pMiss_max = 0.6
            ana[target] = TAnalysisEG2( path + "/OrAnalysisTrees/AdjustedTrees" , "SRC_e2p_adjusted_300Pmiss600_%s_PrecFiducials"%target )
        #}
        elif 'NoPrecFiducials' in flags.DataType and 'allPmiss' in flags.DataType:#{
            Fiducials = 'NoPrecFiducials'
            directory_name = 'OrDataTrees'
            print 'running ',Fiducials,'at',directory_name
            pMiss_max = 1.0
            ana[target] = TAnalysisEG2( path + "/OrAnalysisTrees/AdjustedTrees" , "SRC_e2p_adjusted_%s_NoPrecFiducials"%target )
        #}
        elif 'allPmiss' in flags.DataType: #{
            Fiducials = 'PrecFiducials'
            directory_name = 'OrDataTrees'
            print 'running ',Fiducials,'at',directory_name
            pMiss_max = 1.0
            ana[target] = TAnalysisEG2( path + "/OrAnalysisTrees/AdjustedTrees" , "SRC_e2p_adjusted_%s_PrecFiducials"%target )
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
    cm_pars.to_csv( CMParsFname(ppPath+'/'+directory_name+'/alltargets_'+Fiducials+'_data') , header=True , index=False )
    print_filename( CMParsFname(ppPath+'/'+directory_name+'/alltargets_'+Fiducials+'_data') , "c.m. parameters" )
    print 'done extractCMparsAllNuclei'; print_line()
#}




# generate runs with different \sigma (for acceptance correction)
# ----------------------------------------------------------
if 'generate' in flags.option: #{

    ana_data = dict()
    for target in targets:#{
        ana_data[target] = TAnalysisEG2( path + "/OrAnalysisTrees/AdjustedTrees" , "SRC_e2p_adjusted_300Pmiss600_%s_PrecFiducials"%target )
    #}

    
    hyperparameters = dict({'start_run':flags.run,
                           'Nruns':flags.NumberOfRuns,
                           'range_sigma_t':(0.0,0.3),       # around 0.160 (0,0.3)
                           'NRand':20,
                           'Ntimes':50,                     # wanted number of events, multiplied by the number of data events in 12C
                           'N(accepted-events)':15000,
                           'NgenMax':200000,                # maximal number of attempts
                           'do random entry':False,
                           'do proton acceptance':True,
                           'do p(rec)>0.35 cut':True,
                           'do p(rec) FV cuts':True,
                           'do p(rec) resolution smearing':False, # we will lateer subtract 20+/-2 MeV/c from the results.
                           'p(rec) resolution smearing':0.020, # [GeV/c] momentum resolution
                           'generated mean(x)':0.0,
                           'generated mean(y)':0.0,
                           'do print results':True,
                           # -- - - -- -- --- -- - -- - -- - - --- - -- - -
                           'generation method': 'N(uncertainties) band around measured values' ,
                           #'max mean(z), N(uncertainties) band around measured sigma(z)' ,
                           #'const mean(z), N(uncertainties) band around measured sigma(z)' ,
                           #'N(uncertainties) band around measured values' ,
                           #'unifrom N(uncertainties) band around measured' ,
                           #'mean(z) linear in Pmiss',
                           #'constant band' ,
                           # -- - - -- -- --- -- - -- - -- - - --- - -- - -
                           # take the longitudinal parameters as variable input to the simulation,
                           # distributed as a Gaussian around their measured value
                           # with a width that is N(uncertainties) times the uncertainty in the measured value
                           'p(miss) fit-type': 'vanish at 0.3', # fit: p(cm)-z = slope * ( p(miss) - 0.3 )
                           'maximal slope': 1.010,
                           'minimal slope': 0.282,
                           'N(uncertainties) in generation': 5,
                           })
                           
    if hyperparameters['do p(rec) FV cuts']==True:#{
        measured_mean_z     = [0.106,0.118,0.149,0.177]
        measured_mean_z_err = [0.009,0.015,0.010,0.025]
        measured_sigma_z    = [0.147,0.141,0.151,0.169]
        measured_sigma_z_err= [0.006,0.010,0.007,0.018]
        eep_events          = [7598 ,2573 ,8558 ,2635 ]
        eepp_events         = [266  ,88   ,227  ,45   ]
    #}
    elif hyperparameters['do p(rec) FV cuts']==False:#{
        measured_mean_z     = [0.100,0.119,0.147,0.166]
        measured_mean_z_err = [0.008,0.015,0.010,0.023]
        measured_sigma_z    = [0.146,0.143,0.153,0.167]
        measured_sigma_z_err= [0.006,0.010,0.007,0.018]
    #}
    
    for target_name,my_taregt_name,mean_z,mean_z_err,sigma_z,sigma_z_err,NRand,Neep,Neepp in zip(['C','Al','Fe','Pb']
                                                                                                 ,['C12','Al27','Fe56','Pb208']
                                                                                                 ,measured_mean_z,measured_mean_z_err,measured_sigma_z,measured_sigma_z_err
                                                                                                 ,[20,70,20,70]
                                                                                                 ,eep_events,eepp_events):#{
#    for target_name,my_taregt_name,mean_z,mean_z_err,sigma_z,sigma_z_err,NRand in zip(['Pb'] ,['Pb208'],[0.177],[0.025],[0.169],[0.018],[70]):#{


        hyperparameters['NRand'] = NRand
        hyperparameters['target name'] = target_name
        hyperparameters['my target name'] = my_taregt_name
        
        # for method: 'N(uncertainties) band around measured values'
        hyperparameters['measured mean(z)'] = mean_z
        hyperparameters['measured mean(z) err'] = mean_z_err
        hyperparameters['measured sigma(z)'] = sigma_z
        hyperparameters['measured sigma(z) err'] = sigma_z_err

        hyperparameters['Neep'] = Neep
        hyperparameters['Neepp'] = Neepp


        # for fixed mean and sigme to all nuclei
        if 'const mean(z)' in hyperparameters['generation method']: #{
            hyperparameters['const mean(z)'] = 0.3
        #}
        if 'max mean(z)' in hyperparameters['generation method']: #{
            hyperparameters['max mean(z)'] = 0.3
        #}
        # for fixed mean and sigme to all nuclei
        if hyperparameters['generation method'] ==  'constant band': #{
            hyperparameters['measured mean(z) err band'] = 0.075 # fixed 75 MeV/c for all nuclei
            hyperparameters['measured sigma(z) err band'] = 0.050 # fixed 50 MeV/c for all nuclei
        #}

        print_important( "grabbing "+target_name+"(e,e'p) and simulating" )
            
        test_name = 'simulation_300Pmiss600_%s_runs_%d_%d'%( hyperparameters['target name']
                                                            , hyperparameters['start_run']
                                                            , hyperparameters['start_run'] + hyperparameters['Nruns']
                                                            )
        full_path = ppPath+'/simulation_300Pmiss600/'+test_name
    
        generate_runs_with_random_sigma( option=flags.option,
                                        hyperparameters=hyperparameters,
                                        debug=flags.verbose,
                                        buildup_resultsFName=buildup_resultsFName( full_path ),
                                        do_results_file=True,
                                        ana_data_target=ana_data[target]
                                        )
        print_important( "done "+target_name+"(e,e'p) simulations ")
        print_xline()
    #}
    print 'done '+flags.option; print_line()
#}

print_important( 'done simulate_eepp_from_eep_sigma_t.py' )
print




