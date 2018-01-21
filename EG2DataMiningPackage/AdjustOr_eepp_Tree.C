/*
 AdjustOr_eepp_Tree(
 int A=12
 , bool DoFiducialCuts=true
 , bool Do300Pmiss600=true
 , int eep_or_eepp=2
 , bool for_event_generator=false
 , int debug=1
 )

 usage:
 root -l AdjustOr_eepp_Tree.C\(\12,true,true,2,true,0\)
 - --- -- ---- - - -- ---- --- - --- -
 grab an (e,e'p) or (e,e'pp) tree from Or
 and adjust it to my analysis:
 (1) apply fiducial cuts to the recoil proton
 (2) rotate p(c.m.) to the p(miss) reference frame
 */
// Aug-1,2017
#include "TEG2dm.h"

// globals
Float_t         q_phi, Pmiss_phi, Pmiss_theta, rooWeight, Q2;
Float_t         Mott, DipoleFF2, omega;
Float_t         Plead_P , Plead_theta , Plead_phi, Precoil_P, Precoil_theta , Precoil_phi;
Float_t         electron_phi, electron_theta, Emiss;
TVector3        Pcm3Vector, Prec3Vector;
TLorentzVector  Plead, Pmiss, Precoil, q, Pcm, e;
TLorentzVector  Beam( 0 , 0 , 5.014 , 5.014 );
TEG2dm * eg2dm = new TEG2dm();



//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void Build_Pmiss_q_frame(){
    //     q is the z axis, Pmiss is in x-z plane: Pmiss=(Pmiss[x],0,Pmiss[q])
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
void ComputeWeights(){
    Float_t Theta           = e.Theta();
    Mott            = pow( cos(Theta/2.) , 2 ) / pow( sin(Theta/2.) , 4 );
    DipoleFF2       = pow( 1./(1. + Q2/0.71) , 4);
    rooWeight       =  1./ ( Mott * DipoleFF2 ) ;
}




//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void AdjustOr_eepp_Tree(int A=12, bool DoFiducialCuts=true, bool Do300Pmiss600=true, int eep_or_eepp=2,  bool for_event_generator=false, int debug=1){
    
    TString Or_target;
    switch (A) {
        case 12:
            Or_target = "C";
            break;
        case 27:
            Or_target = "Al";
            break;
        case 56:
            Or_target = "Fe";
            break;
        case 208:
            Or_target = "Pb";
            break;
        default:
            break;
    }
    TString My_target = eg2dm->Target( A );
    
    TFile * InFile;
    if (eep_or_eepp==1){
        InFile = new TFile( Form("/Users/erezcohen/Desktop/DataMining/OrAnalysisTrees/OrOriginalTrees/SRC_e1p_%s_GoodRuns_coulomb.root",Or_target.Data()) );
    }
    else if (eep_or_eepp==2){
        InFile = new TFile( Form("/Users/erezcohen/Desktop/DataMining/OrAnalysisTrees/OrOriginalTrees/SRC_e2p_%s_GoodRuns_coulomb.root",Or_target.Data()) );
    }
    
    TTree * InTree = (TTree * )InFile->Get("T");
    TFile * OutFile;
    
    TString OutTreeName , OutFilePath;
    if (for_event_generator){
        OutFilePath = "/Users/erezcohen/Desktop/DataMining/Analysis_DATA/ppSRCcm/DATA_300Pmiss600/";
        OutTreeName = "T";
    }
    else {
        OutFilePath = "/Users/erezcohen/Desktop/DataMining/OrAnalysisTrees/AdjustedTrees/";
        OutTreeName = "anaTree";
    }
    
    if (DoFiducialCuts){
        if (Do300Pmiss600){
            OutFile = new TFile( OutFilePath + Form("SRC_e%dp_adjusted_300Pmiss600_%s_PrecFiducials.root",eep_or_eepp,My_target.Data()) , "recreate");
        }
        else {
            cout << OutFilePath + Form("SRC_e%dp_adjusted_300Pmiss1000_%s_PrecFiducials.root",eep_or_eepp,My_target.Data()) << endl;
            OutFile = new TFile( OutFilePath + Form("SRC_e%dp_adjusted_300Pmiss1000_%s_PrecFiducials.root",eep_or_eepp,My_target.Data()) , "recreate");
//            OutFile = new TFile( OutFilePath + Form("SRC_e%dp_adjusted_%s_PrecFiducials.root",eep_or_eepp,My_target.Data()) , "recreate");
        }
    } else {
        if (Do300Pmiss600){
            OutFile = new TFile( OutFilePath + Form("SRC_e%dp_adjusted_300Pmiss600_%s_NoPrecFiducials.root",eep_or_eepp,My_target.Data()) , "recreate");
        }
        else{
            OutFile = new TFile( OutFilePath + Form("SRC_e%dp_adjusted_%s_NoPrecFiducials.root",eep_or_eepp,My_target.Data()) , "recreate");
        }
    }
    
    TTree * OutTree = new TTree(OutTreeName,"adjusted form Or' tree");
    Int_t Nentries = InTree->GetEntries();
    
    Float_t Rp[20][3], Pp_size[20], Ep[20], Nu;
    Float_t Pp_components[20][3],q_components[3],Pmiss_components[2][3];
    
    InTree -> SetBranchAddress("Nu", &Nu);
    InTree -> SetBranchAddress("Rp", &Rp);
    InTree -> SetBranchAddress("Pp", &Pp_components);
    InTree -> SetBranchAddress("Ep", &Ep);
    InTree -> SetBranchAddress("Pp_size", &Pp_size);
    InTree -> SetBranchAddress("q"      , &q_components);
    InTree -> SetBranchAddress("Pmiss"  , &Pmiss_components);
    
    
    Float_t Pmiss3Mag, pcmX, pcmY, pcmZ;
    OutTree -> Branch("omega"               ,&omega                 , "omega/F");
    OutTree -> Branch("Pmiss3Mag"           ,&Pmiss3Mag             , "Pmiss3Mag/F");
    OutTree -> Branch("Emiss"               ,&Emiss                 , "Emiss/F");
    OutTree -> Branch("pcmX"                ,&pcmX                  , "pcmX/F");
    OutTree -> Branch("pcmY"                ,&pcmY                  , "pcmY/F");
    OutTree -> Branch("pcmZ"                ,&pcmZ                  , "pcmZ/F");
    OutTree -> Branch("rooWeight"           ,&rooWeight             , "rooWeight/F");
    OutTree -> Branch("Mott"                ,&Mott                  , "Mott/F");
    OutTree -> Branch("DipoleFF2"           ,&DipoleFF2             , "DipoleFF2/F");
    OutTree -> Branch("Precoil_P"           ,&Precoil_P             , "Precoil_P/F");
    OutTree -> Branch("Precoil_theta"       ,&Precoil_theta         , "Precoil_theta/F");
    OutTree -> Branch("Precoil_phi"         ,&Precoil_phi           , "Precoil_phi/F");
    OutTree -> Branch("Plead_P"             ,&Plead_P               , "Plead_P/F");
    OutTree -> Branch("Plead_theta"         ,&Plead_theta           , "Plead_theta/F");
    OutTree -> Branch("Plead_phi"           ,&Plead_phi             , "Plead_phi/F");
    OutTree -> Branch("electron_theta"      ,&electron_theta        , "electron_theta/F");
    OutTree -> Branch("electron_phi"        ,&electron_phi          , "electron_phi/F");
    
    OutTree -> Branch("Pcm"                 ,&Pcm);
    OutTree -> Branch("Precoil"             ,&Precoil);
    OutTree -> Branch("Plead"               ,&Plead);
    if (for_event_generator==false){
        OutTree -> Branch("q"                   ,&q);
        OutTree -> Branch("Pmiss"               ,&Pmiss);
    }
    OutTree -> Branch("e"                   ,&e);

    // -- - - -- -- - -- -- -- - -- - - -- - -- -- - - -- - - -- --- -- - - --
    // for event generator
    Int_t   OrTree_nmb;
    Float_t OrTree_Q2;
    Float_t OrTree_Xb;
    Float_t OrTree_Pe;
    Float_t OrTree_theta_e;
    Float_t OrTree_Pe_size;
    Float_t OrTree_Ep[20];
    Float_t OrTree_Pp[20][3];
    Float_t OrTree_Rp[20][3];
    Float_t OrTree_Pp_size[20];
    Float_t OrTree_Pmiss[20][3];
    Float_t OrTree_theta_Pmiss;
    Float_t OrTree_phi_Pmiss;
    Float_t OrTree_Pmiss_size[20][3];
    Float_t OrTree_q[3];
    Float_t OrTree_q_size;
    Float_t OrTree_Pmiss_q_angle;

    InTree -> SetBranchAddress("Q2"      ,           &OrTree_Q2);
    InTree -> SetBranchAddress("Xb"      ,           &OrTree_Xb);
    InTree -> SetBranchAddress("Pe"      ,           &OrTree_Pe);
    InTree -> SetBranchAddress("theta_e" ,           &OrTree_theta_e);
    InTree -> SetBranchAddress("Pe_size" ,           &OrTree_Pe_size);
//    InTree -> SetBranchAddress("Ep"      ,           &OrTree_Ep);
//    InTree -> SetBranchAddress("Pp"      ,           &OrTree_Pp);
//    InTree -> SetBranchAddress("Rp"      ,           &OrTree_Rp);           // proton vertex
//    InTree -> SetBranchAddress("Pp_size" ,           &OrTree_Pp_size);
//    InTree -> SetBranchAddress("Pmiss"   ,           &OrTree_Pmiss);
    InTree -> SetBranchAddress("theta_Pmiss",        &OrTree_theta_Pmiss);
    InTree -> SetBranchAddress("phi_Pmiss",          &OrTree_phi_Pmiss);
    InTree -> SetBranchAddress("Pmiss_size",         &OrTree_Pmiss_size);
//    InTree -> SetBranchAddress("q"       ,           &OrTree_q);
    InTree -> SetBranchAddress("q_size"  ,           &OrTree_q_size);
    InTree -> SetBranchAddress("Pmiss_q_angle",      &OrTree_Pmiss_q_angle);
    InTree -> SetBranchAddress("nmb",                &OrTree_nmb);
    
    
    
    if (for_event_generator==true){
        
        OutTree -> Branch("nmb"     ,           &OrTree_nmb                         , "nmb/I");
        OutTree -> Branch("Q2"      ,           &OrTree_Q2                          , "Q2/F");
        OutTree -> Branch("Xb"      ,           &OrTree_Xb                          , "Xb/F");
        OutTree -> Branch("Pe"      ,           &OrTree_Pe                          , "Pe[3]/F");
        OutTree -> Branch("theta_e" ,           &OrTree_theta_e                     , "theta_e/F");
        OutTree -> Branch("Pe_size" ,           &OrTree_Pe_size                     , "Pe_size[3]/F");
        OutTree -> Branch("Ep"      ,           &OrTree_Ep                          , "Ep[nmb]/F");
        OutTree -> Branch("Pp"      ,           &OrTree_Pp                          , "Pp[nmb][3]/F");
        OutTree -> Branch("Rp"      ,           &OrTree_Rp                          , "Rp[nmb][3]/F");
        OutTree -> Branch("Pp_size" ,           &OrTree_Pp_size                     , "Pp_size/F");
        OutTree -> Branch("theta_Pmiss",        &OrTree_theta_Pmiss                 , "theta_Pmiss[nmb]/F");
        OutTree -> Branch("phi_Pmiss",          &OrTree_phi_Pmiss                   , "phi_Pmiss[nmb]/F");
        
        OutTree -> Branch("Pmiss_size",         &OrTree_Pmiss_size                  , "Pmiss_size[nmb]/F");
        OutTree -> Branch("q_size"  ,           &OrTree_q_size                      , "q_size/F");
        OutTree -> Branch("Pmiss_q_angle",      &OrTree_Pmiss_q_angle               , "Pmiss_q_angle[nmb]/F");
        OutTree -> Branch("q"       ,           &q_components                   , "q[3]/F");
        OutTree -> Branch("Pmiss"   ,           &Pmiss_components               , "Pmiss[nmb][3]/F");
    }
    // -- - - -- -- - -- -- -- - -- - - -- - -- -- - - -- - - -- --- -- - - --
    
    
    
    for (int entry = 0 ; entry < Nentries ; entry++) {
        
        InTree->GetEntry(entry);
        
        for (int i=0;i<20;i++){
            OrTree_Ep[i] = Ep[i];
            OrTree_Pp_size[i] = Pp_size[i];
            for (int j=0; j<3; j++){
                OrTree_Pp[i][j] = Pp_components[i][j];
                OrTree_Rp[i][j] = Rp[i][j];
                OrTree_Pmiss[i][j] = Pmiss_components[i][j];
            }
        }
        for (int j=0; j<3; j++){
            OrTree_q[j] = q_components[j];
        }
        
        
        if (
                TMath::Abs(Rp[0][2]+22.25)<2.25
            &&  ((eep_or_eepp==1) || (eep_or_eepp==2 && TMath::Abs(Rp[1][2]+22.25)<2.25))
            &&  Pp_size[0] < 2.4
            &&  ((eep_or_eepp==1) || (eep_or_eepp==2 && 0.35 < Pp_size[1]))
            )
        {
            q = TLorentzVector( q_components[0] , q_components[1] , q_components[2] , Nu );
            omega = Nu;
            e = Beam - q;
            electron_theta = e.Theta() ;
            electron_phi = eg2dm->ChangePhiToPhiLab( r2d*e.Phi() ) ;
            Q2 = -q.Mag2();
            ComputeWeights();
            
            Plead = TLorentzVector( Pp_components[0][0] , Pp_components[0][1] , Pp_components[0][2] , Ep[0] );
            Precoil = TLorentzVector( Pp_components[1][0] , Pp_components[1][1] , Pp_components[1][2] , Ep[1] );
            
            Plead_P = Plead.P();  Plead_theta = Plead.Theta();
            Plead_phi = eg2dm->ChangePhiToPhiLab( r2d*Plead.Phi() ) ;
            Precoil_P = Precoil.P();  Precoil_theta = Precoil.Theta();
            Precoil_phi = eg2dm->ChangePhiToPhiLab( r2d*Precoil.Phi() ) ;

            Prec3Vector = Precoil.Vect();
            
            Int_t PrecoilFiducial = eg2dm->protonFiducial( Precoil.Vect() , debug );
            if ( (eep_or_eepp==1) || ( ( eep_or_eepp==2 ) && ( PrecoilFiducial || DoFiducialCuts==false )) ){
                Pmiss.SetVectMag( TVector3( Pmiss_components[0][0] , Pmiss_components[0][1] , Pmiss_components[0][2] ) , 0.938 );
                Pmiss3Mag = Pmiss.P();
                Emiss = Pmiss.E();
                
                if ( (Do300Pmiss600 && Pmiss3Mag < 0.6) || (!Do300Pmiss600) ){
                    Pcm = Pmiss + Precoil;
                    Pcm3Vector = Pcm.Vect();
                    
                    
                    Build_Pmiss_q_frame();
                    eg2dm->RotVec2_Pm_q_Frame( & Pcm3Vector , Pmiss_phi, Pmiss_theta, q_phi );
                    eg2dm->RotVec2_Pm_q_Frame( & Prec3Vector , Pmiss_phi, Pmiss_theta, q_phi );
                    Pcm3Vector = Pmiss.Vect() + Prec3Vector;
                    // SHOWTVector3(Pcm3Vector);
                    
                    
                    pcmX = Pcm3Vector.X();
                    pcmY = Pcm3Vector.Y();
                    pcmZ = Pcm3Vector.Z();
                    OutTree -> Fill();
                    
                    if (debug){
                        Printf("vertex(p(lead))-z: %.2f, vertex(p(recoil))-z:%.2f",Rp[0][2],Rp[1][2]);
                        Printf("p(lead): %.2f",Pp_size[0]);
                        Printf("p(recoil): %.2f",Pp_size[1]);
                        Pcm3Vector.Print();
                        PrintLine();
                    }
                }
            }
        }
    }
    
    cout << "wrote to anaTree in " << OutFile->GetName() << endl;
    SHOW(OutTree->GetEntries());
    
    InFile->Close();
    OutTree->Write();
    OutFile->Close();
    Printf("Done");
    gROOT->ProcessLine(".q");
}




