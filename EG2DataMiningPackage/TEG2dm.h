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
#define d2r TMath::DegToRad()

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
    
    
    
    Double_t ChangePhiToPhiLab(Double_t Phi) { // change the axis with phi angle (-180,180) to sit in (-30,330)
        return ( (Phi < -30.) ? (Phi + 360.) : ( (Phi > 330.) ? (Phi - 360.) : Phi ) );
    }

    
    // momentum corrections: energy loss and Coulomb corrections
    TVector3    EnergyLossCorrrection ( TVector3 );
    TVector3        CoulombCorrection ( TVector3 , Float_t );
    TString                    Target ( int );
    TString            TargetAsString ( int, float *mA = 0 , float *CoulombDeltaE = 0);
    void           RotVec2_q_Pm_Frame ( TVector3* , float , float , float);
    void       RotVec_from_q_Pm_Frame ( TVector3* , float , float , float);
    void           RotVec2_Pm_q_Frame ( TVector3* , float , float , float);
    void       RotVec_from_Pm_q_Frame ( TVector3* , float , float , float);

    Float_t                LCfraction ( TLorentzVector , Float_t ); // for a vector in the q-frame
    Float_t                LCfraction ( TLorentzVector , TLorentzVector , Float_t ); // for a general vector + q

    
    TCutG                  * pEdepCut (int);
    TCutG          * alpha12_vs_XbCut ();
    
    Int_t              protonFiducial ( TVector3 , int debug = 1 );


    // proton fiducial parameters
    const Double_t P0_a[6][2] = { {25     ,25      }, {25      ,24.8096}, {25    ,24.8758}, {25      ,25      }, {25      ,25      }, {25      ,25     } };
    const Double_t P1_a[6][2] = { {-12    ,-11.9735}, {-12     ,-8     }, {-12   ,-8     }, {-12     ,-12     }, {-12     ,-8.52574}, {-12     ,-8     } };
    const Double_t P2_a[6][2] = { {1.64476,0.803484}, {1.51915 ,0.85143}, {1.1095,1.01249}, {0.977829,0.910994}, {0.955366,0.682825}, {0.969146,0.88846} };
    const Double_t P3_a[6][2] = { {4.4    ,4.40024 }, {4.4     ,4.8    }, {4.4   ,4.8    }, {4.4     ,4.4     }, {4.4     ,4.79866 }, {4.4     ,4.8    } };
    
    const Double_t P0_b[6][2] = { {4        ,2.53606 }, {4  ,2.65468  }, {2.78427 ,3.17084}, {3.58539,2.47156 }, {3.32277  ,2.42349 }, {4      ,2.64394} };
    const Double_t P1_b[6][2] = { {2        ,0.442034}, {2  ,0.201149 }, {2       ,1.27519}, {1.38233,1.76076 }, {0.0410601,1.25399 }, {2      ,0.15892} };
    const Double_t P2_b[6][2] = { {-0.978469,-2      }, {-2 ,-0.179631}, {-1.73543,-2     }, {-2     ,-1.89436}, {-0.953828,-2      }, {-2     ,-2     } };
    const Double_t P3_b[6][2] = { {0.5      ,1.02806 }, {0.5,1.6      }, {0.5     ,0.5    }, {0.5    ,1.03961 }, {0.5      ,0.815707}, {1.08576,1.31013} };
    
    const Double_t P0_theta[6] = { 7.00823 , 5.5      , 7.06596   , 6.32763 , 5.5     , 5.5      };
    const Double_t P1_theta[6] = { 0.207249, 0.1      , 0.127764  , 0.1     , 0.211012, 0.281549 };
    const Double_t P2_theta[6] = { 0.169287, 0.506354 , -0.0663754, 0.221727, 0.640963, 0.358452 };
    const Double_t P3_theta[6] = { 0.1     , 0.1      , 0.100003  , 0.1     , 0.1     , 0.1      };
    const Double_t P4_theta[6] = { 0.1     , 3.30779  , 4.499     , 5.30981 , 3.20347 , 0.776161 };
    const Double_t P5_theta[6] = { -0.1    , -0.651811, -3.1793   , -3.3461 , -1.10808, -0.462045};
    
    Double_t P0 , P1 , P2 , P3 , P4 , P5 , mom , a , b ;

};

#endif
/** @} */ // end of doxygen group 

