
// grab an (e,e'pp) tree from Or
// and adjust it to my analysis:
// (1) apply fiducial cuts to the recoil proton
// (2) rotate p(c.m.) to the p(miss) reference frame
#include "TEG2dm.h"


// globals
Float_t         q_phi, Pmiss_phi, Pmiss_theta;
TVector3        Pcm3Vector;
TLorentzVector  Plead, Pmiss, Precoil, q, Pcm;
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
void AdjustOr_eepp_Tree(int A=12, int debug=1){
    
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
    TFile OutFile( Form("/Users/erezcohen/Desktop/DataMining/OrAnalysisTrees/AdjustedTrees/SRC_e2p_adjusted_%s.root",My_target.Data()) , "recreate");
    TTree * OutTree = new TTree("anaTree","adjusted form Or' tree");
    Int_t Nentries = InTree->GetEntries();
    
    Float_t Rp[20][3], Pp_size[20], Ep[20], Nu;
    Float_t Pp_components[20][3],q_components[3],Pmiss_components[3];
    
    InTree -> SetBranchAddress("Nu", &Nu);
    InTree -> SetBranchAddress("Rp", &Rp);
    InTree -> SetBranchAddress("Pp", &Pp_components);
    InTree -> SetBranchAddress("Ep", &Ep);
    InTree -> SetBranchAddress("Pp_size", &Pp_size);
    InTree -> SetBranchAddress("q"      , &q_components);
    InTree -> SetBranchAddress("Pmiss"  , &Pmiss_components);
    
    
    Float_t Pmiss3Mag, pcmX, pcmY, pcmZ;
    OutTree -> Branch("Pmiss3Mag"           ,&Pmiss3Mag             , "Pmiss3Mag/F");
    OutTree -> Branch("pcmX"                ,&pcmX                  , "pcmX/F");
    OutTree -> Branch("pcmY"                ,&pcmY                  , "pcmY/F");
    OutTree -> Branch("pcmZ"                ,&pcmZ                  , "pcmZ/F");
    OutTree -> Branch("Pmiss"               ,&Pmiss);
    OutTree -> Branch("Pcm"                 ,&Pcm);
    OutTree -> Branch("Precoil"             ,&Precoil);
    OutTree -> Branch("Plead"               ,&Plead);
    OutTree -> Branch("q"                   ,&q);
    
    for (int entry = 0 ; entry < Nentries ; entry++) {
        
        InTree->GetEntry(entry);
        
        
        if (    TMath::Abs(Rp[0][2]+22.25)<2.25
            &&  TMath::Abs(Rp[1][2]+22.25)<2.25
            &&  Pp_size[0] < 2.4
            &&  0.35 < Pp_size[1]
            )
        {
            q = TLorentzVector( q_components[0] , q_components[1] , q_components[2] , Nu );
            Plead = TLorentzVector( Pp_components[0][0] , Pp_components[0][1] , Pp_components[0][2] , Ep[0] );
            Precoil = TLorentzVector( Pp_components[1][0] , Pp_components[1][1] , Pp_components[1][2] , Ep[1] );
            
            
            Int_t PrecoilFiducial = eg2dm->protonFiducial( Precoil.Vect() , debug );
            if (PrecoilFiducial){
                Pmiss.SetVectMag( TVector3( Pmiss_components[0] , Pmiss_components[1] , Pmiss_components[2] ) , 0.938 );
                Pmiss3Mag = Pmiss.P();
                
                Pcm = Pmiss + Precoil;
                Pcm3Vector = Pcm.Vect();
                
                
                Build_Pmiss_q_frame();
                Printf("before Pcm rotation:");
                SHOWTVector3(Pcm3Vector);
                eg2dm->RotVec2_Pm_q_Frame( & Pcm3Vector , Pmiss_phi, Pmiss_theta, q_phi );
                Printf("after Pcm rotation:");
                SHOWTVector3(Pcm3Vector);
                PrintLine();
                
                pcmX = Pcm3Vector.X();
                pcmY = Pcm3Vector.Y();
                pcmZ = Pcm3Vector.Z();
                OutTree -> Fill();
                
                if (debug){
                    Printf("vertex(p(lead))-z: %.2f, vertex(p(recoil))-z:%.2f",Rp[0][2],Rp[1][2]);
                    Printf("p(lead): %.2f",Pp_size[0]);
                    Printf("p(recoil): %.2f",Pp_size[1]);
                    Pcm3Vector.Print();
                }
            }
        }
    }
    
    
    Printf("OutTree->GetEntries(): %lld",OutTree->GetEntries());
    
    InFile.Close();
    OutTree->Write();
    OutFile.Close();
    Printf("Done");
    gROOT->ProcessLine(".q");
}




