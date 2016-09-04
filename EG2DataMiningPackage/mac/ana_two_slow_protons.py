'''
    usage:
    --------
    python mac/ana_two_slow_protons.py -A12 --DataType=New_NoCTofDATA_C12_TwoSlowProtons --option="DIS/correlation in alpha12:Xb" -var=DIS_and_correlation
'''

import ROOT ,os, sys , math
from ROOT import TEG2dm , TPlots , TAnalysisEG2 , TSchemeDATA
from rootpy.interactive import wait
sys.path.insert(0, '../../mySoftware/MySoftwarePackage/mac')
import GeneralPlot as gp, Initiation as init , input_flags
from root_numpy import root2array, tree2array , hist2array
from matplotlib import pyplot as plt

init.createnewdir()
flags = input_flags.get_args()




Nbins       = flags.Nbins
Var         = flags.variable
dm          = TEG2dm()
XbMin       = 0.8
cut         = flags.cut + ROOT.TCut("((0.938*0.938 + 2*0.938*q.E() - Q2)<2 && Xb>%f && PcmFinalState.Pt() < 2.4)"%XbMin)
ana         = TAnalysisEG2( flags.DataType , cut )
pppCandidats= TAnalysisEG2( "C12_Al27_Fe56_Pb28" , cut )



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
    pppCandidats.H2("Xb","alpha[1] + alpha[2]",pppCandidats.pppSRCCut,"same",Nbins,0.9*XbMin,2.5,Nbins,1.,2.6,"",gp.XbTit, gp.alphaTit("p_{1}") + " + " + gp.alphaTit("p_{2}") , 1 , 21 , 1  )
    c.Update()
    wait()
    c.SaveAs(init.dirname()+"/"+flags.DataType+"_Prec_q_vs_Xb.pdf")

#    T  = tree2array(ana.GetTree(),branches=['Xb','alpha[0]+alpha[1]'])
#    X , Y , labels = T['Xb'],T['alpha[0]+alpha[1]'],[ '$x_{B}$' , '$\\alpha(p_{1}) + \\alpha(p_{2})$']
#    fig = gp.sns2d_with_projections( X , Y , labels , "hex")
#    plt.savefig(init.dirname()+"/"+flags.DataType+"_Prec_q_vs_Xb.pdf")




# ------------------------------------------------------------------ #


# ------------------------------------------------------------------ #
elif flags.option == "DIS/correlation in alpha12:Xb":


    cut_ppNothinalpha12_vs_XbCutDIS = cut + ana.alpha12_vs_XbCutDIS;
    cut_ppNothinalpha12_vs_XbCutCorrelation = cut + ana.alpha12_vs_XbCutCorrelation;
    
    args = []
    if (flags.variable == "DIS_and_correlation"):
        args = ["Xb","alpha[0] + alpha[1]",0.9*XbMin,2.5,1.,2.6,gp.XbTit, gp.alphaTit("p_{1}") + " + " + gp.alphaTit("p_{2}")]
    
    elif (flags.variable == "opening_anlge"):
        args = ["Xb","TMath::RadToDeg()*thetaLeadRec",0.9*XbMin,2.5,0,180,gp.XbTit, gp.ThetaTit("p_{1},p_{2}")]

    elif (flags.variable == "cm"):
        args = ["Xb","PcmFinalState.P()",0.9*XbMin,2.5,0,2,gp.XbTit, "|#vec{p}_{1}+#vec{p}_{2}| [GeV/c]"]

    elif (flags.variable == "p1_vs_p2"):
        args = ["protons[0].P()","protons[1].P()",0.25,0.75,0.25,0.75,"|#vec{p}_{1}| [GeV/c]","|#vec{p}_{2}| [GeV/c]"]

    elif (flags.variable == "theta1_vs_theta2"):
        args = ["TMath::RadToDeg()*protons[0].Theta()","TMath::RadToDeg()*protons[1].Theta()",0,180,0,180,gp.ThetaTit("p_{1}"), gp.ThetaTit("p_{2}")]
    
    elif (flags.variable == "cm_vs_q"):
        args = ["q.P()","PcmFinalState.P()",1.1,4,0.,1.5,"|#vec{q}| [GeV/c]", "|#vec{p}_{1}+#vec{p}_{2}| [GeV/c]"]
    
    elif (flags.variable == "pt"):
#        args = ["Xb","PcmFinalState.Pt()",0.9*XbMin,2.5,0.,1.5,gp.XbTit, "(#vec{p}_{1}+#vec{p}_{2})_{perp} [GeV/c]"]
        args = ["q.P()","PcmFinalState.Pt()",1.1,4,0.,1.5,"|#vec{q}| [GeV/c]", "(#vec{p}_{1}+#vec{p}_{2})_{perp} [GeV/c]"]
        Nbins = Nbins/2


    c = ana.CreateCanvas(flags.option)
    ana.H2(args[0],args[1],cut_ppNothinalpha12_vs_XbCutDIS,"colz",Nbins,args[2],args[3],Nbins,args[4],args[5],"",args[6],args[7])
    c.SaveAs(init.dirname()+"/"+flags.DataType+"_"+flags.variable+"_DIS.pdf")
    ana.H2(args[0],args[1],cut_ppNothinalpha12_vs_XbCutCorrelation,"colz",Nbins,args[2],args[3],Nbins,args[4],args[5],"",args[6],args[7])
    if (flags.variable == "DIS_and_correlation"):
        ana.Line(args[2],3-args[2],3-args[4],args[4],1,2) # add a line of y = 3-x
    c.SaveAs(init.dirname()+"/"+flags.DataType+"_"+flags.variable+"_correlation.pdf")

    c.Update()
    wait()

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
