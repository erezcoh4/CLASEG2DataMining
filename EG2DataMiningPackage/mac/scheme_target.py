import ROOT , os , sys
from ROOT import TSchemeDATA
from ROOT import TEG2dm
sys.path.insert(0, '/Users/erezcohen/larlite/UserDev/mySoftware/MySoftwarePackage/mac')
import input_flags
flags = input_flags.get_args()


# options are: "data" / "no ctof"
A = flags.atomic_mass
DataType    = "no ctof"
dm          = TEG2dm()
FileName    = "NoCTofDATA_%s.root"% dm.Target(A)



scheme = TSchemeDATA(DataType,"/Users/erezcohen/Desktop/DataMining",FileName,"T")

scheme.protons_from_nuclei() # protons from solid targets that pass CTOF cuts

print 'schemed for protons in solid target and'




print "done"

