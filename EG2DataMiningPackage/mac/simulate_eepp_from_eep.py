from definitions import *
from cm_tools import *
'''
    usage:
    ---------------
    python mac/simulate_eepp_from_eep.py --option=extractCMparsAllNuclei
    python mac/simulate_eepp_from_eep.py --option=generate_analyse -nruns=10
'''
    



# extract cm-parameters from data for all targets (no acc. correction)
# ----------------------------------------------------------
if 'extractCMparsAllNuclei' in flags.option: #{
    
    cm_pars , cm_fits = [] , []
    ana = dict()
    for target in targets:
        ana[target] = TAnalysisEG2( path+"/AnaFiles" ,  "Ana_ppSRCCut_DATA_%s"%target )
        cm_parameters , _ = calc_cm_parameters(ana[target] , PmissBins ,
                                               CMRooFitsName( ppPath + '/DATA/%s_unweighted'%target ) ,
                                               CMRooFitsName( ppPath + '/DATA/%s_weighted'%target ) ,
                                               DoSaveCanvas = True )

        cm_parameters.to_csv( CMParsFname(ppPath+'/DATA/%s_data'%target) , header=True , index=False)
        cm_pars.append( cm_parameters )
        fits = fit_cm_parameters( run=target+' data', data=cm_parameters, FigureFName=FigureFName(ppPath+'/DATA/data', target) , DoPlot=True )
        fits.to_csv( CMfitsFname( ppPath+'/DATA/data' , target ) , header=True , index=False)
        print_filename( CMfitsFname(ppPath+'/DATA/data' , target )  , target + " data c.m. fits at")
        cm_fits.append( fits )

    # plot longitudinal width and mean for all nuclei
    widths_z = fit_widths_z( cm_pars , colors=target_colors , labels=labels , FigureFName = FigureFName(ppPath+'/DATA/widths_z_all_nuclei') )
    mean_z = fit_means_z( cm_pars , colors=target_colors , labels=labels  , FigureFName = FigureFName(ppPath+'/DATA/means_z_all_nuclei') )
    print 'done extractCMparsAllNuclei'; print_line()
    #}





# generate and analyse runs
# ----------------------------------------------------------
if 'generate' in flags.option or 'analyse' in flags.option:#{
    
    cm_pars , cm_fits = dict() , dict()
    ana_data = dict()

    for target in targets:
        cm_pars[target] = pd.read_csv( CMParsFname(ppPath+'/DATA/%s_data'%target) )
        cm_fits[target] = pd.read_csv( CMfitsFname(ppPath+'/DATA/data',target ) )
        ana_data[target] = TAnalysisEG2( path+"/AnaFiles" ,  "Ana_ppSRCCut_DATA_%s"%target )
    
    hyperparameters = dict({'start_run':flags.run,
                           'Nruns':flags.NumberOfRuns,
                           'range_sigma_t':(0.1  , 0.3),    # 0.160
                           'range_a1':(-0.4 , 1.0),         # 0.143
                           'range_a2':(0.0  , 0.5),         # 0.158
                           'range_b1':(-0.2 , 1.4),         # 0.569
                           'range_b2':(-0.1 , 0.6),         # 0.159
                           'NRand':20}
                           )

    test_name = 'runs_%d_%d'%( hyperparameters['start_run'] , hyperparameters['start_run'] + hyperparameters['Nruns'] )
    full_path = ppPath+'/simulation/'+test_name+'_simulation'

    generate_runs_with_random_parameters( option=flags.option, hyperparameters=hyperparameters,
                                         ana_data=ana_data,
                                         cm_pars=cm_pars, cm_fits=cm_fits,
                                         debug=flags.verbose , PmissBins=PmissBins , Q2Bins=Q2Bins , thetapmqBins=thetapmqBins ,
                                         buildup_resutlsFName=buildup_resutlsFName( full_path ),
                                         reco_fitsFName=CMfitsFname( full_path ),
                                         root_resutlsFName=root_resutlsFName( full_path ),
                                         do_root_file=False, do_reco_fits_file=False, do_resutls_file=True, do_add_plots=False
                                         )
    

    print 'done '+flags.option; print_line()

    #}

print_important( 'done simulate_eepp_from_eep.py' )
print
