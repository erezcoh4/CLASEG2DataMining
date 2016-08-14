import ROOT , os , sys
from ROOT import TSchemeDATA , TEG2dm
sys.path.insert(0, '/Users/erezcohen/larlite/UserDev/mySoftware/MySoftwarePackage/mac')
import input_flags
flags = input_flags.get_args()



# scheme data file to have two protons with momenta in the range 0.3 < p < 0.7 GeV/c
A   = flags.atomic_mass


dm          = TEG2dm()
FileName    = "New_NoCTofDATA_%s"% dm.Target(A)
scheme      = TSchemeDATA("no ctof","/Users/erezcohen/Desktop/DataMining",FileName,"T")


pMin = 0.3
pMax = 0.7
scheme.TwoSlowProtons( 2 , pMin , pMax ) # target-type = 2, momentum minimum and maximum
print "schemed in nuclear target, for 2 protons with momentum %.1f < p < %.1f..."%(pMin,pMax)





print "done"

