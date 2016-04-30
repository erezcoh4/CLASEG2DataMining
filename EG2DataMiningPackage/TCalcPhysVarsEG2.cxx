#ifndef TCALCPHYSVARSEG2_CXX
#define TCALCPHYSVARSEG2_CXX

#include "TCalcPhysVarsEG2.h"




//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
TCalcPhysVarsEG2::TCalcPhysVarsEG2( TTree * fInTree, TTree * fOutTree, int fA , TString fDataType, TString fFrameName){
    SetDataType     (fDataType);
    SetInTree       (fInTree);
    SetOutTree      (fOutTree);
    SetFrameName    (fFrameName);
    A = fA;
    InitGlobals     ();
    InitInputTree   ();
    InitOutputTree  ();
}


//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void TCalcPhysVarsEG2::InitInputTree(){
    InTree -> SetBranchAddress("Xb"                 , &Xb);
    InTree -> SetBranchAddress("Q2"                 , &Q2);
    InTree -> SetBranchAddress("P_nmb"              , &Np);
  
    if(DataType == "data") {
        InTree -> SetBranchAddress("Q2"             , &Q2);
        InTree -> SetBranchAddress("Nu"             , &Nu);
        InTree -> SetBranchAddress("Px_e"           , &Px_e);
        InTree -> SetBranchAddress("Py_e"           , &Py_e);
        InTree -> SetBranchAddress("Pz_e"           , &Pz_e);
        InTree -> SetBranchAddress("X_e"            , &X_e);
        InTree -> SetBranchAddress("Y_e"            , &Y_e);
        InTree -> SetBranchAddress("Z_e"            , &Z_e);
        InTree -> SetBranchAddress("Px"             , &PpX);
        InTree -> SetBranchAddress("Py"             , &PpY);
        InTree -> SetBranchAddress("Pz"             , &PpZ);
        InTree -> SetBranchAddress("X"              , &Xp);
        InTree -> SetBranchAddress("Y"              , &Yp);
        InTree -> SetBranchAddress("Z"              , &Zp);
        InTree -> SetBranchAddress("CTOF"           , &uns_pCTOF);
    }
    
    else if(DataType == "no ctof") {
        InTree -> SetBranchAddress("N_Px"           , &N_Px);    // negative particles momenta (electron is the first)
        InTree -> SetBranchAddress("N_Py"           , &N_Py);    // negative particles momenta (electron is the first)
        InTree -> SetBranchAddress("N_Pz"           , &N_Pz);    // negative particles momenta (electron is the first)
        InTree -> SetBranchAddress("P_Px"           , &PpX);    // protons momenta
        InTree -> SetBranchAddress("P_Py"           , &PpY);
        InTree -> SetBranchAddress("P_Pz"           , &PpZ);
        InTree -> SetBranchAddress("P_X"            , &Xp);
        InTree -> SetBranchAddress("P_Y"            , &Yp);
        InTree -> SetBranchAddress("P_Z"            , &Zp);
        InTree -> SetBranchAddress("P_CTOF"         , &uns_pCTOF);      // protons CTOF
        InTree -> SetBranchAddress("P_PID"          , &uns_pID);        // positive particles momenta
        InTree -> SetBranchAddress("P_cut"          , &uns_pCut);       // positive particles momenta
        InTree -> SetBranchAddress("P_Edep"         , &uns_pEdep);
    }
    
    Nentries    = InTree -> GetEntries();
    std::cout << "Initialized Input InTree TCalcPhysVarsEG2 for " << InTree -> GetName() <<", Nentries = " <<  Nentries << std::endl;
}




//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void TCalcPhysVarsEG2::InitOutputTree(){

    // Integer branches
    OutTree -> Branch("target atomic mass"  ,&A                     ,"A/I");
    OutTree -> Branch("number of protons"   ,&Np                    ,"Np/I");
    OutTree -> Branch("pCTOFCut"            ,&pCTOFCut              );// std::vector<Int_t>

    
    // Float_t branches
    OutTree -> Branch("Bjorken x"           ,&Xb                    , "Xb/F");
    OutTree -> Branch("Bjorken x (moving p)",&XbMoving              , "XbMoving/F");
    OutTree -> Branch("Q2"                  ,&Q2                    , "Q2/F");
    OutTree -> Branch("missing mass"        ,&Mmiss                 , "Mmiss/F");
    OutTree -> Branch("missing energy"      ,&Emiss                 , "Emiss/F");
    OutTree -> Branch("theta (pq)"          ,&theta_pq              , "theta_pq/F");
    OutTree -> Branch("p/q"                 ,&p_over_q              , "p_over_q/F");
    OutTree -> Branch("q LC fraction"       ,&alpha_q               , "alpha_q/F");
    OutTree -> Branch("sum of LC fractions" ,&sum_alpha             , "sum_alpha/F");
    OutTree -> Branch("theta p(miss)-p2 p3" ,&thetaMiss23           , "thetaMiss23/F");
    OutTree -> Branch("phi p(miss)-p2 p3"   ,&phiMiss23             , "phiMiss23/F");
    OutTree -> Branch("alpha"               ,&alpha                 );// std::vector<Float_t>
    OutTree -> Branch("pCTOF"               ,&pCTOF                 );// std::vector<Float_t>
    OutTree -> Branch("pEdep"               ,&pEdep                 );// std::vector<Float_t>


    
    // TVector3 branches
    OutTree -> Branch("pVertex"             ,&pVertex);             // std::vector<TVector3>
 
    
    // TLorentzVector branches
    OutTree -> Branch("Pmiss"               ,"TLorentzVector"       ,&Pmiss);
    OutTree -> Branch("Pcm"                 ,"TLorentzVector"       ,&Pcm);
    OutTree -> Branch("Plead"               ,"TLorentzVector"       ,&Plead);
    OutTree -> Branch("Prec"                ,"TLorentzVector"       ,&Prec);
    OutTree -> Branch("q"                   ,"TLorentzVector"       ,&q);
    OutTree -> Branch("protons"             ,&protons);             // std::vector<TLorentzVector>
    
    
    
    // p(cm) for rooFit
    OutTree -> Branch("p(c.m.) x direction" ,&pcmX                   , "pcmX/D");
    OutTree -> Branch("p(c.m.) y direction" ,&pcmY                   , "pcmY/D");
    OutTree -> Branch("p(c.m.) z direction" ,&pcmZ                   , "pcmZ/D");

    
    std::cout << "Initialized Output Tree TCalcPhysVarsEG2 on " << OutTree -> GetTitle() << std::endl;



}


//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void TCalcPhysVarsEG2::InitGlobals(){
    TargetAsString( A      , &mA   , &CoulombDeltaE);
    TargetAtRest.SetVectM( TVector3() , mA  );   // Target initially at rest relative to beam
    NucleonAtRest.SetVectM( TVector3() , Mp  );   // Target initially at rest relative to beam
    A_over_mA  = (float)A/mA;
    pA.SetVectM( TVector3() , Mp * A  );
    Beam = TLorentzVector( 0 , 0 , 5.009 , 5.009 );

}


//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void TCalcPhysVarsEG2::InitEvent(){
    if (!p3vec.empty())     p3vec.clear();   // unsorted protons
    if (!protons.empty())   protons.clear();
    if (!pVertex.empty())   pVertex.clear();
    if (!alpha.empty())     alpha.clear();
    if (!pCTOF.empty())     pCTOF.clear();
    if (!pCTOFCut.empty())  pCTOFCut.clear();
    if (!pEdep.empty())     pEdep.clear();
    Plead = TLorentzVector();
}



//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void TCalcPhysVarsEG2::ComputePhysVars(int entry){

    InitEvent();
    InTree -> GetEntry(entry);
    
    // electron
    if(DataType == "data") {
        Pe      = TVector3( Px_e , Py_e , Pz_e );
        //        q.SetPxPyPzE( - Px_e , - Py_e , 5.009 - Pz_e , Nu); delete may 27
    }
    else if (DataType == "no ctof"){
        Pe = TVector3( N_Px[0] , N_Py[0] , N_Pz[0] );
        //        q.SetPxPyPzE( - N_Px[0] , - N_Py[0] , 5.009 - N_Pz[0], Nu); delete may 27
    }
    e.SetVectM( Pe , Me );
    q = Beam - e;
    Q2 = -q.Mag2();
    
    
   
    // get protons - energy loss correction and Coulomb corrections
    for (int i = 0 ; i < Np ; i++ ){

        p3vec.push_back( TVector3 (PpX[i],PpY[i],PpZ[i] ) );
        EnergyLossCorrrection( p3vec.back() );
        CoulombCorrection( p3vec.back() , CoulombDeltaE );
        if ( p3vec.back().Mag() > Plead.P() )
            Plead.SetVectM( p3vec.back() , Mp ) ;           // Plead is first calculated in Lab-Frame
        
    }

    // Pmiss , p/q , 𝜃(p,q)
    Pmiss       = Plead - q;
    theta_pq    = r2d * Plead.Vect().Angle(q.Vect());
    p_over_q    = Plead.P() / q.P();

//        XbMoving    = Q2 / ( 2. * (Pmiss * q) ); // = Q2 / 2pq [Q2 / ( 2. * (Pmiss * q) )]
//    SHOWTLorentzVector(Plead);
//    SHOWTLorentzVector(q);
//    SHOWTLorentzVector(Pmiss);
//        SHOW(Xb);
//        SHOW(XbMoving);

    
    // Bjorken scaling for a moving nucleon
    // Invariant mass of the system produced in the interaction of balancing nucleon with a virtual photon
    pA_Np_1.SetVectM( TVector3() , Mp * (A - Np - 1)  );
    Wtilde      = pA - pA_Np_1 + q ;
    
    
    
    
    // move to prefered axes frame
    ChangeAxesFrame();
    
    
    // α-s
    alpha_q     = LCfraction(q , A_over_mA);
    sum_alpha   = -alpha_q;
    
    
    // c.m. momentum
    Pcm         = -q;
    
    
    
    // A(e,e'p)X missing energy
    Mrec        = mA - Np * Mp;            // taking out the 1 proton off the initial target
    Trec        = sqrt( Pmiss.P()*Pmiss.P() + Mrec*Mrec) - Mrec;
    Emiss       = Nu - Trec;
    

    
    // sort the protons and loop on them for variables calculations only once more!
    loop_protons();

    
    // all recoil protons together (just without the leading proton)
    Plead       = protons.at(0);            // now Plead is calculated in q-Pmiss frame
    Prec        = Pcm - (Plead - q);        // Prec is the 4-vector sum of all recoiling protons
    
    
    // A(e,e'p) missing mass M²(miss) = (q + 2mN - Plead)² , all 4-vectors
    Mmiss       = (q + 2*NucleonAtRest - Plead).Mag();

    
    // Bjorken scaling for a moving nucleon
    XbMoving    = Q2 / ( Wtilde.Mag2() + Q2 - Mp2  ); // = Q2 / 2pq [Q2 / ( 2. * (Pmiss * q) )]
    SHOWTLorentzVector(Wtilde);
    SHOW(Wtilde.Mag2());
    SHOW(Mp2);
    SHOW(Xb);
    SHOW(XbMoving);

    
    // if we have 3 protons, randomize protons 2 and 3
    if (Np==3) {
        p23Randomize();
        thetaMiss23 = r2d*Pmiss.Vect().Angle(Prec.Vect());
        phiMiss23   = 90 - r2d*( Pmiss.Vect().Angle(protons.at(1).Vect().Cross(protons.at(2).Vect()).Unit()) );
    }

    
    pcmX = Pcm.Px();
    pcmY = Pcm.Py();
    pcmZ = Pcm.Pz();
    
    // finally, fill the TTree output
    OutTree -> Fill();

}


//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void TCalcPhysVarsEG2::ChangeAxesFrame(){
    if (FrameName == "q(z) - Pmiss(x-z) frame")
        q_Pmiss_frame();
    else if(FrameName == "Pmiss(z) - q(x-z) frame")
        Pmiss_q_frame();
}




//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void TCalcPhysVarsEG2::q_Pmiss_frame(){
    //     q is the z axis, Pmiss is in x-z plane: Pmiss=(Pmiss[x],0,Pmiss[q])
    q_phi   = q.Phi();
    q_theta = q.Theta();

    Pmiss.RotateZ(-q_phi);
    Pmiss.RotateY(-q_theta);
    Pmiss_phi = Pmiss.Phi();
    Pmiss.RotateZ(-Pmiss_phi);
    
    q.RotateZ(-q_phi);
    q.RotateY(-q_theta);
}


//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void TCalcPhysVarsEG2::Pmiss_q_frame(){
    //     Pmiss is the z axis, q is in x-z plane: q=(q[x],0,q[Pmiss])
    Pmiss_phi   = Pmiss.Phi();
    Pmiss_theta = Pmiss.Theta();

    q.RotateZ(-Pmiss_phi);
    q.RotateY(-Pmiss_theta);
    q_phi = q.Phi();
    q.RotateZ(-q_phi);
    
    Pmiss.RotateZ(-Pmiss_phi);
    Pmiss.RotateY(-Pmiss_theta);
}




//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void TCalcPhysVarsEG2::loop_protons(){


    for (auto i: sort_pMag( p3vec )){
        
        // protons
        if (FrameName == "q(z) - Pmiss(x-z) frame")
            RotVec2_q_Pm_Frame( & p3vec.at(i) , q_phi, q_theta, Pmiss_phi );
        else if(FrameName == "Pmiss(z) - q(x-z) frame")
            RotVec2_Pm_q_Frame( & p3vec.at(i) , Pmiss_phi, Pmiss_theta, q_phi );
        
        protons .push_back( TLorentzVector( p3vec.at(i) , sqrt( p3vec.at(i).Mag2() + Mp2 ) ) );
        Pcm     += protons.back();
        
        
        // proton vertex
        pVertex .push_back( TVector3( Xp[i] , Yp[i] , Zp[i] ) );
        
        // proton identification
        pCTOFCut.push_back( uns_pCut[i] * uns_pID[i] );
        pCTOF   .push_back( uns_pCTOF[i]  );
        pEdep   .push_back( uns_pEdep[i]  );
        
 
        
        // α-s
        alpha.push_back( LCfraction(protons.back() , A_over_mA ) );
        sum_alpha += alpha.back();
        
        
       
        // A(e,e'p)X missing energy
        Emiss      -= protons.back().E() - Mp;
     
        
        // Invariant mass of the system produced in the interaction of balancing nucleon with a virtual photon
        Wtilde     -= protons.back();
    }
    
    
}



//....oooOO0OOooo........oooOO0OOooo........oooOO0OåOooo........oooOO0OOooo......
vector<size_t> TCalcPhysVarsEG2::sort_pMag(const vector<TVector3> &v) {
    std::vector<size_t> idx(v.size());
    for (size_t i = 0; i != idx.size(); ++i) idx[i] = i;
    std::sort(idx.begin(), idx.end(), [&v](size_t i1, size_t i2) {return v[i1].Mag() > v[i2].Mag();});
    return idx;
}


//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void TCalcPhysVarsEG2::p23Randomize(){
        // If we have 3 protons, randomly choose which is p₂ and which is p₃ with a probablity of 50%
        if( rand.Uniform() > 0.5 ){
            
            std::iter_swap(protons.begin()+1    ,protons.begin()+2);
            std::iter_swap(pCTOFCut.begin()+1   ,pCTOFCut.begin()+2);
            std::iter_swap(pCTOF.begin()+1      ,pCTOF.begin()+2);
            std::iter_swap(pEdep.begin()+1      ,pEdep.begin()+2);
            std::iter_swap(pVertex.begin()+1    ,pVertex.begin()+2);
            std::iter_swap(alpha.begin()+1      ,alpha.begin()+2);
            
        }
}



//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void TCalcPhysVarsEG2::PrintData(int entry){
    
    SHOW(entry);
    SHOW(Xb);
    SHOW(Q2);
    SHOW(XbMoving);
    SHOWTLorentzVector(q);
    SHOW(alpha_q);
    SHOWvectorTLorentzVector(protons);
    SHOWstdTVector3(pVertex);
    SHOWvectorFloat_t(alpha);
    SHOW(alpha_q);
    SHOWvectorInt_t(pCTOFCut);
    SHOWvectorFloat_t(pEdep);
    SHOWTLorentzVector(Plead);
    SHOW(sum_alpha);
    SHOWTLorentzVector(Pmiss);
    SHOWTLorentzVector(Prec);
    SHOWTLorentzVector(Pcm);
    SHOW(theta_pq);
    SHOW(p_over_q);
    PrintLine();
}



#endif
