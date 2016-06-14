import ROOT , os , sys
from ROOT import TSchemeDATA , TEG2dm



# scheme data file to have two protons with momenta in the range 0.3 < p < 0.7 GeV/c

if len(sys.argv)>1:
    A       = int(sys.argv[1])
else:
    print '\n run this script with: \n > python mac/scheme_TwoSlowProtons.py <target A> \n\n'
    exit(0)

dm          = TEG2dm()
FileName    = "NoCTofDATA_%s"% dm.Target(A)
scheme      = TSchemeDATA("no ctof","/Users/erezcohen/Desktop/DataMining",FileName,"T")


pMin = 0.3
pMax = 0.7
scheme.TwoSlowProtons( 2 , pMin , pMax ) # target-type = 2, momentum minimum and maximum
print "schemed in nuclear target, for 2 protons with momentum %.1f < p < %.1f..."%(pMin,pMax)





print "done"

