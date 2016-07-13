import ROOT , os , sys
from ROOT import TSchemeDATA , TEG2dm



'''
    july-12, 2016
    scheme meytal events w/ leading n and two p,
    to look only on the recoiling two protons....
'''

dm          = TEG2dm()
FileName    = "Meytal_npp_DATA_C12"
scheme      = TSchemeDATA("(e,e'npp)","/Users/erezcohen/Desktop/DataMining",FileName,"Tree")


pMin = 0.3
pMax = 0.7
n_pMin = 1.0  # neutron minimum momentum = 1.1 GeV/c
scheme.TwoSlowProtons_npp( n_pMin, pMin , pMax )
print "schemed in nuclear target, for 2 protons with momentum %.1f < p < %.1f..."%(pMin,pMax)





print "done"

