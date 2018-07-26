
'''
    usage:
    --------
    make && python mac/calc_gsim_vars.py -werez --run=5001 --DataType=MC -evf=1 -p1000 -A56
    python mac/calc_gsim_vars.py -werez --run=5001 --DataType=MC -evf=1 -p1000 -A56 --print_mod=100
    
'''
from definitions import *
DataType    = flags.DataType


FileName    = "GSIMulationOutput_run%04d"%flags.run
InFile      = ROOT.TFile(path + "/GSIM_DATA/"+FileName+".root")
InTree      = InFile.Get("data")
OutFileName = path + "/AnaFiles/"+"Ana_"+FileName+".root"
OutFile     = ROOT.TFile( OutFileName ,"RECREATE")
axes_frame  = "lab frame"

Nentries    = InTree.GetEntries()
OutTree     = ROOT.TTree("anaTree","physical variables")
gsim = TCalcGSIMVarsEG2( InTree , OutFileName , A , flags.DataType , axes_frame , flags.verbose)

for entry in range(0, int(flags.evnts_frac*Nentries)):
    gsim.ComputePhysVars( entry )
    if (flags.verbose>0 and entry%flags.print_mod == 0):
        gsim.PrintData( entry )

gsim.Close()

print "done filling %d events" % int(flags.evnts_frac*Nentries)
print "wrote file " + OutFileName

print "Hey, I am done!"
print "I computed physical observables for %d events"%(flags.evnts_frac*Nentries)