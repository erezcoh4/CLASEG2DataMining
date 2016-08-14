import ROOT,os, sys , math , os.path , math
from ROOT import TEG2dm , TSchemeDATA
sys.path.insert(0, '/Users/erezcohen/larlite/UserDev/mySoftware/MySoftwarePackage/mac')
sys.path.insert(0, '/home/erez/larlite/UserDev/mySoftware/MySoftwarePackage/mac')
import input_flags
flags = input_flags.get_args()

'''
    usage:
    --------
    > python scheme_file.py -A12 -werez --operation='scheme SRCPmissXb'
'''

if flags.worker == "erez":
    path = "/Users/erezcohen/Desktop/DataMining"

elif flags.worker == "helion":
    path = "/home/erez/DataMining"

scheme = TSchemeDATA("data",path,"DATA_C12","T")




if (flags.option=="SRCPmissXb"):
    
    scheme.SRCPmissXb( 2 , 1.1 ) # target-type = 2, Bjorken x > 1.1
    print 'schemed for SRC in nuclear target (1 > p(miss) > 0.3 GeV/c) and Xb > 1.1'


else:
    
    print 'not scheming...'



print "done"

