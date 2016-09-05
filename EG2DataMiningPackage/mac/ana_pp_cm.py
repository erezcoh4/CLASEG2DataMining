'''
    usage:
    ------
    python mac/ana_pp_cm.py --option=roofit_cm_parameters
    
'''

import ROOT , time , sys
from ROOT import TPlots, TAnalysisEG2 , TEG2dm , TSchemeDATA
from rootpy.interactive import wait
sys.path.insert(0, '../../mySoftware/MySoftwarePackage/mac')
import GeneralPlot as gp, Initiation as init , input_flags
from matplotlib import pyplot as plt

init.createnewdir()
flags = input_flags.get_args()



PmissMin    = [0.3  , 0.45 , 0.55 , 0.65 , 0.75]
PmissMax    = [0.45 , 0.55 , 0.65 , 0.75 , 1.0 ]
dm          = TEG2dm()
DataName    = "DATA_%s"% dm.Target(flags.atomic_mass)
SchemedName = "ppSRCCut_%s"% DataName


if flags.option=='scheme':
    print 'scheming from %s'% DataName
    ana     = TAnalysisEG2( DataName , flags.cut )
    scheme  = TSchemeDATA()
    scheme.SchemeOnTCut( "/Users/erezcohen/Desktop/DataMining/AnaFiles" , "Ana_"+DataName+".root", "anaTree", "Ana_"+SchemedName+".root", ana.ppSRCCut )
    print 'schemed to %s'%SchemedName

ana         = TAnalysisEG2( SchemedName , flags.cut )

if flags.option=="DrawCM3D" :
    c = ana.CreateCanvas("c.m. momentum","DivideSquare",9)
    Nbins       = 50

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



elif flags.option=="roofit_cm_parameters":
    outfile = open("/Users/erezcohen/Desktop/CMparametes.dat", "wb")
    outfile.write('\n\n')
    outfile.write("p(miss): min \t max \t mean(x) \t sigma(x) \t mean(y) \t sigma(y) \t mean(z) \t sigma(z) \n")
    outfile.write("-------------------------------------------------------------------------------------------------------------------------\n")
    for i in range(len(PmissMin)):
        x = ana.RooFitCM(PmissMin[i],PmissMax[i]) # RooFitCM return a parameter vector
        outfile.write("%.2f \t %.2f \t %f \t %f \t %f \t %f \t %f \t %f\n" % ( PmissMin[i] , PmissMax[i] , x(0,0) , x(1,0) , x(2,0) , x(3,0) , x(4,0) , x(5,0)))
    outfile.write('\n\n')
    outfile.close()
    print "done calculating parameters, output can be found in the file: ", outfile.name
    print '\n\n'




elif flags.option=="PrintPcm":
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

