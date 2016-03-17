/**
 * \file TEG2dm.h
 *
 * \ingroup EG2DataMiningPackage
 * 
 * \brief Class def header for a class TEG2dm
 *
 * @author erezcohen
 */

/** \addtogroup EG2DataMiningPackage

    @{*/
#ifndef TEG2DM_H
#define TEG2DM_H

#include <iostream>
#include "MySoftwarePackage/TPlots.h"
#include "MySoftwarePackage/TCalculations.h"
#include "MySoftwarePackage/TAnalysis.h"
#define r2d TMath::RadToDeg()

/**
   \class TEG2dm
   User defined class TEG2dm ... these comments are used to generate
   doxygen documentation!
    This class will be used for every EG2 datamining analysis:
    It should have the basic data-mining methods as energy and coulomb corrections for particles momenta
 
 */
class TEG2dm{

public:

  /// Default constructor
  TEG2dm(){}

  /// Default destructor
  ~TEG2dm(){}
    
    
    
    
    // momentum corrections: energy loss and Coulomb corrections
    TVector3    EnergyLossCorrrection ( TVector3 );
    TVector3        CoulombCorrection ( TVector3 , Float_t );
    TString            TargetAsString ( int, float *mA = 0 , float *CoulombDeltaE = 0);
    void    RotateVec_To_qPmiss_frame ( TVector3* , float , float , float);

    Float_t                LCfraction ( TLorentzVector , Float_t );

};

#endif
/** @} */ // end of doxygen group 

