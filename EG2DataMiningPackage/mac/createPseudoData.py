from definitions import *
from cm_tools import *
'''
    usage:
    ---------------
    
    python mac/createPseudoData.py --option=SingleRun --DataType=C12 -r5
    python mac/createPseudoData.py --option=MultipleRuns -nruns=10
'''

# create a sample of pseudo-data which is ~ similar to the measured data


PseudoDataPath = "/Users/erezcohen/Desktop/DataMining/Analysis_DATA/ppSRCcm/PseudoData/"


hpars_C = dict({'target name':'C', 'my target name':'C12',
               'sigma(t)':0.143,
               'mean(z)':0.130, 'sigma(z)':0.150,
               # -- - - -- -- --- -- - -- - -- - - --- - -- - -
               'N(accepted)':266, # the number of events in A(e,e'pp) data - accepted, post-CLAS
               })
hpars_Pb = dict({'target name':'Pb', 'my target name':'Pb208',
               'sigma(t)':0.156,
               'mean(z)':0.180,'sigma(z)':0.17,
               # -- - - -- -- --- -- - -- - -- - - --- - -- - -
               'N(accepted)':45 # accepted, post-CLAS
               })

if flags.DataType=='C12': hpars=hpars_C
if flags.DataType=='Pb208': hpars=hpars_Pb

# flags
# -- - - -- -- --- -- - -- - -- - - --- - -- - -
hpars['do random entry']=True
hpars['do proton acceptance']=True
hpars['do p(rec)>0.35 cut']=True
hpars['do p(rec) FV cuts']=True
hpars['NRand']=1
# generation, pre-CLAS
# -- - - -- -- --- -- - -- - -- - - --- - -- - -
hpars['run']=flags.run
hpars['mean(x)']=0.0
hpars['mean(y)']=0.0

# - - -- - - -- - - -- -- - -- --- -- - - --- - -- - -- -- -- -- - --- -
if flags.option=="SingleRun":#{
    generate_with_fixed_parameters(
                               hpars=hpars,
                               debug=flags.verbose,
                               )
#}
# - - -- - - -- - - -- -- - -- --- -- - - --- - -- - -- -- -- -- - --- -



# - - -- - - -- - - -- -- - -- --- -- - - --- - -- - -- -- -- -- - --- -
elif flags.option=="MultipleRuns":#{
    Nruns = flags.NumberOfRuns
    print 'simulating',Nruns,'runs'
    for i in range(Nruns):#{
        run = 1000 + i
        print 'run',run
        hpars['run'] = run
        Nevents,file_name = generate_with_fixed_parameters(
                                       hpars=hpars,
                                       debug=flags.verbose,
                                       )
        if Nevents>1:#{
            source_to_cp = "/Users/erezcohen/Desktop/DataMining/Analysis_DATA/ppSRCcm/eg_rootfiles/"+file_name
            destination = PseudoDataPath + hpars['my target name'] + "/" + file_name
            print 'copying ',source_to_cp,'to',destination
            shutil.copyfile(source_to_cp, destination)
        #}
    #}
#}
# - - -- - - -- - - -- -- - -- --- -- - - --- - -- - -- -- -- -- - --- -

print_important( "done "+hpars['target name']+"(e,e'pp) simulation")
