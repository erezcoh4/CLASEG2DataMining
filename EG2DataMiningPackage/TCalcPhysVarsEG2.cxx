#ifndef TCALCPHYSVARSEG2_CXX
#define TCALCPHYSVARSEG2_CXX

#include "TCalcPhysVarsEG2.h"




//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
TCalcPhysVarsEG2::TCalcPhysVarsEG2( TTree * fInTree, TTree * fOutTree, int fA , TString fDataType, TString fFrameName, int fdebug){
    SetDebug        (fdebug);
    SetDataType     (fDataType);
    SetInTree       (fInTree);
    SetOutTree      (fOutTree);
    SetFrameName    (fFrameName);
    Setk0           (0.15);
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
    InTree -> SetBranchAddress("T_nmb"              , &Ntotal);
    InTree -> SetBranchAddress("N_nmb"              , &Nnegative);
  
    if (DataType == "DATA" || DataType == "GSIM") {
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
    
    else if(DataType == "NoCTof_DATA" || DataType == "New_NoCTofDATA") {
        InTree -> SetBranchAddress("N_Px"           , &N_Px);    // negative particles momenta (electron is the first)
        InTree -> SetBranchAddress("N_Py"           , &N_Py);    // negative particles momenta (electron is the first)
        InTree -> SetBranchAddress("N_Pz"           , &N_Pz);    // negative particles momenta (electron is the first)
        InTree -> SetBranchAddress("P_Px"           , &PpX);     // protons momenta
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

    else if(DataType == "(e,e'npp)") {
        NMom = P1Mom = P2Mom = e3Vector = 0;
        
        InTree -> SetBranchAddress("e3Vector"       , &e3Vector);
        InTree -> SetBranchAddress("NMom"           , &NMom);
        InTree -> SetBranchAddress("P1Mom"          , &P1Mom);
        InTree -> SetBranchAddress("P2Mom"          , &P2Mom);
    }
    
    if(DataType == "GSIM") {
        InTree -> SetBranchAddress("Q2_g"           , &Q2_g);
        InTree -> SetBranchAddress("Nu_g"           , &Nu_g);
        InTree -> SetBranchAddress("Px_e_g"         , &Px_e_g);
        InTree -> SetBranchAddress("Py_e_g"         , &Py_e_g);
        InTree -> SetBranchAddress("Pz_e_g"         , &Pz_e_g);
        InTree -> SetBranchAddress("X_e_g"          , &X_e_g);
        InTree -> SetBranchAddress("Y_e_g"          , &Y_e_g);
        InTree -> SetBranchAddress("Z_e_g"          , &Z_e_g);
        InTree -> SetBranchAddress("Px_g"           , &PpX_g);
        InTree -> SetBranchAddress("Py_g"           , &PpY_g);
        InTree -> SetBranchAddress("Pz_g"           , &PpZ_g);
    }
    
    
    Nentries    = InTree -> GetEntries();
    if (debug>0) std::cout << "Initialized Input InTree TCalcPhysVarsEG2 for " << InTree -> GetName() <<", Nentries = " <<  Nentries << std::endl;
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void TCalcPhysVarsEG2::InitOutputTree(){

    // Integer branches
    OutTree -> Branch("target atomic mass"  ,&A                     ,"A/I");
    OutTree -> Branch("Np"                  ,&Np                    ,"Np/I");
    OutTree -> Branch("NpBack"              ,&NpBack                ,"NpBack/I"); // number of backward going protons
    OutTree -> Branch("NpCumulative"        ,&NpCumulative          ,"NpCumulative/I"); // number of backward going protons with 0.3<p
    OutTree -> Branch("NpCumulativeSRC"     ,&NpCumulativeSRC       ,"NpCumulativeSRC/I"); // number of backward going protons with 0.3<p<0.7
    OutTree -> Branch("total particle num." ,&Ntotal                ,"Ntotal/I");
    OutTree -> Branch("neg. particles num." ,&Nnegative             ,"Nnegative/I");
    OutTree -> Branch("pCTOFCut"            ,&pCTOFCut              );// std::vector<Int_t>

    
    // Float_t branches
    OutTree -> Branch("Xb"                  ,&Xb                    , "Xb/F");
    OutTree -> Branch("Bjorken x (moving p)",&XbMoving              , "XbMoving/F");
    OutTree -> Branch("Q2"                  ,&Q2                    , "Q2/F");
    OutTree -> Branch("Mmiss"               ,&Mmiss                 , "Mmiss/F");
    OutTree -> Branch("missing energy"      ,&Emiss                 , "Emiss/F");
    OutTree -> Branch("theta (pq)"          ,&theta_pq              , "theta_pq/F");
    OutTree -> Branch("p/q"                 ,&p_over_q              , "p_over_q/F");
    OutTree -> Branch("q LC fraction"       ,&alpha_q               , "alpha_q/F");
    OutTree -> Branch("sum of LC fractions" ,&sum_alpha             , "sum_alpha/F");
    OutTree -> Branch("theta p(miss)-p2 p3" ,&thetaMiss23           , "thetaMiss23/F");
    OutTree -> Branch("theta p(lead)-p(rec)",&thetaLeadRec          , "thetaLeadRec/F");
    OutTree -> Branch("phi p(miss)-p2 p3"   ,&phiMiss23             , "phiMiss23/F");
    OutTree -> Branch("alpha"               ,&alpha                 );// std::vector<Float_t>
    OutTree -> Branch("proton_angle"        ,&proton_angle          );// std::vector<Float_t>
    OutTree -> Branch("pCTOF"               ,&pCTOF                 );// std::vector<Float_t>
    OutTree -> Branch("pEdep"               ,&pEdep                 );// std::vector<Float_t>
    OutTree -> Branch("TpMiss"              ,&TpMiss                , "TpMiss/F");
    OutTree -> Branch("Tp"                  ,&Tp                    );// std::vector<Float_t> - kinetic energies
    OutTree -> Branch("q_phi"               ,&q_phi                 , "q_phi/F");
    OutTree -> Branch("q_theta"             ,&q_theta               , "q_theta/F");
    OutTree -> Branch("Pmiss_phi"           ,&Pmiss_phi             , "Pmiss_phi/F");


    
    // TVector3 branches
    OutTree -> Branch("PmRctLab3"           ,"TVector3"             ,&PmRctLab3);
    OutTree -> Branch("eVertex"             ,"TVector3"             ,&eVertex);
    OutTree -> Branch("pVertex"             ,&pVertex);             // std::vector<TVector3>
 
    
    // TLorentzVector branches
    OutTree -> Branch("Pmiss"               ,"TLorentzVector"       ,&Pmiss);
    OutTree -> Branch("PmissRct"            ,"TLorentzVector"       ,&PmissRct);
    OutTree -> Branch("Pcm"                 ,"TLorentzVector"       ,&Pcm);
    OutTree -> Branch("PcmFinalState"       ,"TLorentzVector"       ,&PcmFinalState);
    OutTree -> Branch("Plead"               ,"TLorentzVector"       ,&Plead);
    OutTree -> Branch("Prec"                ,"TLorentzVector"       ,&Prec);
    OutTree -> Branch("q"                   ,"TLorentzVector"       ,&q);
    OutTree -> Branch("e"                   ,"TLorentzVector"       ,&e);
    OutTree -> Branch("Wtilde"              ,"TLorentzVector"       ,&Wtilde);
    OutTree -> Branch("Wmiss"               ,"TLorentzVector"       ,&Wmiss);
    OutTree -> Branch("WmissWithCm"         ,"TLorentzVector"       ,&WmissWithCm);
    OutTree -> Branch("WmissCmEps"          ,"TLorentzVector"       ,&WmissCmEps);
    OutTree -> Branch("protons"             ,&protons);             // std::vector<TLorentzVector>

    
    
    // p(cm) for rooFit
    OutTree -> Branch("p(c.m.) x direction" ,&pcmX                  , "pcmX/D");
    OutTree -> Branch("p(c.m.) y direction" ,&pcmY                  , "pcmY/D");
    OutTree -> Branch("p(c.m.) z direction" ,&pcmZ                  , "pcmZ/D");

    
    if(DataType == "GSIM") {
        OutTree -> Branch("generated Q2"            ,&Q2_g          , "Q2_g/F");
        OutTree -> Branch("generated Bjorken x"     ,&Xb_g          , "Xb_g/F");

    }
    if(DataType == "(e,e'npp)"){
        OutTree -> Branch("Nlead"               ,"TLorentzVector"       ,&Plead);
        OutTree -> Branch("Nmiss"               ,"TLorentzVector"       ,&Nmiss);
    }
    
    if (debug>0) std::cout << "Initialized Output Tree TCalcPhysVarsEG2 on " << OutTree -> GetTitle() << std::endl;
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void TCalcPhysVarsEG2::InitGlobals(){
    TargetAsString( A      , &mA   , &CoulombDeltaE);
    TargetAtRest.SetVectM( TVector3() , mA  );   // Target initially at rest relative to beam
    NucleonAtRest.SetVectM( TVector3() , Mp  );   // Target initially at rest relative to beam
    m_A_1 = mA - Mp;
    A_over_mA  = (float)A/mA;
    pA.SetVectM( TVector3() , Mp * A  );
    Beam = TLorentzVector( 0 , 0 , 5.009 , 5.009 );
    
    if (debug > 2) Printf("intialized globals");

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
    if (!Tp.empty())        Tp.clear();
    if (!proton_angle.empty()) proton_angle.clear();
    Np = NpBack = NpCumulative = NpCumulativeSRC = 0;
    Plead = TLorentzVector();
    Wmiss.SetVectM( TVector3() , 3. * Mp  );


    // see how much the W2 peak is broadened because of motion of three nucleons as a whole
    // add 3-momentum for the nucleons and, put with exp(-(k/k0)^2, k0 ~ 150-200 MeV/c
    kCMmag = rand.Gaus( 0 , k0 );
    rand.Sphere( Px , Py , Pz , kCMmag );
    WmissWithCm.SetVectM( TVector3(Px , Py , Pz) , 3. * Mp  );

    // maybe interesting to see how much answer changes if 3m_N is changed to 3m_N - epsilon where epsilon ~ 40 MeV
    WmissCmEps.SetVectM( TVector3(Px , Py , Pz) , 3. * Mp - 0.040 );

    if (debug > 2) Printf("initialized event");
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void TCalcPhysVarsEG2::ComputePhysVars(int entry){

    InitEvent();
    InTree -> GetEntry(entry);
    if (debug > 2) Printf("got entry");

    // electron
    if(DataType == "data" || DataType == "GSIM" ) {
        Pe      = TVector3( Px_e , Py_e , Pz_e );
        eVertex = TVector3( X_e , Y_e , Z_e );
    }
    else if (DataType == "NoCTOF_DATA" || DataType == "New_NoCTofDATA"){
        Pe = TVector3( N_Px[0] , N_Py[0] , N_Pz[0] );
    }
    else if (DataType == "(e,e'npp)"){
        Pe = *e3Vector;
    }
    e.SetVectM( Pe , Me );
    q = Beam - e;
    Q2 = -q.Mag2();
    if (debug > 2) Printf("extracted electron' kinematics");

    
    
    // get protons - energy loss correction and Coulomb corrections
    for (int i = 0 ; i < Np ; i++ ){

        p3vec.push_back( TVector3 (PpX[i],PpY[i],PpZ[i] ) );
        EnergyLossCorrrection( p3vec.back() );
        CoulombCorrection( p3vec.back() , CoulombDeltaE );
        if ( p3vec.back().Mag() > Plead.P() )
            Plead.SetVectM( p3vec.back() , Mp ) ;           // Plead is first calculated in Lab-Frame
        
    }
    
    if (DataType == "(e,e'npp)"){
        // momenta corrections have already performed
        p3vec.push_back(*NMom);
        Plead.SetVectM( p3vec.back() , Mn ) ;           
        p3vec.push_back(*P1Mom);
        p3vec.push_back(*P2Mom);
    }
    if(p3vec.size()==3)
        PmRctLab3   = q.Vect() - p3vec.at(1) - p3vec.at(2);
    if (debug > 2) Printf("extracted protons' kinematics");

    
    
    
    // Pmiss , p/q , 𝜃(p,q)
    Pmiss       = Plead - q;
    // p(A-1) = -p(init) , and E(A-1) + E(p(init)) = m(A) => E(p(init)) = m(A) - E(A-1)
    E_p_init    = mA - sqrt( pow( m_A_1 , 2 ) + pow( Pmiss.P() , 2 ) );
    M_p_init    = Mp;
    TpMiss      = E_p_init - M_p_init; // should be < 0, since the nucleon is bound - the p is off the energy shell

    theta_pq    = r2d * Plead.Vect().Angle(q.Vect());
    p_over_q    = Plead.P() / q.P();
    if (debug > 2) Printf("computed Pmiss , p/q , 𝜃(p,q) , p(A-1)");


    
    // Bjorken scaling for a moving nucleon
    // Invariant mass of the system produced in the interaction of balancing nucleon with a virtual photon
    pA_Np_1.SetVectM( TVector3() , Mp * (A - Np + 1)  );
    Wtilde      = pA - pA_Np_1 + q ;

    
    
    // move to prefered axes frame
    ChangeAxesFrame();
    if (debug > 2) Printf("Changed Axes Frame");

    
    // α-s
    alpha_q     = LCfraction(q , A_over_mA);
    sum_alpha   = -alpha_q;
    

    // c.m. momentum
    Wmiss      += q;
    WmissWithCm+= q;
    WmissCmEps += q;
    
    Pcm         = -q;
    PcmFinalState = TLorentzVector();
    

    
    // A(e,e'p)X missing energy
    Mrec        = mA - Np * Mp;            // taking out the 1 proton off the initial target
    Trec        = sqrt( Pmiss.P()*Pmiss.P() + Mrec*Mrec ) - Mrec;
    Emiss       = Nu - Trec;


    
    if (debug > 2) Printf("starting to sort the protons and loop over them");
    // sort the protons and loop on them for variables calculations only once more!
    loop_protons();
    if (debug > 2) Printf("finished sorting the protons and looping over them");

    // all recoil protons together (just without the leading proton)
    Plead       = protons.at(0);            // now Plead is calculated in q-Pmiss frame
    Prec        = Pcm - (Plead - q);        // Prec is the 4-vector sum of all recoiling protons

    
    // A(e,e'p) missing mass M²(miss) = (q + 2mN - Plead)² , all 4-vectors
    Mmiss       = (q + 2*NucleonAtRest - Plead).Mag();

    
    // Bjorken scaling for a moving nucleon
    XbMoving    = Q2 / ( Wtilde.Mag2() + Q2 - Mp2  ); // = Q2 / 2pq [Q2 / ( 2. * (Pmiss * q) )]
 

    // if we have 3 protons, randomize protons 2 and 3
    if(DataType == "(e,e'npp)"){
        Nlead = Plead; // the leader is a n
        Nmiss = Nlead - q;
        Np = 3;
    }
    if (Np==2) {
        p12Randomize();
    }
    else if (Np==3) {
        p23Randomize();
        PmissRct    = q - protons.at(1) - protons.at(2);
        thetaMiss23 = r2d*Pmiss.Vect().Angle(Prec.Vect());
        phiMiss23   = 90 - r2d*( Pmiss.Vect().Angle(protons.at(1).Vect().Cross(protons.at(2).Vect()).Unit()) );
        Wmiss       += protons.at(0);
        WmissWithCm += protons.at(0);
        WmissCmEps  += protons.at(0);
    }
    thetaLeadRec = Plead.Vect().Angle(Prec.Vect());
    
    
    
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
        if (debug > 3) Printf("rotated proton to %s",FrameName.Data());
        
        protons.push_back( TLorentzVector( p3vec.at(i) , sqrt( p3vec.at(i).Mag2() + Mp2 ) ) );
        Pcm     += protons.back();
        PcmFinalState += protons.back();
        
        
        
        // proton vertex
        pVertex .push_back( TVector3( Xp[i] , Yp[i] , Zp[i] ) );

        // kinetic energies
        Tp      .push_back( protons.back().E() - protons.back().M() );

        // proton identification
        if (DataType == "NoCTOF_DATA" || DataType == "New_NoCTofDATA") {
            
            pCTOFCut.push_back( uns_pCut[i] * uns_pID[i] );
            pCTOF   .push_back( uns_pCTOF[i]  );
            pEdep   .push_back( uns_pEdep[i]  );
            if (debug > 2) Printf("extracted proton identification information");
        }
        else {
            pCTOFCut.push_back( 1 );
        }


        // cumulative protons
        proton_angle.push_back(r2d * p3vec.at(i).Angle(q.Vect()));
        if ( pCTOFCut.back()==1 && proton_angle.back() > 90. ){
            NpBack ++ ;
            if (p3vec.at(i).Mag()>0.3){
                NpCumulative++;
                if (p3vec.at(i).Mag()<0.7){
                    NpCumulativeSRC++;
                }
            }
        }

        
        // α-s
        alpha.push_back( LCfraction(protons.back() , A_over_mA ) );
        sum_alpha += alpha.back();
        
        
       
        // A(e,e'p)X missing energy
        Emiss      -= protons.back().E() - Mp;
     
        
        // Invariant mass of the system produced in the interaction of balancing nucleon with a virtual photon
        Wtilde     -= protons.back();
        Wmiss      -= protons.back();
        WmissWithCm-= protons.back();
        WmissCmEps -= protons.back();
        if (debug > 3) Printf("finished going over this proton...");
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
        std::iter_swap(pVertex.begin()+1    ,pVertex.begin()+2);
        std::iter_swap(alpha.begin()+1      ,alpha.begin()+2);
        
        if (DataType == "NoCTOF_DATA" || DataType == "New_NoCTofDATA") {
            std::iter_swap(pCTOFCut.begin()+1   ,pCTOFCut.begin()+2);
            std::iter_swap(pCTOF.begin()+1      ,pCTOF.begin()+2);
            std::iter_swap(pEdep.begin()+1      ,pEdep.begin()+2);
        }
    }
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void TCalcPhysVarsEG2::p12Randomize(){
    // If we have 2 protons, randomly choose which is p₂ with a probablity of 50%
    if( rand.Uniform() > 0.5 ){
        
        std::iter_swap(protons.begin()    ,protons.begin()+1);
        std::iter_swap(pVertex.begin()    ,pVertex.begin()+1);
        std::iter_swap(alpha.begin()      ,alpha.begin()+1);
        
        if (DataType == "NoCTOF_DATA" || DataType == "New_NoCTofDATA") {
            std::iter_swap(pCTOFCut.begin()   ,pCTOFCut.begin()+1);
            std::iter_swap(pCTOF.begin()      ,pCTOF.begin()+1);
            std::iter_swap(pEdep.begin()      ,pEdep.begin()+1);
        }
    }
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void TCalcPhysVarsEG2::PrintData(int entry){
    
    SHOW(entry);
    cout << "\033[35m"<< "\t [" << 100*(float)entry/Nentries  << "%]" << "\033[0m"<< endl;
    PrintLine();
    SHOW(Xb);
    SHOW(Q2);
    SHOW(M_p_init);
    SHOW(E_p_init);
    SHOW(XbMoving);
    SHOWTLorentzVector(e);
    SHOWTLorentzVector(q);
    SHOW(alpha_q);
    SHOWvectorTLorentzVector(protons);
    SHOWstdTVector3(pVertex);
//    SHOWstdVector(protons);
//    SHOWstdVector(pVertex);
    SHOWstdVector(alpha);
//    SHOWvectorFloat_t(alpha);
    SHOW(alpha_q);
//    SHOWvectorInt_t(pCTOFCut);
//    SHOWvectorFloat_t(pEdep);
//    SHOWvectorFloat_t(Tp);
//    SHOWvectorFloat_t(proton_angle);
    SHOWstdVector(pCTOFCut);
    SHOWstdVector(pEdep);
    SHOWstdVector(Tp);
    SHOWstdVector(proton_angle);
    SHOWTLorentzVector(Plead);
    SHOW(sum_alpha);
    SHOWTLorentzVector(Pmiss);
    SHOWTLorentzVector(Wmiss);
    SHOWTLorentzVector(WmissWithCm);
    SHOWTLorentzVector(WmissCmEps);
    SHOW(TpMiss);
    SHOWTLorentzVector(Prec);
    SHOWTLorentzVector(Pcm);
    SHOW(theta_pq);
    SHOW(p_over_q);
    SHOW(NpBack);
    SHOW(NpCumulative);
    SHOW(NpCumulativeSRC);
    
    EndEventBlock();
}



#endif
