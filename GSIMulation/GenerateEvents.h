/**
 * \file GenerateEvents.h
 *
 * \ingroup GSIMulation
 * 
 * \brief Class def header for a class GenerateEvents
 *
 * @author erezcohen
 */

/** \addtogroup GSIMulation

    @{*/
#ifndef GENERATEEVENTS_H
#define GENERATEEVENTS_H

#include <iostream>
#include "MySoftwarePackage/myIncludes.h"
#include "MySoftwarePackage/TPlots.h"


#include <TSystem.h>
#include <TFile.h>
#include <TTree.h>
#include <TBranchElement.h>
#include <TROOT.h>
#include <TCanvas.h>
#include <TH1F.h>
#include <TH2F.h>
#include <TProfile.h>
#include <TPad.h>
#include <TStyle.h>
#include <TMultiGraph.h>
#include <TGraphErrors.h>
#include <TLegend.h>
#include <TPaveStats.h>
#include <TChain.h>
#include <TBranch.h>
#include <TLeaf.h>
#include <TMath.h>
#include <TCut.h>

#include <TGClient.h>
#include <TCanvas.h>
#include <TF1.h>
#include <TRandom.h>
#include <TGButton.h>
#include <TGFrame.h>
#include <TRootEmbeddedCanvas.h>
#include <RQ_OBJECT.h>
#include "TApplication.h"
#include "TGButtonGroup.h"
#include "TGFileDialog.h"
#include "TGNumberEntry.h"
#include "TGTextEntry.h"
#include "TGLabel.h"
#include "TText.h"

#include <unistd.h>
#include <TRandom3.h>
#include <ctime>
#include "TEG2dm.h"

/**
   \class GenerateEvents
   User defined class GenerateEvents ... these comments are used to generate
   doxygen documentation!
 */
class GenerateEvents: public myIncludes{

public:

    ~GenerateEvents(){}

    GenerateEvents ( TString fPath = "" , Int_t fRunNumber = 1 , Int_t fdebug = 1 );

    Int_t                   DoGenerate ( TString Type = "(e,e'pp)"
                                        , bool DoGetRootFile = true
                                        , bool DoGenTextFile = false
                                        , TString BaryonName = "p"
                                        , bool DoReeNFromTree = false
                                        , bool DoReeNFromDist = false
                                        , bool DoFlateeN = false);
    
    Int_t          DoGenerateRun_eepp ( Int_t run = 1
                                       , bool DoGetRootFile = true
                                       , bool DoGenTextFile = false);
    
    Int_t                        DoGenerate_eepp_from_eep ( Int_t run=1);
    Int_t   DoGenerate_eepp_from_eep_SingleParameterSigma ( Int_t run=1);
    Int_t                   Generate_eepp_from_3dGaussian ( Int_t run=1);

    void          SetMyInputChain_eep ();
    void         SetRootTreeAddresses ();
    void                    SetLimits ( Float_t , Float_t , Float_t , Float_t );
    void          SetHistThetaHistMag ( TH1F * , TH1F * );
    void           Set_eep_Parameters ( Float_t , Float_t , Float_t , Float_t , Float_t , Float_t , Float_t , Float_t );
    void Set_eep_Parameters_MeanXYZ_Sigma (Float_t, Float_t, Float_t, Float_t );
    
    void                 Set_eeN_tree ( TTree * feeNTree) { eeNTree = feeNTree;};
    void              OutputInfo2File ();
    void             OutPutToTextFile ( const int, TVector3*, int*, float*, int*);
    void            AddInputChain_eep (TString ChainOption="300<p(miss)<600 MeV/c");
    void            SetInputChain_eep ();
    void        ReleaseInputChain_eep ();
    void                    InitEvent ();
    void                      InitRun ();
    void   SetAcceptedEventsPmissBins ( float fPmiss3Mag );
    void   SetEventsLossIn10PmissBins ( float fPmiss3Mag , bool fAcceptEvent );
    int  GrabEntryInUnfilledPmissBins ( );
    int             FindWhichPmissBin ( float fPmiss3Mag );
    int           FindWhichPmiss10Bin ( float fPmiss3Mag );
    bool           AllPmissBinsFilled ();
    
    
    // simple setters
    void                     SetNRand ( Int_t fNRand = 1 )                { NRand = fNRand; };
    void                   SetNPTheta ( Int_t fNPTheta = 10 )             { NPTheta = fNPTheta; };
    void                   SetNeTheta ( Int_t fNeTheta = 10 )             { NeTheta = fNeTheta; };
    void         Use_protonAcceptacne ( bool fDo_pAcceptance = false )    {Do_pAcceptance = fDo_pAcceptance;};
    void           SetDo_PrecFiducial ( bool fDo_PrecFiducial = false )   {Do_PrecFiducial = fDo_PrecFiducial;};
    void             SetDo_PrecMinCut ( bool fDo_PrecMinCut = false )     {Do_PrecMinCut = fDo_PrecMinCut;};
    void Use_PrecResolution ( bool fDoPrecResolution = true , float fPrecResolution = 0.020 ) { DoPrecResolution = fDoPrecResolution; PrecResolution = fPrecResolution;} ;
    void         Set_protonAcceptacne ( TH3F * h)                         { h_protonAcceptance = h; };
    void               ComputeWeights ();
    void   MapInputEntriesInPmissBins ();
    
    // more complicated setters
    void                 SetNgenMax ( int fNgenMAX = 10000 )               { NgenMAX = fNgenMAX; };
    
    // set the desired number of events when the simulation ends in 5 Pmiss bins
    void      SetNeventsPerPmissBin ( int NWantedPmissBin0=100 , int NWantedPmissBin1=100 , int NWantedPmissBin2=100 , int NWantedPmissBin3=100 , int NWantedPmissBin4=100 ){
        NWantedPmissBins[0]=NWantedPmissBin0 ;
        NWantedPmissBins[1]=NWantedPmissBin1 ;
        NWantedPmissBins[2]=NWantedPmissBin2 ;
        NWantedPmissBins[3]=NWantedPmissBin3 ;
        NWantedPmissBins[4]=NWantedPmissBin4 ;
    };

    
    void         SetNAcceptedEvents ( int fNWantedEvents=100 ) { NWantedEvents=fNWantedEvents ;};
    
    void               SetPmissBins () {
        float fPmissBins[5][2] = { {0.3,0.45}, {0.45,0.55}, {0.55,0.65}, {0.65,0.75}, {0.75,1.0} };
        for (int i=0;i<5;i++){
            for (int j=0;j<2;j++){
                PmissBins[i][j]=fPmissBins[i][j];
            }
        }
        if (debug>5){
            for (int i=0;i<5;i++){
                Printf("PmissBin %d: %.2f < p(miss) < %.2f GeV/c",i,PmissBins[i][0],PmissBins[i][1]);
            }
        }
    } ;
    
    void        Set10PmissBins () {
        float fsmall10PmissBins[10][2] = { {0.3,0.4},{0.4,0.5},{0.5,0.6},{0.6,0.7},{0.7,0.8},{0.8,0.9},{0.9,1.0}};
        for (int i=0;i<10;i++){
            for (int j=0;j<2;j++){
                small10PmissBins[i][j]=fsmall10PmissBins[i][j];
            }
        }
    } ;

    ofstream    TextFile , OutRunNumberFile , RunsInfoFile;
    
    TChain      * InputT;
    
    TFile       * RootFile;
    TTree       * RootTree , * eeNTree;

    TRandom3    * gRandom;
 
    bool        Do_pAcceptance , Do_PrecFiducial, Do_PrecMinCut, AcceptEvent;
    bool        DoPrecResolution;
    
    
    Int_t       RunNumber   , Nevents   , NAcceptedEvents,  NWantedEvents;
    Int_t       NRand       , NPTheta   , NeTheta,  entry,  InputNentries;
    // maximal total number of generated events
    Int_t       NgenMAX;
    // accepted number of events in 5 Pmiss bins
    Int_t       NWantedPmissBins[5];
    Int_t       NAcceptedPmissBins[5];
    std::vector<int> EntriesInPmissBins[5];
    // in 10 small Pmiss bins
    Int_t       NGen10PmissBins[10], NAcc10PmissBins[10];
    Int_t       NLoss10PmissBins[10];
    // -- - -- -- - --- - -- - -- - -- -- -- -- -- --- -- - -- - -
    
    Float_t     Q2      , Xb            , PoverQ    , Mmiss;
    Float_t     ThetaPQ , theta_miss_q   , ThetaPmissPrecoil;
    Float_t     theta_Pmiss , phi_Pmiss;
    Float_t     theta_e ;
    Float_t     MeanX   , MeanY, MeanZ, SigmaX, SigmaY, SigmaZ, Sigma;
    Float_t     a1      , a2 , b1  , b2  ;
    Float_t     Pmin    , Pmax  , Thetamin  , Thetamax;
    Float_t     Pmiss3Mag   , pcmX      , pcmY          , pcmT      , pcmZ  ;
    Float_t     Theta       , Mott      , DipoleFF2                 , rooWeight;
    Float_t     q_Phi, Pmiss_theta, Pmiss_phi;

    const Float_t Ebeam = 5.014 , e2 = 1; // sqaure of e-charge in e-charge units (for simplcity)

    Float_t     Pe[3]       , Pe_size;                                              // electron
    Float_t     Ep[2]       , Rproton[2][3] , Pproton[2][3] ,   Pproton_size[2];    // Proton
    Float_t     Pm[2][3]    , Pm_size[2];                                           // Proton missing momentum magnitude
    Float_t     q[3]        , q_size;                                               // q momentum transfer
    Float_t     PmissBins[5][2], small10PmissBins[10][2];
    Float_t     PrecResolution;
    
    TVector3    e                          ,       Pp1                     ,   Pp2             , Precoil;
    TVector3    Rp1                        ,       Rp2;                                                    // proton vertex
    TVector3    q3Vector                   ,       Pcm                     ,   Pmiss;
    TVector3    q3Vector_in_Pmiss_q_system ,       Pmiss_in_Pmiss_q_system ,   Pcm_in_Pmiss_q_system   , Precoil_in_Pmiss_q_system;
    TVector3    q_q_sys                    ,       Pmiss_q_sys             ,   Pcm_q_sys;

    TLorentzVector  Proton  ,       Prec    ,   q4Vector        , m2N       , miss , Pmiss4vec, Plead4vec;

    TString     Path , RunsInfoFileName , txtFilename , rootFilename , runsFilename;
    
    
    TH1F        * histMag , * histTheta;
    TH3F        * h_protonAcceptance;
    
    TEG2dm      * eg2dm;
    time_t      now ;
    tm          * dt;

    
    vector<Int_t>       pFiducCut     ;
    vector<TVector3>    pVertex   ;
    
    
};

#endif
/** @} */ // end of doxygen group 

