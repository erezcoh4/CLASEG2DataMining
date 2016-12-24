import sys, pandas as pd, numpy as np
import ROOT , time , os, sys , math , datetime
import matplotlib.pyplot as plt
import matplotlib as mpl , seaborn as sns; sns.set(style="white", color_codes=True , font_scale=1)
sys.path.insert(0, '/Users/erezcohen/larlite/UserDev/mySoftware/MySoftwarePackage/mac')
sys.path.insert(0, '/Users/erezcohen/larlite/UserDev/CLASEG2DataMining/EG2DataMiningPackage/mac')
import GeneralPlot as gp , Initiation as init, plot_tools as pt
from plot_tools import *
from calc_tools import *
from root_numpy import tree2array
from ROOT import TPlots, TAnalysis, TAnalysisEG2 , TEG2dm , TCalcPhysVarsEG2 , TSchemeDATA
dirname = init.createnewdir()
dm  = TEG2dm()



path = "/Users/erezcohen/Desktop/DataMining"
my_hot_cmap = gp.reverse_colourmap(mpl.cm.hot)

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




# ----------------------------------------------------------
def plot_sns( simulation_results , x , y , xlabel = '' , ylabel = '' ):
    with sns.axes_style("white"):
        g = sns.JointGrid(x=simulation_results[x], y=simulation_results[y] )
        g.plot_joint(sns.regplot, order=2)
        g.plot_marginals(sns.distplot)
    if xlabel=='': xlabel = x
    if ylabel=='': ylabel = y
    g.set_axis_labels(xlabel,ylabel)
    plt.show()
    g.savefig(dirname + "/%s_vs_%s.pdf"%(x,y))

e3c = sns.color_palette()[2]
def plot_sns_scatter( simulation_results , x , y , xlabel = '' , ylabel = '' , xmin = -1 , xmax = -1 ):
    with sns.axes_style("white"):
        g = sns.JointGrid(x=simulation_results[x], y=simulation_results[y])
        g.plot_marginals(sns.distplot, kde=False, color=e3c)
        g.plot_joint(plt.scatter, color=e3c, alpha=.2)
    if xlabel=='': xlabel = x
    if ylabel=='': ylabel = y
    g.set_axis_labels(xlabel,ylabel)
    if xmin<xmax: print "xmin:",xmin; plt.xlim(xmin,xmax)
    plt.show()
    g.savefig(dirname + "/%s_vs_%s_scatter.pdf"%(x,y))

# ----------------------------------------------------------
def plot_sns_heatmap( simulation_results , x , y , xlabel = '' , ylabel = '' ):
    with sns.axes_style("white"):
        g = sns.jointplot(x=simulation_results[x], y=simulation_results[y] ,
                          cmap=my_hot_cmap, kind="hex", stat_func=None,
                          marginal_kws={'color': 'green'})
    if xlabel=='': xlabel = x
    if ylabel=='': ylabel = y
    g.set_axis_labels(xlabel,ylabel)
    plt.colorbar()
    plt.show()
    g.savefig(dirname + "/%s_vs_%s_heatmap.pdf"%(x,y))



# ----------------------------------------------------------
def plot_1d( simulation_results , x , xlabel=''):
    ax = sns.distplot(simulation_results[x])
    if xlabel=='': xlabel = x
    fig = ax.get_figure()
    plt.show()
    fig.savefig(dirname + "/%s.pdf"%x)

# ----------------------------------------------------------
def sigma_l(direction,addition):
    return addition + ' $\sigma_{%s}$'%direction

# ----------------------------------------------------------
def mean_l(direction,addition):
    return addition + ' $\mu_{%s}$'%direction