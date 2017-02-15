from definitions import *
from cm_tools import *
'''
    example usages:
    ---------------
    
    python mac/cm_parameters_data_and_sim.py --option=scheme
    python mac/cm_parameters_data_and_sim.py --option=bands
    python mac/cm_parameters_data_and_sim.py --option=AllTargets
    python mac/cm_parameters_data_and_sim.py --option=generate_analyze -v2 -r1 -nruns=1
    
    
    options (can be ran simultaneously):
    ------------------------------------
    acceptance          {"recoil proton acceptance"}
    calc                {"calc. phys. vars."}
    scheme              {"scheme pp-SRC"}
    extract             {"extract data cm-parameters"}
    extractionAllTragets{"plot all parameters for all targets"}
    bends               {"create bands for EG"}
    generate            {"generate runs"}
    analyze             {"analyze runs"}
    generate_analyze    {"generate and analyze runs"}
    genmodcut_anamodcut {"enerate and analyze runs with different cuts"}
'''

targets = ['C12', 'Al27' , 'Fe56' , 'Pb208' ]
labels  = ['$^{12}$C'   , '$^{27}$Al'   , '$^{56}$Fe'   , '$^{208}$Pb'  ]


if flags.run > 0:
    start_run = flags.run
else:
    start_run = 1

if flags.NumberOfRuns > 0:
    Nruns = flags.NumberOfRuns
else:
    Nruns = 1

PmissBins   = [[0.3,0.45]  , [0.45,0.55] , [0.55,0.65]  , [0.65,0.75] , [0.75,1.0]]
Q2Bins      = [[0,1.5]     , [1.5,2]     , [2,2.5]      , [2.5,6]]
thetapmqBins= [[100,135]   , [135,145]   , [145,155]    , [155,180]]

# Jan 2017, chaning to fit pcmZ = a1*( p(miss) - 0.6 ) + a2
# 12C nominal values
nom_vals = pd.DataFrame({'SigmaT':0.167 ,'SigmaT_err':0.006,
                'SigmaZa1':0.143,'SigmaZa1_err':0.075   ,'SigmaZa2':0.158   ,'SigmaZa2_err':0.009,
                'MeanZa1':0.562 ,'MeanZa1_err':0.078    ,'MeanZa2':0.159    ,'MeanZa2_err':0.009},index=[0])
# best correspondance
cor_vals = pd.DataFrame({'SigmaT':0.155 ,'SigmaT_err':0.0010,
                'SigmaZa1':0.143,'SigmaZa1_err':0.075   ,'SigmaZa2':0.158   ,'SigmaZa2_err':0.009,
                'MeanZa1':0.562 ,'MeanZa1_err':0.078    ,'MeanZa2':0.159    ,'MeanZa2_err':0.009},index=[0])



#N = pd.DataFrame({'SigmaT':1,'SigmaZa1':1 ,'SigmaZa2':1 ,'MeanZa1':1 ,'MeanZa2':1 ,'StartRun':0 , 'NRand':1}, index=[0]) # for debugging

#runs 1500000-1501000, 1504000-1505000, 'SigmaZa1':1000
#runs 1501000-1502000, 1505000-1506000, 'SigmaZa2':1000
#runs 1502000-1503000, 1506000-1507000, 'MeanZa1':1000
#runs 1503000-1504000, 1507000-1508000, 'MeanZa2':1000

##runs 10000-72500
#SigmaTBandRange     = [0.05,0.35]       # [0.05,0.35]
#SigmaZa1BandRange   = [0.05,0.25]          # [-0.4,1.2]    # [-0.4,1.2]    # [0,0.4]
#SigmaZa2BandRange   = [0.0,0.3]        # [-0.6,0.5]    # [-0.6,0.5]    # [-0.2,0.2]
#MeanZa1BandRange    = [0.45,0.65]         # [-0.1,1.5]    # [-0.1,1.5]    # [0.4,0.8]
#MeanZa2BandRange    = [0.0,0.3]        # [-0.3,0.6]    # [-0.3,0.6]    # [-0.3,0.0]
#N = pd.DataFrame({'SigmaT':5,'SigmaZa1':15 ,'SigmaZa2':15 ,'MeanZa1':15 ,'MeanZa2':15 ,'StartRun':100000 , 'NRand':10 }, index=[0])

##runs 100000-353125:
#SigmaTBandRange     = [0.145,0.165]
#SigmaZa1BandRange   = [-0.1,0.6]
#SigmaZa2BandRange   = [-0.1,0.6]
#MeanZa1BandRange    = [0.1,1.1]
#MeanZa2BandRange    = [-0.1,0.6]
#N = pd.DataFrame({'SigmaT':5,'SigmaZa1':15 ,'SigmaZa2':15 ,'MeanZa1':15 ,'MeanZa2':15 ,'StartRun':100000 , 'NRand':10 }, index=[0])


##runs 400000-500000:
#SigmaTBandRange     = [0.11,0.21]
#SigmaZa1BandRange   = [-0.3,0.7]
#SigmaZa2BandRange   = [0.0,0.5]
#MeanZa1BandRange    = [-0.1,1.2]
#MeanZa2BandRange    = [0.0,0.5]
#N = pd.DataFrame({'SigmaT':10,'SigmaZa1':10 ,'SigmaZa2':10 ,'MeanZa1':10 ,'MeanZa2':10 ,'StartRun':400000 , 'NRand':10 }, index=[0])


#runs 500000-1000000:
SigmaTBandRange     = [0.06,0.26]
SigmaZa1BandRange   = [-0.3,0.9]
SigmaZa2BandRange   = [-0.2,0.8]
MeanZa1BandRange    = [-0.1,1.2]
MeanZa2BandRange    = [-0.1,0.9]
N = pd.DataFrame({'SigmaT':15,'SigmaZa1':15 ,'SigmaZa2':15 ,'MeanZa1':15 ,'MeanZa2':15 ,'StartRun':500000 , 'NRand':10 }, index=[0])



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


# (3) cuts sensitivity studies for (e,e'pp)/(e,e'p)
# ---------------------------------------------------
if 'cuts sensitivity studies' in flags.option or 'sensitivity' in flags.option: # scheme to pp-SRC in wider cuts
    # xB >= 1.15 and xB >= 1.25
    # theta_pq < 20 and theta_pq < 30
    # 0.57 < p/q < 0.91 and 0.67 < p/q < 1.01
    # m_miss < 1050 and m_miss < 1150 (open to m_miss < 1.3 to study it)
    relaxed_src_cuts = '(1.0<Xb) && (theta_pq < 40) && (0.37 < p_over_q && p_over_q < 1.21) && (Mmiss<1.500) && (0.3 < Pmiss.P() && Pmiss.P() < 1.0)'
    p_lead_cut = '-24.5 < pVertex[0].Z() && pVertex[0].Z() < -20'
    relaxed_eep_cut = ROOT.TCut("(%s) && (%s) "%(relaxed_src_cuts,p_lead_cut))
    p_rec_cut = '0.35 < Prec.P()  &&  -24.5 < pVertex[1].Z() && pVertex[1].Z() < -20 && pFiducCut[1] == 1'
    relaxed_cut = ROOT.TCut("(%s) && (%s) && (%s) && (1<Np)"%(relaxed_src_cuts,p_lead_cut,p_rec_cut))
    
    
    DataName    = "DATA_%s"% dm.Target(flags.atomic_mass)
    ana     = TAnalysisEG2( path+"/AnaFiles" , "Ana_SRCPmissXb_"+DataName , flags.cut )
    scheme  = TSchemeDATA()
    SchemedName = "relaxed_ppSRCCut_%s"% DataName
    scheme.SchemeOnTCut( path+"/AnaFiles","Ana_SRCPmissXb_"+DataName+".root","anaTree","Ana_"+SchemedName+".root",ROOT.TCut(relaxed_cut) )
    SchemedName = "eep_in_relaxed_ppSRCCut_%s"% DataName
    scheme.SchemeOnTCut( path+"/AnaFiles","Ana_SRCPmissXb_"+DataName+".root","anaTree","Ana_"+SchemedName+".root",ROOT.TCut(relaxed_eep_cut) )
    print 'schemed to %s'%SchemedName


# (3) extract cm-parameters from data (no acc. correction)
# ----------------------------------------------------------
if 'extract data cm-parameters' in flags.option or 'extract' in flags.option: # DATA

    # (A) calc cm parameters of data
    ana_data = TAnalysisEG2( path+"/AnaFiles" , "Ana_ppSRCCut_DATA_%s"% dm.Target(A) )
    cm_parameters , do_fits = calc_cm_parameters( ana_data  , PmissBins , CMRooFitsName( ppPath + '/DATA/unweighted' ) , CMRooFitsName( ppPath + '/DATA/weighted' ) , DoSaveCanvas = True )
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
if 'plot all parameters for all targets' in flags.option or 'AllTargets' in flags.option: # DATA
    
    # (A) compute width and mean for all nuclei
    colors  = ['black'      , 'red'         , 'green'       , 'blue'        ]
    
    ana , cm_pars , cm_fits = [] , [] , []
    for target in targets:
        ana.append( TAnalysisEG2( path+"/AnaFiles" ,  "Ana_ppSRCCut_DATA_%s"%target ) )
        cm_parameters , _ = calc_cm_parameters( ana[-1]  , PmissBins ,
                                            CMRooFitsName( ppPath + '/DATA/%s_unweighted'%target ) ,
                                            CMRooFitsName( ppPath + '/DATA/%s_weighted'%target ) ,
                                            DoSaveCanvas = True )
        cm_parameters.to_csv( CMParsFname(ppPath+'/DATA/%s_data'%target) , header=True , index = False)
        cm_pars.append( cm_parameters )
        fits = fit_cm_parameters( target + ' data' , cm_parameters , FigureFName(ppPath+'/DATA/data', target) , DoPlot = True )
        fits.to_csv( CMfitsFname( ppPath+'/DATA/data' , target ) , header=True , index=False)
        print_filename( CMfitsFname(ppPath+'/DATA/data' , target )  , target + " data c.m. fits at")
        cm_fits.append( fits )



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

    cm_parameters = pd.read_csv( CMParsFname(ppPath+'/DATA/C12_data' ) )
    fits = pd.read_csv( CMfitsFname( ppPath+'/DATA/data' , 'C12' ) )

    generate_cm_bands( cm_parameters , fits , N ,
                      flags.verbose ,
                      CMBandFname( ppPath+'/DATA/data' ) , FigureBandFName( ppPath+'/DATA/data' ) , GeneParsFName ( ppPath+'/simulation/' ) ,
                      DoSaveCanvas = True,
                      SigmaTBandRange = SigmaTBandRange,
                      SigmaZa1BandRange = SigmaZa1BandRange,
                      SigmaZa2BandRange = SigmaZa2BandRange,
                      MeanZa1BandRange  = MeanZa1BandRange,
                      MeanZa2BandRange = MeanZa2BandRange,
                      nom_vals = cor_vals
                      )




# (5) generate runs with different parameters
# ----------------------------------------------------------
if 'generate and analyze runs' in flags.option or 'generate' in flags.option or 'analyze' in flags.option or 'analyse' in flags.option:

    fits_12C = pd.read_csv( CMfitsFname( ppPath+'/DATA/data' , 'C12' ) )
    fits_27Al = pd.read_csv( CMfitsFname( ppPath+'/DATA/data' , 'Al27' ) )
    fits_56Fe = pd.read_csv( CMfitsFname( ppPath+'/DATA/data' , 'Fe56' ) )
    fits_208Pb = pd.read_csv( CMfitsFname( ppPath+'/DATA/data' , 'Pb208' ) )
    print_filename(GeneParsFName ( ppPath+'/simulation/' ),'reading generated-parameters...')
    generated_parameters = pd.read_csv( GeneParsFName ( ppPath+'/simulation/' ) )
    if debug>3: print 'generated_parameters:',generated_parameters
    print start_run , start_run + Nruns
    generated_parameters = generated_parameters[(start_run <= generated_parameters.run) & (generated_parameters.run < start_run + Nruns)] # perhaps:  generated_parameters.run < start_run + Nruns ? check!
    
    if debug>2: print 'generated_parameters:',generated_parameters
    test_name = 'runs%dto%d_NsigmaT_%d_NSigmaZa1_%d_NSigmaZa2_%d_NMeanZa1_%d_NMeanZa2_%d_NRand_%d'%( start_run , start_run+Nruns , N.SigmaT , N.SigmaZa1 , N.SigmaZa2 , N.MeanZa1 , N.MeanZa2 , N.NRand ) # perhaps: start_run+Nruns-1 ?
    full_path = ppPath+'/simulation/'+test_name+'_simulation'
    generate_runs_with_different_parameters( flags.option ,
                                            fits_12C, fits_27Al, fits_56Fe, fits_208Pb,
                                            generated_parameters ,
                                            flags.verbose , PmissBins , Q2Bins, thetapmqBins,
                                            buildup_resutlsFName( full_path ) ,
                                            CMfitsFname( full_path ) ,
                                            dm.Target(A) ,
                                            N ,
                                            root_resutlsFName( full_path ) )








mod_cut = dict({'name':"Mmiss_1050",
               'XbCut':"1.2<Xb",
               'theta_pqCut':"theta_pq < 25",
               'p_over_qCut':"0.62 < p_over_q && p_over_q < 0.96",
               'MmissCut':"Mmiss<1.050"})
    
mod_src_cuts = ROOT.TCut("(%s) && (%s) && (%s) && (%s) && (1<Np)"
                         %(mod_cut['XbCut'],mod_cut['theta_pqCut'],mod_cut['p_over_qCut'],mod_cut['MmissCut']))
        

p_lead_cut = '-24.5 < pVertex[0].Z() && pVertex[0].Z() < -20'
mod_eep_cut = ROOT.TCut("(%s) && (%s) "%(mod_src_cuts,p_lead_cut))
p_rec_cut = '0.35 < Prec.P()  &&  -24.5 < pVertex[1].Z() && pVertex[1].Z() < -20 && pFiducCut[1] == 1'
mod_eepp_cut = ROOT.TCut("(%s) && (%s) && (%s) && (1<Np)"%(mod_src_cuts,p_lead_cut,p_rec_cut))


# (6) prepare runs with different parameters
# ----------------------------------------------------------
if 'prepare to generate/analyzes with modified cuts' in flags.option or 'prepmodcut' in flags.option:
    
    scheme  = TSchemeDATA()
    ana , cm_pars  , fits  = dict() , dict() , dict()
        
    for target in targets:
        
        DataName  = "DATA_%s"%target
        # scheme to modified cuts
        SchemedName = "eep_in_mod_cut_%s_ppSRCCut_%s"% (mod_cut['name'],DataName)
        scheme.SchemeOnTCut( path+"/AnaFiles","Ana_SRCPmissXb_"+DataName+".root","anaTree","Ana_"+SchemedName+".root",mod_eep_cut )
        SchemedName = "mod_cut_%s_ppSRCCut_%s"% (mod_cut['name'],DataName)
        scheme.SchemeOnTCut( path+"/AnaFiles","Ana_SRCPmissXb_"+DataName+".root","anaTree","Ana_"+SchemedName+".root",mod_eepp_cut )
        
        # get cm parameters and fit
        ana[target] = TAnalysisEG2( path+"/AnaFiles" ,  "Ana_"+SchemedName )
        cm_pars[target] , _ = calc_cm_parameters( ana[target]  , PmissBins  )
        cm_pars[target].to_csv( CMParsFname(ppPath+'/DATA/%s_data_mod_cut_%s'%(target,mod_cut['name'])) , header=True , index = False)
        
        fits[target] = fit_cm_parameters( target + ' data  cut %s'%mod_cut['name'], cm_pars[target] ,  )
        fits[target].to_csv( CMfitsFname( ppPath+'/DATA/data_mod_cut_%s'%mod_cut['name'] , target ) , header=True , index=False)
        print_filename( CMfitsFname( ppPath+'/DATA/data_mod_cut_%s'%mod_cut['name'], target )  , target + "c.m. fits (modified cut %s)"%mod_cut['name'])



# (6) generate runs with different parameters
# ----------------------------------------------------------
if 'generate/analyzes with modified cuts' in flags.option or 'genmodcut' in flags.option or 'anamodcut' in flags.option in flags.option:
    
    fits = dict()
    for target in targets:
        fits[target] = pd.read_csv( CMfitsFname( ppPath+'/DATA/data_mod_cut_%s'%mod_cut['name'] , target ) )
    
        
    print_filename(GeneParsFName ( ppPath+'/simulation/' ),'reading generated-parameters...')
    generated_parameters = pd.read_csv( GeneParsFName ( ppPath+'/simulation/' ) )
    if debug>3: print 'generated_parameters:',generated_parameters
    print start_run , start_run + Nruns
    generated_parameters = generated_parameters[(start_run <= generated_parameters.run) & (generated_parameters.run < start_run + Nruns)]
    
    if debug>2: print 'generated_parameters:',generated_parameters
    test_name = 'runs%dto%d_NsigmaT_%d_NSigmaZa1_%d_NSigmaZa2_%d_NMeanZa1_%d_NMeanZa2_%d_NRand_%d_mod_cut_%s'%( start_run , start_run+Nruns , N.SigmaT , N.SigmaZa1 , N.SigmaZa2 , N.MeanZa1 , N.MeanZa2 , N.NRand , mod_cut['name'] )
    full_path = ppPath+'/simulation/'+test_name+'_simulation'
    generate_runs_with_different_parameters( flags.option ,
                                            fits['C12'], fits['Al27'], fits['Fe56'], fits['Pb208'],
                                            generated_parameters ,
                                            flags.verbose , PmissBins , Q2Bins, thetapmqBins,
                                            buildup_resutlsFName( full_path ) ,
                                            CMfitsFname( full_path ) ,
                                            dm.Target(A) ,
                                            N ,
                                            root_resutlsFName( full_path ) ,
                                            main_cut=mod_eepp_cut )




