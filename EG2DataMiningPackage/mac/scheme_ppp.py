from ROOT import TSchemeDATA

# options are: "data" / "no ctof"
DataType  = "no ctof"




if DataType == "data":
    FileName    = "DATA_C12"
else :
    FileName    = "NoCTofDATA_C12"


scheme = TSchemeDATA(DataType,"/Users/erezcohen/Desktop/DataMining",FileName,"T")



DoSchemeSRC     = True
DoScheme3pSRC   = False







if DoSchemeSRC:
    
    scheme.SRCPmissXb( 2 , 1.0 ) # target-type = 2, Bjorken x > 1.0
    print 'schemed for SRC in nuclear target (1 > p(miss) > 0.3 GeV/c) and Xb > 1.0'

if DoScheme3pSRC:
    
    scheme.SRCPmissXb( 2 , 1.0 , 3 , 5 ,"3p")
    print 'schemed for ppp-SRC in nuclear target (1 > p(miss) > 0.3 GeV/c) , Xb > 1.0 and 5 > Np > 3'




print "done"

