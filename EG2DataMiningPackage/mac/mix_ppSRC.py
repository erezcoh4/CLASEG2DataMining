from definitions import *
from cm_tools import *
'''
    usage:
    ----------
    python mac/mix_ppSRC.py -A12
    '''

variables = [ 'Xb'
             ,'Prec.Px()'   , 'Prec.Py()'   , 'Prec.Pz()' ,'Prec.P()'
             ,'Pmiss.Px()'  , 'Pmiss.Py()'  , 'Pmiss.Pz()','Pmiss.P()'
             ,'q_phi'       , 'Pmiss_theta' , 'Pmiss_phi'
             ]

ana = TAnalysisEG2( path+"/AnaFiles" , "Ana_ppSRCCut_DATA_%s"%dm.Target(A) , ROOT.TCut() )
anarr = tree2array( ana.GetTree() , branches=variables )

mixd_filename = path+"/AnaFiles/Ana_ppSRCCut_mixed_%s.csv"%dm.Target(A)
print_filename( mixd_filename , "starting to plug into output file - mixed p(miss)+p(recoil)")


i,mixed_counter = 0,0
for i in range(len(anarr)-1):
    i=i+1
    if i%20==0: print 'taking p(miss)',i,',so far written',mixed_counter,'mixed p(miss)+p(recoil)'
    
#    PmissX = anarr[i]['Pmiss.Px()']
#    PmissY = anarr[i]['Pmiss.Py()']
#    PmissZ = anarr[i]['Pmiss.Pz()']
#    Pmiss = anarr[i]['Pmiss.P()']

    q_phi       = anarr[i]['q_phi']
    Pmiss_theta = anarr[i]['Pmiss_theta']
    Pmiss_phi   = anarr[i]['Pmiss_phi']

    # rotate into the lab frame
    Pmiss = ROOT.TVector3(anarr[i]['Pmiss.Px()'],anarr[i]['Pmiss.Py()'],anarr[i]['Pmiss.Pz()'])
    Pmiss.RotateZ(q_phi)
    Pmiss.RotateZ(Pmiss_phi)
    Pmiss.RotateY(Pmiss_theta)

    for j in range(i+1,len(anarr)-1):
        mixed_counter += 1

#        PrecX = anarr[j]['Prec.Px()']
#        PrecY = anarr[j]['Prec.Py()']
#        PrecZ = anarr[j]['Prec.Pz()']
        Prec = ROOT.TVector3(anarr[j]['Prec.Px()'],anarr[j]['Prec.Py()'],anarr[j]['Prec.Pz()'])

        # rotate into the lab frame
        Prec.RotateZ(q_phi)
        Prec.RotateZ(Pmiss_phi)
        Prec.RotateY(Pmiss_theta)


        Pcm = Pmiss + Prec
        Prel = 0.5*(Pmiss - Prec)
#        pcmX = PmissX + PrecX
#        pcmY = PmissY + PrecY
#        pcmZ = PmissZ + PrecZ
#        pcm = np.sqrt(pcmX*pcmX + pcmY*pcmY + pcmZ*pcmZ)
#        
#        prelX = 0.5*(PmissX - PrecX)
#        prelY = 0.5*(PmissY - PrecY)
#        prelZ = 0.5*(PmissZ - PrecZ)
#        prel = np.sqrt(prelX*prelX + prelY*prelY + prelZ*prelZ)

        # rotate back into the p(miss)-q frame
#        Pcm = ROOT.TVector3(pcmX,pcmY,pcmZ)
#        print 'pcmX before rotation:',Pcm.X()
        Pcm.RotateZ(-Pmiss_phi)
        Pcm.RotateY(-Pmiss_theta)
        Pcm.RotateZ(-q_phi)
#        print 'pcmX after rotation:',Pcm.X()

        # rotate back into the p(miss)-q frame
        Prel.RotateZ(-Pmiss_phi)
        Prel.RotateY(-Pmiss_theta)
        Prel.RotateZ(-q_phi)


        mixed = pd.DataFrame({
                     'Pmiss':Pmiss.Mag()
                     ,'Precoil':Prec.Mag()
#                     ,'Original_pcmX':anarr[i]['pcmX']
                     ,'pcmX':Pcm.X()
                     ,'pcmY':Pcm.Y()
                     ,'pcmZ':Pcm.Z()
                     ,'pcm':Pcm.Mag()
                     ,'prelX':Prel.X()
                     ,'prelY':Prel.Y()
                     ,'prelZ':Prel.Z()
                     ,'prel':Prel.Mag()
                     }
                     ,index=[mixed_counter])
        stream_dataframe_to_file( mixed , mixd_filename )

print_filename( mixd_filename , "output file - mixed p(miss)+p(recoil)")
