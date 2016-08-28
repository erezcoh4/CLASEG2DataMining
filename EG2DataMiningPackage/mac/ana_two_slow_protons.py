'''
    usage:
    --------
    > python mac/ana_two_slow_protons.py -A12 -werez --DataType=New_NoCTofDATA_C12_TwoSlowProtons --option="Xb vs. recoil LC"
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
XbMin       = 1.
cut         = flags.cut + ROOT.TCut("((0.938*0.938 + 2*0.938*q.E() - Q2)<2 && Xb>%f && PcmFinalState.Pt() < 0.4)"%XbMin)
ana         = TAnalysisEG2( flags.DataType , cut )



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
    
    



    c = gp.plot(ana,"slow2p_"+flags.DataType+"_"+Var,plot_args)
    wait()
    c.SaveAs(init.dirname()+"/"+flags.DataType+"_"+Var+".pdf")

# ------------------------------------------------------------------ #




# ------------------------------------------------------------------ #
elif flags.option == "Xb vs. Preq q":
    
    
    
    c = ana.CreateCanvas(flags.option)
    ana.H2("Xb","protons[0].Pz() + protons[1].Pz()",cut,"colz",Nbins,0.9*XbMin,2.5,Nbins,-0.2,1.4,"",gp.XbTit,"#vec{p}_{1}#hat{q} + #vec{p}_{2}#hat{q}")
    ana.Line(1,0,2,1,1,2)
    ana.Text(1.8,0.5,"#vec{p}_{rec}#hat{q} = -#vec{p}_{miss}#hat{q} = x_{B}+1")
    ana.Text(1.8,0.3,"#pm 0.2GeV/c c.m.")
    ana.Line(1,0-0.2,2,1-0.2,1,2,2)
    ana.Line(1,0+0.2,2,1+0.2,1,2,2)

    
    c.Update()
    wait()
    c.SaveAs(init.dirname()+"/"+flags.DataType+"_Prec_q_vs_Xb.pdf")


# ------------------------------------------------------------------ #



# ------------------------------------------------------------------ #
elif flags.option == "Xb vs. recoil LC":
    
    
    
    c = ana.CreateCanvas(flags.option)
    ana.H2("Xb","alpha[0] + alpha[1]",cut,"colz",Nbins,0.9*XbMin,2.5,Nbins,1.,2.6,"",gp.XbTit, gp.alphaTit("p_{1}") + " + " + gp.alphaTit("p_{2}")  )
#    ana.Line(1,0,2,1,1,2)
#    ana.Text(1.8,0.5,"#vec{p}_{rec}#hat{q} = -#vec{p}_{miss}#hat{q} = x_{B}+1")
#    ana.Text(1.8,0.3,"#pm 0.2GeV/c c.m.")
#    ana.Line(1,0-0.2,2,1-0.2,1,2,2)
#    ana.Line(1,0+0.2,2,1+0.2,1,2,2)

    
    c.Update()
    wait()
    c.SaveAs(init.dirname()+"/"+flags.DataType+"_Prec_q_vs_Xb.pdf")


# ------------------------------------------------------------------ #



# ------------------------------------------------------------------ #
elif flags.option == "protons angles":



    c = ana.CreateCanvas("protons angles","Divide",2,1)
    for i in range(2):
        c.cd(i+1)
        ana.H2("Xb","proton_angle[%d]"%i,cut,"colz",100,0,2,100,0,180,"",gp.XbTit,gp.ThetaTit("#vec{p}(%d),#vec{q}"%(i+1)))



    c.Update()
    wait()
    c.SaveAs(init.dirname()+"/"+flags.DataType+"_protons_angles_to_q.pdf")


# ------------------------------------------------------------------ #
