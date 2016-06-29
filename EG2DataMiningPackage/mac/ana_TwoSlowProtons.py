import ROOT ,os, sys , math
from ROOT import TEG2dm , TPlots , TAnalysisEG2 , TSchemeDATA
from rootpy.interactive import wait
sys.path.insert(0, '/Users/erezcohen/larlite/UserDev/mySoftware/MySoftwarePackage/mac')
import GeneralPlot as gen_plot
import Initiation as init
#init.createnewdir()
#ROOT.gStyle.SetOptStat(0000)



Operation   = "compare different samples"
Var         = sys.argv[1] if len(sys.argv)>1 else "Xb"
Nbins       = 40
dm          = TEG2dm()
Path        = "/Users/erezcohen/Desktop/DataMining/AnaFiles"



print "looking at sample of ?pp events, operation = " +Operation + ", Var = " + Var



# ------------------------------------------------------------------ #
if Operation == "compare different samples":
 
    XbCut = ROOT.TCut("Xb>1.05")
    
    DataType = int(input("Data Type? (C12_TwoSlowProtons / FullCandidates / C12_TwoSlowProtons_ppp / no_physics)"))
    Data  = sys.argv[2] if len(sys.argv)>2 else "C12_TwoSlowProtons"
    if (Data == "FullCandidates"):
        ana = TAnalysisEG2("C12_Al27_Fe56_Pb28",XbCut) # two recoilong protons + from our sample of candidates
        cut = ana.pppSRCCut
    elif (Data == "C12_TwoSlowProtons"):
        ana = TAnalysisEG2("C12_TwoSlowProtons",XbCut) # two slow protons + nothing else
        cut = XbCut
    elif (Data == "C12_TwoSlowProtons_ppp"):
        ana = TAnalysisEG2("C12_TwoSlowProtons_ppp",XbCut) # two slow protons + additional fast proton (>1. GeV/c)
        cut = XbCut
    elif (Data == "no_physics"):
        ana = TAnalysisEG2("GSIM_run0091_eep",XbCut) # two slow protons from synthetic data of candidates + 2 random protons
        cut = ana.Sim3pSRCCut



    if (Var=="Pcm"):
        if (Data == "C12_TwoSlowProtons"):
            plot_args = ["PcmFinalState.P()" , cut , Nbins , 0 , 1.5 , "|#vec{p} (c.m.)| [GeV/c]"]
        else:
            plot_args = ["Prec.P()" , cut , Nbins , 0 , 1.5 , "|#vec{p} (c.m.)| [GeV/c]"]
    elif (Var=="Xb"):
        plot_args = [Var , cut , Nbins , 1 , 4 , "Bjorken x"]
    elif (Var=="q"):
        plot_args = ["q.P()" , "q.E()"  , cut , Nbins , 1.1 , 4 , Nbins , 0 , 3.1 ,"|#vec{q}| [GeV/c]" , "#omega [GeV]"]
    elif (Var=="Q2"):
        plot_args = [Var , cut , Nbins , 1 , 5 , "Q^{2} (GeV/c) ^{2}"]
    elif (Var=="p3momenta"):
        plot_args = ["protons[1].P()" ,"protons[2].P()" , cut , Nbins , 0.27 , 0.73 , Nbins , 0.27 , 0.73 ,"|#vec{p}(1)| [GeV/c]" , "|#vec{p}(2)| [GeV/c]"]
    elif (Var=="cos_opening_angle"):
        plot_args = [ str(ana.CosTheta("protons[1].Vect()","protons[2].Vect()")) , cut , Nbins , -1 , 1 , "cos (#theta_{12})"]
    elif (Var=="opening_angle"):
        plot_args = [ str(ana.Theta("protons[1].Vect()","protons[2].Vect()")) , cut , Nbins , 0 , 180 , "#theta_{12} [deg.]"]
    elif (Var=="Wmiss"):
        plot_args = ["Wmiss.Mag()" , cut , Nbins , -3 , 3 , "#sqrt{ |3M_{N} + q - p_{1} - p_{2}|^{2} } [GeV/c ^{2}]"]


    print "ploting " + Var
    gen_plot.plot(ana,"slowProtons_"+Data+"_"+Var,plot_args)


# ------------------------------------------------------------------ #



