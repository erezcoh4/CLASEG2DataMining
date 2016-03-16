#ifndef TCALCPHYSVARSEG2_CXX
#define TCALCPHYSVARSEG2_CXX

#include "TCalcPhysVarsEG2.h"




//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
TCalcPhysVarsEG2::TCalcPhysVarsEG2( TTree * fInTree, TTree * fOutTree, int fA , TString fDataType){
    SetDataType     (fDataType);
    SetInTree       (fInTree);
    SetOutTree      (fOutTree);
    A = fA;
    InitGlobals     ();
    InitInputTree   ();
    InitOutputTree  ();
}


//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void TCalcPhysVarsEG2::InitInputTree(){
    InTree -> SetBranchAddress("Xb"                 , &Xb);
    InTree -> SetBranchAddress("P_nmb"              , &Np);
    if(DataType == "data") {
        InTree -> SetBranchAddress("Q2"             , &Q2);
        InTree -> SetBranchAddress("Nu"             , &Nu);
        InTree -> SetBranchAddress("Px_e"           , &Px_e);
        InTree -> SetBranchAddress("Py_e"           , &Py_e);
        InTree -> SetBranchAddress("Pz_e"           , &Pz_e);
        InTree -> SetBranchAddress("W"              , &W);
        InTree -> SetBranchAddress("X_e"            , &X_e);
        InTree -> SetBranchAddress("Y_e"            , &Y_e);
        InTree -> SetBranchAddress("Z_e"            , &Z_e);
        InTree -> SetBranchAddress("CTOF"           , &uns_CTOF);
        InTree -> SetBranchAddress("Px"             , &PpX);
        InTree -> SetBranchAddress("Py"             , &PpY);
        InTree -> SetBranchAddress("Pz"             , &PpZ);
    }
    Nentries    = InTree -> GetEntries();
    std::cout << "Initialized Input InTree TCalcPhysVarsEG2 for " << InTree -> GetName() <<", Nentries = " <<  Nentries << std::endl;
}


//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void TCalcPhysVarsEG2::InitOutputTree(){

    // Integer branches
    OutTree -> Branch("Np"                  ,&Np                    ,"Np/I");
    
    
    // Float_t branches
    OutTree -> Branch("Xb"                  ,&Xb                    , "Xb/F");
    OutTree -> Branch("Q2"                  ,&Q2                    , "Q2/F");
    OutTree -> Branch("Mmiss"               ,&Mmiss                 , "Mmiss/F");
    OutTree -> Branch("Emiss"               ,&Emiss                 , "Emiss/F");
    OutTree -> Branch("theta_pq"            ,&theta_pq              , "theta_pq/F");
    OutTree -> Branch("p_over_q"            ,&p_over_q              , "p_over_q/F");
    OutTree -> Branch("alpha_q"             ,&alpha_q               , "alpha_q/F");
    OutTree -> Branch("alpha"               ,&alpha                 , "alpha[Np]/F");
    OutTree -> Branch("sum_alpha"           ,&sum_alpha             , "sum_alpha/F");

    
    // TVector3ahmio
    OutTree -> Branch("Pmiss"               ,"TVector3"             ,&Pmiss);
    OutTree -> Branch("Pcm"                 ,"TVector3"             ,&Pcm);
    OutTree -> Branch("Plead"               ,"TVector3"             ,&Plead);

    
    // TLorentzVector branches
    OutTree -> Branch("protons"             ,&protons);             // std::vector<TLorentzVector>
    OutTree -> Branch("q"                   ,"TLorentzVector"       ,&q);

    
    
    
    std::cout << "Initialized Output Tree TCalcPhysVarsEG2 on " << OutTree -> GetTitle() << std::endl;



}


//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void TCalcPhysVarsEG2::InitGlobals(){
    TargetAsString( A      , &mA   , &CoulombDeltaE);
    TargetAtRest.SetVectM( TVector3() , mA  );   // Target initially at rest relative to beam
    A_over_mA  = (float)A/mA;
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void TCalcPhysVarsEG2::InitEvent(){
    if (!p3vec.empty())     p3vec.clear();   // unsorted protons
    if (!protons.empty())   protons.clear();
    if (!pMag.empty())      pMag.clear();
    if (!p3vec.empty())     p3vec.clear();
    if (!pVertex.empty())   pVertex.clear();
    Pmiss   = TVector3();
    Pcm     = TVector3();
    Prec    = TVector3();
    Plead    = TVector3();
}



//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void TCalcPhysVarsEG2::AcquireNucleons(int entry){

    InitEvent();
    InTree -> GetEntry(entry);
    SHOW(entry);
    // electron
    q3vec   .SetXYZ( - Px_e , - Py_e , 5.009 - Pz_e );
    q_phi   = q3vec.Phi();
    q_theta = q3vec.Theta();
    eVertex .SetXYZ( X_e , Y_e , Z_e );
    
    
    
    // get protons - energy loss correction and Coulomb corrections
    for (int p = 0 ; p < Np ; p++ ){

        p3vec.push_back( TVector3 (PpX[p],PpY[p],PpZ[p] ) );
        EnergyLossCorrrection( p3vec.back() );
        CoulombCorrection( p3vec.back() , CoulombDeltaE );
//        pMag.push_back(p3vec.back().Mag());

    }
    sort_protons();
    
//    // If we have 3 protons, randomly choose which is p2 and which is p3
//    if( (Np==3) && (random -> Uniform() > 0.5) ){ // switch between p2 and p3 with a probablity of 50%
//        int TmpInDeX  = InDeX[1];
//        InDeX[1]      = InDeX[2];
//        InDeX[2]      = TmpInDeX;
//    }
}





//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void TCalcPhysVarsEG2::sort_protons(){
//    for (auto i: sort_pMag( pMag )){
    for (auto i: sort_pMag( p3vec )){
        protons.push_back( TLorentzVector( p3vec.at(i) , sqrt( p3vec.at(i).Mag2() + Mp2 ) ) );
        plot.Print4Momentum(protons.back(),Form("p(%lu)",protons.size()));
    }
    Plead       = protons.at(0).Vect();
    theta_pq    = Plead.Angle(q.Vect());
    p_over_q    = Plead.Mag() / q.P();
    Pmiss       = Plead - q.Vect();
    Prec        = protons.at(1).Vect();
}


//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
vector<size_t> TCalcPhysVarsEG2::sort_pMag(const vector<float> &v) {
    std::vector<size_t> idx(v.size());
    for (size_t i = 0; i != idx.size(); ++i) idx[i] = i;
    std::sort(idx.begin(), idx.end(),
              [&v](size_t i1, size_t i2) {return v[i1] > v[i2];});
    return idx;
}


//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
vector<size_t> TCalcPhysVarsEG2::sort_pMag(const vector<TVector3> &v) {
    std::vector<size_t> idx(v.size());
    for (size_t i = 0; i != idx.size(); ++i) idx[i] = i;
    std::sort(idx.begin(), idx.end(),
              [&v](size_t i1, size_t i2) {return v[i1].Mag() > v[i2].Mag();});
    return idx;
}





//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
//void TCalcPhysVars::ComputePhysVariables(){
//    
//    pLead       = Pp.at(0);
//    Pmiss       = pLead - q3Vector;
//    //     p/q , 𝜃(p,q)
//    PoverQ      = pLead.Mag() / q3Vector.Mag();
//    ThetaPQ     = RAD2DEG*( pLead.Angle(q3Vector) );
//    
//    //     imidiately transform to q-Pmiss-frame, to calculate everything in this frame
//    //     q is the z axis, Pmiss is in x-z plane: Pmiss=(Pmiss[x],0,Pmiss[q])
//    Pmiss       .RotateZ(-q_phi);
//    Pmiss       .RotateY(-q_theta);
//    Pmiss_Phi   = Pmiss.Phi();
//    Pmiss       .RotateZ(-Pmiss_Phi);
//    q3Vector    .RotateZ(-q_phi);
//    q3Vector    .RotateY(-q_theta);
//    q           .SetVect( q3Vector );
//    q           .SetE( Nu );
//    
//    
//    // A(e,e'p)X missing energy
//    double Mre  = mA - Np*Mp;            // taking out the 1 proton off the initial target
//    double Tp[20];
//    double Trec = sqrt(Pmiss.Mag2() + Mre*Mre) - Mre;
//    Emiss       =  Nu - Trec;
//    
//    // c.m. momentum
//    // Light cone fractions
//    alpha_q     = A2mA * ( Nu - q3Vector.Z() );
//    SumAlpha    = SumpBackAlpha = -alpha_q;
//    Pcm         = -q3Vector ;
//    
//    
//    // Wtilde = (mA - m'(A - Np - 1)  + q - P0 - P1 - P2 - ... ) = invariant mass of the outgoing hadronic system
//    Wtilde      = A_4Vector + q;
//    
//    
//    
//    // Loop over the protons....
//    for (int p = 0 ; p < Np ; p++){
//        RotateVector( & Pp.at(p) );
//        Pcm        += Pp.at(p);
//        p4momentum  .SetVectM( Pp.at(p) , Mp );
//        P           .push_back( p4momentum );
//        
//        
//        
//        // A(e,e'p)X missing energy
//        Tp[p]       = P.at(p).E() - Mp;      // kinetic energy of the proton (p)
//        Emiss      -= Tp[p];
//        
//        
//        
//        // Light cone fractions
//        alpha[p]    = A2mA * ( P.at(p).E() - P.at(p).Pz()  )   ;
//        SumAlpha   += alpha[p];
//        
//        
//        
//        // backward going protons
//        theta_pq[p] = RAD2DEG*( Pp.at(p).Angle(q3Vector) );
//        if ( theta_pq[p] > 110 ){
//            pBack.push_back( p4momentum );
//            pBackAlpha[NpBack]   = A2mA * ( pBack.at(NpBack).E() - pBack.at(NpBack).Pz()  )   ;
//            SumpBackAlpha       += pBackAlpha[NpBack];
//            Wtilde              -= pBack.at(NpBack);
//            NpBack ++;
//        }
//    }
//    
//    A_Np_1_4Vector .SetVectM( TVector3() , (A - NpBack - 1)*Mp );  // approximation of the A-NpBack-1 ... system mass
//    Wtilde      -= A_Np_1_4Vector;
//    
//    
//    W2tilde     = fabs(Wtilde.Mag2());
//    Xbtilde     = Q2 / (W2tilde + Q2 - Mp2) ;
//    if (Xbtilde < 0) {
//        Printf(" W2tilde = %f , Q2 = %f,Mp2 = %f , W2tilde + Q2 - Mp2 = %f, Q2 / (W2tilde + Q2 - Mp2) = %f"
//               ,W2tilde , Q2 , Mp2,W2tilde + Q2 - Mp2,Q2 / (W2tilde + Q2 - Mp2));
//    }
//    
//    counter++;
//    OutTree -> Fill();
//}



#endif
