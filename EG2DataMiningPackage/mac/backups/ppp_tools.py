from definitions import *
from my_tools import *
from cuts import *






def mix_ppp_events( ana3p ):
    file = ROOT.TFile("$DataMiningAnaFiles/Ana_Mixed_C12_Al27_Fe56_Pb28.root","recreate")
    tree = ROOT.TTree("anaTree","mixed pppSRC C12+Al27+Fe56+Pb28")
    ana3p.MixEvents(tree,False)
    tree.Write()
    file.Close()
    print 'done mixing....'


#ana_all = TAnalysisEG2("SRCPmissXb_NoCTofDATA_%s"% dm.Target(flags.atomic_mass) , ROOT.TCut(xB_cut))
#ana_ppp = TAnalysisEG2("pppSRCCut_NoCTofDATA_%s"% dm.Target(flags.atomic_mass) , ROOT.TCut(xB_cut) )
#variables = ['Xb'   ,'Pmiss.P()'    ,'Pmiss.Pt()'   ,'theta_pq'     ,'p_over_q' ]
#all_events = tree2array( ana_all.GetTree() , branches=variables , selection=None )
#all_ppp = tree2array( ana_all.GetTree() , branches=variables , selection='Np>=3' )
#ppp_src = tree2array( ana_ppp.GetTree() , branches=variables )


## ----------------------------------------
#def plot_distplot( x , bins , label , x_label ,  xmin , xmax ):
##    ax = plt.subplot(111)
#    g = sns.distplot( x , bins=bins, kde=False , label=label)
#    g.set_xlabel(x_label)
#    g.set( yscale="log" )
##    return g


#
## ----------------------------------------
#def plot_hist1d_ppp( df , var , x_label ):
#    
#    var_features = df.loc[df['var'] == var]
#    xmin,xmax = float(var_features.xmin),float(var_features.xmax)
#    bins = np.linspace(xmin,xmax,int(var_features.nbins))
#    fig = plt.figure(figsize = [10,8])
#    plot_distplot( all_events[var] , bins , 'all' , x_label , xmin , xmax )
#    plot_distplot( all_ppp[var]  , bins , 'all 3p' , x_label , xmin , xmax )
#    plot_distplot( ppp_src[var] , bins , 'ppp-candidates (%d)'%len(ppp_src) , x_label ,  xmin , xmax )
#    plt.legend()
#    fig.subplots_adjust(bottom=0.15)
#    plt.show()
#    plt.savefig( "/Users/erezcohen/Desktop/ppp_" + var + ".pdf" )
#
## ----------------------------------------
#def plot_hist2d_ppp( df , var_x , x_label , var_y , y_label ):
#    
#    varx_features = df.loc[df['var'] == var_x]
#    xmin,xmax = float(varx_features.xmin),float(varx_features.xmax)
#    binsx = np.linspace(xmin,xmax,int(varx_features.nbins))
#    vary_features = df.loc[df['var'] == var_y]
#    ymin,ymax = float(vary_features.xmin),float(vary_features.xmax)
#    binsy = np.linspace(ymin,ymax,int(vary_features.nbins))
#    fig = plt.figure(figsize = [10,8])
#    ax = plt.subplot(111)
#    plt.scatter(all_events[var_x], all_events[var_y] , label='all' , color='blue')
#    plt.scatter(all_ppp[var_x], all_ppp[var_y] , label='all 3p' , color='green')
#    plt.scatter(ppp_src[var_x], ppp_src[var_y] , label='ppp-candidates (%d)'%len(ppp_src) , color='red')
#    ax.set_xlim(xmin,xmax)
#    ax.set_ylim(ymin,ymax)
#    ax.set_xlabel(x_label)
#    ax.set_ylabel(y_label)
#    plt.show()
#    plt.savefig( "/Users/erezcohen/Desktop/ppp_" + var_x + "_vs_" + var_y + ".pdf" )
#
#
## ----------------------------------------
#def plot_variables_with_ppp_cuts( cuts_variables , xmins , xmaxs , nbins , x_labels  ):
#    
#    for var,xmin,xmax,nbins,x_label in zip(cuts_variables,xmins,xmaxs,nbins,x_labels):
#        plot_hist1d_ppp( var , xmin , xmax , nbins , x_label )
#


