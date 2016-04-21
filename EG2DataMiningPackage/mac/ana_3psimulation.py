import sys , ROOT
from ROOT import TPlots , TAnalysis , TAnalysisEG2
from rootpy.interactive import wait
sys.path.insert(0, '/Users/erezcohen/larlite/UserDev/mySoftware/MySoftwarePackage/mac')
import Initiation as init
init.createnewdir()
ROOT.gStyle.SetOptStat(0000)


DoAllVariables  = True

Var         = "pp_scattering_CMtheta_vs_Mpp"
Path        = "/Users/erezcohen/Desktop/DataMining/AnaFiles"
analysis    = TAnalysis()
Nbins       = 100
XbMin       = 1.05
XbCut       = ROOT.TCut("%f <= Xb"%XbMin)
ana         = TAnalysisEG2("FSI3pSimulation", XbCut )


# April - 07
if DoAllVariables:
    
    cSRC = ana.CreateCanvas("canvas", "Divide" , 1 , 1 )
    if (Var=="q_vs_omega"):
        ana.H2("q.P()" , "q.E()" , ROOT.TCut() , "colz" , 100 , 0 , 5 , 100 , 0 , 4 , "","|#vec{q}| [GeV/c]","#omega [GeV]")
    elif (Var=="Xb"):
        ana.Draw1DVarAndCut(cSRC , 1 , Var         , Nbins , 1     , 2.5  , "Bjorken x"   ,"Bjorken x" , ana.cutSRC , True  , "SRC")
    elif (Var=="Pmiss"):
        ana.Draw1DVarAndCut(cSRC , 2 , "Pmiss.P()"  , Nbins , 0     , 2.5
                            , "#vec{p}(miss) = #vec{p}(lead) - #vec{q}"   ,"p(miss) [GeV/c]" , ana.cutSRC)
    elif (Var=="PoverQ_vs_ThetaPQ"):
        ana.Draw2DVarAndCut(cSRC , 3 , "p_over_q"  ,  "theta_pq"   , Nbins , 0.6   , 1.1  , Nbins , 0   , 50
                                        , "p/q vs. #theta (p,q)" , "p/q" , "#theta (p,q) [deg.]" , ana.cutSRC , True  , "SRC")
    elif (Var=="RecoilProtons"):
        ana.Draw2DVarAndCut(cSRC , 4 , "protons[1].P()"  ,  "protons[2].P()"   , Nbins , 0.2   , 1  , Nbins , 0.2   , 1
                                    , "recoil protons momenta" , "p(2) [GeV/c]" , "p(3) [GeV/c]" , ana.Sim3pSRCCut , True  , "3pSRC")
    elif (Var=="theta_vs_phi"):
        ana.Draw2DVarAndCut(cSRC , 5 , "fabs(phiMiss23)" , "thetaMiss23"   , Nbins , 0 , 80 , Nbins , 80 , 180
                        ,"#phi vs. #theta - FSI simulation","|#phi| [deg.]","#theta [deg.]" , ana.Sim3pSRCCut )
    elif (Var=="pp_scattering_CMtheta_vs_Mpp"):
        ana.H2("Mpp" , "(180/3.1415)*Theta_cm" , ROOT.TCut() ,"surf2" , Nbins , 1.9 , 4.2 , Nbins , 0 , 180
           ,"#theta vs. #sqrt{s}","m(pp) [GeV/c^{2}]","#theta [deg.]" )




    cSRC.Update()
    wait()
    cSRC.SaveAs(init.dirname()+"/FSI3p_sim_"+Var+".pdf")






