import ROOT
from ROOT import T3pSimulation , TAnalysis
from rootpy.interactive import wait
analysis = TAnalysis()



DoDraw  = False


Path = "/Users/erezcohen/Desktop/DataMining"
h_q = analysis.GetH2FromAFile(Path+"/EG2_DATA/inclusive_q.root" , "h_inclusive_q")
OutFile = ROOT.TFile(Path+"/AnaFiles/FSI3pSimulation.root","recreate")
OutTree = ROOT.TTree("anaTree","FSI 2 (scatter off low-momentum p followed by rescattering off pp-pair)")
sim3p   = T3pSimulation( OutTree )
sim3p.Imp_q_Histo( h_q ,  DoDraw )
if (DoDraw) : wait()
sim3p.Imp_ppElasticHisto( DoDraw )
if (DoDraw) : wait()
sim3p.ImpMomentumDist( DoDraw )
if (DoDraw) : wait()



sim3p.RunInteractions( 5 , False )       # run interactions and fill output tree
print "done filling %d events " % OutTree.GetEntries() + "in " + OutTree.GetTitle()
OutTree.Write()
OutFile.Close()
