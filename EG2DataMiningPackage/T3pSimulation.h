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
#include "TRandom3.h"
/**
   \class T3pSimulation
   User defined class T3pSimulation ... these comments are used to generate
   doxygen documentation!
 */
class T3pSimulation{

public:

    TPlots    plot;
    TAnalysis analysis;
    TCalculations calculations;
    TRandom3  rand;
    
    TTree   * OutTree;

    
    TF1     * SRCk4Tail;
    TH2F    * h_q , * h_ppElastic;
    
    
    Double_t    Px  , Py    , Pz    , Pp;
    
    TLorentzVector q , struck_p , p_knocked , p1_ppPair , pcm_ppPair , p2_ppPair;
    TLorentzVector p_knocked_r , p1_ppPair_r , p2_ppPair_r;
    TLorentzVector Pcm , Plead , Pmiss , Prec;
    std::vector<TLorentzVector> protons;

    Float_t     Theta_cm;
    Int_t       binEcm;
    
    
    /// Default constructor
    T3pSimulation(){}
    T3pSimulation( TTree * fOutTree );
    
    ~T3pSimulation(){}

    // GETs

    
    // SETs
    void         SetOutTree ( TTree * fOutTree ) {OutTree = fOutTree;};
    void Set_ppElasticHisto ( TH2F * h ) {h_ppElastic = h;};
  
    
    void    ImpMomentumDist ( bool DoPlot){calculations.CFGMomentumDist(DoPlot,SRCk4Tail);}
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



};

#endif
/** @} */ // end of doxygen group

