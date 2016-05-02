import sys , ROOT , math
from ROOT import TPlots , TAnalysis , TAnalysisEG2, TSchemeDATA
from rootpy.interactive import wait
sys.path.insert(0, '/Users/erezcohen/larlite/UserDev/mySoftware/MySoftwarePackage/mac')
import Initiation as init
init.createnewdir()
ROOT.gStyle.SetOptStat(0000)


DoAllVariables  = False
Do1D            = True
Do2D            = False
DoPrint2GSIM    = True

Var         = "Pmiss"
Path        = "/Users/erezcohen/Desktop/DataMining/AnaFiles"
analysis    = TAnalysis()
Nbins       = 50
XbMin       = 1.05
XbCut       = ROOT.TCut("%f <= Xb"%XbMin)


# April - 07
if DoAllVariables:
    ana         = TAnalysisEG2("GSIM_run0088_eep", XbCut )
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
            xyAxes = ["p_over_q" ,  "theta_pq" , 0.6   , 1.1 ,  0   , 50 , "p(2) [GeV/c]" , "p(3) [GeV/c]" , ana.cutSRC , "SRC"]
        elif (Var=="RecoilProtons"):
            xyAxes = ["protons[1].P()" ,  "protons[2].P()" , 0.2   , 1.1 ,  0.2   , 1.1 , "p/q" , "#theta (p,q) [deg.]" , ana.Sim3pSRCCut , "3pSRC"]
        elif (Var=="theta_vs_phi"):
            xyAxes = ["fabs(phiMiss23)" , "thetaMiss23" , 0 , 80 ,  80 , 180 , "|#phi| [deg.]","#theta [deg.]" , ana.Sim3pSRCCut , "3pSRC"]
        elif (Var=="pp_scattering_CMtheta_vs_Mpp"):
            ana.H2("Mpp" , "(180/3.1415)*Theta_cm" , ROOT.TCut() ,"surf2" , Nbins , 1.9 , 4.2 , Nbins , 0 , 180 ,"#theta vs. #sqrt{s}","m(pp) [GeV/c^{2}]","#theta [deg.]" )
        c = ana.Draw2DVarAndCut(xyAxes[0] ,  xyAxes[1]   , Nbins , xyAxes[2]  , xyAxes[3]  , Nbins , xyAxes[4]   , xyAxes[5] , "" , xyAxes[6] , xyAxes[7] , xyAxes[8] , True  , xyAxes[9])
    if (Var=="DalitzPlot"):
        c = ana.CreateCanvas("Dalitz")
        ana.Dalitz("Pmiss","protons[1]","protons[2]",ana.Sim3pSRCCut,100,0,5,100,0,5);

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
        ana.AddLegend(hp2,"p(2)",hp3,"p(3)")
    c.Update()
    wait()
    c.SaveAs(init.dirname()+"/FSI3p_sim_"+Var+".pdf")





# April - 30
if DoPrint2GSIM:
    ana     = TAnalysisEG2("FSI3pSimulation", XbCut )
    outfile = open(Path+"/FSI3p_events.txt", "wb")
    for i in range(0,ana.GetEntries(ROOT.TCut())):
        evt = ana.GetGSIMEvt(i,True)
        outfile.write("%d\n" % evt.at(0))
        for j in range(0,4):
            outfile.write("%d  %f  %f  %f  %f \n" % (evt.at(1+11*j) , evt.at(2+11*j) , evt.at(3+11*j) , evt.at(4+11*j), evt.at(5+11*j)))
            outfile.write("%f  %d \n" % (evt.at(6) , evt.at(7)))
            outfile.write("%d  %d  %d  %d  %d \n" % (evt.at(8) , evt.at(9) , evt.at(10) , evt.at(11) , evt.at(12)))
    outfile.close()
    print "\ndone writing %d events to "%ana.GetEntries(ROOT.TCut()) + outfile.name
