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

using namespace std;
/**
   \class TCalcPhysVarsEG2
   User defined class TCalcPhysVarsEG2 ... these comments are used to generate
   doxygen documentation!
 */
class TCalcPhysVarsEG2 : public TEG2dm{

public:

    TString DataType    , Path;
    TString InFileName  , InTreeName;
    TString OutFileName , OutTreeName;
    
    TFile   * InFile    , * OutFile;
    TTree   * InTree    , * OutTree;
    TPlots  plot;
    
    int     Nentries    , Entry;
    
    
    
    
    // PARTICLES....
    Int_t   targ_type   , A;
    Int_t   Np          , Nn;
    Int_t   P_cut[20]   , P_PID[20]  ;             //positive particles
    
    Float_t Xb          , Q2        , Nu        , W;
    Float_t PpX[20]     , PpY[20]   , PpZ[20]   ;  //proton momentum
    Float_t Px_e        , Py_e      , Pz_e      , X_e     ,   Y_e     ,   Z_e   ;
    Float_t alpha_q     , alpha[20] , sum_alpha;
    Float_t p_over_q    , theta_pq  ;
    Float_t q_phi       , q_theta   , Pmiss_phi;
    Float_t Emiss       , Mmiss;
    Float_t mA          , CoulombDeltaE         , A_over_mA;
    Float_t uns_CTOF[20];
    
    vector<Float_t>    pMag;
    
    
    
    TVector3    q3vec   , eVertex;
    TVector3    uns_p3vec[20];
    TVector3    Plead   , Pmiss     , Pcm       , Prec;
    
    vector<TVector3>   p3vec   , pVertex   ;
    
    
    
    
    
    TLorentzVector  q   , TargetAtRest;
    vector<TLorentzVector> Uprotons , protons ;

    
    
    
    
    
    /// Default constructor
    TCalcPhysVarsEG2    (){}
    TCalcPhysVarsEG2    (TTree * fInTree, TTree * fOutTree, int fA = 12, TString fDataType = "data" );

 
    /// Default destructor
    ~TCalcPhysVarsEG2(){}

    
    
    // GETs
    
    
    // SETs
    void      SetDataType (TString type){DataType = type;};
    void          SetPath (TString path){Path = path;};
    void        SetInTree (TTree * tree){InTree = tree;};
    void       SetOutTree (TTree * tree){OutTree = tree;};

    
    
    
    void    InitInputTree ();
    void   InitOutputTree ();
    void      InitGlobals ();
    void        InitEvent ();
    
    
    void  AcquireNucleons (int entry);
    void     sort_protons ();
    vector<size_t> sort_pMag (const vector<float> &v);
    vector<size_t> sort_pMag (const vector<TVector3> &v);
    
    
    
};

#endif
/** @} */ // end of doxygen group 

