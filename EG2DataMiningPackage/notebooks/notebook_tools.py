import sys, pandas as pd, numpy as np
import ROOT , time , os, sys , math , datetime
import matplotlib.pyplot as plt
import matplotlib as mpl , seaborn as sns; sns.set(style="white", color_codes=True , font_scale=1)
sys.path.insert(0, '/Users/erezcohen/larlite/UserDev/mySoftware/MySoftwarePackage/mac')
sys.path.insert(0, '/Users/erezcohen/larlite/UserDev/CLASEG2DataMining/EG2DataMiningPackage/mac')
import GeneralPlot as gp , Initiation as init, plot_tools as pt
from root_numpy import tree2array
from ROOT import TPlots, TAnalysis, TAnalysisEG2 , TEG2dm , TCalcPhysVarsEG2 , TSchemeDATA
dirname = init.createnewdir()
dm  = TEG2dm()



path = "/Users/erezcohen/Desktop/DataMining"

# ----------------------------------------------------------
def plot_hist1d( ana , var , xmin , xmax , nbins=10 , x_label='' , y_label=''
                , color='b', alpha=1, histtype='stepfilled', do_preliminary=True ):
    
    fig , ax = plt.subplots(figsize = [10,10])
    n , bins , patches = plt.hist( ana[var] , bins=np.linspace(xmin,xmax,nbins) , color=color , alpha=alpha , histtype=histtype )
    pt.set_axes( ax , x_label , y_label , fontsize=30)
    if do_preliminary:
        ax.text( xmin+(xmax-xmin)/3. , 0.6*np.max(n) , 'preliminary' , color='red' , alpha=0.2 , fontsize=50 )
                        
# ----------------------------------------------------------
def plot_hist1d_ppp( var , xmin , xmax , nbins , x_label ):
    
    bins = np.linspace(xmin,xmax,nbins)
    fig = plt.figure(figsize = [10,8])
    ax = plt.subplot(111)
    pt.plot_distplot( all_events[var] , bins , 'all' , x_label , xmin , xmax )
    pt.plot_distplot( all_ppp[var]  , bins , 'all 3p' , x_label , xmin , xmax )
    pt.plot_distplot( ppp_src[var] , bins , 'ppp-candidates (%d)'%len(ppp_src) , x_label ,  xmin , xmax )
    plt.legend(fontsize=25)
    fig.subplots_adjust(bottom=0.15)
    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(25)
    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(25)

