import ROOT,os, sys , math , os.path , math
from ROOT import TEG2dm , TPlots , TAnalysisEG2 , TSchemeDATA
from rootpy.interactive import wait
import matplotlib.pyplot as plt
sys.path.insert(0, '/Users/erezcohen/larlite/UserDev/mySoftware/MySoftwarePackage/mac')
import Initiation as init , GeneralPlot as gp
init.createnewdir()
import input_flags
flags = input_flags.get_args()
ROOT.gStyle.SetOptStat(0000)

'''
    usage:
    --------
    > python ana_SRC.py -A12 -var='Prec' --option='pp-events'
'''

Nbins       = 35
A           = flags.atomic_mass
var         = flags.variable
cut         = flags.cut

if flags.operation == 12:
    flags.option = 'short-tracks'
if var == 12:
    var = 'Prec'

XbCut       = ROOT.TCut("%f <= Xb"%1.2)
Path        = "/Users/erezcohen/Desktop/DataMining/AnaFiles"


# ------------------------------------------------------------------ #
dm  = TEG2dm()
def addPreliminaryText(h):
    ana.Text( 1.1*h.GetXaxis().GetXmin() , 0.1*h.GetMaximum() ,"preliminary - not corrected for CLAS acceptance" , 46 , 0.07 , 30 , 0.15 )

# ------------------------------------------------------------------ #




# ------------------------------------------------------------------ #
if flags.option == "ppSRC":
    
    ana = TAnalysisEG2("NoCTofDATA_%s"% dm.Target(A), XbCut ) #

    c = ana.CreateCanvas("SRC signature of cumulative kinematics in Q2" )

    if var == "Prec":
        h = ana.H1( "Prec.P()" ,  ana.ppSRCCut , "hist" , Nbins , 0.3 , 1. , "" , gp.PrecTit )
        addPreliminaryText(h)


    elif var == "Pmiss":
        
        c.Divide(1,2,0,0)
        c.cd(1)
        heep = ana.H1( "Pmiss.P()", ana.eepInSRCCut, "hist", Nbins , 0.3 ,1,"",gp.PmissTit )
        addPreliminaryText(heep)
        ana.Text( 0.5 , 0.8*heep.GetMaximum() , "^{12}C(e,e'p)" , 1, 0.1 )

        c.cd(2)
        h = ana.H1( "Pmiss.P()", ana.ppSRCCut, "hist", Nbins , 0.3 , 1 , "" , gp.PmissTit )
        addPreliminaryText(h)
        ana.Text( 0.5 , 0.8*h.GetMaximum() , "^{12}C(e,e'pp)" , 1 , 0.1 )


    c.Update()
    wait()
    c.SaveAs(init.dirname()+"/ppSRC_"+var+".pdf")
# ------------------------------------------------------------------ #




elif flags.option == "(e,e'pp)/(e,e'p)":
    
    ana = TAnalysisEG2("NoCTofDATA_%s"% dm.Target(A), XbCut )
    heep = ana.H1( "Pmiss.P()", ana.eepInSRCCut, "goff", Nbins , 0.3 ,0.9 )
    heepp = ana.H1( "Pmiss.P()", ana.ppSRCCut, "goff", Nbins , 0.3 , 0.9 )
        
    Pmiss = []
    PmissErr = []
    ratio = []
    ratioErr = []
        
    for bin in range(Nbins):
            
        Pmiss.append(heep.GetXaxis().GetBinCenter(bin))
        PmissErr.append(heep.GetXaxis().GetBinWidth(bin)/2.)
            
        if heep.GetBinContent(bin)<0.1 or heepp.GetBinContent(bin)<0.1 :
            ratio.append( 0 )
            ratioErr.append( 0 )
            
        else:
            r = heepp.GetBinContent(bin) / heep.GetBinContent(bin)
            ratio.append( 100*r )
            err = r * math.sqrt( 1. / heepp.GetBinContent(bin) + 1. / heep.GetBinContent(bin) )
            ratioErr.append( 100*err )


    fig = plt.figure(1, figsize = (6,4) )
    plt.errorbar(Pmiss, ratio, fmt='ro', xerr=PmissErr, yerr=ratioErr, ecolor='black')
    plt.xlabel(r'$|\vec{p}_{miss}|$ [GeV/c]',fontsize=22)
    plt.ylabel(r'${\frac{^{12}C(e,e\'pp)}{^{12}C(e,e\'p)}}$ [%]',fontsize=25)
    ax = fig.add_subplot(111)
    ax.text( 0.4, 10, "preliminary - not corrected for CLAS acceptance" , fontsize=22 , color='red' , alpha = 0.15 , rotation=30)
    plt.savefig(init.dirname()+"/ppSRC_12C_eepp_eep_ratio.pdf")
    plt.show()




# ------------------------------------------------------------------ #
elif flags.option == "SRC signature of cumulative kinematics in Q2":
    
    ana = TAnalysisEG2("everything_NoCTofDATA_%s"% dm.Target(A), XbCut ) #
    
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


