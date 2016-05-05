# run:
# > python mac/ana_ppp.py <target A>

import ROOT
import os, sys , math
from ROOT import TEG2dm , TPlots , TAnalysisEG2
from rootpy.interactive import wait
sys.path.insert(0, '/Users/erezcohen/larlite/UserDev/mySoftware/MySoftwarePackage/mac')
import Initiation as init
init.createnewdir()
ROOT.gStyle.SetOptStat(0000)



DoDrawVar           = False
DoCuts              = False
DoCTOFsubtraction   = False
DoCount_p_2p_3p     = False
DoGenCombinedFile   = False
DoCombineTargets    = True

Var     = "DalitzPlot"
Nbins   = 50
XbMin   = 1.05
cut     = ROOT.TCut()
XbCut   = ROOT.TCut("%f <= Xb"%XbMin)
dm      = TEG2dm()
if len(sys.argv)>1:
    A   = int(sys.argv[1])
    ana = TAnalysisEG2("NoCTofDATA_%s"% dm.Target(A), XbCut )



if len(sys.argv)>1 and DoDrawVar:
    c = ana.CreateCanvas(Var)
    cut = ROOT.TCut()
    if (Var=="XbMoving"):
        xAxis = [0 , 2, "Bjorken x' (moving nucleon)"]
    elif (Var=="Q2"):
        xAxis = [0 , 4 , "Q ^{2} (GeV/c) ^{2}"]
    elif (Var=="Xb"):
        xAxis = [0.8 , 2 , "Bjorken x"]
    ana.H1(Var , ana.cut1pSRC , "BAR E" , Nbins , xAxis[0] , xAxis[1] , "" , xAxis[2] )
    ana.H1(Var , ana.ppSRCCut , "BAR E same" , Nbins , xAxis[0] , xAxis[1] , "" , xAxis[2] , "", 2 , 2 )
    ana.H1(Var , ana.pppSRCCut , "BAR E same" , Nbins , xAxis[0] , xAxis[1] , "" , xAxis[2] , "" , 3 , 3)
    c.Update()
    wait()
    c.SaveAs(init.dirname()+"/%s"%dm.Target(A)+"_"+Var+".pdf")


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

if DoGenCombinedFile:
    if ( int(input("re-create the merged file (all targets together): [0-no/ 1-yes]")) == 1 ):
        os.system("rm $DataMiningAnaFiles/Ana_C12_Al27_Fe56_Pb28.root")
        anaAll  = [TAnalysisEG2("NoCTofDATA_C12",XbCut) , TAnalysisEG2("NoCTofDATA_Al27",XbCut) , TAnalysisEG2("NoCTofDATA_Fe56",XbCut) , TAnalysisEG2("NoCTofDATA_Pb208",XbCut)]
        os.system("hadd $DataMiningAnaFiles/Ana_C12_Al27_Fe56_Pb28.root %s %s %s %s"%(anaAll[0].GetFileName() , anaAll[1].GetFileName() , anaAll[2].GetFileName() , anaAll[3].GetFileName() ))

if DoCombineTargets:
    anaEG2  = TAnalysisEG2("C12_Al27_Fe56_Pb28",XbCut)
    c = anaEG2.CreateCanvas("All targets together")
    if (Var=="theta_vs_phi"):
        anaEG2.H2("fabs(phiMiss23)" , "thetaMiss23" , anaEG2.pppSRCCut , "" , Nbins , 0 , 80 , Nbins , 80 , 180 , "","|#phi| [deg.]","#theta [deg.]",4,20,0.5)
        anaEG2.Box(0,155,15,180,1,0.1)
        evts = anaEG2.GetEntries(anaEG2.pppSRCCut)
        evtsErr = math.sqrt(evts)
        print "%d +/- %d events"%(evts,evtsErr)
        evts_in_box = anaEG2.GetEntries(anaEG2.Final3pCut)
        evts_in_boxErr = math.sqrt(evts_in_box)
        print "%d +/- %d events in box"%(evts_in_box,evts_in_boxErr)
        percentage = 100*(float(evts_in_box)/evts)
        percentageErr = percentage*math.sqrt( math.pow(evtsErr/evts,2) +  math.pow(evts_in_boxErr/evts_in_box,2))
        anaEG2.Text(20,160,"%d events (%.1f #pm %.1f %%)"%(evts_in_box , percentage , percentageErr))
    elif (Var=="pMiss_p2_p3"):
        hp2 = anaEG2.H2("Pmiss.P()" , "protons[1].P()", anaEG2.pppSRCCut ,"" , Nbins , 0.25 , 1.1 , Nbins , 0.25 , 1.1
                     ,"","|#bf{p}(miss)| [GeV/c]","recoil protons momenta [GeV/c]" , 3 , 20 , 1 , 0.8)
        hp3 = anaEG2.H2("Pmiss.P()" , "protons[2].P()", anaEG2.pppSRCCut ,"same" , Nbins , 0.25 , 1.1 , Nbins , 0.25 , 1.1
                                ,"","|#bf{p}(miss)| [GeV/c]","recoil protons momenta [GeV/c]" , 4 ,  20 , 1 , 0.8)
        anaEG2.AddLegend(hp2,"p(2)",hp3,"p(3)")
    elif (Var=="DalitzPlot"):
        anaEG2.Dalitz("Tp[0]","Tp[1]","Tp[2]",ROOT.TCut("Np==3"));

    else:
        if (Var=="Pcm"):
            xAxis = ["Pcm.P()" , 0 , 1.4, "| #vec{p} (c.m.) | [GeV/c]"]
        elif (Var=="Tp" or Var=="TpMiss"):
            xAxis = [Var , 0 , 2 , "T(p) [GeV]"]
        elif (Var=="Xb"):
            xAxis = [Var , 1 , 2, "Bjorken x"]
        elif (Var=="XbMoving"):
            xAxis = [Var , 0 , 2, "Bjorken x' (moving nucleon)"]
        elif (Var=="opening_angle"):
            xAxis = [anaEG2.CosTheta("Pmiss.Vect()","Prec.Vect()") , -1 , 1, "cos (#theta)"]
        anaEG2.H1(xAxis[0] , anaEG2.pppSRCCut , "BAR E" , Nbins , xAxis[1] , xAxis[2] , "",xAxis[3])
        anaEG2.H1(xAxis[0] , anaEG2.Final3pCut , "BAR E same" , Nbins , xAxis[1] , xAxis[2] , "",xAxis[3],"",1,1)

    c.Update()
    wait()
    c.SaveAs(init.dirname()+"/C12_Al_27_Fe56_Pb28_"+Var+".pdf")

