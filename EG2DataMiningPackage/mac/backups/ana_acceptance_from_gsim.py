'''
    usage:
    --------
    python mac/ana_acceptance_from_gsim.py -r80 -var=pTheta_vs_pMag
'''

import ROOT ,os, sys , math
from ROOT import  TPlots
from rootpy.interactive import wait
sys.path.insert(0, '../../mySoftware/MySoftwarePackage/mac')
import GeneralPlot as gp, Initiation as init , input_flags
from root_numpy import root2array, tree2array , hist2array
from matplotlib import pyplot as plt
import numpy as np

init.createnewdir()
flags = input_flags.get_args()

FileName    = "Ana_GSIM_run%04d_eep"%flags.run
Path        = "/Users/erezcohen/Desktop/DataMining/AnaFiles"

ana = TPlots( Path + "/" + FileName + ".root" , "anaTree" )
T = tree2array(ana.GetTree(),branches=['protons[0].Theta()','protons[0].P()','protons_g[0].Theta()','protons_g[0].P()'])
if (flags.verbose>1): print "loaded tree into array"

#Px,Py,Pz,Px_g,Py_g,Pz_g = T['Px[0]'],T['Py[0]'],T['Pz[0]'],T['Px_g[0]'],T['Py_g[0]'],T['Pz_g[0]']
#Px = Px.astype('float')
#Py = Py.astype('float')
#Pz = Pz.astype('float')
#pMag    = np.sqrt(np.power(Px,2) + np.power(Py,2) + np.power(Pz,2))
#pTheta  = np.arctan2( Pz , np.sqrt(np.power(Px,2) + np.power(Py,2)) )
#Px_g = Px_g.astype('float')
#Py_g = Py_g.astype('float')
#Pz_g = Pz_g.astype('float')
#pMag_g      = np.sqrt(np.power(Px_g,2) + np.power(Py_g,2) + np.power(Pz_g,2))
#pTheta_g    = np.arctan2( Pz_g , np.sqrt(np.power(Px_g,2) + np.power(Py_g,2)) )

pMag  , pTheta   = T['protons[0].P()']  , T['protons[0].Theta()']
pMag  , pTheta   = pMag.astype('float') ,  pTheta.astype('float')

pMag_g, pTheta_g = T['protons_g[0].P()'], T['protons_g[0].Theta()']
pMag_g, pTheta_g = pMag_g.astype('float'),  pTheta_g.astype('float')


if (flags.verbose>1): print "loaded momenta"


if (flags.variable == "pX_vs_pY"):
    fig = gp.sns2d_with_projections( Px , Py , ['p(x)','p(y)'] , "hex")


if (flags.variable == "pTheta_vs_pMag"):
    bins = 10
#    hAccepted  = numpy.histogram2d( pMag , (180./3.1415)*pTheta , bins=bins )
#    hGenerated = numpy.histogram2d( pMag_g , (180./3.1415)*pTheta_g , bins=bins )

    fig = plt.figure(1)
    plt.subplot(2,1,1)
    hAccepted = plt.hist2d( pMag , (180./3.1415)*pTheta, bins=bins , norm=LogNorm())
    plt.colorbar()
    plt.title('reconstructed')
    plt.xlabel(r'|$\vec{p}$| [GeV/c]')
    plt.ylabel(r'$\theta_{p}$ [deg]')
    plt.subplot(2,1,2)
    hGenerated = plt.hist2d( pMag_g , (180./3.1415)*pTheta_g, bins=bins , norm=LogNorm() )
    plt.title('generated')
    plt.xlabel(r'|$\vec{p}$| [GeV/c]')
    plt.ylabel(r'$\theta_{p}$ [deg]')
    plt.colorbar()
    plt.show()

    hAcceptance = hAccepted/hGenerated
    fig = plt.figure(2)

#    fig = gp.sns2d_with_projections( pMag , (180./3.1415)*pTheta , [r'|$\vec{p}$| [GeV/c]',r'$\theta_{p}$ [deg]'] , "hex")
#    fig = gp.sns2d_with_projections( pMag_g , (180./3.1415)*pTheta_g , [r'generated |$\vec{p}$| [GeV/c]',r'generated $\theta_{p}$ [deg]'] , "hex")
