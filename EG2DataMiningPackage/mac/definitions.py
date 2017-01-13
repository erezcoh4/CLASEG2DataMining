
import ROOT , time , os, sys , math , datetime
sys.path.insert(0, '/Users/erezcohen/larlite/UserDev/mySoftware/MySoftwarePackage/mac')
sys.path.insert(0, '/home/erez/larlite/UserDev/mySoftware/MySoftwarePackage/mac')
sys.path.insert(0, '../../GSIMulation')
import matplotlib as mpl, pandas as pd , numpy as np
import seaborn as sns ; sns.set(style="white", color_codes=True , font_scale=1)
from ROOT import TPlots, TAnalysis, TAnalysisEG2 , TEG2dm , TCalcPhysVarsEG2 , TSchemeDATA ,GenerateEvents
from matplotlib import pyplot as plt

import input_flags , Initiation as init, GeneralPlot as gp , gc
from my_tools import *
from calc_tools import *
from root_pandas import read_root
from scipy.optimize import curve_fit


flags = input_flags.get_args()




# paths
if 'erez' in flags.worker or 'Erez' in flags.worker :
    import rootpy.plotting.root2matplotlib as rplt
    path = "/Users/erezcohen/Desktop/DataMining"

elif flags.worker == "helion":
    path = "/home/erez/DataMining"

elif 'jlab' in flags.worker or 'Jlab' in flags.worker or 'JLAB' in flags.worker or 'farm' in flags.worker :
    path = "/work/halla/e07006/disk1/Erez/DataMining"

eg2_data_path = path + "/EG2_DATA"

if 'Lacie' in flags.worker:
    eg2_data_path = "/Volumes/LaCie/erezcohen/Desktop/DataMining/EG2_DATA"

schemed_eg2_data_path = path + "/Schemed_EG2_DATA"
ppPath = path + "/Analysis_DATA/ppSRCcm"

print "running option ",flags.option



# instances
dm  = TEG2dm()
analysis = TAnalysis()
scheme = TSchemeDATA()


# flags
A = flags.atomic_mass
debug = flags.verbose



if 'ppSRC' in flags.option or 'pppSRC' in flags.option:
    axes_frame  = "Pmiss(z) - q(x-z) frame"
else:
    axes_frame  = "q(z) - Pmiss(x-z) frame"
