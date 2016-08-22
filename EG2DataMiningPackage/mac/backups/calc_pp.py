import ROOT
from ROOT import TEG2dm
from ROOT import TSchemeDATA
from ROOT import TAnalysisEG2
from ROOT import TCalcPhysVarsEG2


A           = 12
Path        = "/Users/erezcohen/Desktop/DataMining"
SchemeType  = "SRCPmissXb"
FileName    = "DATA_C12"

InFile      = ROOT.TFile(Path + "/Schemed_EG2_DATA/"+"Schemed_"+SchemeType+"_"+FileName+".root")
InTree      = InFile.Get("T")
Nentries    = InTree.GetEntries()

OutFile     = ROOT.TFile(Path + "/AnaFiles/"+"Ana_"+"ppSRC_"+FileName+".root","recreate")
OutTree     = ROOT.TTree("anaTree","physical variables ppSRC")

calc    = TCalcPhysVarsEG2( InTree , OutTree , A , "data" , "Pmiss(z) - q(x-z) frame" ) 
dm      = TEG2dm()
scheme  = TSchemeDATA()
anaEG2  = TAnalysisEG2()
anaEG2.SetSRCCuts()



for entry in range(0, (int)(1.*Nentries)):
    
    calc.ComputePhysVars( entry );
#    calc.PrintData( entry );


print "done filling %d events" % OutTree.GetEntries()

OutTree.Write()
OutFile.Close()



scheme.SchemeOnTCut(Path+"/AnaFiles", "Ana_ppSRC_"+FileName+".root", "anaTree","Ana_ppSRC_"+FileName+"_FullCuts.root", anaEG2.ppSRCCut)


#vars    = [ROOT.TString("Np")]# , "Xb" , "Pmiss.P()"   , "theta_pq"    , "p_over_q"    , "Mmiss"   , "pVertex[0].Z()"  , "pVertex[1].Z()"  , "Prec.P()"]
#Min     = [2]#    , 1.2  , 0.3           , 0             , 0.62          , 0         , -24.5             , -24.5             , 0.35]
#Max     = [2]#    , 5    , 1.0           , 25            , 0.96          , 1.1       , -20               , -20               , 1.1]
#scheme.SchemeOnTCut(Path+"/AnaFiles", "Ana_ppSRC_"+FileName+".root", "anaTree","Ana_ppSRC_"+FileName+"_FullCuts.root", vars, Min,  Max)



