
// usage:
// root -l AdjustOr_eepp_Tree.C\(\12,false,0\)
// - --- -- ---- - - -- ---- --- - --- -
// grab an (e,e'pp) tree from Or
// and adjust it to my analysis:
// (1) apply fiducial cuts to the recoil proton
// (2) rotate p(c.m.) to the p(miss) reference frame
#include "TEG2dm.h"


// globals
Float_t         q_phi, Pmiss_phi, Pmiss_theta, rooWeight, Q2, theta_e, OrMott ;
TVector3        Pcm3Vector, Prec3Vector, Pmiss3Vector;
TLorentzVector  Plead, Pmiss, Precoil, q, Pcm, e;
TLorentzVector  Beam( 0 , 0 , 5.014 , 5.014 );
TEG2dm * eg2dm = new TEG2dm();

TVector3 v_q , v1 , v2 , v_cm;


//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void Build_Pmiss_q_frame(){
    //     q is the z axis, Pmiss is in x-z plane: Pmiss=(Pmiss[x],0,Pmiss[q])
    Pmiss_phi   = Pmiss.Phi();
    Pmiss_theta = Pmiss.Theta();
    
    q.RotateZ(-Pmiss_phi);
    q.RotateY(-Pmiss_theta);
    q_phi = q.Phi();
    q.RotateZ(-q_phi);
}


//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void ComputeWeights(){
    theta_e = TMath::DegToRad()*theta_e ;
    Float_t Mott = pow( cos(theta_e/2.) , 2 ) / pow( sin(theta_e/2.) , 4 );
//    Float_t DipoleFF2 = pow( 1./(1. + Q2/0.71) , 4);
    Float_t DipoleFF2 = pow( 1./Q2 , 4);
    rooWeight =  1./ ( Mott * DipoleFF2 ) ;
    
    OrMott = 1./ ( (1./3500) *
                (
                 (
                  cos(theta_e/2)
                  /
                  pow(  pow(   sin(theta_e/2)    ,2)     ,2)
                  )
                 )
                * pow((10./Q2),4)
                );
    // SHOW4( cos(theta_e/2) , pow(  pow(   sin(theta_e/2)    ,2)     ,2) , pow((10./Q2),4) , OrMott);
}




//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void AdjustOr_eepp_Tree(int A=12, bool DoFiducialCuts=true, int debug=1){
    
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
    
    TFile InFile( Form("/Users/erezcohen/Desktop/DataMining/OrAnalysisTrees/OrOriginalTrees/SRC_e2p_%s_GoodRuns_coulomb.root",Or_target.Data()) );
    TTree * InTree = (TTree * )InFile.Get("T");
    TFile * OutFile;
    if (DoFiducialCuts){
                OutFile = new TFile( Form("/Users/erezcohen/Desktop/DataMining/OrAnalysisTrees/AdjustedTrees/SRC_e2p_adjusted_%s.root",My_target.Data()) , "recreate");
//        OutFile = new TFile( Form("/Users/erezcohen/Desktop/DataMining/OrAnalysisTrees/AdjustedTrees/SRC_e2p_adjusted_300Pmiss600_%s.root",My_target.Data()) , "recreate");
    } else {
                OutFile = new TFile( Form("/Users/erezcohen/Desktop/DataMining/OrAnalysisTrees/AdjustedTrees/SRC_e2p_adjusted_%s_noFiducials.root",My_target.Data()) , "recreate");
//        OutFile = new TFile( Form("/Users/erezcohen/Desktop/DataMining/OrAnalysisTrees/AdjustedTrees/SRC_e2p_adjusted_300Pmiss600_%s_noFiducials.root",My_target.Data()) , "recreate");
    }
    TTree * OutTree = new TTree("anaTree","adjusted form Or' tree");
    Int_t Nentries = InTree->GetEntries();
    
    Float_t Rp[20][3], Pp_size[20], Ep[20], Nu, Pmiss_size[20];
    Float_t Pp_components[20][3],q_components[3],Pmiss_components[2][3];
    
    InTree -> SetBranchAddress("Nu", &Nu);
    InTree -> SetBranchAddress("Rp", &Rp);
    InTree -> SetBranchAddress("Pp", &Pp_components);
    InTree -> SetBranchAddress("Ep", &Ep);
    InTree -> SetBranchAddress("Pp_size", &Pp_size);
    InTree -> SetBranchAddress("Pmiss_size", &Pmiss_size);
    InTree -> SetBranchAddress("q"      , &q_components);
    InTree -> SetBranchAddress("Q2"     , &Q2);
    InTree -> SetBranchAddress("Pmiss"  , &Pmiss_components);
    InTree -> SetBranchAddress("theta_e", &theta_e);
    
    
    
    Float_t Pmiss3Mag, pcmX, pcmY, pcmZ;
    OutTree -> Branch("Pmiss3Mag"           ,&Pmiss3Mag             , "Pmiss3Mag/F");
    OutTree -> Branch("pcmX"                ,&pcmX                  , "pcmX/F");
    OutTree -> Branch("pcmY"                ,&pcmY                  , "pcmY/F");
    OutTree -> Branch("pcmZ"                ,&pcmZ                  , "pcmZ/F");
    OutTree -> Branch("rooWeight"           ,&rooWeight             , "rooWeight/F");
    OutTree -> Branch("Mott"                ,&OrMott                , "Mott/F"); // Or weight
    OutTree -> Branch("Pmiss"               ,&Pmiss);
    OutTree -> Branch("Pcm"                 ,&Pcm);
    OutTree -> Branch("Precoil"             ,&Precoil);
    OutTree -> Branch("Plead"               ,&Plead);
    OutTree -> Branch("q"                   ,&q);
    OutTree -> Branch("e"                   ,&e);
    OutTree -> Branch("v1"                  ,&v1);
    OutTree -> Branch("v2"                  ,&v2);
    OutTree -> Branch("v_q"                 ,&v_q);
    OutTree -> Branch("v_cm"                ,&v_cm);

    OutTree -> Branch("Pmiss3Vector"        ,&Pmiss3Vector);
    OutTree -> Branch("Prec3Vector"         ,&Prec3Vector);
    OutTree -> Branch("Pcm3Vector"          ,&Pcm3Vector);
    
    
    for (int entry = 0 ; entry < Nentries ; entry++) {
        
        InTree->GetEntry(entry);
        
        
        if (
            TMath::Abs(Rp[0][2]+22.25)<2.25
            &&  TMath::Abs(Rp[1][2]+22.25)<2.25
            //            &&  Pp_size[0] < 2.4
            &&  0.35 < Pp_size[1]
            //            &&  0.3 < Pmiss_size[0]  &&  Pmiss_size[0] < 0.6
            )
        {
            q = TLorentzVector( q_components[0] , q_components[1] , q_components[2] , Nu );
            e = Beam - q;
            ComputeWeights();

            Plead = TLorentzVector( Pp_components[0][0] , Pp_components[0][1] , Pp_components[0][2] , Ep[0] );
            Precoil = TLorentzVector( Pp_components[1][0] , Pp_components[1][1] , Pp_components[1][2] , Ep[1] );
            Prec3Vector = Precoil.Vect();
            
            Int_t PrecoilFiducial = eg2dm->protonFiducial( Precoil.Vect() , debug );
            if ( PrecoilFiducial || DoFiducialCuts==false ){
                Pmiss.SetVectMag( TVector3( Pmiss_components[0][0] , Pmiss_components[0][1] , Pmiss_components[0][2] ) , 0.938 );
                Pmiss3Mag = Pmiss.P();
                Pcm = Pmiss + Precoil;
                Pmiss3Vector = Pmiss.Vect();
                
//                Printf("before Build_Pmiss_q_frame()");
//                SHOW3(Pmiss_phi , Pmiss_theta , q_phi);
                Build_Pmiss_q_frame();
//                Printf("after Build_Pmiss_q_frame()");
//                SHOWTVector3(q.Vect());
//                SHOW3(Pmiss_phi , Pmiss_theta , q_phi);
//                Printf("before RotVec2_Pm_q_Frame()");
//                SHOWTVector3(Pmiss3Vector);
//                SHOWTVector3(Prec3Vector);
                eg2dm->RotVec2_Pm_q_Frame( & Pmiss3Vector , Pmiss_phi, Pmiss_theta, q_phi );
                eg2dm->RotVec2_Pm_q_Frame( & Prec3Vector , Pmiss_phi, Pmiss_theta, q_phi );
//                Printf("after RotVec2_Pm_q_Frame()");
//                SHOWTVector3(Pmiss3Vector);
//                SHOWTVector3(Prec3Vector);
                Pcm3Vector = Pmiss3Vector + Prec3Vector;
//                PrintLine();
                
                
                // Or' script from 2015
                // -- -- - -- - - -- -- -- -- - -- - - - -- - - - -- -- - -- -- --- -- - - -- -- - -- -- - - -- -- - -
                v_q.SetX(q_components[0]);
                v_q.SetY(q_components[1]);
                v_q.SetZ(q_components[2]);
                v1.SetX(Pmiss_components[0][0]);
                v1.SetY(Pmiss_components[0][1]);
                v1.SetZ(Pmiss_components[0][2]);
                v2.SetX(Pp_components[1][0]);
                v2.SetY(Pp_components[1][1]);
                v2.SetZ(Pp_components[1][2]);
                Double_t Pmiss_phi     = v1.Phi();
                Double_t Pmiss_theta   = v1.Theta();
                //--------------------------
                v_q.RotateZ(-Pmiss_phi);
                v_q.RotateY(-Pmiss_theta);
                Double_t q_phi = v_q.Phi();
                v_q.RotateZ(-q_phi);
                //--------------------------
                v2.RotateZ(-Pmiss_phi);
                v2.RotateY(-Pmiss_theta);
                v2.RotateZ(-q_phi);
                //--------------------------
                v1.RotateZ(-Pmiss_phi);
                v1.RotateY(-Pmiss_theta);
                v1.RotateZ(-q_phi);
                //--------------------------
                v_cm = (v1 + v2);
                // -- -- - -- - - -- -- -- -- - -- - - - -- - - - -- -- - -- -- --- -- - - -- -- - -- -- - - -- -- - -

                
                
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
    
    cout << "wrote to anaTree in " << OutFile->GetName() << endl;
    Printf("OutTree->GetEntries(): %lld",OutTree->GetEntries());
    
    InFile.Close();
    OutTree->Write();
    OutFile->Close();
    Printf("Done");
    gROOT->ProcessLine(".q");
}




