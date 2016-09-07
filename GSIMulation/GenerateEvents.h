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

/**
   \class GenerateEvents
   User defined class GenerateEvents ... these comments are used to generate
   doxygen documentation!
 */
class GenerateEvents{

public:

//    GenerateEvents(){}
    ~GenerateEvents(){}

    GenerateEvents( TString fPath = "" , Int_t fRunNumber = 1 , Int_t fdebug = 1 );

    Int_t DoGenerate( TString Type = "(e,e'pp)"
                     , bool DoGetRootFile = true
                     , bool DoGenTextFile = false
                     , TString BaryonName = "p"
                     , bool DoReeNFromTree = false
                     , bool DoReeNFromDist = false
                     , bool DoFlateeN = false);
    
    void       SetRootTreeAddresses ();
    void                  SetLimits ( Float_t , Float_t , Float_t , Float_t );
    void        SetHistThetaHistMag ( TH1F * , TH1F * );
    void         Set_eep_Parameters ( Float_t , Float_t , Float_t , Float_t , Float_t );
    void               Set_eeN_tree ( TTree * feeNTree) { eeNTree = feeNTree;};
    void            OutputInfo2File ();
    void           OutPutToTextFile ( const int, TVector3*, int*, float*, int*);
    void                   SetNRand ( Int_t fNRand = 1 )    { NRand = fNRand; };
    void                 SetNPTheta ( Int_t fNPTheta = 10 ) { NPTheta = fNPTheta; };
    
    

    ofstream TextFile , OutRunNumberFile , RunsInfoFile;
    
    TChain  * InputT;
    
    TFile   * RootFile;
    TTree   * RootTree , * eeNTree;

    TRandom3 * gRandom;
    
    // Physical variables
    Float_t     Q2      , Xb            , PoverQ    , Mmiss;
    Float_t     ThetaPQ , ThetaPmissQ   , ThetaPmissPrecoil;
    Float_t     Mott    , DipoleFF      , Weight;
    Float_t     theta_e ;
    Float_t     SigmaT  , SigmaL_a1 , SigmaL_a2 , ShiftL_a1 , ShiftL_a2;
    Float_t     Pmin , Pmax , Thetamin , Thetamax;

    
    
    
    TVector3 e                          ,       Pp1                     ,   Pp2             , Precoil;
    TVector3 Rp1                        ,       Rp2;                                                    // proton vertex
    TVector3 q3Vector                   ,       Pcm                     ,   Pmiss;
    TVector3 q3Vector_in_Pmiss_q_system ,       Pmiss_in_Pmiss_q_system ,   Pcm_in_Pmiss_q_system;
    TVector3 q_q_sys                    ,       Pmiss_q_sys             ,   Pcm_q_sys;

    TLorentzVector  Proton                  ,   q4Vector        , m2N       , miss;

    
    
    Int_t       RunNumber   , Nevents;
    Int_t       NRand       , NPTheta   , debug;

    TString     Path , RunsInfoFileName , txtFilename , rootFilename , runsFilename;
    
    
    
    
    TH1F        * histMag , * histTheta;
    
    time_t  now ;
    tm      * dt;

};

#endif
/** @} */ // end of doxygen group 

