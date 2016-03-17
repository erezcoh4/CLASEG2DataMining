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
class TAnalysisEG2 : public TPlots {

public:

    
    
    TString Path , InFileName;
    
    
    
    /// Default constructor
    TAnalysisEG2 (){}
    TAnalysisEG2 (TString fInFileName);
    
    
    
    /// Default destructor
    ~TAnalysisEG2(){}
    
    
    
    
    
    
    // GETs
    
    
    // SETs
    void    SetInFileName (TString name){InFileName = name;};
    void          SetPath (TString path){Path = path;};
    
    
};

#endif
/** @} */ // end of doxygen group 

