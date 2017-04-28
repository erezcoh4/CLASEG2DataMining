/**
 * \file TSchemeDATA.h
 *
 * \ingroup EG2DataMiningPackage
 *
 * \brief Class def header for a class TSchemeDATA
 *
 * @author erezcohen
 */

/** \addtogroup EG2DataMiningPackage
 
 @{*/
#ifndef TSCHEMEDATA_H
#define TSCHEMEDATA_H

#include <iostream>
#include "TEG2dm.h"

/**
 \class TSchemeDATA
 User defined class TSchemeDATA ... these comments are used to generate
 doxygen documentation!
 Scheme EG2 data....
 */
class TSchemeDATA : public TEG2dm{
    
public:
    
    
    TString DataType    , SchemeType;
    TString DataPath    , SchemedPath;
    TString InFileName  , InTreeName;
    TString OutFileName , OutTreeName;
    
    TFile   * InFile    , * OutFile;
    TTree   * InTree    , * OutTree;
    TPlots  plot;
    
    
    int     Nentries    , debug;
    
    
    
    
    
    // PARTICLES....
    Int_t   TargetType  , targ_type  , NpGood;
    Int_t   Np          , Nn         , Ntotal   , Npiminus;
    Int_t   P_cut[20]   , P_PID[20]  ;          //positive particles
    
    Float_t Xb          , XbMin;
    Float_t PpX[20]     , PpY[20]   , PpZ[20];  //proton momentum
    Float_t Px_e        , Py_e      , Pz_e   ;
    Float_t N_Px[20]    , N_Py[20]  , N_Pz[20]; // for raw data
    Float_t N_PathSC[20], N_TimeSC[20] , STT[20];
    Float_t mA          , CoulombDeltaE ;

    
    
//    TVector3    * q     , * Plead   , * proton, Pmiss , *negative_particle_momentum;
    TVector3    *NMom   , * P1Mom   , * P2Mom;
    
    TVector3        Pe;
    TLorentzVector  e, q, Plead, Pmiss, Beam;

    
    
    /// Default constructor
    TSchemeDATA (){}
    TSchemeDATA ( TString, TString, TString, TString, TString, Int_t fdebug = 1);
    
    /// Default destructor
    ~TSchemeDATA(){}
    
    
    
    
    // GETs
    
    
    // SETs
    void      SetDataType (TString type){DataType = type;};
    void    SetSchemeType (TString type){SchemeType = type;};
    void      SetDataPath (TString path){DataPath = path;};
    void   SetSchemedPath (TString path){SchemedPath = path;};
    void    SetInFileName (TString name){InFileName = name;};
    void   SetOutFileName (TString name){OutFileName = name;};
    void    SetInTreeName (TString name){InTreeName = name;};
    void   SetOutTreeName (TString name){OutTreeName = name;};
    void         SetDebug (int d)       {debug = d;};
    
    
    
    
    // Scheming methods
    void       LoadInTree ();
    void    CreateOutTree ();
    void     WriteOutFile ();

    
    void protons_from_nuclei ();
    void                    SRCXb (int fTargetType = 2 , float fXbMin = 1.05, int fNpMin = 1, int fNpMax= 5, TString name="" , Int_t A=12);
    void               SRCPmissXb (int fTargetType = 2 , float fXbMin = 1.05, int fNpMin = 1, int fNpMax= 5, TString name="" , Int_t A=12);
    void           TwoSlowProtons (int fTargetType = 2 , float fpMin = 0.2 , float fpMax = 3. );
    void       TwoSlowProtons_ppp (int fTargetType = 2 , float fpMin = 0.2 , float fpMax = 3. );
    void       TwoSlowProtons_npp (float fn_pMin = 1.1 , float fpMin = 0.2 , float fpMax = 3. );
    void TwoSlowProtons_piminus_p (int fTargetType = 2 , float fpMin = 0.2 , float fpMax = 3. );
    
    
    void     SchemeOnTCut (TString , TString , TString , TString , TCut);
    
    
};

#endif
/** @} */ // end of doxygen group

