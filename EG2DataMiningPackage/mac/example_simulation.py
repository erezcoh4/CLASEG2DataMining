'''
    usage:
    ---- - -- -- --
    python mac/example_simulation.py --option=gen_ana -v2
'''
import sys
from cm_tools import *

scheme = TSchemeDATA()
targets = ['C12','Al27','Fe56','Pb208']
PmissBins   = [[0.3,0.45]  , [0.45,0.55] , [0.55,0.65]  , [0.65,0.75] , [0.75,1.0]]
Pmiss3Bins  = [[0.3,0.52]  , [0.52,0.68]  , [0.68,1.0]]
#path = "/Users/erezcohen/Desktop/DataMining"
ppPath = path + "/Analysis_DATA/ppSRCcm"

cm_pars , cm_fits = dict() , dict()
ana_data = dict()

for target in targets: ana_data[target] = TAnalysisEG2( path + "/OrAnalysisTrees/AdjustedTrees" , "SRC_e2p_adjusted_%s"%target )

def a1a2_create_negative_sigma_z( a1 , a2 ):#{
    '''
        check if a1 and a2 give \sigma_z < 0,
        since we do not want to use those (unreasonable) values.
        we check for the minimal Pmiss (0.3) and the maximal Pmiss (1.0)
        '''
    if a1*(0.3 - 0.6) + a2 < 0: return True
    if a1*(1.0 - 0.6) + a2 < 0: return True
    return False
#}

hyperparameters = dict({'start_run':2,
                       'Nruns':1,
                       'range_sigma_t':(0.1  , 0.3),    # 0.160
                       'range_a1':(-0.4 , 1.0),         # 0.143
                       'range_a2':(0.0  , 0.5),         # 0.158
                       'range_b1':(-0.2 , 1.4),         # 0.569
                       'range_b2':(-0.1 , 0.6),         # 0.159
                       'NRand':20,
                       'Ntimes':10,                     # wanted number of events in each Pmiss bin
                       'NgenMax':100000,                # maximal number of attempts
                       'do_ks_plots':True
                       })

start_run , Nruns = hyperparameters['start_run'], hyperparameters['Nruns']
NRand = hyperparameters['NRand']
pAcceptacneFile = ROOT.TFile( path + "/GSIM_DATA/PrecoilAcceptance.root" )
path = path + "/Analysis_DATA/ppSRCcm"

h = pAcceptacneFile.Get("hRescaled")
gen_events = GenerateEvents( path , 0 , debug-1 )
gen_events.Set_protonAcceptacne( h )

gen_events.SetInputChain_eep()

gen_events.SetNRand( NRand )
gen_events.Use_protonAcceptacne( True )
gen_events.SetDo_PrecFiducial ( True )
gen_events.SetDo_PrecMinCut ( True )

gen_events.SetPmissBins()
gen_events.Set10PmissBins()

# set the desired number of events when the simulation ends in 5 Pmiss bins
# as a 100 times the number of 12C (e,e'pp) events in each bin
Ntimes = hyperparameters['Ntimes']
gen_events.SetNeventsPerPmissBin( 71*Ntimes , 143*Ntimes , 132*Ntimes , 96*Ntimes , 56*Ntimes )
gen_events.SetNgenMax( hyperparameters['NgenMax'] )
gen_events.MapInputEntriesInPmissBins()
# if we don't reach these numbers after generating NMAX events, the parameters should be discarded
# by Pval = 0, which can be obtained by killing the run and flaggind it as a bad run

run = 6
gen_SigmaX , gen_a1 , gen_a2 , gen_b1 , gen_b2 = 0.21	,0.2	,0.160	,0.50     ,0.2
gen_MeanX = -0.02
gen_MeanY = 0.0
gen_SigmaY = gen_SigmaX

print 'run',run,'gen_SigmaX',gen_SigmaX,'gen_a1',gen_a1,'gen_a2',gen_a2,'gen_b1',gen_b1,'gen_b2',gen_b2

if 'gen' in flags.option:#{
    if a1a2_create_negative_sigma_z( gen_a1 , gen_a2 ) is False: #{
    
        gen_events.Set_eep_Parameters( gen_MeanX, gen_SigmaX, gen_MeanY, gen_SigmaY, gen_b1, gen_b2, gen_a1, gen_a2 )
        gen_events.InitRun()
        Nevents = gen_events.DoGenerate_eepp_from_eep( run )
    #}
    else:#{
        print 'a1 (%.2f) and a2(%.2f) create together a negative sigma_z, killing run %d'%( gen_a1 , gen_a2 , run )
    #}
#}

if 'ana' in flags.option:#{
    print 'analyzing run...'
    ana_sim = TAnalysisEG2( path + '/eg_rootfiles', 'run%d'%run )
        
    ks_pval_scores = calc_pval_ks_scores( ana_sim , ana_data
                                             , do_plots=hyperparameters['do_ks_plots'] , run=run )
    print 'finished calculating ks_pval_scores'
    ana_sim.CloseFile()
#}
