from definitions import *
from cm_tools import *
'''
    usage:
    ----------
    python mac/mix_ppSRC.py -A12
    '''

variables = [ 'Xb'
             ,  'Prec.Px()' , 'Prec.Py()' , 'Prec.Pz()','Prec.P()'
             ,'Pmiss.Px()' , 'Pmiss.Py()' , 'Pmiss.Pz()','Pmiss.P()'
             ,'pcmX'
             ]

ana = TAnalysisEG2( path+"/AnaFiles" , "Ana_ppSRCCut_DATA_%s"%dm.Target(A) , ROOT.TCut() )
anarr = tree2array( ana.GetTree() , branches=variables )

mixd_filename = path+"/AnaFiles/Ana_ppSRCCut_mixed_%s.csv"%dm.Target(A)


i,mixed_counter = 0,0
for i in range(len(anarr)-1):
    i=i+1
    if i%20==0: print 'taking p(miss)',i,',so far written',mixed_counter,'mixed p(miss)+p(recoil)'
    
    PmissX = anarr[i]['Pmiss.Px()']
    PmissY = anarr[i]['Pmiss.Py()']
    PmissZ = anarr[i]['Pmiss.Pz()']
    Pmiss = np.sqrt(PmissX*PmissX + PmissY*PmissY + PmissZ*PmissZ)


    for j in range(i+1,len(anarr)-1):
        mixed_counter += 1

        PrecX = anarr[j]['Prec.Px()']
        PrecY = anarr[j]['Prec.Py()']
        PrecZ = anarr[j]['Prec.Pz()']
        Prec = np.sqrt(PrecX*PrecX + PrecY*PrecY + PrecZ*PrecZ)


        pcmX = PmissX + PrecX
        pcmY = PmissY + PrecY
        pcmZ = PmissZ + PrecZ
        pcm = np.sqrt(pcmX*pcmX + pcmY*pcmY + pcmZ*pcmZ)


        prelX = 0.5*(PmissX - PrecX)
        prelY = 0.5*(PmissY - PrecY)
        prelZ = 0.5*(PmissZ - PrecZ)
        prel = np.sqrt(prelX*prelX + prelY*prelY + prelZ*prelZ)


        mixed = pd.DataFrame({
                     'Pmiss':Pmiss
                     ,'Precoil':Prec
                     ,'Original_pcmX':anarr[i]['pcmX']
                     ,'pcmX':pcmX
                     ,'pcmY':pcmY
                     ,'pcmZ':pcmZ
                     ,'pcm':pcm
                     ,'prelX':prelX
                     ,'prelY':prelY
                     ,'prelZ':prelZ
                     ,'prel':prel
                     }
                     ,index=[mixed_counter])
        stream_dataframe_to_file( mixed , mixd_filename )

print_filename( mixd_filename , "output file - mixed p(miss)+p(recoil)")
