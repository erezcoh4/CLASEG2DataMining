import ROOT
import os, sys
from ROOT import TEG2dm
from ROOT import TPlots
from ROOT import TAnalysisEG2
from rootpy.interactive import wait
ROOT.gStyle.SetOptStat(0000)



DoCuts              = False
DoCTOFsubtraction   = False
DoCount_p_2p_3p     = False
DoCombineTargets    = True
DoGenCombinedFile   = False


A       = 208
Nbins   = 50
XbMin   = 1.05
XbCut   = ROOT.TCut("%f <= Xb"%XbMin)
dm      = TEG2dm()
ana     = TAnalysisEG2("NoCTofDATA_%s"% dm.Target(A), XbCut )
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


if DoCombineTargets:
    if DoGenCombinedFile:
        if ( int(input("re-create the merged file (all targets together): [0-no/ 1-yes]")) == 1 ):
            os.system("rm %s/Ana_C12_Fe56_Pb28.root"%ana.GetPath())
            anaAll  = [TAnalysisEG2("NoCTofDATA_C12",XbCut) , TAnalysisEG2("NoCTofDATA_Fe56",XbCut) , TAnalysisEG2("NoCTofDATA_Pb208",XbCut)]
            os.system("hadd %s/Ana_C12_Fe56_Pb28.root %s %s %s"%(ana.GetPath() , anaAll[0].GetFileName() , anaAll[1].GetFileName() , anaAll[2].GetFileName() ))
    anaEG2  = TAnalysisEG2("C12_Fe56_Pb28",XbCut)
    cSRC = anaEG2.CreateCanvas("All targets together","Divide",2,2 )
    cSRC.cd(1)
    anaEG2.H1("Pcm.P()" , anaEG2.pppSRCCut , "BAR E" , 20 , 0 , 1.1, "c.m. momentum - stacked ^{12}C ^{56}Fe ^{208}Pb","|#vec{p}(c.m.)| [GeV/c]")
#    anaEG2.Draw1DVarAndCut(cSRC , 1 , "Pcm.P()" , Nbins , 0 , 1.5, "c.m. momentum - stacked ^{12}C ^{56}Fe ^{208}Pb","|#vec{p}(c.m.)| [GeV/c]" , anaEG2.pppSRCCut , True , "SRC")
    cSRC.cd(2)
    anaEG2.H2("fabs(phiMiss23)" , "thetaMiss23" , anaEG2.pppSRCCut , "" , Nbins , 0 , 80 , Nbins , 80 , 180 , "#phi vs. #theta - stacked  ^{12}C ^{56}Fe ^{208}Pb","|#phi| [deg.]","#theta [deg.]")
    cSRC.Update()
    wait()


