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
    
    // Tako Test
    TFile* fout;
    TTree* tree;
    std::vector<TLorentzVector> vec1;
    void Close ();
    // ------- Tako Test

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
    Float_t Theta       , Mott      , DipoleFF2      , rooWeight;
    const Float_t Ebeam = 5.009 , e2 = 1; // sqaure of e-charge in e-charge units (for simplcity)
    
    Double_t k0         , kCMmag    , Px    , Py    ,Pz ;
    
    Float_t             Pmiss3Mag   , pcmX          , pcmY          , pcmT      , pcmZ          ;
    Float_t             TpMiss      , m_A_1         , E_p_init      , M_p_init  , pq            ;
    vector<Float_t>     alpha       , pEdep         , pCTOF         , Tp        , proton_angle  ;
    vector<Int_t>       pCTOFCut    , pFiducCut     , pFiducCut_g;
    
    
    TVector3            Pbeam       , Pe        , Pe_g;
    TVector3            * NMom      , * P1Mom   , * P2Mom           , * e3Vector;
    TVector3            PmRctLab3   , eVertex   ;
    std::vector<TVector3>    p3vec       , p3vec_g   , pVertex   ;
    
    
    
    TLorentzVector      Beam        , e         , e_g       ,  p    , Wmiss     , kCM   , WmissWithCm , WmissCmEps;
    TLorentzVector      Wtilde      , pA       ,  pA_Np_1;
    TLorentzVector      q           , q_g       , NucleonAtRest     , TargetAtRest  ;
    TLorentzVector      Plead       , Plead_g   , Pmiss     , Pmiss_g , Pcm   , Prec , PcmFinalState;
    TLorentzVector      PmissRct    , Nlead     , Nmiss     ;
    std::vector<TLorentzVector>  protons , protons_g , protonsLab;

    
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

