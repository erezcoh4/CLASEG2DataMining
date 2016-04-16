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

    
    
    TString Path , InFileName;
    TFile * InFile;
    TTree * Tree;
    
    /// Default constructor
    TAnalysisEG2 (){    SetSRCCuts();   }
    TAnalysisEG2 ( TString fInFileName , TCut XbCut = "1.2 <= Xb" );
    
    
    
    /// Default destructor
    ~TAnalysisEG2(){}
    
    
    
    
    
    
    // GETs
    TString           GetPath (){return Path;};

    
    
    // SETs
    void        SetInFileName (TString name){InFileName = name;};
    void            SetInFile (TFile * file){InFile = file;};
    void              SetTree (TTree * tree){Tree = tree;};
    void              SetPath (TString path){Path = path;};
    
    
    
    
    
    // cuts
    TCut    cutXb       , cutPmiss    , cutThetaPQ , cutPoverQ  , cutMmiss  , cutPlead  , cutPrec  , cutP1 , cutP2 , cutP3 , cutAngles2p , cutAngles3p;
    TCutG   * pEdepCut[3];
    TCut    pCTOFCut[3] , ppEdepCut   , ppCTOFCut   , pppEdepCut , pppCTOFCut  ;
    TCut    cutSRC      , ppSRCCut    , pppSRCCut   , Final3pCut , Sim3pSRCCut;
    
    void         SetSRCCuts ( TCut XbCut = "1.2 <= Xb");
    void        PrintInCuts ();
    
    
    // rooFit
    TMatrix        RooFitCM (Float_t PmissMin, Float_t PmissMax);
    vector<Float_t> GetPcmEntry (int);
};

#endif
/** @} */ // end of doxygen group 

