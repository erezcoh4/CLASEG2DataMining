'''
    usage:
    ---------
    python mac/cm_parameters_data_and_sim.py --option="scheme pp-SRC , extract cm-parameters , create bands for EG , generate runs " --run=0
'''



import ROOT , time , sys , math , datetime ,  matplotlib , pandas as pd , numpy as np
from ROOT import TPlots, TAnalysisEG2 , TEG2dm , TSchemeDATA ,GenerateEvents
sys.path.append('../mac') ; sys.path.append('../../mySoftware/MySoftwarePackage/mac')
import input_flags, cm_tools as tools
flags = input_flags.get_args()

PmissBins = [[0.3,0.45]  , [0.45,0.55] , [0.55,0.65] , [0.65,0.75] , [0.75,1.0]]
path = "/Users/erezcohen/Desktop/DataMining/Analysis_DATA/ppSRCcm"
A = 12
start_run  = flags.run
dm = TEG2dm()
DoWeight = True if flags.DoWeight==1 else False



if 'scheme pp-SRC' in flags.option: # scheme to pp-SRC

    # ToDo: add proton fiducial cuts!
    DataName    = "DATA_%s"% dm.Target(flags.atomic_mass)
    SchemedName = "ppSRCCut_%s"% DataName
    ana     = TAnalysisEG2( "SRCPmissXb_"+DataName , flags.cut )
    scheme  = TSchemeDATA()
    scheme.SchemeOnTCut( "/Users/erezcohen/Desktop/DataMining/AnaFiles" , "Ana_SRCPmissXb_"+DataName+".root", "anaTree", "Ana_"+SchemedName+".root", ana.ppSRCCut + ana.PrecFiducial)
    print 'schemed to %s'%SchemedName


if 'extract cm-parameters' in flags.option: # DATA

    # (1) calc cm parameters of data
    ana_data = TAnalysisEG2( "ppSRCCut_DATA_%s"% dm.Target(A) )
    tools.calc_cm_parameters( ana_data  , PmissBins , tools.CMParsFname(path+'/DATA/') , tools.CMfitsFname( path + '/DATA/') , DoWeight )

    # (2) plot cm parameters
    cm_parameters = pd.read_csv( tools.CMParsFname(path+'/DATA/') )
    tools.plot_cm_parameters( cm_parameters , tools.CMfitsFname(path+'/DATA/') , tools.FigureFName(path+'/DATA/') )




if 'create bands for EG' in flags.option:
    
    # (3) create bands for event generation
    cm_parameters = pd.read_csv( tools.CMParsFname(path+'/DATA/') )
    tools.generate_cm_bands( cm_parameters , start_run , tools.CMfitsFname( path+'/DATA/' ) , tools.CMBandFname( path+'/DATA/' ) , tools.RunsInfoFileName( path+'/simulation/' ) , tools.FigureBandFName( path+'/simulation/' ))



if 'generate runs' in flags.option:
    
    # (4) generate runs with different parameters
    cm_pars_bands = pd.read_csv( tools.CMBandFname(path+'/DATA/') )
    tools.generate_runs_with_different_parameters( tools.CMfitsFname( path+'/DATA/' ) , cm_pars_bands , start_run , tools.RunsInfoFileName( path+'/simulation/' ) ,
                                                  path , flags.verbose , PmissBins , tools.SimParametersFileName( path+'/simulation/' ) , dm.Target(A) , DoWeight )








