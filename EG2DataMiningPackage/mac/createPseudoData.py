from definitions import *
from cm_tools import *
'''
    usage:
    ---------------
    
    python mac/createPseudoData.py
'''

# create a sample of pseudo-data which is ~ similar to the measured data




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
             'run':3,
             'mean(x)':0.0,
             'mean(y)':0.0,
             'sigma(t)':0.143,
             'mean(z)':0.13,
             'sigma(z)':0.15,
             
             # accepted, post-CLAS
             # -- - - -- -- --- -- - -- - -- - - --- - -- - -
             'N(accepted)':266, # the number of events in C(e,e'pp) data
             })

generate_with_fixed_parameters(
                               hpars=hpars,
                               debug=flags.verbose,
                               )


print_important( "done "+hpars['target name']+"(e,e'pp) simulation")
