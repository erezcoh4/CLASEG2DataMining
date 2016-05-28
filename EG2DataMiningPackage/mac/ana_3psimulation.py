import sys , ROOT , math
from ROOT import TPlots , TAnalysis , TAnalysisEG2, TSchemeDATA
from rootpy.interactive import wait
sys.path.insert(0, '/Users/erezcohen/larlite/UserDev/mySoftware/MySoftwarePackage/mac')
import Initiation as init
init.createnewdir()
ROOT.gStyle.SetOptStat(0000)

Operation   = "protons in the process"
Do1D        = False
Do2D        = False

Var         = "pMiss_p2_p3"
Path        = "/Users/erezcohen/Desktop/DataMining/AnaFiles"
analysis    = TAnalysis()
plot        = TPlots()
Nbins       = 200
XbMin       = 1.05
XbCut       = ROOT.TCut("%f <= Xb"%XbMin)


# April - 07
if (Operation == "plot variables"):
    ana = TAnalysisEG2("GSIM_run0088_eep", XbCut ) # TAnalysisEG2("FSI3pSimulation", XbCut )
    if Do1D:
        if (Var=="Xb"):
            xAxis = [Var , 1  , 2.5, "Bjorken x" , ana.cutSRC , "SRC"]
        elif (Var=="Q2"):
            xAxis = [Var , 0  , 4, "Q^{2} [GeV/c]" , ana.cutSRC , "SRC"]
        elif (Var=="Pmiss"):
            xAxis = ["Pmiss.P()" , 0  , 2.5 , "#vec{p}(miss) = #vec{p}(lead) - #vec{q} [GeV/c]"  , ana.cutSRC , "SRC"]
        c = ana.Draw1DVarAndCut(xAxis[0] , Nbins , xAxis[1]  , xAxis[2]  , ""   , xAxis[3] , xAxis[4] , True  , xAxis[5])
    elif Do2D:
        if (Var=="q_vs_omega"):
            ana.H2("q.P()" , "q.E()" , ROOT.TCut() , "colz" , 100 , 0 , 5 , 100 , 0 , 4 , "","|#vec{q}| [GeV/c]","#omega [GeV]")
        elif (Var=="PoverQ_vs_ThetaPQ"):
            xyAxes = ["p_over_q" ,  "theta_pq" , 0.6   , 1.1 ,  0   , 50 , "p/q" , "#theta (p,q) [deg.]" , ana.cutSRC , "SRC"]
        elif (Var=="RecoilProtons"):
            xyAxes = ["protons[1].P()" ,  "protons[2].P()" , 0.2   , 1.1 ,  0.2   , 1.1 , "p(2) [GeV/c]" , "p(3) [GeV/c]" , ana.Sim3pSRCCut , "3pSRC"]
        elif (Var=="theta_vs_phi"):
            xyAxes = ["fabs(phiMiss23)" , "thetaMiss23" , 0 , 80 ,  80 , 180 , "|#phi| [deg.]","#theta [deg.]" , ana.Sim3pSRCCut , "3pSRC"]
        elif (Var=="pp_scattering_CMtheta_vs_Mpp"):
            ana.H2("Mpp" , "(180/3.1415)*Theta_cm" , ROOT.TCut() ,"surf2" , Nbins , 1.9 , 4.2 , Nbins , 0 , 180 ,"#theta vs. #sqrt{s}","m(pp) [GeV/c^{2}]","#theta [deg.]" )
        c = ana.Draw2DVarAndCut(xyAxes[0] ,  xyAxes[1]   , Nbins , xyAxes[2]  , xyAxes[3]  , Nbins , xyAxes[4]   , xyAxes[5] , "" , xyAxes[6] , xyAxes[7] , xyAxes[8] , True  , xyAxes[9])
    if (Var=="DalitzPlot"):
        c = ana.CreateCanvas("Dalitz")
        ana.Dalitz("protons[1].P()","protons[2].P()","Pmiss.P()",ana.Sim3pSRCCut,100,-1.7,1.7,100,-1.1,2,"p_{2}","p_{3}","p_{miss}") # "Modified" Dalitz plot since T is not

    if (Var=="theta_vs_phi"):
        ana.Box(0,155,15,180,1,0.1)
        evts = ana.GetEntries(ana.Sim3pSRCCut)
        evtsErr = math.sqrt(evts)
        print "%d +/- %d events"%(evts,evtsErr)
        evts_in_box = ana.GetEntries(ana.FinalSim3pSRCCut)
        evts_in_boxErr = math.sqrt(evts_in_box)
        print "%d +/- %d events in box"%(evts_in_box,evts_in_boxErr)
        percentage = 100*(float(evts_in_box)/evts)
        percentageErr = percentage*math.sqrt( math.pow(evtsErr/evts,2) +  math.pow(evts_in_boxErr/evts_in_box,2))
        ana.Text(20,160,"%d events (%.1f #pm %.1f %%)"%(evts_in_box , percentage , percentageErr))
    if (Var=="pMiss_p2_p3"):
        c = ana.CreateCanvas(Var)
        hp2 = ana.H2("Pmiss.P()" ,"protons[1].P()",  ana.Sim3pSRCCut ,"" , Nbins , 0.25 , 1.1 , Nbins , 0.25 , 1.1
                     ,"","|#bf{p}(miss)| [GeV/c]","recoil protons momenta [GeV/c]" , 3 , 20 , 1 , 0.8)
        hp3 = ana.H2("Pmiss.P()" , "protons[2].P()", ana.Sim3pSRCCut ,"same" , Nbins , 0.25 , 1.1 , Nbins , 0.25 , 1.1
                                  ,"","|#bf{p}(miss)| [GeV/c]","recoil protons momenta [GeV/c]" , 4 ,  20 , 1 , 0.8)
#        plot.AddLegend(hp2,"p(2)",hp3,"p(3)")
    c.Update()
    wait()
    c.SaveAs(init.dirname()+"/FSI3p_sim_"+Var+".pdf")


# April - 30
if (Operation == "Print data for GSIMulation"):
    ana     = TAnalysisEG2("FSI3pSimulation", XbCut )
    outfile = open(Path+"/FSI3p_events.txt", "wb")
    for i in range(0,ana.GetEntries(ROOT.TCut())):
        evt = ana.GetGSIMEvt(i,False)
        outfile.write("%d\n" % evt.at(0))
        for j in range(0,4):
            outfile.write("%d  %f  %f  %f  %f \n" % (evt.at(1+11*j) , evt.at(2+11*j) , evt.at(3+11*j) , evt.at(4+11*j), evt.at(5+11*j)))
            outfile.write("%f  %d \n" % (evt.at(6+11*j) , evt.at(7+11*j)))
            outfile.write("%d  %d  %d  %d  %d \n" % (evt.at(8+11*j) , evt.at(9+11*j) , evt.at(10+11*j) , evt.at(11+11*j) , evt.at(11+11*j)))
    outfile.close()
    print "\ndone writing %d events to "%ana.GetEntries(ROOT.TCut()) + outfile.name




# May-26
if (Operation == "protons in the process"):
    ana = TAnalysisEG2("FSI3pSimulation", XbCut )
    cut = ROOT.TCut() # ana.cutSRC
    c = plot.CreateCanvas(Operation,"Divide",3,3)
    c.cd(1)
    ana.H1("struck_p.P()" , cut,"hist",50, 0 , 0.3 , "struck proton (before hit)" , "p [GeV/c]" )
    c.cd(2)
    ana.H1("p_knocked.P()", cut,"hist",50, 1.0 , 3.2 , "knocked proton" , "p [GeV/c]" )
    c.cd(3)
    ana.H2("pcm_ppPair.Px()" ,"pcm_ppPair.Py()" , cut,"colz",50, -0.5, 0.5, 50, -0.5, 0.5, "p(c.m.) of the pp-pair" , "p_{x} [GeV/c]", "p_{y} [GeV/c]" )
    c.cd(4)
    ana.H1("p1_ppPair.P()" , cut,"hist", 50, 0, 1, "proton 1 from pp-pair before rescattering" , "p [GeV/c]" )
    c.cd(5)
    ana.H1("p2_ppPair.P()" , cut,"hist", 50, 0, 1, "proton 2 from pp-pair before rescattering" , "p [GeV/c]" )
    c.cd(6)
    ana.H2("p1_ppPair.P()" ,"p2_ppPair.P()" , cut,"colz",50, 0.2, 0.75, 50, 0, 1, "pp-pair momenta (p_{1} from k^{-4} tail)" , "p_{1} [GeV/c]", "p_{2} [GeV/c]" )
    c.cd(7)
    ana.H1("p_knocked_r.P()" , cut,"hist", 50, 0, 3.1, "knocked proton after rescattering" , "p [GeV/c]" )
    c.cd(8)
    hLowTheta = ana.H1("p1_ppPair_r.P()" , ROOT.TCut("(180/3.1415)*Theta_cm<90") ,"hist", 50, 0, 3.1, "p-1 (pp-pair) after rescattering" , "p [GeV/c]","",2,2 )
    ana.Text(0.5,0.8*hLowTheta.GetMaximum(),"#theta(c.m.) < 90^{0}",2)
    hHighTheta = ana.H1("p1_ppPair_r.P()" , ROOT.TCut("(180/3.1415)*Theta_cm>90") ,"hist same", 50, 0, 3.1, "" , "","",4,4 )
    ana.Text(1.9,0.8*hHighTheta.GetMaximum(),"#theta(c.m.) > 90^{0}",4)
    c.cd(9)
    ana.H1("p2_ppPair_r.P()" , cut,"hist", 50, 0, 1.1, "proton 2 from pp-pair after rescattering" , "p [GeV/c]" )
    c.Update()
    
    wait()
    c.SaveAs(init.dirname()+"/protons-in-the-process.pdf")
