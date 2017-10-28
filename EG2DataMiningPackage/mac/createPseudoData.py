from definitions import *
from cm_tools import *
'''
    usage:
    ---------------
    
    python mac/createPseudoData.py --option=SingleRun -r3
    python mac/createPseudoData.py --option=MultipleRuns -nruns=10
'''

# create a sample of pseudo-data which is ~ similar to the measured data


PseudoDataPath = "/Users/erezcohen/Desktop/DataMining/Analysis_DATA/ppSRCcm/PseudoData/"

hpars = dict({
             'target name':'C',
             'my target name':'C12',
             
             # flags
             # -- - - -- -- --- -- - -- - -- - - --- - -- - -
             'do random entry':True,
             'do proton acceptance':True,
             'do p(rec)>0.35 cut':True,
             'do p(rec) FV cuts':True,
             'NRand':1,

             # generation, pre-CLAS
             # -- - - -- -- --- -- - -- - -- - - --- - -- - -
             'run':flags.run,
             'mean(x)':0.0,
             'mean(y)':0.0,
             'sigma(t)':0.143,
             'mean(z)':0.13,
             'sigma(z)':0.15,
             
             # accepted, post-CLAS
             # -- - - -- -- --- -- - -- - -- - - --- - -- - -
             'N(accepted)':266, # the number of events in C(e,e'pp) data
             })

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
            destination = PseudoDataPath+file_name
            print 'copying ',source_to_cp,'to',destination
            shutil.copyfile(source_to_cp, destination)
        #}
    #}
#}
# - - -- - - -- - - -- -- - -- --- -- - - --- - -- - -- -- -- -- - --- -

print_important( "done "+hpars['target name']+"(e,e'pp) simulation")
