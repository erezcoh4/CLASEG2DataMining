
import ROOT , time , sys , math , datetime ,  matplotlib
import matplotlib as mpl, pandas as pd , numpy as np, seaborn as sns ; sns.set(style="white", color_codes=True , font_scale=1)
from ROOT import TPlots, TAnalysisEG2 , TEG2dm , TSchemeDATA ,GenerateEvents
from matplotlib import pyplot as plt
from root_numpy import hist2array , tree2array
from scipy.stats import ks_2samp
from math import sqrt
sys.path.insert(0, '/Users/erezcohen/larlite/UserDev/mySoftware/MySoftwarePackage/mac')
sys.path.insert(0, '/home/erez/larlite/UserDev/mySoftware/MySoftwarePackage/mac')
import input_flags , GeneralPlot as gp , gc
flags = input_flags.get_args()




# paths
if flags.worker == "erez":
    path = "/Users/erezcohen/Desktop/DataMining"

elif flags.worker == "helion":
    path = "/home/erez/DataMining"

ppPath = path + "/Analysis_DATA/ppSRCcm"

print "running option ",flags.option



# instances
dm  = TEG2dm()
analysis = TAnalysis()