import ROOT , sys
from ROOT import TPlots , TAnalysis , TAnalysisEG2
from rootpy.interactive import wait
ROOT.gStyle.SetOptStat(0000)


DoAllVariables  = True

Path        = "/Users/erezcohen/Desktop/DataMining/AnaFiles"
analysis    = TAnalysis()
Nbins       = 25
XbMin       = 1.05
XbCut       = ROOT.TCut("%f <= Xb"%XbMin)
#ana         = TPlots(Path+"/FSI3pSimulation.root", "anaTree" , "" )
ana         = TAnalysisEG2("FSI3pSimulation", XbCut )


# April - 07
if DoAllVariables:
    
    cSRC = ana.CreateCanvas("canvas", "Divide" , 2 , 2)
    
#    cSRC.cd(1)
#    ana.Draw2DVarAndCut(cSRC , 1 , "q.P()"      ,"q.E()" ,Nbins ,1  ,3.5    ,Nbins  ,0  ,3
#                        , "virtual photon","q [GeV/c]","#omega [GeV]", ana.Sim3pSRCCut , True )

    ana.Draw1DVarAndCut(cSRC , 1 , "Xb"         , Nbins , 1     , 2.5  , "Bjorken x"   ,"x" , ana.Sim3pSRCCut , True )
       
    ana.Draw1DVarAndCut(cSRC , 2 , "Pmiss.P()"  , Nbins , 0     , 2.5
                        , "#vec{p}(miss) = #vec{p}(lead) - #vec{q}"   ,"p(miss) [GeV/c]" , ana.Sim3pSRCCut , True )

    ana.Draw2DVarAndCut(cSRC , 3 , "p_over_q"  ,  "theta_pq"   , Nbins , 0.2   , 1  , Nbins , 0   , 50
                                            , "p/q vs. #theta (p,q)" , "p/q" , "#theta (p,q) [deg.]" , ana.cutSRC , True )
                        
    ana.Draw2DVarAndCut(cSRC , 4 , "protons[1].P()"  ,  "protons[2].P()"   , Nbins , 0.2   , 1  , Nbins , 0.2   , 1
                                            , "recoil protons momenta" , "p(2) [GeV/c]" , "p(3) [GeV/c]" , ana.Sim3pSRCCut , True )
                        
    cSRC.Update()
    wait()
    cSRC.SaveAs("~/Desktop/ana_3p_simulation.pdf")






