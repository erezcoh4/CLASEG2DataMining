/**
 * \file TCalcPhysVarsEG2.h
 *
 * \ingroup EG2DataMiningPackage
 * 
 * \brief Class def header for a class TCalcPhysVarsEG2
 *
 * @author erezcohen
 */

/** \addtogroup EG2DataMiningPackage

    @{*/
#ifndef TCALCPHYSVARSEG2_H
#define TCALCPHYSVARSEG2_H

#include <iostream>
#include "TEG2dm.h"
#include "TRandom3.h"
#include <algorithm> 

using namespace std;
/**
   \class TCalcPhysVarsEG2
   User defined class TCalcPhysVarsEG2 ... these comments are used to generate
   doxygen documentation!
 */
class TCalcPhysVarsEG2 : public TEG2dm, public TCalculations{

public:

    TString DataType    , Path;
    TString InFileName  , InTreeName;
    TString OutFileName , OutTreeName;
    
    TFile   * InFile    , * OutFile;
    TTree   * InTree    , * OutTree;
    TPlots  plot;
    TRandom3  rand;
    
    int     Nentries    , Entry         , debug;
    TString FrameName   ;          // prefered frame of axes to work in....
    
    
    
    // PARTICLES....
    Int_t   targ_type   , A             , Np_g;
    Int_t   Np          , Ntotal        , Nnegative;
    Int_t   NpBack      , NpCumulative  , NpCumulativeSRC;
    Int_t   uns_pCut[20], uns_pID[20];
    
    // for GSIM: generated
    Float_t Xb_g          , Q2_g        , Nu_g        ;
    Float_t PpX_g[20]     , PpY_g[20]   , PpZ_g[20]   ;   // proton momentum and vertex
    Float_t Px_e_g        , Py_e_g      , Pz_e_g      , X_e_g     ,   Y_e_g     ,   Z_e_g   ;   // electron

    // reconstructed
    Float_t Xb          , Q2        , Nu        , XbMoving, W;
    Float_t PpX[20]     , PpY[20]   , PpZ[20]   , Xp[20]  , Yp[20]  ,   Zp[20];   // proton momentum and vertex
    Float_t Px_e        , Py_e      , Pz_e      , X_e     , Y_e     ,   Z_e   ;   // electron
    Float_t alpha_q     , sum_alpha;
    Float_t p_over_q    , theta_pq  ;
    Float_t q_phi       , q_theta   , Pmiss_phi , Pmiss_theta;
    Float_t q_phi_g     , q_theta_g , Pmiss_phi_g, Pmiss_theta_g;
    Float_t Emiss       , Mmiss;
    Float_t mA          , CoulombDeltaE         , A_over_mA ;
    Float_t Mrec        , Trec      ;                           // protons kinetic energy, recoil mass & kinetic energy
    Float_t uns_pCTOF[20], uns_pEdep[20]     ;
    Float_t N_Px[20]    , N_Py[20]  , N_Pz[20];                 // for raw data
    Float_t thetaMiss23 , phiMiss23 , thetaLeadRec;
    Float_t Theta       , Mott      , DipoleFF      , rooWeight;
    const Float_t Ebeam = 5.009 , e2 = 1; // sqaure of e-charge in e-charge units (for simplcity)
    
    Double_t k0         , kCMmag    , Px    , Py    ,Pz;
    
    Float_t             Pmiss3Mag   , pcmX        , pcmY          , pcmZ          ;
    Float_t             TpMiss      , m_A_1         , E_p_init      , M_p_init  , pq;
    vector<Float_t>     alpha       , pEdep         , pCTOF         , Tp        , proton_angle;
    vector<Int_t>       pCTOFCut    , pFiducCut     , pFiducCut_g;
    
    
    TVector3            Pbeam       , Pe        , Pe_g;
    TVector3            * NMom      , * P1Mom   , * P2Mom           , * e3Vector;
    TVector3            PmRctLab3   , eVertex   ;
    vector<TVector3>    p3vec       , p3vec_g   , pVertex   ;
    
    
    
    TLorentzVector      Beam        , e         , e_g       ,  p    , Wmiss     , kCM   , WmissWithCm , WmissCmEps;
    TLorentzVector      Wtilde      , pA       ,  pA_Np_1;
    TLorentzVector      q           , q_g       , NucleonAtRest     , TargetAtRest  ;
    TLorentzVector      Plead       , Plead_g   , Pmiss     , Pmiss_g , Pcm   , Prec , PcmFinalState;
    TLorentzVector      PmissRct    , Nlead     , Nmiss     ;
    vector<TLorentzVector>  protons , protons_g , protonsLab;

    
    // delete Nov-1 (obselete)
//    // proton fiducial parameters
//    const Double_t P0_a[6][2] = { {25     ,25      }, {25      ,24.8096}, {25    ,24.8758}, {25      ,25      }, {25      ,25      }, {25      ,25     } };
//    const Double_t P1_a[6][2] = { {-12    ,-11.9735}, {-12     ,-8     }, {-12   ,-8     }, {-12     ,-12     }, {-12     ,-8.52574}, {-12     ,-8     } };
//    const Double_t P2_a[6][2] = { {1.64476,0.803484}, {1.51915 ,0.85143}, {1.1095,1.01249}, {0.977829,0.910994}, {0.955366,0.682825}, {0.969146,0.88846} };
//    const Double_t P3_a[6][2] = { {4.4    ,4.40024 }, {4.4     ,4.8    }, {4.4   ,4.8    }, {4.4     ,4.4     }, {4.4     ,4.79866 }, {4.4     ,4.8    } };
//    
//    const Double_t P0_b[6][2] = { {4        ,2.53606 }, {4  ,2.65468  }, {2.78427 ,3.17084}, {3.58539,2.47156 }, {3.32277  ,2.42349 }, {4      ,2.64394} };
//    const Double_t P1_b[6][2] = { {2        ,0.442034}, {2  ,0.201149 }, {2       ,1.27519}, {1.38233,1.76076 }, {0.0410601,1.25399 }, {2      ,0.15892} };
//    const Double_t P2_b[6][2] = { {-0.978469,-2      }, {-2 ,-0.179631}, {-1.73543,-2     }, {-2     ,-1.89436}, {-0.953828,-2      }, {-2     ,-2     } };
//    const Double_t P3_b[6][2] = { {0.5      ,1.02806 }, {0.5,1.6      }, {0.5     ,0.5    }, {0.5    ,1.03961 }, {0.5      ,0.815707}, {1.08576,1.31013} };
//    
//    const Double_t P0_theta[6] = { 7.00823 , 5.5      , 7.06596   , 6.32763 , 5.5     , 5.5      };
//    const Double_t P1_theta[6] = { 0.207249, 0.1      , 0.127764  , 0.1     , 0.211012, 0.281549 };
//    const Double_t P2_theta[6] = { 0.169287, 0.506354 , -0.0663754, 0.221727, 0.640963, 0.358452 };
//    const Double_t P3_theta[6] = { 0.1     , 0.1      , 0.100003  , 0.1     , 0.1     , 0.1      };
//    const Double_t P4_theta[6] = { 0.1     , 3.30779  , 4.499     , 5.30981 , 3.20347 , 0.776161 };
//    const Double_t P5_theta[6] = { -0.1    , -0.651811, -3.1793   , -3.3461 , -1.10808, -0.462045};
    
    /// Default constructor
    TCalcPhysVarsEG2    (){}
    TCalcPhysVarsEG2    (TTree * fInTree, TTree * fOutTree, int fA = 12, TString fDataType = "data" , TString fFrameName = "q(z) - Pmiss(x-z) frame", int fdebug = 1);

 
    /// Default destructor
    ~TCalcPhysVarsEG2(){}

    
    
    // GETs
    
    
    // SETs
    void      SetDataType (TString type){DataType = type;};
    void          SetPath (TString path){Path = path;};
    void        SetInTree (TTree * tree){InTree = tree;};
    void       SetOutTree (TTree * tree){OutTree = tree;};
    void     SetFrameName (TString name){FrameName = name;};
    void            Setk0 (Float_t  fk0){k0 = fk0;};
    void         SetDebug (int d)       {debug = d;};
    void          SetNp_g (int fNp_g)   {Np_g = fNp_g;};
//    Int_t  protonFiducial ( TVector3 );
    
    // initializations
    void    InitInputTree ();
    void   InitOutputTree ();
    void      InitGlobals ();
    void        InitEvent ();
    
    
    void  ComputePhysVars (int entry);
    void     loop_protons ();
    vector<size_t> sort_pMag (const vector<TVector3> &v);
    
    
    void ChangeAxesFrame ();
    void   q_Pmiss_frame ();
    void   Pmiss_q_frame ();
    
    void    p23Randomize ();
    void    p12Randomize ();
    
    void  ComputeWeights ();
    
    void       PrintData (int);
};

#endif
/** @} */ // end of doxygen group 

