# run:
# > python mac/ana_ppp.py <target A>

import ROOT
import os, sys , math
import os.path
from ROOT import TEG2dm , TPlots , TAnalysisEG2 , TSchemeDATA
from rootpy.interactive import wait
sys.path.insert(0, '/Users/erezcohen/larlite/UserDev/mySoftware/MySoftwarePackage/mac')
import Initiation as init
init.createnewdir()
ROOT.gStyle.SetOptStat(0000)


# "Draw variable"/ "Show SRC Cuts" / "CTOF subtraction" / "count e,e'p/pp/ppp"  / "combine targets"/ "Mix events" / "Draw" / "elastic x=1" / "DataVsMix" / "generate (e,e'p)+pp for GSIM" / "3p events for random forest"

Operation   = "Draw"
DataType    = "Data" # "FSI-3 Simulation" / "Data" / "NoPhysics3p" / "Mixed" / "RandomBkg"
Var         = sys.argv[1] if len(sys.argv)>1 else "Xb"
Nbins       = 40
XbMin       = 1.05
cut         = ROOT.TCut()
XbCut       = ROOT.TCut("%f <= Xb"%XbMin)
dm          = TEG2dm()
scheme      = TSchemeDATA()
Path        = "/Users/erezcohen/Desktop/DataMining/AnaFiles"


# ------------------------------------------------------------------ #
if len(sys.argv)>1 and Operation == "Draw variable":
    A   = int(sys.argv[1])
    ana = TAnalysisEG2("NoCTofDATA_%s"% dm.Target(A), XbCut )
    
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
# ------------------------------------------------------------------ #

# ------------------------------------------------------------------ #
elif Operation == "Show SRC Cuts":
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
# ------------------------------------------------------------------ #

# ------------------------------------------------------------------ #
elif Operation == "CTOF subtraction":
    cCTOF = ana.CreateCanvas( "cCTOF" )
#    cut = ana.pppEdepCut 
    hCTOF23 = ana.H2( "pCTOF[1]"  ,  "pCTOF[2]"  , cut , "colz" , Nbins , -20   , 20  , Nbins , -20   , 20
           , "recoil protons CTOF" , "CTOF p(2) [ns]" , "CTOF p(3) [ns]" )
    x = ana.SubtractBackground(hCTOF23,  4 , 16 , True)
    x.Print()
    cCTOF.Update()
    wait()
# ------------------------------------------------------------------ #

# ------------------------------------------------------------------ #
elif len(sys.argv)>1 and Operation == "count e,e'p/pp/ppp":
    ana.PrintInCuts()
# ------------------------------------------------------------------ #

# ------------------------------------------------------------------ #
elif Operation == "combine targets":
    if ( int(input("re-create the merged file (all targets together): [0-no/ 1-yes]")) == 1 ):
        os.system("rm $DataMiningAnaFiles/Ana_C12_Al27_Fe56_Pb28.root")
        anaAll  = [TAnalysisEG2("NoCTofDATA_C12",XbCut) , TAnalysisEG2("NoCTofDATA_Al27",XbCut) , TAnalysisEG2("NoCTofDATA_Fe56",XbCut) , TAnalysisEG2("NoCTofDATA_Pb208",XbCut)]
        os.system("hadd $DataMiningAnaFiles/Ana_C12_Al27_Fe56_Pb28.root %s %s %s %s"%(anaAll[0].GetFileName() , anaAll[1].GetFileName() , anaAll[2].GetFileName() , anaAll[3].GetFileName() ))
# ------------------------------------------------------------------ #

# ------------------------------------------------------------------ #
elif Operation == "Mix events":
    scheme = TSchemeDATA()
    anaEG2 = TAnalysisEG2("C12_Al27_Fe56_Pb28",XbCut)
    if ( int(input("re-mix (all targets together): [0-no/ 1-yes]")) == 1 ):
        scheme.SchemeOnTCut("$DataMiningAnaFiles", "Ana_C12_Al27_Fe56_Pb28.root", "anaTree", "Ana_3p_C12_Al27_Fe56_Pb28.root", anaEG2.pppCut)
        ana3p = TAnalysisEG2("3p_C12_Al27_Fe56_Pb28",XbCut)
        file = ROOT.TFile("$DataMiningAnaFiles/Ana_Mixed_C12_Al27_Fe56_Pb28.root","recreate")
        tree = ROOT.TTree("anaTree","mixed 3p C12+Al27+Fe56+Pb28")
        ana3p.MixEvents(tree,False)
        tree.Write()
        file.Close()
        print 'done mixing....'
# ------------------------------------------------------------------ #

# ------------------------------------------------------------------ #
elif Operation == "Draw":


    if DataType == "Data":
        anaDat = TAnalysisEG2("C12_Al27_Fe56_Pb28",XbCut)
        anaEG2 = [anaDat , anaDat.pppCutPmTMm , anaDat.Final3pCut] 
    elif DataType == "FSI3_Simulation":
        anaSim = TAnalysisEG2("GSIM_run0088_eep",XbCut)
        anaEG2 = [anaSim , anaSim.Sim3pSRCCut , anaSim.FinalSim3pSRCCut]
    elif DataType == "NoPhysics3p":
        anaGSM = TAnalysisEG2("GSIM_run0091_eep",XbCut)
        anaEG2 = [anaGSM , anaGSM.Sim3pSRCCut , anaGSM.FinalSim3pSRCCut]
    elif DataType == "Mixed":
        anaMix = TAnalysisEG2("Mixed_C12_Al27_Fe56_Pb28",XbCut)
        anaEG2 = [anaMix , anaMix.Mix3pSRCCut , anaMix.FinalMix3pSRCCut]
    elif DataType == "RandomBkg":
        anaDat = TAnalysisEG2("C12_Al27_Fe56_Pb28",XbCut)
        anaEG2 = [anaDat , anaDat.pppRandomBkg , anaDat.Final3pCut]

    c = anaEG2[0].CreateCanvas(DataType)


    if (Var=="pMiss_p2_p3"):
        hp2 = anaEG2[0].H2("Pmiss.P()" , "protons[1].P()", anaEG2[1] ,"" , Nbins , 0.25 , 1.1 , Nbins , 0.25 , 1.1
                     ,"","|#bf{p}(miss)| [GeV/c]","recoil protons momenta [GeV/c]" , 3 , 20 , 1 , 0.8)
        hp3 = anaEG2[0].H2("Pmiss.P()" , "protons[2].P()", anaEG2[1] ,"same" , Nbins , 0.25 , 1.1 , Nbins , 0.25 , 1.1
                                ,"","|#bf{p}(miss)| [GeV/c]","recoil protons momenta [GeV/c]" , 4 ,  20 , 1 , 0.8)
        anaEG2[0].AddLegend(hp2,"p(2)",hp3,"p(3)")


    elif (Var=="DalitzPlot"):
#        anaEG2[0].Dalitz("protons[1].P()","protons[2].P()","Pmiss.P()",anaEG2[1],1000,-1.7,1.7,1000,-1.1,2,"p_{2}","p_{3}","p_{miss}","",1) # "Modified" Dalitz plot since T is not conserved
        anaEG2[0].Dalitz("protons[1].P()","protons[2].P()","Pmiss.P()",anaEG2[2],50,-1.7,1.7,50,-1.1,2,"p_{2}","p_{3}","p_{miss}","col",4,True)


    else:
        if (Var=="Pcm"):
            xAxis = ["Pcm.P()" , 0 , 2, "| #vec{p} (c.m.) | [GeV/c]"]
 
        elif (Var=="theta_Pcm_q"):
            xAxis = [anaEG2[0].Theta("Pcm.Vect()","q.Vect()") , 0 , 360 , "#theta(q,p(c.m.)) [deg.]"]
        
        
        elif (Var=="RecoilingProtonsOpeningAngle"):
            xAxis = [anaEG2[0].CosTheta("protons[1].Vect()","protons[2].Vect()") , -1 , 1 , "cos(#theta_{23})"]
                
        elif (Var=="Np"):
            xAxis = [Var , 0 , 4 , "numebr of reconstruncted protons"]
            anaEG2[1] = ROOT.TCut("100./%f"%anaEG2[0].GetEntries())

        elif (Var=="Tp" or Var=="TpMiss"):
            xAxis = [Var , 0 , 2 , "T(p) [GeV]"]

        elif (Var=="Pmiss"):
            xAxis = ["Pmiss.P()" , 0.2 , 1.1 , "|#vec{p} (miss)| [GeV/c]"]

        elif (Var=="PmT"):
            xAxis = ["Pmiss.Pt()" , 0.2 , 1.1 , "#vec{p} (miss) - T [GeV/c]"]

        elif (Var=="TransversePmiss"):
            xAxis = ["Pmiss.Pt()" , 0.0 , 2. , "#vec{p} (miss) - #perp [GeV/c]"]

        elif (Var=="PtSquared"):
            xAxis = ["Pmiss.Pt()*Pmiss.Pt()" , 0.0 , 3. , "(#vec{p} (miss) _{#perp})^{2} [GeV/c]"]
        
        elif (Var=="Xb"):
            xAxis = [Var , 0.9 , 2, "Bjorken x"]
            anaEG2[1] = anaEG2[0].eepFinalCut

        elif (Var=="phi"):
            xAxis = ["fabs(phiMiss23)" , 0 , 90, "|#phi| [deg.]"]
        
        elif (Var=="Mmiss"):
            xAxis = ["Pcm.Mag()" , 0 , 6, "#sqrt{|p^{#mu}_{lead}+p^{#mu}_{2}+p^{#mu}_{3}-q^{#mu}|^{2}} [GeV/c ^{2}]"]
        
        
        elif (Var=="Mmiss23"):
            xAxis = ["Prec.Mag()" , 1.8 , 4.1, "#sqrt{|p^{#mu}_{2}+p^{#mu}_{3}|^{2}} [GeV/c ^{2}]"]

        
        elif (Var=="XbMoving"):
            xAxis = [Var , 0 , 10, "Bjorken x' (moving nucleon)"]
        
        
        elif (Var=="opening_angle"):
            xAxis = [anaEG2[0].CosTheta("Pmiss.Vect()","Prec.Vect()") , -1 , 1, "cos (#theta)"]
        
        elif (Var=="cmEvsP"):
                xyAxes = ["Pcm.E()" , "Pcm.P()" , 2 , 5.8 , 0 , 2.7 , "p^{0}_{lead}+p^{0}_{2}+p^{0}_{3}-q^{0} [GeV]" , "|p^{i}_{lead}+p^{i}_{2}+p^{i}_{3}-q^{i}| [GeV/c]" ]
        

        elif (Var=="MmissVsPmiss"):
            xyAxes = ["Pcm.Mag()" , "Pmiss.P()" , -2 , 5 , 0 , 2 , "#sqrt{|p^{#mu}_{lead}+p^{#mu}_{2}+p^{#mu}_{3}-q^{#mu}|^{2}} [GeV/c ^{2}]" , "|p_{miss}| [GeV/c]" ]
        
        
        elif (Var=="MmissVsMmiss23"):
            xyAxes = ["Pcm.Mag()" , "Prec.Mag()" , 2 , 5 , 1.8 , 4.1 , "#sqrt{|p^{#mu}_{lead}+p^{#mu}_{2}+p^{#mu}_{3}-q^{#mu}|^{2}} [GeV/c ^{2}]" , "#sqrt{|p^{#mu}_{2}+p^{#mu}_{3}|^{2}} [GeV/c ^{2}]" ]
        
        
        elif (Var=="MmissVsXb"):
            xyAxes = ["Pcm.Mag()" , "Xb" , -2 , 5 , 0 , 2 , "#sqrt{|p^{#mu}_{lead}+p^{#mu}_{2}+p^{#mu}_{3}-q^{#mu}|^{2}} [GeV/c ^{2}]" , "Bjorken x" ]
            

        elif (Var=="PmissTransversalLongitudinal"):
            xyAxes = ["Pmiss.Pt()" , "Pmiss.Pz()" , 0 , 1 , -1 , 1 , "|#vec{p} (miss)|-T [GeV/c]" , "|#vec{p} (miss)|-L [GeV/c]" ]
        
        elif (Var=="theta_vs_phi"):
            xyAxes = ["fabs(phiMiss23)" , "thetaMiss23" , 0 , 80 , 80 , 180 , "|#phi| [deg.]","#theta [deg.]" ]

        elif (Var=="Pcm_vs_theta_Pcm_q"):
            xyAxes = ["Pcm.P()",anaEG2[0].CosTheta("Pcm.Vect()","q.Vect()") , 0 , 1 , -1 , 1 , "|#vec{p} (c.m.)| [GeV/c]", "cos(#theta(q,p(c.m.)))"]


        elif (Var=="Pcm_vs_PmT"):
            xyAxes = ["Pcm.P()","Pmiss.Pt()" , 0 , 1 , 0 , 0.7 , "|#vec{p} (c.m.)| [GeV/c]", "|#vec{p} (miss)|-T [GeV/c]"]
        

        if 'xAxis' in locals():
            anaEG2[0].H1(xAxis[0] , anaEG2[1] , "hist" , Nbins , xAxis[1] , xAxis[2] , "" ,xAxis[3] , "" ,38)
#            anaEG2[0].H1(xAxis[0] , anaEG2[2] , "hist same" , Nbins , xAxis[1] , xAxis[2] , "" ,xAxis[3] , "" ,1,1)

        elif 'xyAxes' in locals():
                
            anaEG2[0].H2(xyAxes[0] , xyAxes[1], anaEG2[1] , "" , Nbins , xyAxes[2] , xyAxes[3], Nbins , xyAxes[4] , xyAxes[5] , "" ,xyAxes[6] , xyAxes[7] , 1, 20 , 3 )
#            anaEG2[0].H2(xyAxes[0] , xyAxes[1], ROOT.TCut("%s && Pcm.P()<0.3"%anaEG2[1]) , "same" , Nbins , xyAxes[2] , xyAxes[3], Nbins , xyAxes[4] , xyAxes[5] , "" ,xyAxes[6] , xyAxes[7] , 4, 21 , 2 )

    c.Update()
    wait()
    c.SaveAs(init.dirname()+"/"+DataType+Var+".pdf")
# ------------------------------------------------------------------ #


# ------------------------------------------------------------------ #
elif Operation == "DataVsMix":
    anaData= TAnalysisEG2("C12_Al27_Fe56_Pb28",XbCut)
    anaMix = TAnalysisEG2("Mixed_C12_Al27_Fe56_Pb28",XbCut)
    c = anaData.CreateCanvas(DataType)
    
    if (Var=="phi"):
        xAxis = ["fabs(phiMiss23)" , 0 , 90, "|#phi| [deg.]"]
    
    elif (Var=="opening_angle"):
        xAxis = [anaData.CosTheta("Pmiss.Vect()","Prec.Vect()") , -1 , 1, "cos (#theta)"]


    if 'xAxis' in locals():
        hData= anaData.H1(xAxis[0] , anaData.pppCut , "hist" , Nbins , xAxis[1] , xAxis[2] , "" ,xAxis[3] , "" ,38)
        hMix = anaMix.H1(xAxis[0] , anaMix.Mix3pSRCCut , "hist same" , Nbins , xAxis[1] , xAxis[2] , "" ,xAxis[3] , "" , 2 , 0 , 2)
        hMix.Scale(float(hData.GetEntries())/hMix.GetEntries())


    c.Update()
    wait()
    c.SaveAs(init.dirname()+"/DataVsMix_"+Var+".pdf")
# ------------------------------------------------------------------ #

# ------------------------------------------------------------------ #
elif Operation == "elastic x=1":
    
    XbCut   = ROOT.TCut("0.95 < Xb && Xb < 1.05")
#    XbCut   = ROOT.TCut("1.05 < Xb")
    ana     = TAnalysisEG2("C12_Al27_Fe56_Pb28",XbCut)
    cut     = ana.pppSRCCut


    c = ana.CreateCanvas(Var)

    if (Var=="pMiss_p2_p3"):
        hp2 = ana.H2("Pmiss.P()" , "protons[1].P()", cut ,"" , Nbins , 0.25 , 1.1 , Nbins , 0.25 , 1.1
                       ,"","|#bf{p}(miss)| [GeV/c]","recoil protons momenta [GeV/c]" , 3 , 20 , 1 , 0.8)
        hp3 = ana.H2("Pmiss.P()" , "protons[2].P()", cut ,"same" , Nbins , 0.25 , 1.1 , Nbins , 0.25 , 1.1
                           ,"","|#bf{p}(miss)| [GeV/c]","recoil protons momenta [GeV/c]" , 4 ,  20 , 1 , 0.8)
        ana.AddLegend(hp2,"p(2)",hp3,"p(3)")
            
            
    elif (Var=="DalitzPlot"):
        ana.Dalitz("protons[1].P()","protons[2].P()","Pmiss.P()",cut,1000,-1.7,1.7,1000,-1.1,2,"p_{2}","p_{3}","p_{miss}","",1,True)



    else:
        
        if (Var=="Xb"):
            xAxis = [Var , 0.8 , 1.2, "Bjorken x"]
        
        elif (Var=="PmissTransversalLongitudinal"):
            xyAxes = ["Pcm.Pt()" , "Pcm.Pz()" , 0 , 1 , -1 , 1 , "|#vec{p} (miss)|-T [GeV/c]" , "|#vec{p} (miss)|-L [GeV/c]" ]
        
        if 'xAxis' in locals():
            ana.H1(xAxis[0] , cut , "hist" , Nbins , xAxis[1] , xAxis[2] , "" ,xAxis[3] , "" ,38)
        elif 'xyAxes' in locals():
            ana.H2(xyAxes[0] , xyAxes[1], ana.cutSRCNoPm , "" , Nbins , xyAxes[2] , xyAxes[3], Nbins , xyAxes[4] , xyAxes[5] , "" ,xyAxes[6] , xyAxes[7] , 1, 20 , 1 )
#            ana.H2(xyAxes[0] , xyAxes[1], ana.Final3pCut , "same" , Nbins , xyAxes[2] , xyAxes[3], Nbins , xyAxes[4] , xyAxes[5] , "" ,xyAxes[6] , xyAxes[7] , 4, 21 , 1 )

    c.Update()
    wait()
    c.SaveAs(init.dirname()+"/elastic_x1_C12_Al_27_Fe56_Pb28_"+Var+".pdf")
# ------------------------------------------------------------------ #



# ------------------------------------------------------------------ #
elif Operation == "generate (e,e'p)+pp for GSIM":
    ana     = TAnalysisEG2("C12_Al27_Fe56_Pb28",XbCut)
    scheme.SchemeOnTCut( Path, "Ana_C12_Al27_Fe56_Pb28.root", "anaTree", "Ana_C12_Al27_Fe56_Pb28_eep.root", ana.eepFinalCut) # eepFinalCut = cutXb && cutThetaPQ && cutPoverQ && cutPmiss && cutPmT
    ana     = TAnalysisEG2("C12_Al27_Fe56_Pb28_eep",XbCut)
    outfile = open(Path+"/eep_pp_events.txt", "wb")
    h = ROOT.TH2F("hMmiss","M(miss), recoiling protons momenta 0.3-0.5 GeV/c ; recoiling protons generated momentum [GeV/c] ; M(miss) [GeV/c ^{2}]",100,0.25,0.75,100,0,8)

    
    for i in range(0,int(1.*ana.GetEntries())):
        if (i%1000==0):
            print "[%.2f%%]"%(100.*i/ana.GetEntries())
        for j in range (0,10): # for each (e,e'p) event generate 10 (e,e'ppp) events
            evt = ana.GetGSIMeep_pp_Evt(i,False)
            rec_2p_momentum = evt.at(evt.size()-2)
            Mmiss = evt.at(evt.size()-1)
            h.Fill(rec_2p_momentum,Mmiss)
            if Mmiss<(3.*0.938): # consider only events which crossed the Mmiss cut (?)
                outfile.write("%d\n" % evt.at(0))
                for j in range(0,4):
                    outfile.write("%d  %f  %f  %f  %f \n" % (evt.at(1+11*j) , evt.at(2+11*j) , evt.at(3+11*j) , evt.at(4+11*j), evt.at(5+11*j)))
                    outfile.write("%f  %d \n" % (evt.at(6+11*j) , evt.at(7+11*j)))
                    outfile.write("%d  %d  %d  %d  %d \n" % (evt.at(8+11*j) , evt.at(9+11*j) , evt.at(10+11*j) , evt.at(11+11*j) , evt.at(11+11*j)))
    outfile.close()
    print "\ndone writing %d events to "%ana.GetEntries(ROOT.TCut()) + outfile.name
    c = ana.CreateCanvas("Mmiss")
    h.Draw("colz")
    ana.Line(0.25,2.814,0.75,2.814,2,3)
    c.Update()
    wait()
    c.SaveAs(init.dirname()+"/Mmiss_eep_pp.pdf")
# ------------------------------------------------------------------ #




# ------------------------------------------------------------------ #
# write all (e,e'ppp) events to a txt file without applying any kinematical cuts! for Random forest search of special events...
elif Operation == "3p events for random forest":
    ana     = TAnalysisEG2("C12_Al27_Fe56_Pb28",XbCut)
    A = 12
    if (os.path.isfile(Path+"/Ana_C12_Al27_Fe56_Pb28_pppSRC.root") == False):
        scheme.SchemeOnTCut( Path, "Ana_C12_Al27_Fe56_Pb28.root", "anaTree", "Ana_C12_Al27_Fe56_Pb28_pppSRC.root",ana.pppSRCCut )
    ana = TAnalysisEG2("C12_Al27_Fe56_Pb28_pppSRC")
    outfile = open(Path+"/%s_Full_ppp_events.txt"%dm.Target(A), "wb")
    for i in range(0,int(ana.GetEntries())):
        evt = ana.GetFullpppEvent(i,False)
        outfile.write("%d" % i)
        for v in range (0,evt.size()):
            outfile.write("\t%f" % evt.at(v))
        outfile.write("\n")
    outfile.close()
    print "\ndone writing %d events to "%ana.GetEntries() + outfile.name
# ------------------------------------------------------------------ #





