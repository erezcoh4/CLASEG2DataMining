
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
flags = input_flags.get_args()




# paths
if flags.worker == "erez":
    import rootpy.plotting.root2matplotlib as rplt
    path = "/Users/erezcohen/Desktop/DataMining"

elif flags.worker == "helion":
    path = "/home/erez/DataMining"

ppPath = path + "/Analysis_DATA/ppSRCcm"

print "running option ",flags.option



# instances
dm  = TEG2dm()
analysis = TAnalysis()
scheme = TSchemeDATA()


# flags
A = flags.atomic_mass




if (flags.option == "ppSRC"):
    axes_frame  = "Pmiss(z) - q(x-z) frame"
else:
    axes_frame  = "q(z) - Pmiss(x-z) frame"
