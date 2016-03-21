from ROOT import TSchemeDATA

scheme = TSchemeDATA("data","/Users/erezcohen/Desktop/DataMining","DATA_C12","T")



DoSchemeSRC     = True
DoScheme3pSRC   = False







if DoSchemeSRC:
    
    scheme.SRCPmissXb( 2 , 1.0 ) # target-type = 2, Bjorken x > 1.1
    print 'schemed for SRC in nuclear target (1 > p(miss) > 0.3 GeV/c) and Xb > 1.0'

if DoScheme3pSRC:
    
    scheme.SRCPmissXb( 2 , 1.0 , 3 , 5 ,"3p")
    print 'schemed for ppp-SRC in nuclear target (1 > p(miss) > 0.3 GeV/c) , Xb > 1.0 and 5 > Np > 3'

else:
    
    print 'not scheming...'



print "done"

