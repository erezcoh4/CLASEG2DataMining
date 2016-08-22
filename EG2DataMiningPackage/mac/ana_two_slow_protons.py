'''
    usage:
    --------
    > python mac/ana_two_slow_protons.py -A12 -werez --option="diff.samples" --cut="Xb>0" --DataType="New_NoCTofDATA_C12_TwoSlowProtons"
'''

import ROOT ,os, sys , math
from ROOT import TEG2dm , TPlots , TAnalysisEG2 , TSchemeDATA
from rootpy.interactive import wait
sys.path.insert(0, '../../mySoftware/MySoftwarePackage/mac')
import GeneralPlot as gp, Initiation as init , input_flags
init.createnewdir()
flags = input_flags.get_args()




Nbins       = flags.Nbins
Var         = flags.variable
dm          = TEG2dm()

ana         = TAnalysisEG2( flags.DataType , flags.cut )
cut         = flags.cut



#    
#DataType = int(input("Data Type? \n( FullCandidates-1 / C12_TwoSlowProtons-2 / C12_TwoSlowProtons_ppp-3 / C12_TwoSlowProtons_npp-4 / no_physics-5 ):\n > "))
#
#Data  = sys.argv[2] if len(sys.argv)>2 else "C12_TwoSlowProtons"
#if (DataType == 1):
#    DataName = "C12_Al27_Fe56_Pb28"
#    ana = TAnalysisEG2(DataName,XbCut) # two recoilong protons + from our sample of candidates
#    cut = ana.pppSRCCut
#elif (DataType == 2):
#    DataName = "C12_TwoSlowProtons"
#    ana = TAnalysisEG2(DataName,XbCut) # two slow protons + nothing else
#    cut = XbCut
#elif (DataType == 3):
#    DataName = "C12_TwoSlowProtons_ppp"
#    ana = TAnalysisEG2(DataName,XbCut) # two slow protons + additional fast proton (>1. GeV/c)
#    cut = XbCut #&& TMath::RadToDeg()*PmRctLab3.Theta()<45")
#elif (DataType == 4):
#    DataName = "C12_TwoSlowProtons_npp"
#    ana = TAnalysisEG2(DataName,XbCut) # two slow protons + additional fast proton (>1. GeV/c)
#    cut = XbCut
#elif (DataType == 5):
#    DataName = "GSIM_run0091_eep"
#    ana = TAnalysisEG2(DataName,XbCut) # two slow protons from synthetic data of candidates + 2 random protons
#    cut = ana.Sim3pWmissCut #    cut = ana.Sim3pSRCCut
#
#



# ------------------------------------------------------------------ #
if flags.option == "diff. samples":
 
 
    if (Var=="PmissQ"):
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
        plot_args = ["Xb","(0.938*0.938 + 2*0.938*q.E() - Q2)",cut,200,0,2.8,200,-2,9,gp.XbTit,gp.We2Tit]



    elif (Var=="XbVsWseely"):
        plot_args = ["Xb","((q.E()+0.938)**2 - q.P()**2)",cut,200,0,2.8,200,-2,9,gp.XbTit,gp.Wseely2Tit]
    
    
    elif (Var=="XbVs_op_angle"):
        if "NoCTof" in flags.DataType:
            plot_args = ["Xb","TMath::RadToDeg()*thetaLeadRec" , cut ,200,0,2.8,200,0,180,gp.XbTit,gp.ThetaTit("12")]
        else:
            plot_args = ["Xb",str(ana.Theta("protons[1].Vect()","protons[2].Vect()")) , cut ,200,0,2.8,Nbins,0,180,gp.XbTit,gp.ThetaTit("12")]



    c = gp.plot(ana,"slow2p_"+flags.DataType+"_"+Var,plot_args)
    wait()
    c.SaveAs(init.dirname()+"/"+flags.DataType+"_"+Var+".pdf")

# ------------------------------------------------------------------ #






# ------------------------------------------------------------------ #
elif flags.option == "protons angles":



    c = ana.CreateCanvas("protons angles","Divide",2,1)
    for i in range(2):
        c.cd(i+1)
        ana.H2("Xb","proton_angle[%d]"%i,cut,"colz",100,0,2,100,0,180,"","Bjorken x",gp.ThetaTit("#vec{p}(%d),#vec{q}"%(i+1)))



    c.Update()
    wait()
    c.SaveAs(init.dirname()+"/"+flags.DataType+"_protons_angles_to_q.pdf")


# ------------------------------------------------------------------ #
