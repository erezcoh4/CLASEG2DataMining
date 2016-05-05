import ROOT
from ROOT import TPlots
from rootpy.interactive import wait
import time
ROOT.gStyle.SetOptStat(0000)


Do_inclusive_q    = True


Path        = "/Users/erezcohen/Desktop/DataMining/EG2_DATA"
FileName    = "DATA_C12"
ana         = TPlots(Path + "/"+FileName+".root","T","inclusive")

if Do_inclusive_q:
    XbMin = 1.05
    cEv = ana.CreateCanvas("omega vs q")
    file = ROOT.TFile("~/Desktop/DataMining/EG2_DATA/inclusive_q.root","recreate")
    h2 = ana.H2("q","Nu",ROOT.TCut("Xb>%f"%XbMin),"colz",100,1,3.5,100,0.4,2.2,"#omega vs. q","|q| [GeV/c]","#omega [GeV]")
    cEv.Update()
    wait()
    cEv.SaveAs("~/Desktop/inclusive_q.pdf")
    h2.SetName("h_inclusive_q")
    h2.Write()
    file.Close()

