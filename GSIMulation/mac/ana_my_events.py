'''
    usage:
    --------
    python mac/ana_my_events.py --option="missing evts vs. p(miss)"
'''

import ROOT ,os, sys , numpy as np , random
from ROOT import TPlots
sys.path.insert(0, '../../mySoftware/MySoftwarePackage/mac')
import GeneralPlot as gp, Initiation as init , input_flags
from matplotlib import pyplot as plt
from matplotlib import ticker

init.createnewdir()
flags = input_flags.get_args()


runs     = np.arange(100,505)
PrecMin  = 0.35

PmissLow = [ 0.3  , 0.45 , 0.55 , 0.65 , 0.75]
PmissUp  = [ 0.45 , 0.55 , 0.65 , 0.75 , 1.0 ]
Pmiss    = [ 0.5*(PmissLow[i] + PmissUp[i]) for i in range(len(PmissLow))]

if(flags.verbose>2):
    print "ploting runs ",runs
    print "on %d p(miss) bins"%len(PmissLow)
    print Pmiss




if flags.option=="missing evts vs. p(miss)":
    
    if(flags.verbose>0):
        print "looking for the fraction of events with p(recoil)>%.2f GeV/c, as a function of p(miss)"%PrecMin
#    plt.figure(figsize=(20,10))
    fig, ax = plt.subplots(1,1,figsize=(20,10))

    for run in runs:
        if (run%flags.print_mod==0):
            print "\trun=%d,[%.1f%%]"%(run,100*float(run)/len(runs))
    
        ana = TPlots("/Users/erezcohen/Desktop/DataMining/GSIM/eg_rootfiles/run0%d.root"%run,"anaTree")
        fracGoodPrec = []
        '''
            find how many events were 'lost' due to the cut on p(rec) > 0.35
            as a function of p(miss)
        '''
        for i in range(len(PmissLow)):

            CutPmBin = ROOT.TCut("%f<Pmiss.Mag() && Pmiss.Mag()<%f"%(PmissLow[i],PmissUp[i]))
            CutPrec  = ROOT.TCut("%f<Precoil.Mag()"%PrecMin)
            NentriesPmissBin = ana.GetEntries( CutPmBin )
            NentriesPrecCut = ana.GetEntries( CutPmBin + CutPrec )
            if (NentriesPmissBin > 0):
                fracGoodPrec.append(100*(1-float(NentriesPrecCut)/NentriesPmissBin))
            else:
                fracGoodPrec.append(100)


        l, = plt.plot( Pmiss , fracGoodPrec , label='run %d'%run )
#        index = int(random.random()*len(PmissLow))
        index = 1
        pos = [(Pmiss[index-1]+Pmiss[index])/2., (fracGoodPrec[index-1]+fracGoodPrec[index])/2.]
        xscreen = ax.transData.transform(zip(Pmiss[-2::],fracGoodPrec[-2::]))
        rot = np.rad2deg(np.arctan2(*np.abs(np.gradient(xscreen)[0][0][::1])))
        ltex = plt.text(pos[0], pos[1], '%d'%run , size=9, rotation=rot, color = l.get_color(),
                        ha="center", va="center",bbox = dict(ec='1',fc='1'))
        ana.Close()

    plt.xlabel(gp.pmiss_label)
    plt.ylabel('loss for $p_{rec}>0.35$ GeV/c cut [%]')
    plt.show()



