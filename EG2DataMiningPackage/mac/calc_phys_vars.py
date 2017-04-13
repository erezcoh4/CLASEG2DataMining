
'''
    usage:
    --------
    python mac/calc_phys_vars.py -werez --option=ppSRC --DataType=DATA -evf=1 -p10000 -v2 -A12
    python mac/calc_phys_vars.py -werez --option=pppSRC --DataType=NoCTofDATA -evf=1 -p10000 -A12
    python mac/calc_phys_vars.py --DataType=GSIM -evf=0.01 -p10000 -r80
    python mac/calc_phys_vars.py -A12 --DataType=New_NoCTofDATA --SchemedType=TwoSlowProtons -evf=1 -p10000
    python mac/calc_phys_vars.py -A12 --DataType=New_NoCTofDATA --SchemedType=TwoSlowProtons_piminus_p -evf=1 -p10000
'''
from definitions import *

SchemeType  = flags.SchemedType
DataType    = flags.DataType


if (DataType == "GSIM"):
    FileName    = "GSIM_run%04d_eep"%flags.run
    InFile      = ROOT.TFile(path + "/GSIM_DATA/"+FileName+".root")
    InTree      = InFile.Get("proton_data")
    OutFileName = path + "/AnaFiles/"+"Ana_"+FileName+".root"
    OutFile     = ROOT.TFile( OutFileName ,"RECREATE")
    axes_frame  = "lab frame"

else:
    FileName    = "%s_%s_%s"% (SchemeType,DataType,dm.Target(A))
    InFile      = ROOT.TFile( schemed_eg2_data_path + "/"+"Schemed_"+FileName+".root" )
    InTree      = InFile.Get("T")
    OutFileName = path + "/AnaFiles/"+"Ana_"+FileName+".root"
    OutFile     = ROOT.TFile( OutFileName ,"RECREATE")
    print 'InFile:',InFile,'OutFile:',OutFile


Nentries    = InTree.GetEntries()
OutTree     = ROOT.TTree("anaTree","physical variables")
calc = TCalcPhysVarsEG2( InTree , OutFileName , A , flags.DataType , axes_frame , flags.verbose)

if (DataType == "GSIM"):
    calc.SetNp_g(1)


for entry in range(0, int(flags.evnts_frac*Nentries)):
    calc.ComputePhysVars( entry )
    if (flags.verbose>0 and entry%flags.print_mod == 0):
        calc.PrintData( entry )


calc.Close()

print "done filling %d events" % int(flags.evnts_frac*Nentries)
print "wrote file " + OutFileName





