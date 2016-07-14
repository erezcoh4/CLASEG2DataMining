import ROOT ,os, sys , math
from ROOT import TEG2dm , TPlots , TAnalysisEG2 , TSchemeDATA
from rootpy.interactive import wait
sys.path.insert(0, '/Users/erezcohen/larlite/UserDev/mySoftware/MySoftwarePackage/mac')
import GeneralPlot as gen_plot
import Initiation as init
#init.createnewdir()
#ROOT.gStyle.SetOptStat(0000)



Operation   = "diff.samples"
Var         = sys.argv[1] if len(sys.argv)>1 else "Xb"
Nbins       = 40
dm          = TEG2dm()
Path        = "/Users/erezcohen/Desktop/DataMining/AnaFiles"



print "looking at sample of ?pp events, operation = " +Operation + ", Var = " + Var

XbCut = ROOT.TCut("Xb>1.05")
    
DataType = int(input("Data Type? \n( FullCandidates-1 / C12_TwoSlowProtons-2 / C12_TwoSlowProtons_ppp-3 / C12_TwoSlowProtons_npp-4 / no_physics-5 ):\n > "))
Data  = sys.argv[2] if len(sys.argv)>2 else "C12_TwoSlowProtons"
if (DataType == 1):
    DataName = "C12_Al27_Fe56_Pb28"
    ana = TAnalysisEG2(DataName,XbCut) # two recoilong protons + from our sample of candidates
    cut = ana.pppSRCCut
elif (DataType == 2):
    DataName = "C12_TwoSlowProtons"
    ana = TAnalysisEG2(DataName,XbCut) # two slow protons + nothing else
    cut = XbCut
elif (DataType == 3):
    DataName = "C12_TwoSlowProtons_ppp"
    ana = TAnalysisEG2(DataName,XbCut) # two slow protons + additional fast proton (>1. GeV/c)
    cut = ROOT.TCut("Xb>1.05 && TMath::RadToDeg()*PmRctLab3.Theta()<45")
elif (DataType == 4):
    DataName = "C12_TwoSlowProtons_npp"
    ana = TAnalysisEG2(DataName,XbCut) # two slow protons + additional fast proton (>1. GeV/c)
    cut = XbCut
elif (DataType == 5):
    DataName = "GSIM_run0091_eep"
    ana = TAnalysisEG2(DataName,XbCut) # two slow protons from synthetic data of candidates + 2 random protons
    cut = ana.Sim3pSRCCut




# ------------------------------------------------------------------ #
if Operation == "diff.samples":
 
    if (Var=="Pcm"):
        if (DataType == 2):
            plot_args = ["PcmFinalState.P()" , cut , Nbins , 0 , 1.5 , "|#vec{p} (c.m.)| [GeV/c]"]
        else:
            plot_args = ["Prec.P()" , cut , Nbins , 0 , 1.5 , "|#vec{p} (c.m.)| [GeV/c]"]
    elif (Var=="PmissRctAngle"):
        plot_args = ["TMath::RadToDeg()*PmRctLab3.Theta()" , cut , Nbins , 0 , 180 , "#theta(#vec{q} - #vec{p}_{1} - #vec{p}_{2})"]
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
    elif (Var=="WmissWithCm"):
        plot_args = ["WmissWithCm.Mag()" , cut , Nbins , -3 , 3 , "#sqrt{ |(3M_{N},#vec{k}_{cm}) + q - p_{1} - p_{2}|^{2} } [GeV/c ^{2}]"]
    elif (Var=="WmissCmEps"):
        plot_args = ["WmissCmEps.Mag()" , cut , Nbins , -3 , 3 , "#sqrt{ |(3M_{N}-#varepsilon,#vec{k}_{cm}) + q - p_{1} - p_{2}|^{2} } [GeV/c ^{2}]"]
    elif (Var=="WmissVsAngles"):
        plot_args = ["Wmiss.Mag()","(TMath::RadToDeg()*Prec.Theta())",cut,Nbins,-3,3, Nbins,0,180,"#sqrt{|3M_{N} + q - p_{1} - p_{2}|^{2} } [GeV/c ^{2}]", "#theta(#vec{p}_{1} + #vec{p}_{2})"]
    

    gen_plot.plot(ana,"slow2p_"+DataName+"_"+Var,plot_args)
# ------------------------------------------------------------------ #



# ------------------------------------------------------------------ #
elif Operation == "Xb":
    c = ana.CreateCanvas("Xb")
    h = ana.H1("Xb",cut,"hist",40,1,4,"","Bjorken x")
    LargeXfrac = h.Integral( h.GetXaxis().FindBin(2) , h.GetXaxis().GetNbins() ) / h.Integral()
    ana.Text( 1.6 , 0.5*h.GetMaximum() , "%.2f%% w/ x>2"%(100.*LargeXfrac) )
    c.Update()
    wait()
    c.SaveAs(init.dirname()+"/"+DataName+"_xB.pdf")
# ------------------------------------------------------------------ #



