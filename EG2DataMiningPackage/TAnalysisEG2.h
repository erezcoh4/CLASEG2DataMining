/**
 * \file TAnalysisEG2.h
 *
 * \ingroup EG2DataMiningPackage
 * 
 * \brief Class def header for a class TAnalysisEG2
 *
 * @author erezcohen
 */

/** \addtogroup EG2DataMiningPackage

    @{*/
#ifndef TANALYSISEG2_H
#define TANALYSISEG2_H

#include <iostream>
#include "TEG2dm.h"


/**
   \class TAnalysisEG2
   User defined class TAnalysisEG2 ... these comments are used to generate
   doxygen documentation!
 */
class TAnalysisEG2 : public TPlots , public TAnalysis , public TEG2dm{

public:

    
    TRandom3 rand;
    TString Path , InFileName;
    TFile * InFile;
    TTree * Tree;
    Double_t Pp , Px , Py , Pz;
    Float_t  q_phi , q_theta , Pmiss_phi;
    TVector3 p3vec;
    
    /// Default constructor
    TAnalysisEG2 (){    SetSRCCuts();   }
    TAnalysisEG2 ( TString fPath , TString fInFileName , TCut MainCut = "0 <= Xb" );
    TAnalysisEG2 ( TString fInFileName , TCut MainCut = "0 <= Xb" );
    
    
    
    /// Default destructor
    ~TAnalysisEG2(){}
    
    
    void            CloseFile (){   InFile->Close();    File->Close(); };
    
    
    
    // GETs
    TString           GetPath (){return Path;};

    
    
    // SETs
    void        SetInFileName (TString name){InFileName = name;};
    void            SetInFile (TFile * file){InFile = file;};
    void              SetTree (TTree * tree){Tree = tree;};
    void              SetPath (TString path){Path = path;};
    
    
    
    
    
    // cuts
    TCutG   * pEdepCut[3], * ppNothing_alpha12_vs_XbCut;
    TCut    alpha12_vs_XbCutDIS , alpha12_vs_XbCutCorrelation;
    TCut    cutXb       , cutPmiss          , cutPmT        , cutThetaPQ    , cutPoverQ     , cutMmiss2;
    TCut    cutMmiss    , cutPlead          , cutPrec       , cutP1         , cutP2         , cutP3 ;
    TCut    cutWmiss    ;
    TCut    cutAngles2p , cutAngles3p       , cutSRCNoPm;
    TCut    pCTOFCut[3] , p1EdepCut         , p1CTOFCut     , ppEdepCut     , ppCTOFCut     , pppEdepCut    ;
    TCut    pppCTOFCut  ;
    TCut    cutSRC      , eepFinalCut       , cut1pSRC      , ppSRCCut      ;
    TCut    pppSRCCut   , pppSRCMmiss       , Final3pCut    ;
    TCut    pppRandomBkg, pppCut            , pppCutPmT     , pppCutPmTMm   ;
    TCut    Sim3pSRCCut , FinalSim3pSRCCut  , Sim3pWmissCut ;
    TCut    Mix3pSRCCut , FinalMix3pSRCCut  , Mix3pPmT      , Mix3pPmTMm    ;
    TCut    eepInSRCCut , eeppInSRCCut      , PrecFiducial;
    
    void         SetSRCCuts ( TCut MainCut = "1.05 <= Xb");
    void        PrintInCuts ();
    
    
    // rooFit
    std::vector<Double_t>    RooFitCM (Float_t PmissMin, Float_t PmissMax, bool DoWeight = false, bool PlotFits = false, TCanvas * c = nullptr, Int_t start_cd = 1 );
    vector<Float_t>       GetPcmEntry (int);
    vector<Float_t>   GetFullpppEvent (int, bool DoPrint = false);
    vector<Float_t>        GetGSIMEvt (int, bool DoPrint = false);
    vector<Float_t>     GetGSIMeep_pp_Evt (int, bool DoPrint = false);
    void                    MixEvents (TTree *, bool DoPrint = false);
};

#endif
/** @} */ // end of doxygen group 

