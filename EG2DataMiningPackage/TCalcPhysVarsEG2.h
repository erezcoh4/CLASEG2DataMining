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
    
    int     Nentries    , Entry;
    TString FrameName   ;          // prefered frame of axes to work in....
    
    
    
    // PARTICLES....
    Int_t   targ_type   , A;
    Int_t   Np          ;
    Int_t   uns_pCut[20], uns_pID[20];
    
    // for GSIM: generated
    Float_t Xb_g          , Q2_g        , Nu_g        ;
    Float_t PpX_g[20]     , PpY_g[20]   , PpZ_g[20]   ;   // proton momentum and vertex
    Float_t Px_e_g        , Py_e_g      , Pz_e_g      , X_e_g     ,   Y_e_g     ,   Z_e_g   ;   // electron

    // reconstructed
    Float_t Xb          , Q2        , Nu        , XbMoving;
    Float_t PpX[20]     , PpY[20]   , PpZ[20]   , Xp[20]  ,   Yp[20]  ,   Zp[20];   // proton momentum and vertex
    Float_t Px_e        , Py_e      , Pz_e      , X_e     ,   Y_e     ,   Z_e   ;   // electron
    Float_t alpha_q     , sum_alpha;
    Float_t p_over_q    , theta_pq  ;
    Float_t q_phi       , q_theta   , Pmiss_phi , Pmiss_theta;
    Float_t Emiss       , Mmiss;
    Float_t mA          , CoulombDeltaE         , A_over_mA ;
    Float_t Mrec        , Trec      ;             // protons kinetic energy, recoil mass & kinetic energy
    Float_t uns_pCTOF[20], uns_pEdep[20]     ;
    Float_t N_Px[20]    , N_Py[20]  , N_Pz[20]; // for raw data
    Float_t thetaMiss23 , phiMiss23;
    
    Double_t    pcmX    , pcmY      , pcmZ  ;
    
    Float_t             TpMiss      ;
    vector<Float_t>     alpha       , pEdep         , pCTOF         , Tp;
    vector<Int_t>       pCTOFCut    ;
    
    
    TVector3            Pbeam        , Pe;
    vector<TVector3>    p3vec        , pVertex   ;
    TLorentzVector      Beam         , e        ,  p;
    TLorentzVector      Wtilde       , pA       ,  pA_Np_1;

    
    
    
    TLorentzVector          q     , NucleonAtRest     , TargetAtRest  ,   Plead   , Pmiss     , Pcm       , Prec;
    vector<TLorentzVector>  protons ;

    
    
    
    
    
    /// Default constructor
    TCalcPhysVarsEG2    (){}
    TCalcPhysVarsEG2    (TTree * fInTree, TTree * fOutTree, int fA = 12, TString fDataType = "data" , TString fFrameName = "q(z) - Pmiss(x-z) frame");

 
    /// Default destructor
    ~TCalcPhysVarsEG2(){}

    
    
    // GETs
    
    
    // SETs
    void      SetDataType (TString type){DataType = type;};
    void          SetPath (TString path){Path = path;};
    void        SetInTree (TTree * tree){InTree = tree;};
    void       SetOutTree (TTree * tree){OutTree = tree;};
    void     SetFrameName (TString name){FrameName = name;};
    
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
    
    
    void       PrintData (int);
};

#endif
/** @} */ // end of doxygen group 

