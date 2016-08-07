import ROOT,os, sys , math , os.path
from ROOT import TEG2dm , TPlots , TAnalysisEG2 , TSchemeDATA
from rootpy.interactive import wait
sys.path.insert(0, '/Users/erezcohen/larlite/UserDev/mySoftware/MySoftwarePackage/mac')
import Initiation as init , GeneralPlot as gp
init.createnewdir()
import input_flags
flags = input_flags.get_args()
ROOT.gStyle.SetOptStat(0000)


Operation   = "SRC signature of cumulative kinematics in Q2"
Nbins       = 100
cut         = ROOT.TCut()
XbCut       = ROOT.TCut("%f <= Xb"%0.)
Path        = "/Users/erezcohen/Desktop/DataMining/AnaFiles"


# ------------------------------------------------------------------ #
A   = flags.atomic_mass
dm  = TEG2dm()
ana = TAnalysisEG2("everything_NoCTofDATA_%s"% dm.Target(A), XbCut ) #
# ------------------------------------------------------------------ #

# ------------------------------------------------------------------ #
if Operation == "SRC signature of cumulative kinematics in Q2":
    
    c = ana.CreateCanvas("SRC signature of cumulative kinematics in Q2" )
    h1DQ2 = ana.H1( "Q2" , XbCut ,"goff"   , Nbins , 0 , 5  , ""   , gp.Q2Tit )
    h2 = ana.H2( "Q2" , "NpCumulative" , ROOT.TCut("Np>1") , "col"  , Nbins , 0 , 5 , 5 , 0 , 8 , "" , gp.Q2Tit,"number of backward protons (#theta>90^{0})"  )

    c.Update()
    wait()

    hCumulativeDetected = ROOT.TH1F( "hCumulativeDetected","", Nbins , 0 , 5 )
#    hCumulativeDetected.GetXaxis().SetTitle(gp.Q2Tit)
#    hCumulativeDetected.GetXaxis().CenterTitle()
#    hCumulativeDetected.GetYaxis().SetTitle("backward protons with momentum > 0.3 GeV/c")
#    hCumulativeDetected.GetYaxis().CenterTitle()
#    
#    for Q2bin in range(Nbins):
#        
#        NpCumulativePerQ2 = 0
#        
#        for NpCumulativebin in range( 2 , h2.GetYaxis().GetNbins() ):
#            
#            NpCumulativebinCenter = h2.GetYaxis().GetBinCenter(NpCumulativebin)
#            print "NpCumulative = %.2f, h2.GetBinContent( Q2bin , NpCumulativebin ) = %f"%(NpCumulativebinCenter,h2.GetBinContent( Q2bin , NpCumulativebin ))
#            NpCumulativePerQ2 += h2.GetBinContent( Q2bin , NpCumulativebin )
#    
#        print "Q2: ",h2.GetXaxis().GetBinCenter(Q2bin)
#        print "NpCumulativePerQ2: ",NpCumulativePerQ2
#        print "and h1DQ2.GetBinContent(Q2bin) is ",h1DQ2.GetBinContent(Q2bin)
#        hCumulativeDetected.SetBinContent(Q2bin , 1 if NpCumulativePerQ2 > 0.01*h1DQ2.GetBinContent(Q2bin) else 0 )
#        print "so bin content is ",hCumulativeDetected.GetBinContent(Q2bin)
#    
#
#    c = ana.CreateCanvas("hCumulativeDetected" )
#    hCumulativeDetected.Draw("hist")
#    c.Update()
#    wait()

# ------------------------------------------------------------------ #


