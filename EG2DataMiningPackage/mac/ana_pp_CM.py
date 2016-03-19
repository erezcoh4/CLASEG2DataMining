import ROOT
from ROOT import TPlots
from ROOT import TAnalysisEG2
from rootpy.interactive import wait
ROOT.gStyle.SetOptStat(0000)


ana = TAnalysisEG2("ppSRC_DATA_C12_FullCuts")
Nbins = 50



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
ana.H3("Pcm.Px()","Pcm.Py()","Pcm.Pz()",cut,"",Nbins,-0.8,0.8,Nbins,-0.8,0.8,Nbins,-0.8,0.8
       ," 0.4 < p(miss) < 0.5 (%d events)" % ana.GetEntries(cut) ,"p(c.m.) ^{x} [GeV/c]","p(c.m.) ^{y} [GeV/c]","p(c.m.) ^{z} [GeV/c]")



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

