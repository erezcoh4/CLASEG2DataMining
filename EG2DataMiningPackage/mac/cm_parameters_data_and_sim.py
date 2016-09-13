'''
    usage:
    ---------
    python mac/cm_parameters_data_and_sim.py --option=" extract cm-parameters , create bands for EG , generate runs "
    '''



import ROOT , time , sys , math , datetime
from matplotlib import pyplot as plt
import matplotlib , pandas as pd , numpy as np
from ROOT import TPlots, TAnalysisEG2 , TEG2dm , TSchemeDATA ,GenerateEvents
sys.path.append('../mac')
sys.path.append('../../mySoftware/MySoftwarePackage/mac')
import input_flags, cm_tools as tools
flags = input_flags.get_args()

PmissBins = [[0.3,0.45]  , [0.45,0.55] , [0.55,0.65] , [0.65,0.75] , [0.75,1.0]]
path = "/Users/erezcohen/Desktop/DataMining/Analysis_DATA/ppSRCcm"
A = 12
dm = TEG2dm()




if 'extract cm-parameters' in flags.option: # DATA

    # ToDo: add proton fiducial cuts!
    # (1) calc cm parameters of data
    SchemedName = "ppSRCCut_DATA_%s_ppSRC"% dm.Target(A)
    ana_data = TAnalysisEG2( SchemedName )
    tools.calc_cm_parameters( ana_data  , PmissBins , tools.CMParsFname(path+'/DATA') )

    # (2) plot cm parameters
    data = pd.read_csv( tools.CMParsFname(path+'/DATA') )
    tools.plot_cm_parameters( data , tools.CMFitsFname(path+'/DATA') , tools.FigureFName(path+'/DATA') )



else:

    data = pd.read_csv( tools.CMParsFname(path+'/DATA') )


if 'create bands for EG' in flags.option:
    
    # (3) create bands for event generation
    run  = flags.run # starting run number
    tools.generate_cm_bands( data , run , tools.CMFitsFname( path+'/DATA' ) , tools.CMBandFname( path+'/DATA' ) , tools.RunsInfoFileName( path+'/simulation' ) , tools.FigureBandFName( path+'/simulation' ))


if 'generate runs' in flags.option:
    
    # (4) generate runs with different parameters
    tools.generate_runs_with_different_parameters( data , run , tools.RunsInfoFileName( path+'/simulation' )  )






