import ROOT , os , sys
from ROOT import TSchemeDATA
from ROOT import TEG2dm

# options are: "data" / "no ctof"
if len(sys.argv)>1:
    A       = int(sys.argv[1])
else:
    print '\n run this script with: \n > python mac/scheme_ppp.py <target A> \n\n'
    exit(0)
DataType    = "no ctof"



dm          = TEG2dm()
if DataType == "data":
    FileName    = "DATA_%s"% dm.Target(A)
else :
    FileName    = "NoCTofDATA_%s"% dm.Target(A)


scheme = TSchemeDATA(DataType,"/Users/erezcohen/Desktop/DataMining",FileName,"T")



DoSchemeSRC     = True
DoScheme3pSRC   = False







if DoSchemeSRC:
    
    scheme.SRCPmissXb( 2 , 0.9 ) # target-type = 2, Bjorken x > 0.9
    print 'schemed for SRC in nuclear target (1 > p(miss) > 0.3 GeV/c) and Xb > 0.9'

if DoScheme3pSRC:
    
    scheme.SRCPmissXb( 2 , 1.0 , 3 , 5 ,"3p")
    print 'schemed for ppp-SRC in nuclear target (1 > p(miss) > 0.3 GeV/c) , Xb > 1.0 and 5 > Np > 3'




print "done"

