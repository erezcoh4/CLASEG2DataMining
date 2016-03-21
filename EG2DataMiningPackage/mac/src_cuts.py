import ROOT
from ROOT import TPlots
from ROOT import TAnalysisEG2
from rootpy.interactive import wait
ROOT.gStyle.SetOptStat(0000)


Nbins       = 50
DoXb        = False
DoPmiss     = False
DoThetaPQ   = True
DoPoverQ    = True
DopVertex   = True



ana     = TAnalysisEG2("DATA_C12")
cut     = ROOT.TCut()

if DoXb:
    c = ana.CreateCanvas("xb")
    ana.H1("Xb",cut,"HIST",Nbins,1.0,2.0,"Bjorken scaling","Bjorken x")
    wait()

if DoPmiss:
    c = ana.CreateCanvas("pmiss")
    ana.H1("Pmiss.P()",cut,"HIST",Nbins,0.2,1.1 ,"#vec{p}(miss) = #vec{p}(lead) -#vec{q}","|#vec{p}(miss) [GeV/c]")
    wait()



if DoThetaPQ:
    c = ana.CreateCanvas("theta_pq vs p_over_q")
    ana.H2("p_over_q","theta_pq",cut,"colz",Nbins,0,2,Nbins,-1,181
           ,"#vec{p}(lead) -#vec{q} angle vs. |#vec{p}(lead)| / #vec{q}|","|#vec{p}(lead)| / #vec{q}|","#theta(p_{lead},q) [deg.]")
    wait()

