# run:
# > python mac/ana_ppp.py <target A>

import ROOT
import os, sys , math
from ROOT import TEG2dm , TPlots , TAnalysisEG2 , TSchemeDATA
from rootpy.interactive import wait
sys.path.insert(0, '/Users/erezcohen/larlite/UserDev/mySoftware/MySoftwarePackage/mac')
import Initiation as init
init.createnewdir()
ROOT.gStyle.SetOptStat(0000)



Operation   = "Draw C12"
Var         = sys.argv[1] if len(sys.argv)>1 else "Xb"
p           = int(sys.argv[2]) if len(sys.argv)>2 else 0
cut         = ROOT.TCut("Np >= 0")
Nbins       = 100
dm          = TEG2dm()
Path        = "/Users/erezcohen/Desktop/DataMining/AnaFiles"


# ------------------------------------------------------------------ #
if Operation == "Draw C12":


    ana = TAnalysisEG2("C12_TwoSlowProtons")

    c = ana.CreateCanvas(Var)

    if (Var=="Pcm"):
        xAxis = ["Pcm.P()" , 0 , 1.4, "|#vec{p} (c.m.)| [GeV/c]"]
 
    elif (Var=="proton_3momentum"):
        xAxis = ["protons[%d].P()"%p , 0 , 3 , "|#vec{p}(%d)| [GeV/c]"%p  ]
    
    
    
    elif (Var=="Wtilde"):
        xAxis = ["Wtilde.Mag()" , -5 , 5 , "#sqrt{ W'^{#mu} W'_{#mu} } [GeV/c ^{2}]"]
    
    
    


    elif (Var=="Np"):
        xAxis = [Var , 0 , 10 , "numebr of reconstruncted protons"]


    elif (Var=="Pmiss"):
        xAxis = ["Pmiss.P()" , 0.2 , 1.1 , "|#vec{p} (miss)| [GeV/c]"]

    elif (Var=="PmT"):
        xAxis = ["Pmiss.Pt()" , 0.2 , 1.1 , "#vec{p} (miss) - T [GeV/c]"]


    elif (Var=="PtSquared"):
        xAxis = ["Pmiss.Pt()*Pmiss.Pt()" , 0.0 , 3. , "(#vec{p} (miss) _{#perp})^{2} [GeV/c]"]
        
    elif (Var=="Xb"):
        xAxis = [Var , 0 , 2, "Bjorken x"]


    elif (Var=="Q2"):
        xAxis = [Var , 0 , 5, "Q^{2} (GeV/c) ^{2}"]
    

    elif (Var=="Mmiss"):
        xAxis = ["Pcm.Mag()" , 0 , 6, "#sqrt{|p^{#mu}_{lead}+p^{#mu}_{2}+p^{#mu}_{3}-q^{#mu}|^{2}} [GeV/c ^{2}]"]

        
    elif (Var=="opening_angle"):
        xAxis = [ana.CosTheta("Pmiss.Vect()","Prec.Vect()") , -1 , 1, "cos (#theta)"]


    elif (Var=="cmEvsP"):
        xyAxes = ["Pcm.E()" , "Pcm.P()" , 2 , 5.8 , 0 , 2.7 , "p^{0}_{lead}+p^{0}_{2}+p^{0}_{3}-q^{0} [GeV]" , "|p^{i}_{lead}+p^{i}_{2}+p^{i}_{3}-q^{i}| [GeV/c]" ]
        
    elif (Var=="MmissVsXb"):
        xyAxes = ["Pcm.Mag()" , "Xb" , -2 , 5 , 0 , 2 , "#sqrt{|p^{#mu}_{lead}+p^{#mu}_{2}+p^{#mu}_{3}-q^{#mu}|^{2}} [GeV/c ^{2}]" , "Bjorken x" ]


    elif (Var=="PmissTransversalLongitudinal"):
        xyAxes = ["Pmiss.Pt()" , "Pmiss.Pz()" , 0 , 1 , -1 , 1 , "|#vec{p} (miss)|-T [GeV/c]" , "|#vec{p} (miss)|-L [GeV/c]" ]

    elif (Var=="proton_xy"):
        xyAxes = ["protons[%d].Px()"%p , "protons[%d].Py()"%p , -2 , 2 , -2 , 2 , "#vec{p}(%d)-x [GeV/c]"%p , "#vec{p}(%d)|-y [GeV/c]"%p ]

    elif (Var=="proton_xz"):
        xyAxes = ["protons[%d].Px()"%p , "protons[%d].Pz()"%p , -2 , 2 , -2 , 2 , "#vec{p}(%d)-x [GeV/c]"%p , "#vec{p}(%d)|-z [GeV/c]"%p ]

    elif (Var=="proton_yz"):
        xyAxes = ["protons[%d].Py()"%p , "protons[%d].Pz()"%p , -2 , 2 , -2 , 2 , "#vec{p}(%d)-y [GeV/c]"%p , "#vec{p}(%d)|-z [GeV/c]"%p ]

    elif (Var=="q"):
        xyAxes = ["q.P()" , "q.E()"  , 1 , 5 , 1 , 5 , "|#vec{q}| [GeV/c]" , "#omega [GeV]" ]


    elif (Var=="Wtilde_vs_Q2"):
        xyAxes = ["Wtilde.Mag()" ,"Q2" , -5 , 5 , 0 , 5 , "#sqrt{ W'^{#mu} W'_{#mu} } [GeV/c ^{2}]" , "Q^{2} (GeV/c) ^{2}"]


    if 'xAxis' in locals():
        ana.H1(xAxis[0] , cut , "hist" , Nbins , xAxis[1] , xAxis[2] , "" ,xAxis[3] , "" ,38)

    elif 'xyAxes' in locals():
        ana.H2(xyAxes[0] , xyAxes[1], cut , "colz" , Nbins , xyAxes[2] , xyAxes[3], Nbins , xyAxes[4] , xyAxes[5] , "" ,xyAxes[6] , xyAxes[7] , 1, 20 , 3 )

    c.Update()
    wait()
    c.SaveAs(init.dirname()+"/C12_TwoSlowProtons_"+Var+".pdf")
# ------------------------------------------------------------------ #
