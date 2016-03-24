import ROOT
from ROOT import TPlots
from ROOT import TAnalysisEG2
from rootpy.interactive import wait
ROOT.gStyle.SetOptStat(0000)



DoCuts              = False
DoCTOFsubtraction   = False
DoCount_p_2p_3p     = True



Nbins   = 50
ana     = TAnalysisEG2("NoCTofDATA_C12" , ROOT.TCut("1.05 <= Xb"))
cut     = ROOT.TCut()



if DoCuts:
    cSRC = ana.CreateCanvas("SRCcuts","Divide",3,4 )
    
    ana.Draw1DVarAndCut(cSRC , 1 , "Xb"         , Nbins , 1     , 2.5
                        , "Bjorken x"   ,"x" , ana.cutSRC , True )
                        
    ana.Draw1DVarAndCut(cSRC , 2 , "Pmiss.P()"  , Nbins , 0.2   , 1.1
                        , "#vec{p}(miss) = #vec{p}(lead) - #vec{q}","p(miss) [GeV/c]" , ana.cutSRC , True )
                        
    ana.Draw2DVarAndCut(cSRC , 3 , "p_over_q"  ,  "theta_pq"   , Nbins , 0.2   , 1  , Nbins , 0   , 50
                        , "p/q vs. #theta (p,q)" , "p/q" , "#theta (p,q) [deg.]" , ana.cutSRC )
                        
    ana.Draw2DVarAndCut(cSRC , 4 , "protons[1].P()"  ,  "protons[2].P()"   , Nbins , 0.2   , 1  , Nbins , 0.2   , 1
                                 , "recoil protons momenta" , "p(2) [GeV/c]" , "p(3) [GeV/c]" , ana.pppSRCCut )

    ana.Draw2DVarAndCut(cSRC , 5 , "pCTOF[1]"  ,  "pCTOF[2]"   , Nbins , -20   , 20  , Nbins , -20   , 20
                    , "recoil protons CTOF" , "CTOF p(2) [ns]" , "CTOF p(3) [ns]" , ana.pppSRCCut )
    
    
    ana.Draw2DVarAndCut(cSRC , 7 ,  "protons[0].P()"   , "pEdep[0]"  , Nbins , 0.2   , 2  , Nbins , 0   , 70
                                , "p(lead) Edep in TOF scintillators" , "proton momentum [GeV/c]" , "Edep [MeV]" , ana.pppSRCCut )
                                
    ana.Draw2DVarAndCut(cSRC , 8 ,  "protons[1].P()"   , "pEdep[1]"  , Nbins , 0.2   , 2  , Nbins , 0   , 70
                                , "p(2) Edep in TOF scintillators" , "proton momentum [GeV/c]" , "Edep [MeV]" , ana.pppSRCCut )
                     
    ana.Draw2DVarAndCut(cSRC , 9 ,  "protons[2].P()"   , "pEdep[2]"  , Nbins , 0.2   , 2  , Nbins , 0   , 70
                                    , "p(3) Edep in TOF scintillators" , "proton momentum [GeV/c]" , "Edep [MeV]" , ana.pppSRCCut )
                                    
    ana.Draw1DVarAndCut(cSRC , 10 , "pVertex[0].Z()"  , Nbins , -34   , -20
                                    , "leading proton vertex" , "(p vertex)^{z} [cm]" , ana.pppSRCCut )
                                    
    ana.Draw1DVarAndCut(cSRC , 11 , "pVertex[1].Z()"  , Nbins , -34   , -20
                                  , "proton 2 vertex" , "(p vertex)^{z} [cm]" , ana.pppSRCCut )
                                                    
    ana.Draw1DVarAndCut(cSRC , 12 , "pVertex[2].Z()"  , Nbins , -34   , -20
                                  , "proton 3 vertex" , "(p vertex)^{z} [cm]" , ana.pppSRCCut )
                                                
    cSRC.Update()
    wait()



if DoCTOFsubtraction:
    cCTOF = ana.CreateCanvas( "cCTOF" )
#    cut = ana.pppEdepCut 
    hCTOF23 = ana.H2( "pCTOF[1]"  ,  "pCTOF[2]"  , cut , "colz" , Nbins , -20   , 20  , Nbins , -20   , 20
           , "recoil protons CTOF" , "CTOF p(2) [ns]" , "CTOF p(3) [ns]" )
    x = ana.SubtractBackground(hCTOF23,  4 , 16 , True)
    x.Print()
    cCTOF.Update()
    wait()

if DoCount_p_2p_3p:
    ana.PrintInCuts()
