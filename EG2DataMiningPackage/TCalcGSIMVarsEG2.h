/**
 * \file TCalcGSIMVarsEG2.h
 *
 * \ingroup EG2DataMiningPackage
 *
 * \brief Class def header for a class TCalcGSIMVarsEG2
 *
 * @author erezcohen
 */

/** \addtogroup EG2DataMiningPackage
 
 @{*/
#ifndef TCALCGSIMVARSEG2_H
#define TCALCGSIMVARSEG2_H

#include <iostream>
#include "TEG2dm.h"
#include "TRandom3.h"
#include <algorithm>

using namespace std;

/**
 \class TCalcGSIMVarsEG2
 User defined class TCalcGSIMVarsEG2 ... these comments are used to generate
 doxygen documentation!
 */
class TCalcGSIMVarsEG2: public TEG2dm, public TCalculations{
    
public:
    
    /// Default constructor
    TCalcGSIMVarsEG2    (){};
    TCalcGSIMVarsEG2    (TTree * fInTree, TTree * fOutTree, int fA = 12, TString fDataType = "data" , TString fFrameName = "q(z) - Pmiss(x-z) frame", int fdebug = 1);
    TCalcGSIMVarsEG2    (TTree * fInTree, TString fOutFileName, int fA = 12, TString fDataType = "data" , TString fFrameName = "q(z) - Pmiss(x-z) frame", int fdebug = 1);
    
    
    /// Default destructor
    ~TCalcGSIMVarsEG2(){};

    
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
    Int_t   Number      , particle_id[10];
    Int_t   Number_g    , particle_id_g[10];
    Int_t   targ_type   , A             , Np_g;
    Int_t   Np          , Ntotal        , Nnegative;
    Int_t   NpBack      , NpCumulative  , NpCumulativeSRC;
    Int_t   uns_pCut[20], uns_pID[20];
    Int_t   ppSRCcut, ppSRCcutFiducial, eep_in_ppSRCcut;
    vector<Int_t>       pCTOFCut    , pFiducCut     , pFiducCut_g   , pInDeadRegions;
   
    
    const Float_t Ebeam = 5.014 , e2 = 1; // sqaure of e-charge in e-charge units (for simplcity)
    // for GSIM: generated
    Float_t Xb_g            , Q2_g        , Nu_g        ;
    Float_t Momentum[20]    , Momentumx[20]   , Momentumy[20]   , Momentumz[20];
    Float_t Momentum_g[20]  , Momentumx_g[20] , Momentumy_g[20] , Momentumz_g[20];
    
    
    Float_t PpX_g[20]       , PpY_g[20]   , PpZ_g[20]   ;   // proton momentum and vertex
    Float_t Px_e_g          , Py_e_g      , Pz_e_g      , X_e_g     ,   Y_e_g     ,   Z_e_g   ;   // electron
    
    // reconstructed
    Float_t Xb          , Q2        , Nu        , XbMoving, W;
    Float_t PpX[20]     , PpY[20]   , PpZ[20]   , Xp[20]  , Yp[20]  ,   Zp[20];   // proton momentum and vertex
    Float_t Px_e        , Py_e      , Pz_e      , X_e     , Y_e     ,   Z_e   ;   // electron
    Float_t alpha_q     , sum_alpha;
    Float_t p_over_q    , theta_pq  ;
    Float_t q_phi       , q_theta   , Pmiss_phi , Pmiss_theta;
    Float_t q_phi_g     , q_theta_g , Pmiss_phi_g, Pmiss_theta_g;
    Float_t Emiss       , Mmiss     , Mmiss2    , Mmiss3    ;
    Float_t Emiss_g     ;
    Float_t mA          , CoulombDeltaE         , A_over_mA ;
    Float_t Mrec        , Trec      , theta_rec_q  , theta_miss_q;   // protons kinetic energy, recoil mass & kinetic energy
    Float_t uns_pCTOF[20], uns_pEdep[20]     ;
    Float_t N_Px[20]    , N_Py[20]  , N_Pz[20];                 // for raw data
    Float_t Theta       , Mott      , DipoleFF2     , rooWeight;
    // for 3N SRC studies
    Float_t thetaMiss23 , phiMiss23 , thetaLeadRec  , theta23;
    Float_t m23         , T23       , k23           , E_R;
    Float_t q_          , k_t       , beta_1        , beta_2    , m_S;
    Float_t W2_3N       , alpha_3N;
    
    Float_t theta23_g;
    Float_t m23_g         , T23_g       , k23_g           , E_R_g;
    Float_t q_g_          , k_t_g       , beta_1_g        , beta_2_g    , m_S_g;
    Float_t W2_3N_g       , alpha_3N_g;
    
    
    Float_t             Pmiss3Mag   , pcmX          , pcmY          , pcmT      , pcmZ          ;
    Float_t             prelX       , prelY         , prelZ         ;
    Float_t             TpMiss      , m_A_1         , E_p_init      , M_p_init  , pq            ;
    Float_t             pLab_phi    , pLab_theta    , OpeningAngle;
    vector<Float_t>     alpha       , pEdep         , pCTOF         , Tp        , proton_angle  ;
    
    
    Double_t            k0          , kCMmag        , Px            , Py        , Pz ;

    
    TVector3            Pbeam       , Pe        , Pe_g;
    TVector3            * NMom      , * P1Mom   , * P2Mom           , * e3Vector;
    TVector3            PmRctLab3   , eVertex   ;
    std::vector<TVector3>    p3vec       , p3vec_g   , pVertex   ;
    
    
    
    TLorentzVector      Beam        , e         , e_g       ,  p    , Wmiss     , kCM   , WmissWithCm , WmissCmEps;
    TLorentzVector      Wtilde      , pA       ,  pA_Np_1;
    TLorentzVector      q           , q_g       , NucleonAtRest     , TargetAtRest  ;
    TLorentzVector      Plead       , Plead_g   , Pmiss     , Pmiss_g , Pcm   , Prec , PcmFinalState;
    TLorentzVector      PmissRct    , Nlead     , Nmiss     ;
    TLorentzVector      p_S         , p_S_g;
    std::vector<TLorentzVector>  protons , protons_g , protonsLab;
    
    
    
    
    
    // GETs
    
    
    // SETs
    void      SetDataType (TString type){DataType = type;};
    void          SetPath (TString path){Path = path;};
    void        SetInTree (TTree * tree){InTree = tree;};
    void       SetOutTree (TTree * tree){OutTree = tree;};
    void   SetOutFileName (TString name){OutFileName = name;};
    void       SetOutTree (TString fOutFileName){ OutFile = TFile::Open(fOutFileName,"RECREATE"); OutTree = new TTree("anaTree","physical variables");};
    void     SetFrameName (TString name){FrameName = name;};
    void            Setk0 (Float_t  fk0){k0 = fk0;};
    void         SetDebug (int d)       {debug = d;};
    void          SetNp_g (int fNp_g)   {Np_g = fNp_g;};
    
    void         InitInputTree ();
    void        InitOutputTree ();
    void           InitGlobals ();
    void             InitEvent ();
    void               SetCuts ();
    void       ComputePhysVars (int entry);
    void          loop_protons ();
    void        loop_protons_g ();
    vector<size_t>   sort_pMag (const vector<TVector3> &v);
    void       ChangeAxesFrame ();
    void         q_Pmiss_frame ();
    void         Pmiss_q_frame ();
    void          p23Randomize ();
    void          p12Randomize ();
    void        ComputeWeights ();
    void             PrintData (int);
    
    
};

#endif
/** @} */ // end of doxygen group

