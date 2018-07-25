'''
    usage:
    ---------
    python mac/simulation_analysis/simulation_analysis_with_Nattempts_binomPval.py -nruns=10000
'''


import sys; sys.path.insert(0,'/Users/erezcohen/larlite/UserDev/CLASEG2DataMining/EG2DataMiningPackage/mac/'); sys.path.insert(0,'../notebooks/')
from cm_tools import *


sims = pd.read_csv('/Users/erezcohen/Desktop/DataMining/Analysis_DATA/ppSRCcm/random_parameters_results/Ntimes10_NoCut_OrTrees_Nattempts_results.csv',nrows=flags.NumberOfRuns)
print 'loaded',len(sims),'runs in sims sample'

binom_p = 1./3 # average approximate acceptance

sims=sims[sims['parameters_reconstructed_well']=='True']
sims.fillna(0.0,inplace=True)


print "adding 'Pval_binom_test_Nsucsseses', 'Pval_pcmXYZ_binom_...', and 'PvalTotal_binom_...' colums"
sims['Pval_binom_test_Nsucsseses'] = 0.0
for target in targets: #{
    sims['Pval_pcmXYZ_binom_'+target] = 0.0
    sims['PvalTotal_binom_'+target] = 0.0
#}
for i in range(len(sims)):#{
    run = sims['run'].iloc[i]
    NentriesSimRun , Nattempts =  sims['NentriesSimRun'].iloc[i]/100, sims['Nattempts'].iloc[i]/100
    binom_test_Pval = binom_test( x=NentriesSimRun ,n=Nattempts , p=binom_p )
    sims.set_value(i , 'Pval_binom_test_Nsucsseses', binom_test_Pval )
#    if sims['NentriesSimRun'].iloc[i]>50000 and sims['Pval_binom_test_Nsucsseses'].iloc[i]>1.e-10: print "sims['Pval_binom_test_Nsucsseses'].iloc[i]>1e-10! ",sims['Pval_binom_test_Nsucsseses'].iloc[i]
    for target in targets: #{
        sims.set_value(i,'Pval_pcmXYZ_binom_'+target
                       ,Fisher_combination_Pvals([ binom_test_Pval , sims['ks_Pval_pcmX_pcmY_pcmZ_'+target].iloc[i]]))
                       
        sims.set_value(i,'PvalTotal_binom_'+target
                       ,Fisher_combination_Pvals([ binom_test_Pval , sims['ks_PvalTotal_'+target].iloc[i]]))
#        if i%((len(sims))/10)==0:#{
#            print 'ks_Pval_pcmX_pcmY_pcmZ_'+target,':',sims['ks_Pval_pcmX_pcmY_pcmZ_'+target].iloc[i]
#            print 'Pval_pcmXYZ_binom_'+target,':',Fisher_combination_Pvals([ binom_test_Pval , sims['ks_PvalTotal_'+target].iloc[i]])
#        #}
    #}
    #    if i%((len(sims))/10)==0 or Nattempts>500:#{
    if run==104155:#{
        print 'run',run
        if sims['NentriesSimRun'].iloc[i]>50000 and binom_test_Pval>1.e-10: #{
            print 'weird case:',Nattempts , binom_test_Pval
    #}
        else:#{
            print_line()
            print i , ',' , sims['NentriesSimRun'].iloc[i] , sims['Nattempts'].iloc[i] , binom_test_Pval
            print "sims['Pval_binom_test_Nsucsseses'].iloc[i]:",sims['Pval_binom_test_Nsucsseses'].iloc[i]
        #}
    #}
#}
print 'finished combining Pvalues of Nattepmts and KS'

sims.to_csv('/Users/erezcohen/Desktop/DataMining/Analysis_DATA/ppSRCcm/random_parameters_results/OrTrees_BinomTest_results_binom_p_%.2f.csv'%binom_p)
print_filename('/Users/erezcohen/Desktop/DataMining/Analysis_DATA/ppSRCcm/random_parameters_results/OrTrees_BinomTest_results_binom_p_%.2f.csv'%binom_p,"output file")

print 'done.'