from ROOT import TSchemeDATA

scheme = TSchemeDATA("data","/Users/erezcohen/Desktop/DataMining","DATA_C12","T")



DoSchemeSRC     = False
DoScheme2pSRC   = True







if DoSchemeSRC:
    
    scheme.SRCPmissXb( 2 , 1.1 ) # target-type = 2, Bjorken x > 1.1
    print 'schemed for SRC in nuclear target (1 > p(miss) > 0.3 GeV/c) and Xb > 1.1'

if DoScheme2pSRC:
    
    scheme.SRCPmissXb( 2 , 1.1 , 2 , 2) # target-type = 2, Bjorken x > 1.1
    print 'schemed for ppSRC in nuclear target (1 > p(miss) > 0.3 GeV/c) and Xb > 1.1'

else:
    
    print 'not scheming...'



print "done"

