/**
 * \file T3pSimulation.h
 *
 * \ingroup EG2DataMiningPackage
 * 
 * \brief Class def header for a class T3pSimulation
 *
 * @author erezcohen
 */

/** \addtogroup EG2DataMiningPackage

    @{*/
#ifndef T3PSIMULATION_H
#define T3PSIMULATION_H

#include <iostream>
#include "TEG2dm.h"
#include "TCalcPhysVarsEG2.h"
#include "TRandom3.h"
#include "MySoftwarePackage/ppElastic.h"
/**
   \class T3pSimulation
   User defined class T3pSimulation ... these comments are used to generate
   doxygen documentation!
 */
class T3pSimulation: public TEG2dm, public TCalculations{

public:

    TPlots    plot;
    TAnalysis analysis;
    TCalculations calculations;
    ppElastic pp_elastic;
    
    TRandom3  rand;
    TCalcPhysVarsEG2 calcEG2;
    TTree   * OutTree;

    
    TF1     * SRCk4Tail;
    TH1F    * hCFG ;
    TH2F    * h_q , * h_ppElastic;
    
    Int_t       binEcm      , Np;
    
    Float_t     Xb          , Q2 ;
    Float_t     PpX[3]      , PpY[3]    , PpZ[3];
    Float_t     p_over_q    , theta_pq  ;
    Float_t     q_phi       , q_theta   , Pmiss_phi;
    Float_t     thetaMiss23 , phiMiss23;
    Float_t     Theta_cm    , Phi_cm    , Mpp;

    Double_t    Px  , Py    , Pz    , Pp    ,   Ecm ;
    
    vector<TVector3>   p3vec;
    
    TLorentzVector e , q , struck_p , p_knocked , p1_ppPair , pcm_ppPair , p2_ppPair;
    TLorentzVector p_knocked_r , p1_ppPair_r , p2_ppPair_r;
    TLorentzVector Pcm , Plead , Pmiss , Prec;
    TLorentzVector p1_pk_cm , p1_p1_pk_cm , pk_p1_pk_cm;

    std::vector<TLorentzVector> protons;

    
    
    /// Default constructor
    T3pSimulation(){}
    T3pSimulation( TTree * fOutTree );
    
    ~T3pSimulation(){}

    // GETs

    
    // SETs
    void         SetOutTree ( TTree * fOutTree ) {OutTree = fOutTree;};
    void Set_ppElasticHisto ( TH2F * h ) {h_ppElastic = h;};
  
    
    void    ImpMomentumDist ( bool DoPlot){SRCk4Tail = calculations.CFGMomentumDist(DoPlot);}
    void        Imp_q_Histo ( TH2F * h , bool DoPlot = false );
    void Imp_ppElasticHisto ( bool DoPlot = false );

    void        InitOutTree ();
    void              Gen_q ();
    void       Gen_struck_p ();
    void         q_struck_p ();
    void         Gen_ppPair ();
    void p_rescatter_ppPair ();
    void          PrintDATA ( int);
    void    RunInteractions ( int Ninteractions = 0 , bool DoPrint = false );
    void    ComputePhysVars ( );
    void          InitEvent ();
    void      q_Pmiss_frame ();



};

#endif
/** @} */ // end of doxygen group

