import ROOT , os , sys
from ROOT import TSchemeDATA , TEG2dm

# options are: "data" / "no ctof"
if len(sys.argv)>1:
    run     = int(sys.argv[1])
else:
    print '\n run this script with: \n > python mac/scheme_gsim.py <run-number> \n\n'
    exit(0)
A           = 12
DataType    = "GSIM"
dm          = TEG2dm()
Path        = "/Users/erezcohen/Desktop/DataMining/GSIM_DATA"
FileName    = "GSIM_run%04d"%run


scheme = TSchemeDATA()

scheme.SchemeOnTCut( Path, FileName+".root", "proton_data", FileName + "_eep.root", ROOT.TCut("P_nmb>0"))

print "done"

