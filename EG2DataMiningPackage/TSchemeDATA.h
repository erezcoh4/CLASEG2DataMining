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
class TSchemeDATA{
    
public:
    
    
    TString DataType    , SchemeType;
    TString Path;
    TString InFileName  , InTreeName;
    TString OutFileName , OutTreeName;
    
    TFile   * InFile    , * OutFile;
    TTree   * InTree    , * OutTree;
    TPlots  plot;
    
    
    int     Nentries    ;
    
    
    
    
    
    // PARTICLES....
    Int_t   TargetType  , targ_type  , NpGood;
    Int_t   Np          , Nn         , Ntotal;
    Int_t   P_cut[20]   , P_PID[20]  ;          //positive particles
    
    Float_t Xb          , XbMin;
    Float_t PpX[20]     , PpY[20]   , PpZ[20];  //proton momentum
    Float_t Px_e        , Py_e      , Pz_e   ;
    Float_t N_Px[20]    , N_Py[20]  , N_Pz[20]; // for raw data

    
    TVector3    * q     , * Plead   , * proton, Pmiss;
    TVector3    *NMom   , * P1Mom   , * P2Mom;
    
    
    /// Default constructor
    TSchemeDATA(){}
    TSchemeDATA(TString,TString,TString,TString);
    
    /// Default destructor
    ~TSchemeDATA(){}
    
    
    
    
    // GETs
    
    
    // SETs
    void      SetDataType (TString type){DataType = type;};
    void    SetSchemeType (TString type){SchemeType = type;};
    void          SetPath (TString path){Path = path;};
    void    SetInFileName (TString name){InFileName = name;};
    void   SetOutFileName (TString name){OutFileName = name;};
    void    SetInTreeName (TString name){InTreeName = name;};
    void   SetOutTreeName (TString name){OutTreeName = name;};
    
    
    
    
    // Scheming methods
    void       LoadInTree ();
    void    CreateOutTree ();
    void     WriteOutFile ();

    
    void protons_from_nuclei ();
    void       SRCPmissXb (int fTargetType = 2 , float fXbMin = 1.05, int fNpMin = 1, int fNpMax= 5, TString name="");
    void   TwoSlowProtons (int fTargetType = 2 , float fpMin = 0.2 , float fpMax = 3. );
    void   TwoSlowProtons_ppp (int fTargetType = 2 , float fpMin = 0.2 , float fpMax = 3. );
    void   TwoSlowProtons_npp (float fn_pMin = 1.1 , float fpMin = 0.2 , float fpMax = 3. );
    
    
    void     SchemeOnTCut (TString , TString , TString , TString , TCut);
    
    
};

#endif
/** @} */ // end of doxygen group

