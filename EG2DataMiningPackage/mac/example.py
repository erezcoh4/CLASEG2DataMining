import sys
from ROOT import gSystem
gSystem.Load("libEG2DataMining_EG2DataMiningPackage")
from ROOT import sample

try:

    print "PyROOT recognized your class %s" % str(sample)

except NameError:

    print "Failed importing EG2DataMiningPackage..."

sys.exit(0)

