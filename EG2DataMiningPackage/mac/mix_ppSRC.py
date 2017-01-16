from definitions import *
from cm_tools import *
'''
    usage:
    ----------
    python mac/mix_ppSRC.py -A12
    '''

variables = [ 'Xb'
             ,'protonsLab[0].Px()'  ,'protonsLab[0].Py()'   ,'protonsLab[0].Pz()'
             ,'protonsLab[1].Px()'  ,'protonsLab[1].Py()'   ,'protonsLab[1].Pz()'
             ,'e.Px()'              ,'e.Py()'               ,'e.Pz()'
             ,'q.Px()'      , 'q.Py()'      , 'q.Pz()'      ,'q.P()'
             ,'Prec.Px()'   , 'Prec.Py()'   , 'Prec.Pz()'   ,'Prec.P()'
             ,'Pmiss.Px()'  , 'Pmiss.Py()'  , 'Pmiss.Pz()'  ,'Pmiss.P()'
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
    
    q = ROOT.TVector3( -anarr[i]['e.Px()'] , -anarr[i]['e.Py()'] , 5.009-anarr[i]['e.Pz()'])
    Pmiss = ROOT.TVector3( anarr[i]['protonsLab[0].Px()']-q.X() ,  anarr[i]['protonsLab[0].Py()']-q.Y() ,  anarr[i]['protonsLab[0].Pz()']-q.Z() )

    q_phi       = q.Phi()
    Pmiss_theta = Pmiss.Theta()
    Pmiss_phi   = Pmiss.Phi()


    for j in range(i+1,len(anarr)-1):
        mixed_counter += 1
        Prec = ROOT.TVector3( anarr[j]['protonsLab[1].Px()'] ,  anarr[j]['protonsLab[1].Py()'] ,  anarr[j]['protonsLab[1].Pz()'] )


        Pcm = Pmiss + Prec
        Prel = 0.5*(Pmiss - Prec)

        # rotate into the p(miss)-q frame
        Pcm.RotateZ(-Pmiss_phi)
        Pcm.RotateY(-Pmiss_theta)
        Pcm.RotateZ(-q_phi)

        # rotate into the p(miss)-q frame
        Prel.RotateZ(-Pmiss_phi)
        Prel.RotateY(-Pmiss_theta)
        Prel.RotateZ(-q_phi)


        mixed = pd.DataFrame({
                     'Pmiss':   Pmiss.Mag()
                     ,'Precoil':Prec.Mag()
                     ,'pcmX':   Pcm.X()
                     ,'pcmY':   Pcm.Y()
                     ,'pcmZ':   Pcm.Z()
                     ,'pcm':    Pcm.Mag()
                     ,'prelX':  Prel.X()
                     ,'prelY':  Prel.Y()
                     ,'prelZ':  Prel.Z()
                     ,'prel':   Prel.Mag()
                     }
                     ,index=[mixed_counter])
        stream_dataframe_to_file( mixed , mixd_filename )

print_filename( mixd_filename , "output file - mixed p(miss)+p(recoil)")
