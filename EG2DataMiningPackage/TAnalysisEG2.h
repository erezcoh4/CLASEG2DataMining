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
class TAnalysisEG2 : public TPlots , public TAnalysis{

public:

    
    
    TString Path , InFileName;
    TFile * InFile;
    TTree * Tree;
    
    /// Default constructor
    TAnalysisEG2 (){    SetSRCCuts();   }
    TAnalysisEG2 ( TString fInFileName );
    
    
    
    /// Default destructor
    ~TAnalysisEG2(){}
    
    
    
    
    
    
    // GETs
    
    
    // SETs
    void    SetInFileName (TString name){InFileName = name;};
    void        SetInFile (TFile * file){InFile = file;};
    void          SetTree (TTree * tree){Tree = tree;};
    void          SetPath (TString path){Path = path;};
    
    
    
    // plots
    
    
    // cuts
    TCut    cutXb   ,   cutPmiss    ,   cutThetaPQ , cutPoverQ  , cutMmiss  , cutPlead  , cutPrec  , cutSRC;
    TCut    ppSRCCut;
    
    void      SetSRCCuts ();

    TMatrix  RooFitCM (Float_t PmissMin, Float_t PmissMax);
};

#endif
/** @} */ // end of doxygen group 

