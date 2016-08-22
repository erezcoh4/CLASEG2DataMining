import ROOT ,os, sys , math
from ROOT import TEG2dm , TPlots , TAnalysisEG2 , TSchemeDATA
from rootpy.interactive import wait
sys.path.insert(0, '../../mySoftware/MySoftwarePackage/mac')
import GeneralPlot as gp , Initiation as init



Operation   = "diff.samples"
Var         = sys.argv[1] if len(sys.argv)>1 else "Xb"
Nbins       = 50
dm          = TEG2dm()
Path        = "/Users/erezcohen/Desktop/DataMining/AnaFiles"



print "looking at sample of ?pp events, operation = " +Operation + ", Var = " + Var
XbCut = ROOT.TCut("Xb>0 && (0.938*0.938 + 2*0.938*q.E() - Q2)<1.5")




    
DataType = int(input("Data Type? \n( FullCandidates-1 / C12_TwoSlowProtons-2 / C12_TwoSlowProtons_ppp-3 / C12_TwoSlowProtons_npp-4 / no_physics-5 ):\n > "))

Data  = sys.argv[2] if len(sys.argv)>2 else "C12_TwoSlowProtons"
if (DataType == 1):
    DataName = "C12_Al27_Fe56_Pb28"
    ana = TAnalysisEG2(DataName,XbCut) # two recoilong protons + from our sample of candidates
    cut = ana.pppSRCCut
elif (DataType == 2):
    DataName = "C12_TwoSlowProtons"
    ana = TAnalysisEG2(DataName,XbCut) # two slow protons + nothing else
    cut = XbCut
elif (DataType == 3):
    DataName = "C12_TwoSlowProtons_ppp"
    ana = TAnalysisEG2(DataName,XbCut) # two slow protons + additional fast proton (>1. GeV/c)
    cut = XbCut #&& TMath::RadToDeg()*PmRctLab3.Theta()<45")
elif (DataType == 4):
    DataName = "C12_TwoSlowProtons_npp"
    ana = TAnalysisEG2(DataName,XbCut) # two slow protons + additional fast proton (>1. GeV/c)
    cut = XbCut
elif (DataType == 5):
    DataName = "GSIM_run0091_eep"
    ana = TAnalysisEG2(DataName,XbCut) # two slow protons from synthetic data of candidates + 2 random protons
    cut = ana.Sim3pWmissCut #    cut = ana.Sim3pSRCCut





# ------------------------------------------------------------------ #
if Operation == "diff.samples":
 
    if (Var=="Pcm"):
        if (DataType == 2):
            plot_args = ["PcmFinalState.P()" , cut , Nbins , 0 , 1.5 , gp.PcmTit]
        else:
            plot_args = ["Prec.P()" , cut , Nbins , 0 , 1.5 , gp.PcmTit]
    elif (Var=="PmissRctAngle"):
        plot_args = ["TMath::RadToDeg()*PmRctLab3.Theta()" , cut , Nbins , 0 , 180 , gp.ThetaPrctTit]
    elif (Var=="Xb"):
        plot_args = [Var , cut , Nbins , 1 , 4 , gp.XbTit]
    elif (Var=="q"):
        plot_args = ["q.P()" , "q.E()"  , cut , Nbins , 1.1 , 4 , Nbins , 0 , 3.1 ,"|#vec{q}| [GeV/c]" , "#omega [GeV]"]
    elif (Var=="Q2"):
        plot_args = [Var , cut , Nbins , 1 , 5 , gp.Q2Tit]
    elif (Var=="p3momenta"):
        plot_args = ["protons[1].P()" ,"protons[2].P()" , cut , Nbins , 0.27 , 0.73 , Nbins , 0.27 , 0.73 ,gp.pTit(1) ,gp.pTit(2)]
    elif (Var=="cos_opening_angle"):
        plot_args = [ str(ana.CosTheta("protons[1].Vect()","protons[2].Vect()")) , cut , Nbins , -1 , 1 , gp.cosThetaTit("12")]

    elif (Var=="opening_angle"):
        if (DataType == 2):
            plot_args = [ str(ana.Theta("protons[0].Vect()","protons[1].Vect()")) , cut , Nbins , 0 , 180 , gp.ThetaTit("12")]
        else:
            plot_args = [ str(ana.Theta("protons[1].Vect()","protons[2].Vect()")) , cut , Nbins , 0 , 180 , gp.ThetaTit("12")]

    elif (Var=="Wmiss"):
        plot_args = ["Wmiss.Mag()" , cut , Nbins , -3 , 3 , gp.WmissTit]

    elif (Var=="WmissWithCm"):
        plot_args = ["WmissWithCm.Mag()" , cut , Nbins , -3 , 3 , gp.WmCmTit]

    elif (Var=="WmissCmEps"):
        plot_args = ["WmissCmEps.Mag()" , cut , Nbins , -3 , 3 , gp.WmEpsTit]

    elif (Var=="WmissVsAngles"):
        plot_args = ["Wmiss.Mag()","(TMath::RadToDeg()*Prec.Theta())",cut,Nbins,-3,3, Nbins,0,180,gp.WmissTit, gp.ThetaPrecTit
                     ]
    elif (Var=="PmissQ"):
        plot_args = ["Xb","fabs(Plead.Pz()-q.Pz())",cut,Nbins,1,2,Nbins,-.5,1,gp.XbTit,gp.PmqTit]

    elif (Var=="PrecQ"):
        plot_args = ["Xb","fabs(Prec.Pz())",cut,Nbins,1,2,Nbins,0,1,gp.XbTit,gp.PrecqTit]

    elif (Var=="PrecPmiss"):
        plot_args = ["Prec.Pz()","Pmiss.Pz()",cut,Nbins,-2,2,Nbins,-2,2,gp.PmqTit,gp.PrecqTit]

    elif (Var=="XbVsWmiss"):
        plot_args = ["Xb","Wmiss.Mag()",cut,200,0,3,200,-2,4,gp.XbTit,gp.WmissTit]

    elif (Var=="XbVsPrec_q"):
        plot_args = ["Xb","Prec.Pz()",cut,Nbins,0,2,Nbins,-0.5,0.8,gp.XbTit,gp.PrecqTit]

    elif (Var=="XbVsPcm"):
        plot_args = ["Xb","PcmFinalState.P()",cut,100,0,3,100,0,2,gp.XbTit,"(recoling protons)  " + gp.PcmTit]

    elif (Var=="XbVsProtonsAngle"):
        plot_args = ["Xb","(TMath::RadToDeg()*PcmFinalState.Theta())",cut,100,0,3,100,0,180,gp.XbTit,gp.ThetaPrecTit]
    
    elif (Var=="XbVsMcm"):
        plot_args = ["Xb","-Pcm.Mag()",cut,200,0,2.8,200,-2,4.8,gp.XbTit,gp.qp1p2Tit]


    elif (Var=="XbVsWe"):
        plot_args = ["Xb","0.938*0.938 + 2*0.938*q.E() - Q2",cut,200,0,2.8,200,-2,9,gp.XbTit,gp.We2Tit]



    elif (Var=="XbVsWseely"):
        plot_args = ["Xb","((q.E()+0.938)**2 - q.P()**2)",cut,200,0,2.8,200,-2,9,gp.XbTit,gp.Wseely2Tit]
    
    
    elif (Var=="XbVs_op_angle"):
        if (DataType == 2):
#            plot_args = ["Xb",str(ana.Theta("protons[0].Vect()","protons[1].Vect()")) , cut ,200,0,2.8,Nbins,0,180,gp.XbTit,gp.ThetaTit("12")]
            plot_args = ["Xb","TMath::RadToDeg()*thetaLeadRec" , cut ,200,0,2.8,200,0,180,gp.XbTit,gp.ThetaTit("12")]
        else:
            plot_args = ["Xb",str(ana.Theta("protons[1].Vect()","protons[2].Vect()")) , cut ,200,0,2.8,Nbins,0,180,gp.XbTit,gp.ThetaTit("12")]



    gp.plot(ana,"slow2p_"+DataName+"_"+Var,plot_args)
# ------------------------------------------------------------------ #



# ------------------------------------------------------------------ #
elif Operation == "Xb":
    
    if (Var=="op_angle"):
        Xaxis = ["TMath::RadToDeg()*thetaLeadRec" , 0 , 180 , gp.ThetaTit("12") ]
    elif (Var=="Prec_q"):
        Xaxis = ["Prec.Pz()" , -0.4 , 0.8 , gp.PrecqTit ]

    
    c = ana.CreateCanvas("Xb")
    XbMin = [ 0.0 , 0.2 , 0.5 , 0.8 , 1.0 , 1.2 , 1.4 , 1.6 , 1.8 , 2.0 ]
    Labels = []
    h = []
    for i in range(0,8):
        h.append(ana.H1(Xaxis[0] ,ROOT.TCut("%f < Xb && Xb < %f"%(XbMin[i],XbMin[i+1])),"hist same"
                        ,Nbins,Xaxis[1],Xaxis[2],"",Xaxis[3] , "" , i+1 , 0 ))
        h[i].Scale(1./h[i].GetEntries())
        h[i].SetName("%.1f < x_{B} < %.1f"%(XbMin[i],XbMin[i+1]))
        h[i].GetYaxis().SetRangeUser(0,1)
    c.BuildLegend()
    c.Update()
    wait()
    c.SaveAs(init.dirname()+"/"+DataName+"_xB.pdf")
# ------------------------------------------------------------------ #



