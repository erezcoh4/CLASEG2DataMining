#ifndef TCALCGSIMVARSEG2_CXX
#define TCALCGSIMVARSEG2_CXX

#include "TCalcGSIMVarsEG2.h"


#ifndef TCalcGSIMVarsEG2_CXX
#define TCalcGSIMVarsEG2_CXX

#include "TCalcGSIMVarsEG2.h"




//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
TCalcGSIMVarsEG2::TCalcGSIMVarsEG2( TTree * fInTree, TTree * fOutTree, int fA , TString fDataType, TString fFrameName, int fdebug){
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
TCalcGSIMVarsEG2::TCalcGSIMVarsEG2( TTree * fInTree, TString fOutFileName, int fA , TString fDataType, TString fFrameName, int fdebug){
    SetDebug        (fdebug);
    SetDataType     (fDataType);
    SetInTree       (fInTree);
    SetOutFileName  (fOutFileName);
    SetOutTree      (fOutFileName);
    SetFrameName    (fFrameName);
    Setk0           (0.15);
    A = fA;
    InitGlobals     ();
    InitInputTree   ();
    InitOutputTree  ();
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void TCalcGSIMVarsEG2::InitInputTree(){
    
    
    InTree -> SetBranchAddress("Number"         , &Number);
    
    InTree -> SetBranchAddress("Q2"             , &Q2);
    InTree -> SetBranchAddress("Q2_g"           , &Q2_g);
    
    InTree -> SetBranchAddress("Nu"             , &Nu);
    InTree -> SetBranchAddress("Nu_g"           , &Nu_g);
    
    InTree -> SetBranchAddress("particle"       , &particle_id);
    InTree -> SetBranchAddress("Momentum"       , &Momentum);
    InTree -> SetBranchAddress("Momentumx"      , &Momentumx);
    InTree -> SetBranchAddress("Momentumy"      , &Momentumy);
    InTree -> SetBranchAddress("Momentumz"      , &Momentumz);
    
    Nentries    = InTree -> GetEntries();
    if (debug>0) std::cout << "Initialized Input InTree TCalcGSIMVarsEG2 for " << InTree -> GetName() <<", Nentries = " <<  Nentries << std::endl;
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void TCalcGSIMVarsEG2::InitOutputTree(){
    
    // Integer branches
    OutTree -> Branch("target atomic mass"  ,&A                     ,"A/I");
    OutTree -> Branch("Np_g"                ,&Np_g                  ,"Np_g/I");
    OutTree -> Branch("Np"                  ,&Np                    ,"Np/I");
    OutTree -> Branch("Nnegative"           ,&Nnegative             ,"Nnegative/I");
    OutTree -> Branch("NpBack"              ,&NpBack                ,"NpBack/I"); // number of backward going protons
    OutTree -> Branch("NpCumulative"        ,&NpCumulative          ,"NpCumulative/I"); // number of backward going protons with 0.3<p
    OutTree -> Branch("NpCumulativeSRC"     ,&NpCumulativeSRC       ,"NpCumulativeSRC/I"); // number of backward going protons with 0.3<p<0.7
    OutTree -> Branch("total particle num." ,&Ntotal                ,"Ntotal/I");
    OutTree -> Branch("neg. particles num." ,&Nnegative             ,"Nnegative/I");
    OutTree -> Branch("pCTOFCut"            ,&pCTOFCut              );// std::vector<Int_t>
    OutTree -> Branch("pFiducCut"           ,&pFiducCut             );// std::vector<Int_t>
    OutTree -> Branch("pInDeadRegions"      ,&pInDeadRegions        );// std::vector<Int_t> Or' dead regions
    
    
    // Float_t branches
    OutTree -> Branch("Xb"                  ,&Xb                    , "Xb/F");
    OutTree -> Branch("Bjorken x (moving p)",&XbMoving              , "XbMoving/F");
    OutTree -> Branch("Q2"                  ,&Q2                    , "Q2/F");
    OutTree -> Branch("Mmiss"               ,&Mmiss                 , "Mmiss/F");
    OutTree -> Branch("Mmiss2"              ,&Mmiss2                , "Mmiss2/F");
    OutTree -> Branch("Mmiss3"              ,&Mmiss3                , "Mmiss3/F");
    
    // p(cm) for RooFit
    OutTree -> Branch("Pmiss3Mag"           ,&Pmiss3Mag             , "Pmiss3Mag/F");
    OutTree -> Branch("pcmX"                ,&pcmX                  , "pcmX/F");
    OutTree -> Branch("pcmY"                ,&pcmY                  , "pcmY/F");
    OutTree -> Branch("pcmT"                ,&pcmT                  , "pcmT/F");
    OutTree -> Branch("pcmZ"                ,&pcmZ                  , "pcmZ/F");
    OutTree -> Branch("prelX"               ,&prelX                 , "prelX/F");
    OutTree -> Branch("prelY"               ,&prelY                 , "prelY/F");
    OutTree -> Branch("prelZ"               ,&prelZ                 , "prelZ/F");
    OutTree -> Branch("rooWeight"           ,&rooWeight             , "rooWeight/F");
    
    OutTree -> Branch("missing energy"      ,&Emiss                 , "Emiss/F");
    OutTree -> Branch("theta (pq)"          ,&theta_pq              , "theta_pq/F");
    OutTree -> Branch("theta (rec-q)"       ,&theta_rec_q           , "theta_rec_q/F");
    OutTree -> Branch("theta (miss-q)"      ,&theta_miss_q          , "theta_miss_q/F");
    OutTree -> Branch("p/q"                 ,&p_over_q              , "p_over_q/F");
    OutTree -> Branch("q LC fraction"       ,&alpha_q               , "alpha_q/F");
    OutTree -> Branch("sum of LC fractions" ,&sum_alpha             , "sum_alpha/F");
    OutTree -> Branch("theta p(miss)-p2 p3" ,&thetaMiss23           , "thetaMiss23/F");
    OutTree -> Branch("OpeningAngle"        ,&OpeningAngle          , "OpeningAngle/F");
    OutTree -> Branch("theta23"             ,&theta23               , "theta23/F");
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
    OutTree -> Branch("Pmiss_theta"         ,&Pmiss_theta           , "Pmiss_theta/F");
    OutTree -> Branch("pLab_phi"            ,&pLab_phi              , "pLab_phi/F");
    OutTree -> Branch("pLab_theta"          ,&pLab_theta            , "pLab_theta/F");
    OutTree -> Branch("m23"                 ,&m23                   , "m23/F");
    OutTree -> Branch("T23"                 ,&T23                   , "T23/F");
    OutTree -> Branch("k23"                 ,&k23                   , "k23/F");
    OutTree -> Branch("E_R"                 ,&E_R                   , "E_R/F");
    OutTree -> Branch("alpha_3N"            ,&alpha_3N              , "alpha_3N/F");
    OutTree -> Branch("W2_3N"               ,&W2_3N                 , "W2_3N/F");
    OutTree -> Branch("k_t"                 ,&k_t                   , "k_t/F");
    OutTree -> Branch("beta_1"              ,&beta_1                , "beta_1/F");
    OutTree -> Branch("beta_2"              ,&beta_2                , "beta_2/F");
    
    
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
    OutTree -> Branch("protonsLab"          ,&protonsLab);          // std::vector<TLorentzVector>
    
    
    if(DataType == "GSIM") {
        OutTree -> Branch("generated Q2"            ,&Q2_g          , "Q2_g/F");
        OutTree -> Branch("generated Bjorken x"     ,&Xb_g          , "Xb_g/F");
        OutTree -> Branch("protons_g"               ,&protons_g);             // std::vector<TLorentzVector>
        OutTree -> Branch("pFiducCut_g"             ,&pFiducCut_g);     // std::vector<Int_t>
        
    }
    
    
    // cuts
    
    // (e,e'p) for ppSRC analysis
    OutTree -> Branch("eep_in_ppSRCcut"     ,&eep_in_ppSRCcut           ,"eep_in_ppSRCcut/I");
    // (e,e'pp) for ppSRC analysis, and the recoiling proton also passed fiducial cuts
    OutTree -> Branch("ppSRCcut"            ,&ppSRCcut                  ,"ppSRCcut/I");
    // (e,e'pp) for ppSRC analysis, and the recoiling proton also passed fiducial cuts
    OutTree -> Branch("ppSRCcutFiducial"    ,&ppSRCcutFiducial          ,"ppSRCcutFiducial/I");
    
    if (debug>0) std::cout << "Initialized Output Tree TCalcGSIMVarsEG2 on " << OutTree -> GetTitle() << std::endl;
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void TCalcGSIMVarsEG2::InitGlobals(){
    TargetAsString( A      , &mA   , &CoulombDeltaE);
    TargetAtRest.SetVectM( TVector3() , mA  );   // Target initially at rest relative to beam
    NucleonAtRest.SetVectM( TVector3() , Mp  );   // Target initially at rest relative to beam
    m_A_1 = mA - Mp;
    A_over_mA  = (float)A/mA;
    pA.SetVectM( TVector3() , Mp * A  );
    Beam = TLorentzVector( 0 , 0 , 5.014 , 5.014 );
    
    if (debug > 2) Printf("intialized globals");
    
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void TCalcGSIMVarsEG2::InitEvent(){
    if (!p3vec.empty())     p3vec.clear();   // unsorted protons
    if (!protons.empty())   protons.clear();
    if (!protonsLab.empty())protonsLab.clear();
    if (!pVertex.empty())   pVertex.clear();
    if (!alpha.empty())     alpha.clear();
    if (!pCTOF.empty())     pCTOF.clear();
    if (!pCTOFCut.empty())  pCTOFCut.clear();
    if (!pFiducCut.empty()) pFiducCut.clear();
    if (!pInDeadRegions.empty()) pInDeadRegions.clear();
    if (!pEdep.empty())     pEdep.clear();
    if (!Tp.empty())        Tp.clear();
    if (!proton_angle.empty()) proton_angle.clear();
    if (!p3vec_g.empty())   p3vec_g.clear();   // unsorted protons
    if (!protons_g.empty()) protons_g.clear();
    if (!pFiducCut_g.empty()) pFiducCut_g.clear();
    
    m_S = 0;
    Np = NpBack = NpCumulative = NpCumulativeSRC = 0;
    Pmiss = Plead = Plead_g = TLorentzVector();
    Wmiss.SetVectM( TVector3() , 3. * Mp  );
    p_S = TLorentzVector();
    
    // see how much the W2 peak is broadened because of motion of three nucleons as a whole
    // add 3-momentum for the nucleons and, put with exp(-(k/k0)^2, k0 ~ 150-200 MeV/c
    kCMmag = rand.Gaus( 0 , k0 );
    rand.Sphere( Px , Py , Pz , kCMmag );
    WmissWithCm.SetVectM( TVector3(Px , Py , Pz) , 3. * Mp  );
    k_t = beta_1 = beta_2 = q_ = W2_3N = alpha_3N = 0;
    
    // maybe interesting to see how much answer changes if 3m_N is changed to 3m_N - epsilon where epsilon ~ 40 MeV
    WmissCmEps.SetVectM( TVector3(Px , Py , Pz) , 3. * Mp - 0.040 );
    
    if (debug > 2) Printf("initialized event");
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void TCalcGSIMVarsEG2::ComputePhysVars(int entry){
    
    if(!OutTree) {
        std::cerr << "Cannot call " << __FUNCTION__
        << " before tree is ok!" << std::endl;
        throw std::exception();
    }
    if (debug>3) Printf("starting event number %d",entry);
    
    
    InitEvent();
    InTree -> GetEntry(entry);
    if (debug > 2) Printf("got entry");
    
    // electron
    Pe = TVector3( Momentumx[0], Momentumy[0], Momentumz[0]);
    Pe = CoulombCorrection( Pe , CoulombDeltaE , Me , 1 ); // for the electron, the correction is E'+dE
    eVertex = TVector3( X_e , Y_e , Z_e );
    e.SetVectM( Pe , Me );
    
    q = Beam - e;
    Q2 = -q.Mag2();
    Xb = Q2/(2. * Mp * q.E());
    if (debug > 2) Printf("extracted electron' kinematics");
    
    
    
    // protons
    for (int i = 1 ; i < Number ; i++ ){
        if (particle_id[i]!=8 && particle_id[i]!=9) {
            // 8 = proton, 9 = protonNoFid
            continue;
        }
        TVector3 p_3_momentum( Momentumx[i], Momentumy[i], Momentumz[i] );
        // for all the protons, a correction of Ep-dE is performed
        p_3_momentum = CoulombCorrection( p_3_momentum , CoulombDeltaE , Mp , -1 );
        p3vec.push_back( p_3_momentum );
        if ( p_3_momentum.Mag() > Plead.P() ){
            Plead.SetVectM( p_3_momentum , Mp ) ;           // Plead is first calculated in Lab-Frame
        }
    }
    
    if (p3vec.size()==3) PmRctLab3 = q.Vect() - p3vec.at(1) - p3vec.at(2);
    if (debug > 2) Printf("extracted protons' kinematics");
    
    
    
    // Pmiss , p/q , 𝜃(p,q)
    Pmiss       = Plead - q;
    Pmiss3Mag   = Pmiss.P();
    // p(A-1) = -p(init) , and E(A-1) + E(p(init)) = m(A) => E(p(init)) = m(A) - E(A-1)
    E_p_init    = mA - sqrt( pow( m_A_1 , 2 ) + pow( Pmiss.P() , 2 ) );
    M_p_init    = Mp;
    TpMiss      = E_p_init - M_p_init; // should be < 0, since the nucleon is bound - the p is off the energy shell
    
    
    // Bjorken scaling for a moving nucleon
    // Invariant mass of the system produced in the interaction of balancing nucleon with a virtual photon
    pA_Np_1.SetVectM( TVector3() , Mp * (A - Np + 1)  );
    Wtilde      = pA - pA_Np_1 + q ;
    if (debug > 2) Printf("computed Pmiss , p/q , 𝜃(p,q) , p(A-1)");
    
    
    // move to prefered axes frame
    ChangeAxesFrame();
    if (debug > 2) Printf("Changed Axes Frame");
    
    // α-s
    alpha_q     = LCfraction(q , q , A_over_mA);
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
    
    
    if (debug > 2) Printf("starting to sort the protons and loop over them");
    // sort the protons and loop on them for variables calculations only once more!
    loop_protons();
    
    if (debug > 2) Printf("finished sorting the protons and looping over them");
    
    // all recoil protons together (just without the leading proton)
    if (protons.size()>0) {
        Plead = protons.at(0);            // now Plead is calculated in q-Pmiss frame
        theta_pq = r2d * Plead.Vect().Angle(q.Vect());
        p_over_q = Plead.P() / q.P();
        
        // Misak' mail from May-5, 2018
        // E_m = q_0 + T_f - p_m^2/(2(A-1)*m_N)
        float T_f   = Plead.E() - Mp;
        Emiss       = Nu - T_f - Pmiss.P()*Pmiss.P()/(2.*(A-1.)*Mp);
    }
    // define Precoil:
    // for 2p-SRC, we want at least one proton above 350 MeV/c, and then call it Precoil
    // for Np-SRC this is different - we need to revise it
    
    Prec = (protons.size()>1) ? protons.at(1) : TLorentzVector();
    //    Prec = Pcm - (Plead - q);        // Prec is the 4-vector sum of all recoiling protons
    // for 3p get back to this
    if (debug > 2) Printf("got Prec");
    
    
    // A(e,e'p) missing mass M²(miss) = (q + 2mN - Plead)² , all 4-vectors
    Mmiss = (q + 2*NucleonAtRest - Plead).Mag();
    Mmiss2 = (q + 2*NucleonAtRest - Plead).Mag();
    Mmiss3 = (q + 3*NucleonAtRest - Plead).Mag();
    if (debug > 2) Printf("got Mmiss");
    
    
    // Bjorken scaling for a moving nucleon
    XbMoving = Q2 / ( Wtilde.Mag2() + Q2 - Mp2  ); // = Q2 / 2pq [Q2 / ( 2. * (Pmiss * q) )]
    if (debug > 2) Printf("got XbMoving");
    
    
    if (Np==3) {
        p23Randomize(); // if we have 3 protons, randomize protons 2 and 3
        PmissRct    = q - protons.at(1) - protons.at(2);
        thetaMiss23 = r2d*Pmiss.Vect().Angle(Prec.Vect());
        phiMiss23   = 90 - r2d*( Pmiss.Vect().Angle(protons.at(1).Vect().Cross(protons.at(2).Vect()).Unit()) );
        theta23     = r2d*protons.at(1).Vect().Angle(protons.at(2).Vect());
        
        
        Wmiss       += protons.at(0);
        WmissWithCm += protons.at(0);
        WmissCmEps  += protons.at(0);
        // Misak' comment [m23.pdf, "Estimation of the recoil mass in the 3N SRC"]
        m23 = ( protons.at(1) + protons.at(2) ).Mag();
        T23 = sqrt( m23 * m23 + Pmiss.P() * Pmiss.P() ) - 2 * Mp ;
        k23 = 0.5*sqrt( m23 * m23 - 4 * Mp * Mp );
        E_R = q.E() - (Plead.E() - Mp);
        
        
        
        // comparison with Misak' predictions
        p_S         = (protons.at(1) + protons.at(2));
        q_          = q.E() - q.P();
        // k_t = P2 - (P2 * Ps) Ps
        TVector3  P2 = protons.at(2).Vect();
        TVector3  P2_along_Ps = p_S.Vect().Unit() * (protons.at(2).Vect().Dot( p_S.Vect().Unit() ));
        k_t         = (P2 - P2_along_Ps).Mag() ;
        
        beta_1      = LCfraction(protons.at(1) , q , A_over_mA ); //(protons.at(1).E() - protons.at(1).P())/(p_S.E() - p_S.P());
        beta_2      = LCfraction(protons.at(2) , q , A_over_mA ); //(protons.at(2).E() - protons.at(2).P())/(p_S.E() - p_S.P());
        m_S         = sqrt( 4.*(Mp*Mp + k_t*k_t) / (beta_1 * (2. - beta_1)) );
        W2_3N       = Q2*(3.-Xb)/Xb + 9*Mp*Mp;
        
        float _sqrt_      = sqrt( (1. - ( m_S+Mp )*( m_S+Mp )/(W2_3N) ) * (1. - ( m_S-Mp )*( m_S-Mp )/(W2_3N) ) );
        
        alpha_3N    = 3. - ( (q_ + 3*Mp)/(2.*Mp) )*( 1 + ( m_S*m_S - Mp*Mp )/(W2_3N) + _sqrt_ );
        //        cout << "in event " << entry << " Np==3!" << endl;
        //        SHOW3( Q2 , Xb , q_ );
        //        SHOW4( k_t , beta , m_S , W2_3N );
        //        SHOW( alpha_3N );
    }
    thetaLeadRec = Plead.Vect().Angle(Prec.Vect());
    theta_rec_q  = q.Vect().Angle(Prec.Vect());
    theta_miss_q = q.Vect().Angle(Pmiss.Vect());
    if (debug > 2) Printf("got thetaLeadRec");
    OpeningAngle = r2d*Pmiss.Vect().Angle(Prec.Vect());
    
    
    // roofit
    pcmX = Pcm.Px();
    pcmY = Pcm.Py();
    pcmT = Pcm.Pt();
    pcmZ = Pcm.Pz();
    prelX = 0.5*(Pmiss.Px() - Prec.Px());
    prelY = 0.5*(Pmiss.Py() - Prec.Py());
    prelZ = 0.5*(Pmiss.Pz() - Prec.Pz());
    
    ComputeWeights();
    if (debug > 2) Printf("got roofit c.m. ");
    
    SetCuts();
    OutTree -> Fill();
    if (debug > 2) Printf("filled output tree with %d entries ",(int)OutTree->GetEntries());
    
}


//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void TCalcGSIMVarsEG2::SetCuts(){
    
    eep_in_ppSRCcut = false;
    ppSRCcut = false;
    ppSRCcutFiducial = false;
    
    if ( Np>=1
        && Xb>1.2
        && theta_pq < 25
        && 0.62 < p_over_q && p_over_q < 0.96
        && Mmiss < 1.1
        && 0.3 < Pmiss.P() && Pmiss.P() < 1.0
        && -24.5 < pVertex[0].Z() && pVertex[0].Z() < -20.0
        //        && pInDeadRegions[0]==0
        && -24.5 < eVertex.Z() && eVertex.Z() < -20.0 // automatic cut that comes from target-type==2
        ){
        
        eep_in_ppSRCcut = true;
        
        if (Np>=2
            && 0.35 < Prec.P()
            &&  -24.5 < pVertex[1].Z() && pVertex[1].Z() < -20.0
            //            && pInDeadRegions[1]==0
            ){
            
            ppSRCcut = true;
            
            if (pFiducCut[1]==1){
                
                ppSRCcutFiducial = true;
                
            }
        }
    }
}


//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void TCalcGSIMVarsEG2::Close(){
    if(!OutFile || !OutTree) {
        std::cerr << "Cannot call " << __FUNCTION__
        << " before file is opened!" << std::endl;
        throw std::exception();
    }
    OutFile->cd();
    OutTree->Write();
    OutFile->Close();
    
    OutFile = nullptr;
    OutTree = nullptr;
    
}


//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void TCalcGSIMVarsEG2::ChangeAxesFrame(){
    if (FrameName == "q(z) - Pmiss(x-z) frame")
        q_Pmiss_frame();
    else if(FrameName == "Pmiss(z) - q(x-z) frame")
        Pmiss_q_frame();
    else if(FrameName == "lab frame")
        return;
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void TCalcGSIMVarsEG2::q_Pmiss_frame(){
    //     q is the z axis, Pmiss is in x-z plane: Pmiss=(Pmiss[x],0,Pmiss[q])
    q_phi   = q.Phi();
    q_theta = q.Theta();
    
    Pmiss.RotateZ(-q_phi);
    Pmiss.RotateY(-q_theta);
    Pmiss_phi = Pmiss.Phi();
    Pmiss.RotateZ(-Pmiss_phi);
    
    q.RotateZ(-q_phi);
    q.RotateY(-q_theta);
    
    if (DataType=="GSIM"){
        q_phi_g   = q_g.Phi();
        q_theta_g = q_g.Theta();
        
        Pmiss_g.RotateZ(-q_phi_g);
        Pmiss_g.RotateY(-q_theta_g);
        Pmiss_phi_g = Pmiss_g.Phi();
        Pmiss_g.RotateZ(-Pmiss_phi_g);
        
        q_g.RotateZ(-q_phi_g);
        q_g.RotateY(-q_theta_g);
    }
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void TCalcGSIMVarsEG2::Pmiss_q_frame(){
    //     Pmiss is the z axis, q is in x-z plane: q=(q[x],0,q[Pmiss])
    Pmiss_phi   = Pmiss.Phi();
    Pmiss_theta = Pmiss.Theta();
    
    q.RotateZ(-Pmiss_phi);
    q.RotateY(-Pmiss_theta);
    q_phi = q.Phi();
    q.RotateZ(-q_phi);
    
    Pmiss.RotateZ(-Pmiss_phi);
    Pmiss.RotateY(-Pmiss_theta);
    
    if (DataType=="GSIM"){
        Pmiss_phi_g   = Pmiss_g.Phi();
        Pmiss_theta_g = Pmiss_g.Theta();
        
        q_g.RotateZ(-Pmiss_phi_g);
        q_g.RotateY(-Pmiss_theta_g);
        q_phi_g = q_g.Phi();
        q_g.RotateZ(-q_phi_g);
        
        Pmiss_g.RotateZ(-Pmiss_phi_g);
        Pmiss_g.RotateY(-Pmiss_theta_g);
    }
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void TCalcGSIMVarsEG2::loop_protons(){
    
    
    for (auto i: sort_pMag( p3vec )){
        if (i>0) {
            // -- - - --- - -- --- - - -- - -- -- ------- - -- -- -- - -- - -- -- -- - -- - - -
            // PERFORM energy loss CORRECTION only FOR recoil PROTONs
            p3vec.at(i) = EnergyLossCorrrection( p3vec.at(i) );
        }
        
        protonsLab.push_back( TLorentzVector( p3vec.at(i) , sqrt( p3vec.at(i).Mag2() + Mp2 ) ) );
        pLab_phi = ChangePhiToPhiLab( r2d*p3vec.at(i).Phi() ) ;
        pLab_theta = r2d*p3vec.at(i).Theta() ;
        
        
        // proton fiducial cut is calculated in the lab frame, so it must come before we rotate the protons...
        pFiducCut.push_back( protonFiducial( p3vec.at(i) , debug ) );
        pInDeadRegions.push_back( protonInDeadRegions( p3vec.at(i) , debug ) );
        
        // protons
        if (FrameName == "q(z) - Pmiss(x-z) frame"){
            RotVec2_q_Pm_Frame( & p3vec.at(i) , q_phi, q_theta, Pmiss_phi );
        }
        else if(FrameName == "Pmiss(z) - q(x-z) frame"){
            RotVec2_Pm_q_Frame( & p3vec.at(i) , Pmiss_phi, Pmiss_theta, q_phi );
        }
        else if (FrameName == "lab frame"){
            if (debug>2) cout << "staying in lab frame..." << endl;
        }
        if (debug > 3) Printf("rotated proton to %s",FrameName.Data());
        
        protons.push_back( TLorentzVector( p3vec.at(i) , sqrt( p3vec.at(i).Mag2() + Mp2 ) ) );
        Pcm += protons.back();
        PcmFinalState += protons.back();
        
        
        
        // proton vertex
        pVertex .push_back( TVector3( Xp[i] , Yp[i] , Zp[i] ) );
        
        // kinetic energies
        Tp.push_back( protons.back().E() - protons.back().M() );
        
        
        // proton identification
        if (DataType == "NoCTofDATA" || DataType == "New_NoCTofDATA") {
            
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
        alpha.push_back( LCfraction(protons.back() , q , A_over_mA ) );
        sum_alpha += alpha.back();
        
        
        
        // A(e,e'p)X missing energy
        // Emiss -= protons.back().E() - Mp;
        
        
        // Invariant mass of the system produced in the interaction of balancing nucleon with a virtual photon
        Wtilde     -= protons.back();
        Wmiss      -= protons.back();
        WmissWithCm-= protons.back();
        WmissCmEps -= protons.back();
        if (debug > 3) Printf("finished going over this proton...");
    }
    
    if (DataType == "GSIM"){
        for (auto i: sort_pMag( p3vec_g )){
            
            // proton fiducial cut is calculated in the lab frame, so it must come first...
            pFiducCut_g.push_back( protonFiducial( p3vec_g.at(i) ) );
            
            // protons
            if (FrameName == "q(z) - Pmiss(x-z) frame"){
                RotVec2_q_Pm_Frame( & p3vec_g.at(i) , q_phi_g, q_theta_g, Pmiss_phi_g );
            }
            else if(FrameName == "Pmiss(z) - q(x-z) frame"){
                RotVec2_Pm_q_Frame( & p3vec_g.at(i) , Pmiss_phi_g, Pmiss_theta_g, q_phi_g );
            }
            else if (FrameName == "lab frame"){
                if (debug>2) cout << "staying in lab frame..." << endl;
            }
            if (debug > 3) Printf("rotated proton to %s",FrameName.Data());
            
            protons_g.push_back( TLorentzVector( p3vec_g.at(i) , sqrt( p3vec_g.at(i).Mag2() + Mp2 ) ) );
        }
    }
    
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OåOooo........oooOO0OOooo......
vector<size_t> TCalcGSIMVarsEG2::sort_pMag(const vector<TVector3> &v) {
    std::vector<size_t> idx(v.size());
    for (size_t i = 0; i != idx.size(); ++i) idx[i] = i;
    std::sort(idx.begin(), idx.end(), [&v](size_t i1, size_t i2) {return v[i1].Mag() > v[i2].Mag();});
    return idx;
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void TCalcGSIMVarsEG2::p23Randomize(){
    // If we have 3 protons, randomly choose which is p₂ and which is p₃ with a probablity of 50%
    if( rand.Uniform() > 0.5 ){
        
        std::iter_swap(protons.begin()+1    ,protons.begin()+2);
        std::iter_swap(protonsLab.begin()+1 ,protonsLab.begin()+2);
        std::iter_swap(pVertex.begin()+1    ,pVertex.begin()+2);
        std::iter_swap(alpha.begin()+1      ,alpha.begin()+2);
        
        std::iter_swap(pFiducCut.begin()+1  ,pFiducCut.begin()+2);
        std::iter_swap(pInDeadRegions.begin()+1   ,pInDeadRegions.begin()+2);
        if (DataType == "NoCTofDATA" || DataType == "New_NoCTofDATA") {
            std::iter_swap(pCTOFCut.begin()+1   ,pCTOFCut.begin()+2);
            std::iter_swap(pCTOF.begin()+1      ,pCTOF.begin()+2);
            std::iter_swap(pEdep.begin()+1      ,pEdep.begin()+2);
        }
    }
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void TCalcGSIMVarsEG2::p12Randomize(){
    // If we have 2 protons, randomly choose which is p₂ with a probablity of 50%
    if( rand.Uniform() > 0.5 ){
        
        std::iter_swap(protons.begin()    ,protons.begin()+1);
        std::iter_swap(protonsLab.begin()+1 ,protonsLab.begin()+2);
        std::iter_swap(pVertex.begin()    ,pVertex.begin()+1);
        std::iter_swap(alpha.begin()      ,alpha.begin()+1);
        
        std::iter_swap(pFiducCut.begin()  ,pFiducCut.begin()+1);
        std::iter_swap(pInDeadRegions.begin()+1   ,pInDeadRegions.begin()+2);
        if (DataType == "NoCTofDATA" || DataType == "New_NoCTofDATA") {
            std::iter_swap(pCTOFCut.begin()   ,pCTOFCut.begin()+1);
            std::iter_swap(pCTOF.begin()      ,pCTOF.begin()+1);
            std::iter_swap(pEdep.begin()      ,pEdep.begin()+1);
        }
    }
}



//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void TCalcGSIMVarsEG2::ComputeWeights(){
    Theta           = e.Theta();
    Mott            = pow( cos(Theta/2.) , 2 ) / pow( sin(Theta/2.) , 4 );
    DipoleFF2       = pow( 1./(1. + Q2/0.71) , 4);
    rooWeight       =  1./ ( Mott * DipoleFF2 ) ;
    if (debug>3) {
        SHOW3 ( Mott , DipoleFF2 , rooWeight) ;
    }
}


//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void TCalcGSIMVarsEG2::PrintData(int entry){
    SHOW4(particle_id[0],particle_id[1],particle_id[2],particle_id[3]);
    SHOW(entry);
    cout << "\033[35m"<< "\t [" << 100*(float)entry/Nentries  << "%]" << "\033[0m"<< endl;
    PrintLine();
    SHOW3(Xb , Q2 , alpha_q);
    SHOW2(M_p_init,E_p_init);
    SHOWTLorentzVector(e);
    SHOWTLorentzVector(q);
    SHOWvectorTLorentzVector(protons);
    SHOWvectorTLorentzVector(protonsLab);
    SHOWstdTVector3(pVertex);
    SHOWstdVector(alpha);
    SHOWTLorentzVector(Plead);
    SHOW(sum_alpha);
    SHOWTLorentzVector(Pmiss);
    SHOWTLorentzVector(Wmiss);
    SHOWTLorentzVector(WmissWithCm);
    SHOWTLorentzVector(WmissCmEps);
    SHOWTLorentzVector(Prec);
    SHOWTLorentzVector(Pcm);
    SHOW3(TpMiss , theta_pq , p_over_q);
    // SHOW3(NpBack , NpCumulative , NpCumulativeSRC );
    //    SHOW3(pcmX , pcmY , pcmZ);
    SHOW3(W2_3N , k_t , alpha_3N);
    EndEventBlock();
}



#endif


#endif
