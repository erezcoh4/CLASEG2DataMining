import ROOT
from ROOT import TPlots
from ROOT import TAnalysisEG2
from rootpy.interactive import wait
import time
ROOT.gStyle.SetOptStat(0000)


DoDrawCM3D              = False
DoPrintParameterVectors = False
DoPrintPcm              = True

PmissMin    = [0.3  , 0.45 , 0.55 , 0.65 , 0.75]
PmissMax    = [0.45 , 0.55 , 0.65 , 0.75 , 1.0 ]
ana         = TAnalysisEG2("ppSRC_DATA_C12_FullCuts")
Nbins       = 50




if DoDrawCM3D :
    c = ana.CreateCanvas("c.m. momentum","DivideSquare",9)

    c.cd(1)
    ana.H1("Pcm.Px()",ROOT.TCut(),"HIST",Nbins,-1,1,"","p(c.m.) ^{x} [GeV/c]","",1,46)



    c.cd(2)
    ana.H1("Pcm.Py()",ROOT.TCut(),"HIST",Nbins,-1,1,"","p(c.m.) ^{y} [GeV/c]","",1,46)



    c.cd(3)
    ana.H1("Pcm.Pz()",ROOT.TCut(),"HIST",Nbins,-1,1,"","#vec{p}(c.m.) #dot #vec{p}(miss) [GeV/c]","",1,46)


    c.cd(4)
    cut = ROOT.TCut("")
    ana.H3("Pcm.Px()","Pcm.Py()","Pcm.Pz()",cut,"",Nbins,-0.8,0.8,Nbins,-0.8,0.8,Nbins,-0.8,0.8
       ,"c.m. 3D - all (%d events)" % ana.GetEntries(cut) ,"p(c.m.) ^{x} [GeV/c]","p(c.m.) ^{y} [GeV/c]","p(c.m.) ^{z} [GeV/c]")



    c.cd(5)
    cut = ROOT.TCut("0.3 < Pmiss.P() && Pmiss.P() < 0.4")
    ana.H3("Pcm.Px()","Pcm.Py()","Pcm.Pz()",cut,"",Nbins,-0.8,0.8,Nbins,-0.8,0.8,Nbins,-0.8,0.8
       ," 0.3 < p(miss) < 0.4 (%d events)" % ana.GetEntries(cut) ,"p(c.m.) ^{x} [GeV/c]","p(c.m.) ^{y} [GeV/c]","p(c.m.) ^{z} [GeV/c]")



    c.cd(6)
    cut = ROOT.TCut("0.4 < Pmiss.P() && Pmiss.P() < 0.5")
    ana.H3("Pcm.Px()","Pcm.Py()","Pcm.Pz()",cut,"",Nbins,-0.8,0.8,Nbins,-0.8,0.8,Nbins,-0.8,0.8 ," 0.4 < p(miss) < 0.5 (%d events)" % ana.GetEntries(cut) ,"p(c.m.) ^{x} [GeV/c]","p(c.m.) ^{y} [GeV/c]","p(c.m.) ^{z} [GeV/c]")

    c.cd(7)
    cut = ROOT.TCut("0.5 < Pmiss.P() && Pmiss.P() < 0.6")
    ana.H3("Pcm.Px()","Pcm.Py()","Pcm.Pz()",cut,"",Nbins,-0.8,0.8,Nbins,-0.8,0.8,Nbins,-0.8,0.8
       ," 0.5 < p(miss) < 0.6 (%d events)" % ana.GetEntries(cut) ,"p(c.m.) ^{x} [GeV/c]","p(c.m.) ^{y} [GeV/c]","p(c.m.) ^{z} [GeV/c]")



    c.cd(8)
    cut = ROOT.TCut("0.6 < Pmiss.P() && Pmiss.P() < 0.75")
    ana.H3("Pcm.Px()","Pcm.Py()","Pcm.Pz()",cut,"",Nbins,-0.8,0.8,Nbins,-0.8,0.8,Nbins,-0.8,0.8
       ," 0.6 < p(miss) < 0.75 (%d events)" % ana.GetEntries(cut) ,"p(c.m.) ^{x} [GeV/c]","p(c.m.) ^{y} [GeV/c]","p(c.m.) ^{z} [GeV/c]")



    c.cd(9)
    cut = ROOT.TCut("0.75 < Pmiss.P() && Pmiss.P() < 1.0")
    ana.H3("Pcm.Px()","Pcm.Py()","Pcm.Pz()",cut,"",Nbins,-0.8,0.8,Nbins,-0.8,0.8,Nbins,-0.8,0.8
       ," 0.75 < p(miss) < 1.0 (%d events)" % ana.GetEntries(cut) ,"p(c.m.) ^{x} [GeV/c]","p(c.m.) ^{y} [GeV/c]","p(c.m.) ^{z} [GeV/c]")





    wait()




if DoPrintParameterVectors:
    outfile = open("/Users/erezcohen/Desktop/CMparametes.dat", "wb")
    outfile.write("mean(x) \t sigma(x) \t mean(y) \t sigma(y) \t mean(z) \t sigma(z) \t p(miss) min \t p(miss) max\n")
    outfile.write("-------------------------------------------------------------------------------------------------------------------------\n")
    for i in range(0,5):
        x = ana.RooFitCM(PmissMin[i],PmissMax[i]) # RooFitCM return a parameter vector
        outfile.write("%f \t %f \t %f \t %f \t %f \t %f \t %f \t %f\n" % (x(0,0) , x(1,0) , x(2,0) , x(3,0) , x(4,0) , x(5,0) , PmissMin[i] , PmissMax[i] ))
    outfile.close()
    print "done calculating parameters, output can be found in the file: ", outfile.name
    print '\n\n'




if DoPrintPcm:
    outfile = open("/Users/erezcohen/Desktop/CMdata.dat", "wb")
    outfile.write("c.m. momentum vectors - %d large sample from C12, \t Units:GeV/c, \t" % ana.GetEntries(ROOT.TCut()) )
    outfile.write( time.strftime('%l:%M%p %Z on %b %d, %Y \n') )
    outfile.write("-------------------------------------------------------------------------------------------------------------------------\n")
    outfile.write("p(c.m.)-x \t p(c.m.)-y  \t p(c.m.)-z  \t |p(miss)| \n")
    outfile.write("-------------------------------------------------------------------------------------------------------------------------\n")
    for i in range(0,ana.GetEntries(ROOT.TCut())):
        PcmPmiss = ana.GetPcmEntry(i)
        outfile.write("%f \t %f \t %f \t %f \n" % (PcmPmiss.at(0) , PcmPmiss.at(1) , PcmPmiss.at(2) , PcmPmiss.at(3)))
    outfile.close()
    print "done calculating parameters, output can be found in the file: ", outfile.name
    print '\n\n'

