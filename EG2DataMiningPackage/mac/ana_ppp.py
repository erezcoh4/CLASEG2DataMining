import ROOT
from ROOT import TPlots
from ROOT import TAnalysisEG2
from rootpy.interactive import wait
ROOT.gStyle.SetOptStat(0000)



DoCuts      = True





Nbins   = 50
ana     = TAnalysisEG2("NoCTofDATA_C12")
cut     = ROOT.TCut()



if DoCuts:
    cSRC = ana.CreateCanvas("SRCcuts","DivideSquare",4)
    
    ana.Draw1DVarAndCut(cSRC , 1 , "Xb"         , Nbins , 1     , 2.5
                        , "Bjorken x"   ,"x" , ana.cutSRC , True )
                        
    ana.Draw1DVarAndCut(cSRC , 2 , "Pmiss.P()"  , Nbins , 0.2   , 1.1
                        , "#vec{p}(miss) = #vec{p}(lead) - #vec{q}","p(miss) [GeV/c]" , ana.cutSRC , True )
                        
    ana.Draw2DVarAndCut(cSRC , 3 , "p_over_q"  ,  "theta_pq"   , Nbins , 0.2   , 1  , Nbins , 0   , 50
                        , "p/q vs. #theta (p,q)" , "p/q" , "#theta (p,q) [deg.]" , ana.cutSRC )
    #ADD :
    # prec(2) vs. prec(3) with both cut on >0.3
    # CTOF p1
    # CTOF p2 vs. CTOF p3
    # Edep p1, Edep p2 , Edep p3
    
    wait()

