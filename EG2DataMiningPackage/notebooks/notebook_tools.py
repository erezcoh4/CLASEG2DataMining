import sys, pandas as pd, numpy as np , ast
import ROOT , time , os, sys , math , datetime
import matplotlib.pyplot as plt
import matplotlib as mpl , seaborn as sns; sns.set(style="white", color_codes=True , font_scale=1)
sys.path.insert(0, '/Users/erezcohen/larlite/UserDev/mySoftware/MySoftwarePackage/mac')
sys.path.insert(0, '/Users/erezcohen/larlite/UserDev/CLASEG2DataMining/EG2DataMiningPackage/mac')
import GeneralPlot as gp , Initiation as init, plot_tools as pt
import matplotlib.patches as patches
from matplotlib.lines import Line2D
from scipy.interpolate import interp1d, Akima1DInterpolator,BarycentricInterpolator,splprep
from plot_tools import *
from my_tools import *
from calc_tools import *
from root_numpy import tree2array, root2array
from root_pandas import read_root
from ROOT import TPlots, TAnalysis, TAnalysisEG2 , TEG2dm , TCalcPhysVarsEG2 , TSchemeDATA
from scipy.optimize import curve_fit
from matplotlib.ticker import NullFormatter,MultipleLocator, FormatStrFormatter
from matplotlib.offsetbox import AnchoredText
from scipy.signal import savgol_filter
from scipy.stats import norm



dm  = TEG2dm()

path = "/Users/erezcohen/Desktop/DataMining"
my_hot_cmap = gp.reverse_colourmap(mpl.cm.hot)


# ----------------------------------------------------------
def plot_data(data , Ashift=0, fmt='o', marker='^',color='red',
              markersize=20, linewidth=4,
              vary=None , varyerr=None , label=None , mulfac=1):
    ax.errorbar((data['A']+Ashift), mulfac*data[vary], yerr=mulfac*data[varyerr],
                color=color, marker=marker,markersize=markersize,linewidth=linewidth, fmt=fmt,label=label)
# ----------------------------------------------------------


# ----------------------------------------------------------
def plot_calculation_line( data , varx='A',kind='nearest' , vary=None , color='blue' , label=None, linewidth=4):
    x = data[varx]
    y = data[vary]
    itp = interp1d(x,y, kind='linear')
    
    if kind is None:
        f = interp1d( x , y )
    else:
        f = interp1d( x , y ,kind=kind)
    
    window_size, poly_order = 101, 4
    xnew = np.linspace(x.min(),x.max(), num=500, endpoint=True)
    yy_sg = savgol_filter(itp(xnew), window_size, poly_order)
    plt.plot( xnew, yy_sg, '--', color=color , label=label, linewidth=linewidth )
# ----------------------------------------------------------




# ----------------------------------------------------------
def customaxis(ax, c_left='k', c_bottom='k', c_right='none', c_top='none',
               lw=3, size=12, pad=8):
    
    for c_spine, spine in zip([c_left, c_bottom, c_right, c_top],
                              ['left', 'bottom', 'right', 'top']):
        if c_spine != 'none':
            ax.spines[spine].set_color(c_spine)
            ax.spines[spine].set_linewidth(lw)
        else:
            ax.spines[spine].set_color('none')
        if (c_bottom == 'none') & (c_top == 'none'): # no bottom and no top
            ax.xaxis.set_ticks_position('none')
        elif (c_bottom != 'none') & (c_top != 'none'): # bottom and top
            ax.tick_params(axis='x', direction='out', width=lw, length=7,
                   color=c_bottom, labelsize=size, pad=pad)
        elif (c_bottom != 'none') & (c_top == 'none'): # bottom but not top
            ax.xaxis.set_ticks_position('bottom')
            ax.tick_params(axis='x', direction='out', width=lw, length=7,
                                          color=c_bottom, labelsize=size, pad=pad)
        elif (c_bottom == 'none') & (c_top != 'none'): # no bottom but top
            ax.xaxis.set_ticks_position('top')
            ax.tick_params(axis='x', direction='out', width=lw, length=7,
                                              color=c_top, labelsize=size, pad=pad)

        if (c_left == 'none') & (c_right == 'none'): # no left and no right
                ax.yaxis.set_ticks_position('none')
        elif (c_left != 'none') & (c_right != 'none'): # left and right
            ax.tick_params(axis='y', direction='out', width=lw, length=7,
                       color=c_left, labelsize=size, pad=pad)
        elif (c_left != 'none') & (c_right == 'none'): # left but not right
            ax.yaxis.set_ticks_position('left')
            ax.tick_params(axis='y', direction='out', width=lw, length=7,
                       color=c_left, labelsize=size, pad=pad)
        elif (c_left == 'none') & (c_right != 'none'): # no left but right
            ax.yaxis.set_ticks_position('right')
            ax.tick_params(axis='y', direction='out', width=lw, length=7,
                       color=c_right, labelsize=size, pad=pad)
# ----------------------------------------------------------

# ----------------------------------------------------------
def get_mean_and_sigma( x , w ):
    
    mean_unweighted , mean_weighted = np.average( x ) , np.average( x , weights=w )
    sigma_unweighted, sigma_weighted= np.sqrt(np.average( np.square(x-mean_unweighted) )) , np.sqrt(np.average( np.square(x-mean_weighted) , weights=w  ))
    return mean_unweighted , mean_weighted , sigma_unweighted, sigma_weighted
# ----------------------------------------------------------





# ----------------------------------------------------------
def fit2constant(y=None , yerr=None):
    
    simga2_inverse = [1./np.square(yerr[i]) if yerr[i]>0.01 else 0.01 for i in range(len(y))]
    mean = np.average(y , weights=simga2_inverse)
    sigma = np.sqrt(np.average(np.square(y-mean),weights=simga2_inverse))
    
    return mean , sigma
# ----------------------------------------------------------

# ----------------------------------------------------------
def plot_fit2constant(x=None , y=None , yerr=None , color='black' , do_plot_result=True, alpha=0.1 , xtext=None, ytext=None):
    
    mean , sigma = fit2constant(y=y , yerr=yerr)
    
    if do_plot_result:
        y , yerr = mean*np.ones(len(x)) , sigma*np.ones(len(x))
        plt.plot( x , y , '-',color=color)
        plt.fill_between( x , y-yerr , y+yerr , color=color , alpha=alpha)
        if xtext is None:
            xtext = np.min(x) + 0.1*(np.max(x)-np.min(x))
        if ytext is None:
            ytext = np.min(y) + 0.1*(np.max(y)-np.min(y))
        plt.text(xtext , ytext , '$%.3f \\pm %.3f $'%(mean,sigma) + '%', color=color , fontsize=20)

    return mean , sigma
# ----------------------------------------------------------


# ----------------------------------------------------------
def eta( a , b , do_print=False ):
    ab_avg , ab_diff = 0.5*(a+b) , [float(a[i]-b[i]) for i in range(len(a))]
    eta = [float(ab_diff[i])/ab_avg[i] if ab_avg[i]>0 else 0.01 for i in range(len(a))]
    eta_err = [np.sqrt(np.abs(ab_diff[i]))/ab_avg[i] if ab_avg[i]>0 else 0.01 for i in range(len(a))]
    if do_print:
        print 'eta:',eta
        print 'eta_err:',eta_err
    return np.array(eta) , np.array(eta_err)
# ----------------------------------------------------------

# ----------------------------------------------------------
def linear(x, slope, intercept):
    return slope * ( x ) + intercept
# ----------------------------------------------------------

# ----------------------------------------------------------
def linear_06(x, slope, intercept):
    return slope * ( x - 0.6 ) + intercept
# ----------------------------------------------------------


# ----------------------------------------------------------
def fit_as_a_function_of_pmiss( x , y , yerr, fit_type='const' , title='', x_offset=0.6 ):
    if fit_type=='const':
        p1,v1 = np.polyfit( x , y , 0 , cov=True)
        #         print 'const fit (%s) parameters:\n'%title,p1,'\n covariance:\n',v1
        return p1[0] , sqrt(v1[0][0])

    elif fit_type=='linear':
        if x_offset==0:
            f = linear
        else:
            f = linear_06
        p2, v2 = curve_fit(f, xdata=x, ydata=y,sigma=yerr)# fit data using SciPy's Levenberg-Marquart method

    print 'linear fit (%s)\n-----------\n parameters:\n'%title,p2,'\n covariance:\n',v2
    return p2[0] , sqrt(v2[0][0]) , p2[1] , sqrt(v2[1][1])
# ----------------------------------------------------------

# ----------------------------------------------------------
def fit_par_plot_pp_cm( data , var , weight , target='C12' ,
                       PmissOffset = 0.6,
                       title=None , do_plot_fit_pars=True , fontsize=25, figsize=(20,10),
                       do_save_fit=False):
    
    fig,ax=plt.subplots(figsize=figsize)
    ax.grid(True,linestyle='-',color='0.95')
    p_err = np.zeros(len(pmiss_bin_width))
    print target
    [Xfit,XfitErr] = plot_errorbar_and_fit_pp_cm( ax , Pmiss, data[ var + '_x_' + weight] ,
                                           [p_err,p_err] , [data[ var + '_xErr_' + weight ], data[ var + '_xErr_' + weight ]],
                                           'black','v','none',r'$x-direction$' ,'const',do_plot_fit_pars=do_plot_fit_pars)
        
    [Yfit,YfitErr] = plot_errorbar_and_fit_pp_cm( ax , Pmiss, data[ var + '_y_' + weight] ,
                                           [p_err,p_err] , [data[ var + '_yErr_' + weight ],data[ var + '_yErr_' + weight ]],
                                           'red'  ,'o','none',r'$y-direction$' ,'const',do_plot_fit_pars=do_plot_fit_pars)
    [Za1,Za1err],[Za2,Za2err] = plot_errorbar_and_fit_pp_cm( ax=ax , x=Pmiss, x_offset=PmissOffset, y=data[ var + '_z_' + weight] ,
                                                      xerr=[p_err,p_err] , yerr=data[ var + '_zErr_' + weight ],
                                                      color='blue' ,marker='s',lstyle='none',label=r'$\vec{p}_{miss}-direction$' ,fit_type='linear',
                                                      do_plot_fit_pars=do_plot_fit_pars)

    ax.legend(loc='best',fontsize=fontsize)
    set_axes(ax=ax,x_label='$p_{miss}$ [GeV/c]',y_label='c.m. momentum %s [Gev/c]'%title,fontsize=fontsize)
    if do_save_fit:
    
        plt.savefig('/Users/erezcohen/Desktop/DataMining/AccCorr_ppSRCAnalysisNote/all_figures/fits/%s_fit_%s.odf'%(target,var))

    return Xfit,XfitErr,Yfit,YfitErr,Za1,Za1err,Za2,Za2err
# ----------------------------------------------------------




# ----------------------------------------------------------
def plot_errorbar_and_fit_pp_cm( ax , x , y , xerr , yerr , color , marker , lstyle , label ,
                                fit_type='const' ,do_plot_fit_pars=False, x_offset=0):
    plt.errorbar(x, y, xerr=xerr, yerr=yerr, color=color, marker=marker , linestyle=lstyle , label=None , markersize=15)
    
    if fit_type=='const':
        const_fit , const_fitErr = fit_as_a_function_of_pmiss( x , y , yerr , fit_type , title=label)
        if do_plot_fit_pars: label=label + "$=%.3f\pm%.3f$"%(const_fit,const_fitErr)
        ax.plot(x, np.ones(len(x))*const_fit , color=color , linestyle='--', label=label,linewidth = 2 , )
        print 'const_fit:',const_fit,'+/-',const_fitErr
        return [ const_fit , const_fitErr ]
    
    elif fit_type=='linear':
        a1 , a1err , a2 , a2err  = fit_as_a_function_of_pmiss( x , y,  yerr , fit_type , title=label, x_offset=x_offset)
        if do_plot_fit_pars: label=label + "$=(%.3f)(p_{miss}-%.1f)+(%.3f)$"%( a1 , x_offset, a2 )
        ax.plot( x , a1*(x-x_offset) + a2 , color = color ,label=label )
        print label
        print 'a1:',a1,'+/-',a1err
        print 'a2:',a2,'+/-',a2err
        return [ a1 , a1err] , [ a2 , a2err ]
# ----------------------------------------------------------




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