#ifndef GENERATEEVENTS_CXX
#define GENERATEEVENTS_CXX

#include "GenerateEvents.h"

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
GenerateEvents::GenerateEvents( TString fPath , Int_t fRunNumber , Int_t fdebug ){

    Path = fPath;
    RunNumber = fRunNumber ;
    debug = fdebug;
    runsFilename  = Form("%s/eg_txtfiles/RunNumbers.dat",Path.Data());
    gRandom = new TRandom3( fRunNumber );
    eg2dm = new TEG2dm();

}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void GenerateEvents::Set_eep_Parameters(Float_t fMeanX, Float_t fSigmaX,
                                        Float_t fMeanY, Float_t fSigmaY,
                                        Float_t fMeanZ_a1, Float_t fMeanZ_a2,
                                        Float_t fSigmaZ_a1, Float_t fSigmaZ_a2 ) {

    // Px = gRandom -> Gaus( MeanX  , SigmaX )
    // Py = gRandom -> Gaus( MeanY  , SigmaY )
    // Pz = gRandom -> Gaus( ShiftL_a1*(PmissMag-0.6) + ShiftL_a2  , SigmaL_a1*(PmissMag-0.6) + SigmaL_a2 )
    MeanX     = fMeanX;    SigmaX    = fSigmaX;
    MeanY     = fMeanY;    SigmaY    = fSigmaY;

    MeanZ_a1  = fMeanZ_a1;    MeanZ_a2  = fMeanZ_a2;
    SigmaZ_a1 = fSigmaZ_a1;    SigmaZ_a2 = fSigmaZ_a2;

}





//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void GenerateEvents::SetLimits(Float_t fPmin , Float_t fPmax , Float_t fThetamin , Float_t fThetamax ){
    
    Pmin = fPmin;
    Pmax = fPmax;
    Thetamin = fThetamin;
    Thetamax = fThetamax;
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void GenerateEvents::SetHistThetaHistMag( TH1F * fhistMag , TH1F * fhistTheta ){
    histMag = fhistMag;
    histTheta = fhistTheta;
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void GenerateEvents::SetInputChain_eep(){
    InputT  = new TChain("T");
    // Take 12C(e,e'p) SRC tree data
    InputT -> Add( Path + "/DATA/SRC_e1_C.root");
    InputT -> Add( Path + "/DATA/SRC_e2_C.root");
    
    InputT -> SetBranchAddress("Q2"      ,           &Q2);
    InputT -> SetBranchAddress("Xb"      ,           &Xb);
    InputT -> SetBranchAddress("Pe"      ,           &Pe);
    InputT -> SetBranchAddress("theta_e" ,           &theta_e);
    InputT -> SetBranchAddress("Pe_size" ,           &Pe_size);
    InputT -> SetBranchAddress("Ep"      ,           &Ep);
    InputT -> SetBranchAddress("Pp"      ,           &Pproton);
    InputT -> SetBranchAddress("Rp"      ,           &Rproton);           // proton vertex
    InputT -> SetBranchAddress("Pp_size" ,           &Pproton_size);
    InputT -> SetBranchAddress("Pmiss"   ,           &Pm);
    InputT -> SetBranchAddress("Pmiss_size",         &Pm_size);
    InputT -> SetBranchAddress("q"       ,           &q);
    InputT -> SetBranchAddress("q_size"  ,           &q_size);
    
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void GenerateEvents::ReleaseInputChain_eep(){delete InputT;}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void GenerateEvents::InitEvent(){
    if (!pFiducCut.empty()) pFiducCut.clear();
    if (!pVertex.empty())   pVertex.clear();

}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
Int_t GenerateEvents::DoGenerateRun_eepp( Int_t fRunNumber, bool DoGetRootFile, bool DoGenTextFile){
    
    RunNumber = fRunNumber ;
    NAcceptedEvents = Nevents = 0;
    txtFilename  = Form("%s/eg_txtfiles/run%d.txt",Path.Data(),RunNumber);
    rootFilename = Form("%s/eg_rootfiles/run%d.root",Path.Data(),RunNumber);
    if (DoGenTextFile){
        cout << "Generating " << txtFilename << endl;
        TextFile.open(txtFilename);
    }
    if (DoGetRootFile){
        cout << "Generating " <<  rootFilename << endl;
        RootFile = new TFile( rootFilename ,"recreate" );
    }
    RootTree = new TTree("anaTree","generated events");
    SetRootTreeAddresses();
    int InputNentries = InputT -> GetEntries();
    
    TVector3 * momentum = new TVector3[3];
    int charge[3] = { -1          , 1         , 1     };
    float mass[3] = { 0.000511    , 0.938     , 0.938 };
    int pid[3]    = { 11          , 2212      , 2212  };
    
    for (int entry = 0 ; entry < InputNentries ; entry++ ) {
        if ( debug > 2 && entry%(InputNentries/4) == 0 ) std::cout  <<  (int)(100*(double)entry/InputNentries)+1 << "%\n";
        InitEvent();
        InputT -> GetEntry(entry);
        if(debug > 2) cout << "got entry " << entry << endl;
        
        double PmissMag = Pm_size[0];
        
        e.SetXYZ            ( Pe[0]         , Pe[1]         , Pe[2]);
        q3Vector.SetXYZ     ( q[0]          , q[1]          , q[2] );
        Pmiss.SetXYZ        ( Pm[0][0]      , Pm[0][1]      , Pm[0][2]);
        Pp1.SetXYZ          ( Pproton[0][0] , Pproton[0][1] , Pproton[0][2]);
        

        if(debug > 2) cout << "rotate to Pmiss-q frame" << endl;
        // rotate to Pmiss-q frame: Pmiss is the z axis, q is in x-z plane: q=(q[x],0,q[Pmiss])
        double Pmiss_phi = Pmiss.Phi() , Pmiss_theta = Pmiss.Theta() ;
        q3Vector_in_Pmiss_q_system = q3Vector;
        q3Vector_in_Pmiss_q_system.RotateZ(-Pmiss_phi);
        q3Vector_in_Pmiss_q_system.RotateY(-Pmiss_theta);
        double q_Phi = q3Vector_in_Pmiss_q_system.Phi();
        q3Vector_in_Pmiss_q_system.RotateZ(-q_Phi);
        
        Pmiss_in_Pmiss_q_system = Pmiss;
        Pmiss_in_Pmiss_q_system.RotateZ(-Pmiss_phi);
        Pmiss_in_Pmiss_q_system.RotateY(-Pmiss_theta);
        
        
        // rotate to q-Pmiss frame: q is the z axis, Pmiss is in x-z plane: Pmiss=(Pmiss[x],0,Pmiss[q])
        if(debug > 2) cout << "rotate to q-Pmiss frame" << endl;
        double q_q_phi = q3Vector.Phi() , q_q_theta = q3Vector.Theta() ;
        Pmiss_q_sys = q3Vector;
        Pmiss_q_sys.RotateZ(-q_q_phi);
        Pmiss_q_sys.RotateY(-q_q_theta);
        double Pmiss_Phi = Pmiss_q_sys.Phi();
        Pmiss_q_sys.RotateZ(-Pmiss_Phi);
        
        q_q_sys = q3Vector;
        q_q_sys.RotateZ(-q_q_phi);
        q_q_sys.RotateY(-q_q_theta);
        
        
        if(debug > 2) cout << "define omega and other variables" << endl;
        double  omega   = 5.009 - sqrt( 0.000511*0.000511 + e.Mag()*e.Mag() );
        ThetaPQ         = (180/TMath::Pi())*(Pp1.Angle(q3Vector));
        ThetaPmissQ     = (180/TMath::Pi())*(Pmiss.Angle(q3Vector));
        PoverQ          = Pp1.Mag()/q3Vector.Mag();
        Proton          .SetVectM   ( Pp1 , 0.938 ); // struck proton
        q4Vector        .SetXYZT    ( q3Vector.x() , q3Vector.y() , q3Vector.z() , omega );
        m2N             .SetVectM   ( TVector3(0,0,0) , 2.*0.938 );
        miss            = q4Vector + m2N - Proton;
        Mmiss           = miss.Mag();
        Rp1             .SetXYZ(Rproton[0][0],Rproton[0][1],Rproton[0][2]); // since there is no actual Rp2....
        Rp2 = Rp1;// since there is no actual Rp2....
        if(debug > 2) SHOW3( Mmiss , PoverQ , ThetaPmissQ );
        
        // struck proton fiducial cut and vertex
        pFiducCut.push_back( eg2dm->protonFiducial( Pmiss+q3Vector , debug ) );
        pVertex.push_back( Rp1 );
        // recoil proton vertex
        pVertex.push_back( Rp2 );

        
        for( int j = 0 ; j < NRand  ;  j++ ){    //MC event generation
            
            if(debug > 3) SHOW( j );
            
            float Px = gRandom -> Gaus( MeanX  , SigmaX );
            float Py = gRandom -> Gaus( MeanY  , SigmaY );
            
            float MeanZ = MeanZ_a1*(PmissMag-0.6) + MeanZ_a2    ;
            float SigmaZ = SigmaZ_a1*(PmissMag-0.6) + SigmaZ_a2 ;
            float Pz = gRandom -> Gaus( MeanZ  , SigmaZ ) ;
            //            float Pz = gRandom -> Gaus( ShiftL_a1*PmissMag + ShiftL_a2  , 0.07 );
            if(debug > 4) {
                SHOW( PmissMag );
                SHOW3( MeanZ_a1 , MeanZ_a2 , MeanZ_a1*PmissMag );
                SHOW3( SigmaZ_a1 , SigmaZ_a2 , SigmaZ_a1*PmissMag );
                SHOW3( MeanZ , SigmaZ , Pz );}
            
            Pcm_in_Pmiss_q_system.SetXYZ ( Px , Py , Pz );
            Precoil_in_Pmiss_q_system = Pcm_in_Pmiss_q_system - Pmiss_in_Pmiss_q_system;
            if(debug > 3) cout << "set Pcm_in_Pmiss_q_system and Precoil_in_Pmiss_q_system " ;
            
            // for RooFits
            Pmiss3Mag = PmissMag;
            // here we already work in the Pmiss(z) - q(x-z) frame
            pcmX = Px ;
            pcmY = Py ;
            pcmT = sqrt(Px*Px + Py*Py);
            pcmZ = Pz ;
            ComputeWeights();
            
            // now, rotate back to lab frame
            Pcm = Pcm_in_Pmiss_q_system;
            Pcm.RotateZ  ( q_Phi );
            Pcm.RotateY  ( Pmiss_theta );
            Pcm.RotateZ  ( Pmiss_phi );
            Precoil =   Pp2     = Pcm - Pmiss;
            ThetaPmissPrecoil   = (180/TMath::Pi())*(Pmiss.Angle(Precoil));
            Prec.SetVectM( Precoil , Mp );

            momentum[0] = e ; momentum[1] = Pp1; momentum[2] = Pp2;
            if (DoGenTextFile) OutPutToTextFile(3, momentum , charge , mass , pid );
            
            if(debug > 3) cout << "rotate also to q-Pmiss frame: q is the z axis" << endl;
            // rotate also to q-Pmiss frame: q is the z axis, Pmiss is in x-z plane: Pmiss=(Pmiss[x],0,Pmiss[q])
            Pcm_q_sys = Pcm;
            Pcm_q_sys.RotateZ(-q_q_phi);
            Pcm_q_sys.RotateY(-q_q_theta);
            Pcm_q_sys.RotateZ(-Pmiss_Phi);
            
            // finish
            Nevents++;
            if(debug > 3) SHOW( Nevents );
            
            // recoil proton acceptance
            // ------------------------------------------------
            // decide if this event is accepted as a legitimate (e,e'pp) event based on the recoiling proton acceptance
            AcceptEvent = false;
            if ( !Do_pAcceptance )  AcceptEvent = true; // in case we do not want to use the proton acceptances
            
            
            // recoil proton fiducial cut
            pFiducCut.push_back( eg2dm->protonFiducial( Precoil , debug ) );
            
//            if ( eg2dm->protonFiducial( Precoil , debug ) == 1 ){
            
            
            // #IMPORTANT: the acceptance map that i've created i given in the lab frame
            Double_t PrecoilMag = Precoil.Mag() , PrecoilTheta = r2d*Precoil.Theta() , PrecoilPhi = r2d*Precoil.Phi();
            PrecoilPhi =  eg2dm->ChangePhiToPhiLab( PrecoilPhi ) ; // rescale phi angle to the range [-30,330]
            if(debug > 3) SHOW3( PrecoilMag , PrecoilTheta , PrecoilPhi );
            if (    h_protonAcceptance->GetXaxis()->GetBinCenter(1) < PrecoilMag   && PrecoilMag   < h_protonAcceptance->GetXaxis()->GetBinCenter(h_protonAcceptance->GetNbinsX())
                && h_protonAcceptance->GetYaxis()->GetBinCenter(1) < PrecoilTheta && PrecoilTheta < h_protonAcceptance->GetYaxis()->GetBinCenter(h_protonAcceptance->GetNbinsY())
                && h_protonAcceptance->GetZaxis()->GetBinCenter(1) < PrecoilPhi   && PrecoilPhi   < h_protonAcceptance->GetZaxis()->GetBinCenter(h_protonAcceptance->GetNbinsZ())    ) {
                Double_t PrecoilAcceptance = h_protonAcceptance -> Interpolate( PrecoilMag , PrecoilTheta , PrecoilPhi ) / 100.;
                if(debug > 3) SHOW( PrecoilAcceptance );
                if( gRandom->Uniform() <= PrecoilAcceptance ){ // event is accepted in PrecoilAcceptance %
                    AcceptEvent = true;
                }
                //                }
            }
            if ( PrecoilTheta <= 120 ) AcceptEvent=true;
            // ------------------------------------------------
            
            if (AcceptEvent){
                if(debug > 3) Printf( "event was accepted" );
                RootTree -> Fill();
                NAcceptedEvents++ ;
            } else {
                if(debug > 3) Printf( "event was not accepted" );
            }
            if(debug > 3) SHOW( NAcceptedEvents );
            
        }
    }
    if (DoGetRootFile){
        
        RootFile -> Write();
        RootFile -> Close();
    }
    if (DoGenTextFile){
        TextFile.close();
    }
    
    Printf("done generating %d (e,e'pp) events to %s",NAcceptedEvents,rootFilename.Data());
    
    return Nevents;

}



//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
Int_t GenerateEvents::DoGenerate( TString Type,
                                 bool DoGetRootFile, bool DoGenTextFile,
                                 TString BaryonName,
                                 bool DoReeNFromTree, bool DoReeNFromDist, bool DoFlateeN){
    // return the number of events
    SHOW3( DoReeNFromTree , DoReeNFromDist , DoFlateeN );

    NAcceptedEvents = Nevents = 0;
    txtFilename     = Form("%s/eg_txtfiles/run%d.txt",Path.Data(),RunNumber);
    rootFilename    = Form("%s/eg_rootfiles/run%d.root",Path.Data(),RunNumber);
    if (DoGenTextFile){
        cout << "Generating " << txtFilename << endl;
        TextFile.open(txtFilename);
    }
    if (DoGetRootFile){
        cout << "Generating " <<  rootFilename << endl;
        RootFile = new TFile( rootFilename ,"recreate" );
    }
    RootTree = new TTree("anaTree","generated events");
    SetRootTreeAddresses();
    
    if (Type == "(e,e')" ){
        Printf("generating (e,e')");
        TVector3 e;     // N is a baryon: p/n/𝚫
        RootTree -> Branch( "e"         ,"TVector3" ,&e);
        Double_t mag , theta , phi;
        TVector3 * momentum = new TVector3[1];
        
        int charge[1]   = { -1      };
        float mass[1]   = { 0.000511};
        int pid[1]      = { 11      };
        
        for (int entry = 0 ; entry < NeTheta ; entry++ ) {
            if ( entry%(NeTheta/10) == 0 ) std::cout  << (int)(100*(double)entry/NeTheta) << "%\n";
            theta  = Thetamin + (Thetamax-Thetamin)*gRandom->Uniform();
            mag    = Pmin + (Pmax-Pmin)*gRandom->Uniform();
            for ( int rand = 0 ; rand < NRand ; rand++ ) {
                phi    = 360.*gRandom->Uniform();         // uniform angle between 0 and 360 degrees
                e.SetMagThetaPhi ( mag , (TMath::Pi()/180.)*theta , (TMath::Pi()/180.)*phi );
                momentum[0] = e;
                if (DoGenTextFile) OutPutToTextFile(1, momentum , charge ,mass , pid );
                RootTree -> Fill();
            }
        }
        
    }
    
    else if (Type == "(e,e'pp)" ){
        
        DoGenerateRun_eepp( RunNumber,  DoGetRootFile, DoGenTextFile);
        
    }
    
    else if (Type == "(e,e'B)"){
        Printf("(e,e'%s)",BaryonName.Data());
        TVector3 e , N;     // N is a baryon: p/n/𝚫
        RootTree -> Branch( BaryonName  ,"TVector3" ,&N);
        RootTree -> Branch( "e"         ,"TVector3" ,&e);
        Float_t mag , theta;
        TVector3 * momentum     = new TVector3[2];
        
        int charge[2]           = { -1          , (BaryonName == "p") ? 1       : ((BaryonName == "n") ? 0      : 2)        };
        float mass[2]           = { 0.000511    ,  static_cast<float>((BaryonName == "p") ? 0.938   : ((BaryonName == "n") ? 0.939  : 1.232))    };
        int pid[2]              = { 11          , (BaryonName == "p") ? 2212    : ((BaryonName == "n") ? 2112   : 2214)     };
        
        
        //------- TAKE DATA FROM TREE --------------//
        if (DoReeNFromTree){
            Printf("(e,e'%s) from Tree",BaryonName.Data());

            Float_t PeMag, Theta_e, Phi_e ;//   , PpMag , Theta_p;
            eeNTree -> SetBranchAddress("P_e"       ,   &PeMag);
            eeNTree -> SetBranchAddress("theta_e"   ,   &Theta_e);
            eeNTree -> SetBranchAddress("phi_e"     ,   &Phi_e);
            eeNTree -> SetBranchAddress("P_N"       ,   &mag);
            eeNTree -> SetBranchAddress("theta_N"   ,   &theta);
            Int_t Nentries = (Int_t)eeNTree->GetEntries();
            for (int entry = 0 ; entry < Nentries ; entry++ ) {
                if ( entry%(Nentries/10) == 0 ) std::cout  << (int)(100*(float)entry/Nentries) << "%\n";
                eeNTree -> GetEntry(entry);
                if(debug > 2) SHOW3( PeMag , Theta_e , Phi_e );
                e.SetMagThetaPhi(PeMag,(TMath::Pi()/180.)*Theta_e,(TMath::Pi()/180.)*Phi_e);
                momentum[0] = e;
                for ( int rand = 0 ; rand < NRand ; rand++ ) {
                    Double_t phi    = 360.*gRandom->Uniform();         // uniform angle between 0 and 360 degrees
                    if(debug > 2) SHOW3( mag , (TMath::Pi()/180.)*theta , (TMath::Pi()/180.)*phi );
                    N.SetMagThetaPhi ( mag , (TMath::Pi()/180.)*theta , (TMath::Pi()/180.)*phi);
                    momentum[1] = N;
                    if (DoGenTextFile) OutPutToTextFile(2, momentum , charge ,mass , pid );
                    RootTree -> Fill();
                }
            }
        }
        
        //------- CREATE NEW DATA --------------//
        else {
            Printf("(e,e'%s) from scratch",BaryonName.Data());

            TVector3 e(-0.137*4.306 , -0.339*4.306 , 0.956*4.306 ); // a single electron that passes RECSIS cuts...
            momentum[0] = e;
            for (int entry = 0 ; entry < NPTheta ; entry++ ) {
                if ( entry%(NPTheta/10) == 0 ) std::cout  << (int)(100*(double)entry/NPTheta) << "%\n";
                if (DoFlateeN){ // flat distributions
                    theta  = Thetamin + (Thetamax-Thetamin)*gRandom->Uniform();
                    mag    = Pmin + (Pmax-Pmin)*gRandom->Uniform();
                } else if (DoReeNFromDist){  // take from file histograms
                    theta  = histTheta ->GetRandom();
                    mag    = histMag   ->GetRandom();
                }
                for ( int rand = 0 ; rand < NRand ; rand++ ) {
                    Double_t phi    = 360.*gRandom->Uniform();         // uniform angle between 0 and 360 degrees
                    N.SetMagThetaPhi ( mag , (TMath::Pi()/180.)*theta , (TMath::Pi()/180.)*phi);
                    momentum[1] = N;
                    if (DoGenTextFile) OutPutToTextFile(2, momentum , charge ,mass , pid );
                    RootTree -> Fill();
                }
            }
            
        }
    }
    if (DoGetRootFile){

        RootFile -> Write();
        RootFile -> Close();
    }
    
    if (DoGenTextFile){
        
        TextFile.close();
        
    }
    
    //    if (debug > 2) cout << "Out to Run Number File..." << endl;
    //    OutRunNumberFile.open(runsFilename);
    //    OutRunNumberFile << RunNumber << "\n" ;
    //    OutRunNumberFile.close();
    Printf("done generating events to %s",rootFilename.Data());
    //    if (InputT) delete InputT;
    return Nevents;
}




//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void GenerateEvents::SetRootTreeAddresses(){
    
//    RootTree -> Branch("q3Vector"                    ,"TVector3"     ,&q3Vector);
//    RootTree -> Branch("Pcm"                         ,"TVector3"     ,&Pcm);
//    RootTree -> Branch("Pp1"                         ,"TVector3"     ,&Pp1);
//    RootTree -> Branch("Pp2"                         ,"TVector3"     ,&Pp2);
//    RootTree -> Branch("Pmiss"                       ,"TVector3"     ,&Pmiss);
//    RootTree -> Branch("Precoil"                     ,"TVector3"     ,&Pp2);
//    RootTree -> Branch("q_in_Pmiss_q_system"         ,"TVector3"     ,&q3Vector_in_Pmiss_q_system);
//    RootTree -> Branch("Pmiss_in_Pmiss_q_system"     ,"TVector3"     ,&Pmiss_in_Pmiss_q_system);
//    RootTree -> Branch("Pcm_in_Pmiss_q_system"       ,"TVector3"     ,&Pcm_in_Pmiss_q_system);
//    RootTree -> Branch("q_q_sys"                     ,"TVector3"     ,&q_q_sys);
//    RootTree -> Branch("Pmiss_q_sys"                 ,"TVector3"     ,&Pmiss_q_sys);
//    RootTree -> Branch("Pcm_q_sys"                   ,"TVector3"     ,&Pcm_q_sys);
//    RootTree -> Branch("Rp1"                         ,"TVector3"     ,&Rp1);                      // proton vertex
//    RootTree -> Branch("Rp2"                         ,"TVector3"     ,&Rp2);                      // proton vertex
//    RootTree -> Branch("theta_e"             ,&theta_e               ,"theta_e/F");
//    RootTree -> Branch("Xb"                  ,&Xb                    ,"Xb/F");
//    RootTree -> Branch("ThetaPQ"             ,&ThetaPQ               ,"ThetaPQ/F");              // angle between the leading proton and q
//    RootTree -> Branch("ThetaPmissQ"         ,&ThetaPmissQ           ,"ThetaPmissQ/F");          // angle between the missing momentum and q
//    RootTree -> Branch("ThetaPmissPrecoil"   ,&ThetaPmissPrecoil     ,"ThetaPmissPrecoil/F");    // angle between the missing and recoil momenta
//    RootTree -> Branch("PoverQ"              ,&PoverQ                ,"PoverQ/F");               // ratio |p|/|q| for leading proton
//    RootTree -> Branch("Mmiss"               ,&Mmiss                 ,"Mmiss/F");
//    
    // c.m. analysis
    RootTree -> Branch("pFiducCut"           ,&pFiducCut             );// std::vector<Int_t>
    RootTree -> Branch("Prec"                ,"TLorentzVector"       ,&Prec);
    RootTree -> Branch("pVertex"             ,&pVertex);             // std::vector<TVector3>


    // c.m. analysis
    RootTree -> Branch("Q2"                  ,&Q2                    ,"Q2/F");
    // p(cm) for RooFit
    RootTree -> Branch("Pmiss3Mag"           ,&Pmiss3Mag             , "Pmiss3Mag/F");
    RootTree -> Branch("pcmX"                ,&pcmX                  , "pcmX/F");
    RootTree -> Branch("pcmY"                ,&pcmY                  , "pcmY/F");
    RootTree -> Branch("pcmT"                ,&pcmT                  , "pcmT/F");
    RootTree -> Branch("pcmZ"                ,&pcmZ                  , "pcmZ/F");
    RootTree -> Branch("rooWeight"           ,&rooWeight             , "rooWeight/F");


}


//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void GenerateEvents::ComputeWeights(){
    Theta           = e.Theta();
    Mott            = pow( cos(Theta/2.) , 2 ) / pow( sin(Theta/2.) , 4 );
    DipoleFF2       = pow( 1./(1. + Q2/0.71) , 4);
    rooWeight       =  1./ ( Mott * DipoleFF2 ) ;
}



//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void GenerateEvents::OutPutToTextFile(const int N , TVector3 * momentum , int * charge , float * mass, int * pid){
    if (debug > 3) cout << "OutPutToTextFile..." << endl;
    float x = 0 , y  = 0 , z  = 0 , t_off = 0 ;
    int flag = 0;
    TextFile << N << std::endl;
    for (int j = 0 ; j < N ; j++ ){
        float   p_mag = momentum[j].Mag();
        float   cx  = momentum[j].x()/p_mag, cy = momentum[j].y()/p_mag  , cz = momentum[j].z()/p_mag ;
        TextFile << pid[j]  <<" "<< cx      <<" "<< cy  <<" "<< cz      <<" "<< p_mag     <<std::endl;
        TextFile << mass[j] <<" "<< charge[j]  << std::endl;
        TextFile << x       <<" "<< y       <<" "<< z   <<" "<< t_off   <<" "<< flag    <<std::endl;
    }
}






#endif
