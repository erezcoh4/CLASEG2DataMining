import sys
import ROOT
from ROOT import TPlots
from ROOT import TAnalysis
from rootpy.interactive import wait
ROOT.gStyle.SetOptStat(0000)


DoAllVariables  = True
Nbins           = 100

Path        = "/Users/erezcohen/Desktop/DataMining/AnaFiles"
analysis    = TAnalysis()
ana         = TPlots(Path+"/FSI3pSimulation.root", "anaTree" , "" )


# April - 04
if DoAllVariables:
    
    c = ana.CreateCanvas("canvas", "Divide" , 1 , 1)
    
    c.cd(1)
    ana.H2("q.P()","q.E()",ROOT.TCut(),"colz",Nbins,1,3.5,Nbins,0,3,"virtual photon","q [GeV/c]","#omega [GeV]")
    

    c.Update()
    wait()
    c.SaveAs("~/Desktop/ana_3p_simulation.pdf")






