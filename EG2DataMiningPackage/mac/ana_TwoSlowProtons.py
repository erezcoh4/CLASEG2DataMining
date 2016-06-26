import ROOT
import os, sys , math
from ROOT import TEG2dm , TPlots , TAnalysisEG2 , TSchemeDATA
from rootpy.interactive import wait
sys.path.insert(0, '/Users/erezcohen/larlite/UserDev/mySoftware/MySoftwarePackage/mac')
import GeneralPlot as gen_plot
import Initiation as init
#init.createnewdir()
#ROOT.gStyle.SetOptStat(0000)



Operation   = "Draw C12"
Var         = sys.argv[1] if len(sys.argv)>1 else "Xb"
p           = int(sys.argv[2]) if len(sys.argv)>2 else 0
cut         = ROOT.TCut("Xb>1.05")
Nbins       = 40
dm          = TEG2dm()
Path        = "/Users/erezcohen/Desktop/DataMining/AnaFiles"



print "Operation = " +Operation + ", Var = " + Var

# ------------------------------------------------------------------ #
if Operation == "Draw C12":
    ana = TAnalysisEG2("C12_TwoSlowProtons")
    if (Var=="Pcm"):
        plot_args = ["PcmFinalState.P()" , cut , Nbins , 0 , 1.5 , "|#vec{p} (c.m.)| [GeV/c]"]
    elif (Var=="Xb"):
        plot_args = [Var , cut , Nbins , 1 , 4 , "Bjorken x"]
    elif (Var=="q"):
        plot_args = ["q.P()" , "q.E()"  , cut , Nbins , 1.1 , 4 , Nbins , 0 , 3.1 ,"|#vec{q}| [GeV/c]" , "#omega [GeV]"]
    elif (Var=="Q2"):
        plot_args = [Var , cut , Nbins , 1 , 5 , "Q^{2} (GeV/c) ^{2}"]
    elif (Var=="Wtilde"):
        plot_args = ["Wtilde.Mag()" , cut , Nbins , -5 , 5 , "#sqrt{ W'^{#mu} W'_{#mu} } [GeV/c ^{2}]"]
    elif (Var=="Wtilde_vs_Q2"):
        plot_args = ["Wtilde.Mag()" ,"Q2" , cut , Nbins , -5 , 0 , Nbins , 1 , 5 ,"#sqrt{ W'^{#mu} W'_{#mu} } [GeV/c ^{2}]" , "Q^{2} (GeV/c) ^{2}"]
    elif (Var=="proton_3momentum"):
        p = int(input("which proton ? [ 1 / 2 ]"))
        plot_args = ["protons[%d].P()"%(p-1) , cut , Nbins , 0.27 , 0.73 ,"|#vec{p}(%d)| [GeV/c]"%p]
    elif (Var=="cos_opening_angle"):
        plot_args = [ str(ana.CosTheta("protons[0].Vect()","protons[1].Vect()")) , cut , Nbins , -1 , 1 , "cos (#theta_{12})"]
    elif (Var=="opening_angle"):
        plot_args = [ str(ana.Theta("protons[0].Vect()","protons[1].Vect()")) , cut , Nbins , -180 , 360 , "#theta_{12} [de.]"]
    elif (Var=="Mmiss"):
        plot_args = ["Pcm.Mag()", cut , Nbins , -3.5 , 2.1  , "#sqrt{|p^{#mu}_{1}+p^{#mu}_{2}-q^{#mu}|^{2}} [GeV/c ^{2}]"  ]
#        plot_args = ["PcmFinalState.Mag()", cut , Nbins , -2 , 5  , "#sqrt{|p^{#mu}_{1}+p^{#mu}_{2}|^{2}} [GeV/c ^{2}]"  ]

	print "ploting " + Var
	gen_plot.plot(ana,"TwoSlowProtons_"+Var,plot_args)


# ------------------------------------------------------------------ #
