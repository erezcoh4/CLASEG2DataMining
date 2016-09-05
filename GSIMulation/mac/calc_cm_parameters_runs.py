import ROOT , sys , datetime
from ROOT import GenerateEvents
import numpy as np
sys.path.insert(0, '../../mySoftware/MySoftwarePackage/mac')
import input_flags
flags = input_flags.get_args()
import pandas as pd

path = "/Users/erezcohen/Desktop/DataMining/GSIM"
RunsInfoFileName = path+"/eg_txtfiles/Info_runs.csv"
RunsInfoFile = open(RunsInfoFileName,'wb')
RunsInfoFile.write( "run,time,SigmaT,SigmaL_a1,SigmaL_a2,ShiftL_a1,ShiftL_a2\n" )


run         = 100 # starting run number
SigmaT      = np.linspace(0.1   ,0.2    ,5)
SigmaL_a1   = np.linspace(0.13  ,0.23   ,3)
SigmaL_a2   = np.linspace(0.    ,0.3    ,3)
ShiftL_a1   = np.linspace(0.    ,1.0    ,3)
ShiftL_a2   = np.linspace(-0.1  ,0.1    ,3)


if (flags.verbose > 1): print "running %d runs "%int(len(SigmaT)*len(SigmaL_a1)*len(SigmaL_a2)*len(ShiftL_a1)*len(ShiftL_a2))

for sigT in SigmaT:
    for sigLa1 in SigmaL_a1:
        for sigLa2 in SigmaL_a2:
            for shfLa1 in ShiftL_a1:
                for shfLa2 in ShiftL_a2:

                    run = run+1
    
                    par_str = "%d"%run+","+str(datetime.datetime.now().strftime("%Y%B%d"))+",%f"%sigT+",%f"%sigLa1+",%f"%sigLa2+",%f"%shfLa1+",%f"%shfLa2+"\n"
                    if (flags.verbose > 1):
                        print "generating run " + par_str
                    RunsInfoFile.write( par_str )

                    gen_events = GenerateEvents( path , run , flags.verbose )

                    gen_events.SetNRand( 1 )

                    gen_events.Set_eep_Parameters( sigT , sigLa1 , sigLa2 , shfLa1 , shfLa2 )

                    gen_events.DoGenerate( "(e,e'pp)" )


RunsInfoFile.close()
print "done... see \n",RunsInfoFileName
data=pd.read_csv(RunsInfoFileName)
print data



