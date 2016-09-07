'''
    usage:
    ------
    python mac/ana_pp_cm.py --option=scheme
    
'''

import ROOT , time , sys
from ROOT import TPlots, TAnalysisEG2 , TEG2dm , TSchemeDATA
from rootpy.interactive import wait
sys.path.insert(0, '../../mySoftware/MySoftwarePackage/mac')
import GeneralPlot as gp, Initiation as init , input_flags
from matplotlib import pyplot as plt
import matplotlib , pandas as pd , numpy as np

init.createnewdir()
flags = input_flags.get_args()



PmissMin    = [0.3  , 0.45 , 0.55 , 0.65 , 0.75]
PmissMax    = [0.45 , 0.55 , 0.65 , 0.75 , 1.0 ]
dm          = TEG2dm()
DataName    = "DATA_%s_ppSRC"% dm.Target(flags.atomic_mass)
SchemedName = "ppSRCCut_%s"% DataName


if flags.option=="scheme":
    print 'scheming from %s'% DataName
    ana     = TAnalysisEG2( DataName , flags.cut )
    scheme  = TSchemeDATA()
    scheme.SchemeOnTCut( "/Users/erezcohen/Desktop/DataMining/AnaFiles" , "Ana_"+DataName+".root", "anaTree", "Ana_"+SchemedName+".root", ana.ppSRCCut )
    print 'schemed to %s'%SchemedName

ana = TAnalysisEG2( SchemedName , flags.cut )

def  plot_errorbar_and_fit( ax , x , y , xerr , yerr , color , marker , lstyle , label , offset):
    
    plt.errorbar(x, y, xerr=xerr, yerr=yerr, color=color, marker=marker , linestyle=lstyle , label=None)
    p = np.polyfit( x , y , 1)
    ax.plot(x, p[0] * (x-offset) + p[0]*offset + p[1], color=color , label=label + "=%.2f($p_{miss}$-%.1f)+%.2f"%(p[0],offset,p[0]*offset + p[1]))




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



elif flags.option=="calc_roofit_cm_parameters":
    outfile = open("/Users/erezcohen/Desktop/CMparametes.csv", "wb")
    outfile.write('\n\n')
    outfile.write("pMiss_min,pMiss_max,mean_x,mean_xErr,sigma_x,sigma_xErr,mean_y,mean_yErr,sigma_y,sigma_yErr,mean_z,mean_zErr,sigma_z,sigma_zErr\n")
    for i in range(len(PmissMin)):
        x = ana.RooFitCM(PmissMin[i],PmissMax[i]) # RooFitCM return a parameter vector
        outfile.write("%.2f,%.2f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f\n" % ( PmissMin[i] , PmissMax[i] ,x(0,0) ,x(0,1) ,x(1,0) ,x(1,1) , x(2,0) ,x(2,1) ,x(3,0), x(3,1) , x(4,0), x(4,1) , x(5,0), x(5,1)))
    outfile.write('\n\n')
    outfile.close()
    print "from \n/Users/erezcohen/Desktop/DataMining/AnaFiles/Ana_"+SchemedName+".root"
    print "done calculating parameters, output can be found in the file: ", outfile.name
    print '\n\n'




elif flags.option=="plot_roofit_cm_parameters":
    data = pd.read_csv("/Users/erezcohen/Desktop/CMparametes.csv")
    Pmiss = (data.pMiss_max + data.pMiss_min)/2.
    pMissUpErr , pMissLowErr = data.pMiss_max - Pmiss , Pmiss - data.pMiss_min
    sigma_x = data.sigma_x
    print "data: ",data
    print "Pmiss: ",Pmiss

    fig = plt.figure(figsize=(15,10))
    ax = fig.add_subplot(111)
    ax.text( 0.5 , 0.2 , "no acc. corr." , fontsize=60 , color='red' , alpha = 0.15 )
    ax.grid(True,linestyle='-',color='0.75')

    plot_errorbar_and_fit( ax , Pmiss, data.sigma_x , [pMissLowErr,pMissUpErr] , [data.sigma_xErr,data.sigma_xErr],'black'  ,'v','none',r'$\sigma_{x}$' , 0.5)
    plot_errorbar_and_fit( ax , Pmiss, data.sigma_y , [pMissLowErr,pMissUpErr] , [data.sigma_yErr,data.sigma_yErr],'red'    ,'o','none',r'$\sigma_{y}$' , 0.5)
    plot_errorbar_and_fit( ax , Pmiss, data.sigma_z , [pMissLowErr,pMissUpErr] , [data.sigma_zErr,data.sigma_zErr],'blue'   ,'s','none',r'$\sigma_{\vec{p}_{miss}}$', 0.5)
    
    plt.xlabel(gp.pmiss_label,fontsize=25)
    plt.ylabel( r'c.m. momentum width [Gev/c]',fontsize=25)
    ax.legend(loc="upper left",scatterpoints=1)
#    plt.show()
    plt.savefig("/Users/erezcohen/Desktop/cm_width.pdf")
    
    
    fig = plt.figure(figsize=(15,10))
    ax = fig.add_subplot(111)
    ax.text( 0.5 , 0.1 , "no acc. corr." , fontsize=60 , color='red' , alpha = 0.15 )
    ax.grid(True,linestyle='-',color='0.75')
    
    plot_errorbar_and_fit( ax , Pmiss, data.mean_x , [pMissLowErr,pMissUpErr] , [data.mean_xErr,data.mean_xErr],'black' ,'v','none',r'$mean_{x}$' , 0.3)
    plot_errorbar_and_fit( ax , Pmiss, data.mean_y , [pMissLowErr,pMissUpErr] , [data.mean_yErr,data.mean_yErr],'red'   ,'v','none',r'$mean_{y}$' , 0.3)
    plot_errorbar_and_fit( ax , Pmiss, data.mean_z , [pMissLowErr,pMissUpErr] , [data.mean_zErr,data.mean_zErr],'blue'  ,'v','none',r'$mean_{\vec{p}_{miss}}$' , 0.3)

    plt.xlabel(gp.pmiss_label,fontsize=25)
    plt.ylabel( r'c.m. momentum mean [Gev/c]',fontsize=25)
    ax.legend(loc="upper left",scatterpoints=1)
#    plt.show()
    plt.savefig("/Users/erezcohen/Desktop/cm_mean.pdf")



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

