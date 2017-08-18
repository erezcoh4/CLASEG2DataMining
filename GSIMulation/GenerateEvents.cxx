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
                                        Float_t fb1, Float_t fb2,
                                        Float_t fa1, Float_t fa2 ) {

    // Px = gRandom -> Gaus( MeanX  , SigmaX )
    // Py = gRandom -> Gaus( MeanY  , SigmaY )
    // Pz = gRandom -> Gaus( b1*(PmissMag-0.6) + b2  , a1*(PmissMag-0.6) + a2 )
    MeanX     = fMeanX;    SigmaX    = fSigmaX;
    MeanY     = fMeanY;    SigmaY    = fSigmaY;

    a1 = fa1;
    a2 = fa2;
    b1 = fb1;
    b2 = fb2;
}


//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void GenerateEvents::Set_eep_Parameters_MeanXYZ_Sigma(Float_t fMeanX, Float_t fMeanY, Float_t fMeanZ, Float_t fSigma_t, Float_t fSigmaZ  ) {
    MeanX = fMeanX;
    MeanY = fMeanY;
    MeanZ = fMeanZ;
    Sigma_t = fSigma_t;
    SigmaZ = fSigmaZ;
}


//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void GenerateEvents::Set_eep_Parameters_Pmiss_vanish_at_03(Float_t fMeanX, Float_t fMeanY, Float_t fSigma_t, Float_t fSigmaZ, Float_t fMeanZ_slope) {
    MeanX = fMeanX;
    MeanY = fMeanY;
    Sigma_t = fSigma_t;
    SigmaZ = fSigmaZ;
    // this is for
    // p(cm)-z = slope * ( p(miss) - 0.3 )
    MeanZ_slope = fMeanZ_slope;
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
void GenerateEvents::AddInputChain_eep(TString ChainOption, TString target_name ){
    InputT  = new TChain("T");
    // Take 12C(e,e'p) SRC tree data
    if  (ChainOption == "Or' original trees"){
        InputT -> Add( Path + "/DATA/SRC_e1_C.root");
        InputT -> Add( Path + "/DATA/SRC_e2_C.root");
    }
    else if  (ChainOption == "Or' coulomb trees"){
        InputT -> Add( Path + "/DATA/SRC_e1p_C_GoodRuns_coulomb.root");
        InputT -> Add( Path + "/DATA/SRC_e2p_C_GoodRuns_coulomb.root");
    }
    else if (ChainOption == "300<p(miss)<600 MeV/c"){
        InputT -> Add( Path + "/DATA_300Pmiss600/SRC_e1p_adjusted_300Pmiss600_"+target_name+"_PrecFiducials.root");
        InputT -> Add( Path + "/DATA_300Pmiss600/SRC_e2p_adjusted_300Pmiss600_"+target_name+"_PrecFiducials.root");
    }
    InputNentries = InputT -> GetEntries();
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void GenerateEvents::SetInputChain_eep(){
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
    InputT -> SetBranchAddress("theta_Pmiss",        &theta_Pmiss);
    InputT -> SetBranchAddress("phi_Pmiss",          &phi_Pmiss);
    
    InputT -> SetBranchAddress("Pmiss_size",         &Pm_size);
    InputT -> SetBranchAddress("q"       ,           &q);
    InputT -> SetBranchAddress("q_size"  ,           &q_size);
    InputT -> SetBranchAddress("Pmiss_q_angle",      &theta_miss_q);
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void GenerateEvents::ReleaseInputChain_eep(){delete InputT;}


//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void GenerateEvents::InitRun(){
    
    for (int PmissBin=0; PmissBin<5; PmissBin++){
        NAcceptedPmissBins[PmissBin] = 0;
    }
    for (int smallPmissBin=0; smallPmissBin<10; smallPmissBin++){
        NGen10PmissBins[smallPmissBin] = 0;
        NAcc10PmissBins[smallPmissBin] = 0;
        NLoss10PmissBins[smallPmissBin] = 0;
        for (int Q2Bin=0; Q2Bin<4; Q2Bin++){
            NGen10PmissBins_4Q2Bins[smallPmissBin][Q2Bin] = 0;
            NAcc10PmissBins_4Q2Bins[smallPmissBin][Q2Bin] = 0;
            NLoss10PmissBins_4Q2Bins[smallPmissBin][Q2Bin] = 0;
        }
        for (int theta_Pm_qBin=0; theta_Pm_qBin<4; theta_Pm_qBin++){
            NGen10PmissBins_4theta_Pm_qBins[smallPmissBin][theta_Pm_qBin] = 0;
            NAcc10PmissBins_4theta_Pm_qBins[smallPmissBin][theta_Pm_qBin] = 0;
            NLoss10PmissBins_4theta_Pm_qBins[smallPmissBin][theta_Pm_qBin] = 0;
        }
    }
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void GenerateEvents::InitEvent(){
    Debug(3,"GenerateEvents::InitEvent()");
    if (!pFiducCut.empty()) pFiducCut.clear();
    if (!pVertex.empty())   pVertex.clear();
}

//
////....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
//void GenerateEvents::SetMyInputChain_eep(){
//    InputT  = new TChain("anaTree");
//    // Take 12C(e,e'p) SRC tree data
//    InputT -> Add( "/Users/erezcohen/Desktop/DataMining/AnaFiles/Ana_eep_in_ppSRCCut_DATA_C12.root"); // this tree contains (e,e'p) as well as (e,e'pp)
//    InputT -> SetBranchAddress("*"              ,0);
//    InputT -> SetBranchAddress("Pmiss"          ,&Pmiss4vec);
//    InputT -> SetBranchAddress("Plead"          ,&Plead4vec);
//    InputT -> SetBranchAddress("q_phi"          ,&q_Phi);
//    InputT -> SetBranchAddress("Pmiss_phi"      ,&Pmiss_phi);
//    InputT -> SetBranchAddress("Pmiss_theta"    ,&Pmiss_theta);
//    if (debug>0){SHOW(InputT -> GetEntries());}
//}
//

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void GenerateEvents::MapInputEntriesInPmissBins(){
    for (entry = 0 ; entry < InputNentries ; entry++ ) {
        InputT -> GetEntry( entry );
        Pmiss3Mag = Pm_size[0];
        int PmissBin = FindWhichPmissBin( Pmiss3Mag );
        EntriesInPmissBins[PmissBin].push_back( entry );
    }
    if (debug>3){
        for (int PmissBin=0; PmissBin<5 ;PmissBin++){
            SHOW(PmissBin);
            SHOWstdVector(EntriesInPmissBins[PmissBin]);
        }
    }
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
Int_t GenerateEvents::DoGenerate_eepp_from_eep( Int_t fRunNumber ){
    
    RunNumber = fRunNumber ;
    NAcceptedEvents = Nevents = 0;
    txtFilename  = Form("%s/eg_txtfiles/run%d.txt",Path.Data(),RunNumber);
    rootFilename = Form("%s/eg_rootfiles/run%d.root",Path.Data(),RunNumber);
    if (debug>2) cout << "Generating " <<  rootFilename << endl;
    RootFile = new TFile( rootFilename ,"recreate" );
    RootTree = new TTree("anaTree","generated events");
    SetRootTreeAddresses();
    int attempt=0;
    Nattempts = 0;
    
    // generate events up to NgenMAX
    while (attempt < NgenMAX) {
        
        if ( debug>0 && attempt%(NgenMAX/100) == 0 ) {
            for (int PmissBin=0; PmissBin<5 ;PmissBin++){
                Printf("NWantedPmissBins[%i]=%d , NAcceptedPmissBins[%i]=%d",PmissBin,NWantedPmissBins[PmissBin],PmissBin,NAcceptedPmissBins[PmissBin]);
            }
            PrintLine();
        }
        InitEvent();
        // grab an entry with Pmiss in bins that are not full yet
        entry = GrabEntryInUnfilledPmissBins();
        if (entry==-1) break; // this means that all Pmiss bins are full
        InputT -> GetEntry( entry );
        if (debug>2) SHOW(entry);
        
        theta_miss_q = TMath::DegToRad()*theta_miss_q;
        double PmissMag = Pm_size[0];
        if (debug>2) SHOW(PmissMag);
        
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
        // - -- -- -- - ---- - -- - -- -- -- - -- - -- - -- - -- - -- - -- -- - - -- - - - -- - - - - - - - --
        double omega    = 5.014 - sqrt( 0.000511*0.000511 + e.Mag()*e.Mag() );
        ThetaPQ         = (180/TMath::Pi())*(Pp1.Angle(q3Vector));
        theta_miss_q    = (180/TMath::Pi())*(Pmiss.Angle(q3Vector));
        PoverQ          = Pp1.Mag()/q3Vector.Mag();
        Proton          .SetVectM   ( Pp1 , 0.938 ); // struck proton
        q4Vector        .SetXYZT    ( q3Vector.x() , q3Vector.y() , q3Vector.z() , omega );
        Q2              = - q4Vector.Mag();
        m2N             .SetVectM   ( TVector3(0,0,0) , 2.*0.938 );
        miss            = q4Vector + m2N - Proton;
        Mmiss           = miss.Mag();
        Rp1             .SetXYZ(Rproton[0][0],Rproton[0][1],Rproton[0][2]);
        Rp2 = Rp1;// since there is no actual Rp2....
        if(debug > 2) SHOW3( Mmiss , PoverQ , theta_miss_q );
        // struck proton fiducial cut and vertex
        pFiducCut.push_back( eg2dm->protonFiducial( Pmiss+q3Vector , debug ) );
        pVertex.push_back( Rp1 );
        pVertex.push_back( Rp2 );
        
        for( int j = 0 ; j < NRand  ;  j++ ){    //MC event generation
            
            if(debug > 3) SHOW( j );
            float Px = gRandom -> Gaus( MeanX  , SigmaX );
            float Py = gRandom -> Gaus( MeanY  , SigmaY );
            float MeanZ = b1*(PmissMag-0.6) + b2  ;
            float SigmaZ = a1*(PmissMag-0.6) + a2 ;
            float Pz = gRandom -> Gaus( MeanZ  , SigmaZ ) ;
            
            Pcm_in_Pmiss_q_system.SetXYZ ( Px , Py , Pz );
            Precoil_in_Pmiss_q_system = Pcm_in_Pmiss_q_system - Pmiss_in_Pmiss_q_system;
            
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
            if (DoPrecResolution){ // smear the reconstructed momentum of the recoil proton by the CLAS resolution (20 MeV/c)
                Precoil.SetMag( gRandom->Gaus( Precoil.Mag() , PrecResolution ) );
            }
            ThetaPmissPrecoil   = (180/TMath::Pi())*(Pmiss.Angle(Precoil));
            Prec.SetVectM( Precoil , Mp );
            
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
            auto PrecoilFiducialCut = eg2dm->protonFiducial( Precoil , debug );
            
            
            // #IMPORTANT: the acceptance map that i've created i given in the lab frame
            Double_t PrecoilMag = Precoil.Mag() , PrecoilTheta = r2d*Precoil.Theta() , PrecoilPhi = r2d*Precoil.Phi();
            PrecoilPhi =  eg2dm->ChangePhiToPhiLab( PrecoilPhi ) ; // rescale phi angle to the range [-30,330]
            if(debug > 3) SHOW3( PrecoilMag , PrecoilTheta , PrecoilPhi );
            if ( PrecoilTheta <= 120 ){
                Debug(3 , "in if ( PrecoilTheta <= 120 )");
                if (    h_protonAcceptance->GetXaxis()->GetBinCenter(1) < PrecoilMag   && PrecoilMag   < h_protonAcceptance->GetXaxis()->GetBinCenter(h_protonAcceptance->GetNbinsX())
                    && h_protonAcceptance->GetYaxis()->GetBinCenter(1) < PrecoilTheta && PrecoilTheta < h_protonAcceptance->GetYaxis()->GetBinCenter(h_protonAcceptance->GetNbinsY())
                    && h_protonAcceptance->GetZaxis()->GetBinCenter(1) < PrecoilPhi   && PrecoilPhi   < h_protonAcceptance->GetZaxis()->GetBinCenter(h_protonAcceptance->GetNbinsZ())    ) {
                    Double_t PrecoilAcceptance = h_protonAcceptance -> Interpolate( PrecoilMag , PrecoilTheta , PrecoilPhi ) / 100.;
                    if(debug > 3) SHOW( PrecoilAcceptance );
                    if( gRandom->Uniform() <= PrecoilAcceptance ){ // event is accepted in PrecoilAcceptance %
                        AcceptEvent = true;
                        if (debug>3) SHOW(AcceptEvent);
                    }
                }
            }
            Debug(4,"passed  if ( PrecoilTheta <= 120 )");
            
            
            // if ( PrecoilTheta <= 120 ) AcceptEvent=true;
            // ------------------------------------------------
            
            
            if ( Do_PrecFiducial )  AcceptEvent = (PrecoilFiducialCut == 1) ? AcceptEvent : false;
            if ( Do_PrecMinCut )    AcceptEvent = (Prec.P() > 0.35) ? AcceptEvent : false;

            
            if (AcceptEvent){
                Debug( 3 , Form("event in j=%d was accepted",j) );
                RootTree -> Fill();
                NAcceptedEvents++ ;
                SetAcceptedEventsPmissBins( Pmiss3Mag );
            } else {
                Debug( 3 , Form("event in j=%d was not accepted",j) );
            }
            SetEventsLossIn10PmissBins( Pmiss3Mag , AcceptEvent );
            SetEventsLossIn10PmissBins_4Q2Bins( Pmiss3Mag , Q2 , AcceptEvent );
            SetEventsLossIn10PmissBins_4theta_Pm_qBins( Pmiss3Mag , theta_miss_q , AcceptEvent );
            if(debug > 3) SHOW( NAcceptedEvents );
            attempt++;
        }
    }
    RootFile -> Write();
    RootFile -> Close();
    
    Nattempts = attempt;
    if ( entry==-1 ) {
        Printf("done generating %d (e,e'pp) events (out of %d attempts) to %s",NAcceptedEvents,attempt,rootFilename.Data());
        return NAcceptedEvents;
    }
    else if ( attempt == NgenMAX ) {
        Printf("could not fulfill desired quantites in PmissBins (accepted %d (e,e'pp) events out of %d attempts)",NAcceptedEvents,attempt);
        return -1;
    }
    else {
        SHOW2(entry,attempt);
        return -1;
    }
}




//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
// for analysis of 300 < p(miss) < 600 MeV/c
// -- - - --- -- - -- --- - - --- -- - -- --- - - --- -- - -- --- - - --- -- - -- -
Int_t GenerateEvents::DoGenerate_eepp_from_eep_SingleParameterSigma( Int_t fRunNumber , TString rootFilenameSuffix ){
    
    RunNumber = fRunNumber ;
    NAcceptedEvents = Nevents = 0;
    entry = -1;
    rootFilename = Form("%s/eg_rootfiles/run%d%s.root",Path.Data(),RunNumber,rootFilenameSuffix.Data());
    if (debug>2) cout << "Generating " <<  rootFilename << endl;
    RootFile = new TFile( rootFilename ,"recreate" );
    RootTree = new TTree("anaTree","generated events");
    genTree = new TTree("genTree","no acceptance no nothing. only generated features");
    SetRootTreeAddresses();
    int attempt=0;
    
    // generate events up to NgenMAX
    while (     (attempt < NgenMAX)
           &&   (NAcceptedEvents < NWantedEvents)
           ) {
        if ( debug>0 && attempt%(NgenMAX/100) == 0 ) {
            SHOW3(NWantedEvents,NAcceptedEvents,attempt);
            PrintLine();
        }
        InitEvent();
        if (DoRandomEntry) {
            entry = (int)( InputNentries * gRandom->Uniform() );
        }
        else {
            // use all the entries in the input (e,e'p) tree one-by-one:
            // increment the entry number
            entry += 1;
            // and if we got to the last entry in the input tree, return to the first one
            if (entry > InputNentries) entry = 0;
        }
        InputT -> GetEntry( entry );
        if (debug>2) SHOW(entry);
        
        theta_miss_q = TMath::DegToRad()*theta_miss_q;
        double PmissMag = Pm_size[0];
        if (debug>2) SHOW(PmissMag);
        
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
        // - -- -- -- - ---- - -- - -- -- -- - -- - -- - -- - -- - -- - -- -- - - -- - - - -- - - - - - - - --
        double omega    = 5.014 - sqrt( 0.000511*0.000511 + e.Mag()*e.Mag() );
        ThetaPQ         = (180/TMath::Pi())*(Pp1.Angle(q3Vector));
        PoverQ          = Pp1.Mag()/q3Vector.Mag();
        Proton          .SetVectM   ( Pp1 , 0.938 ); // struck proton
        q4Vector        .SetXYZT    ( q3Vector.x() , q3Vector.y() , q3Vector.z() , omega );
        m2N             .SetVectM   ( TVector3(0,0,0) , 2.*0.938 );
        miss            = q4Vector + m2N - Proton;
        Mmiss           = miss.Mag();
        Rp1             .SetXYZ(Rproton[0][0],Rproton[0][1],Rproton[0][2]);
        Rp2 = Rp1;// since there is no actual Rp2....
        if(debug > 2) SHOW3( Mmiss , PoverQ , theta_miss_q );
        // struck proton fiducial cut and vertex
        pFiducCut.push_back( eg2dm->protonFiducial( Pmiss+q3Vector , debug ) );
        pVertex.push_back( Rp1 );
        pVertex.push_back( Rp2 );
        
        for( int j = 0 ; j < NRand  ;  j++ ){    //MC event generation
            
            if(debug > 3) SHOW( j );
            float Px = gRandom -> Gaus( MeanX , Sigma_t );
            float Py = gRandom -> Gaus( MeanY , Sigma_t );
            
            if (Do_PcmZ_Pmiss_vanish_at_03){
                MeanZ = MeanZ_slope * ( Pmiss3Mag - 0.3 );
            }
            float Pz = gRandom -> Gaus( MeanZ , SigmaZ  );
            if (debug>3){ // ToDo: change to debug>4
                SHOW3( MeanX , MeanY , Sigma_t );
                SHOW3( Pmiss3Mag , MeanZ , SigmaZ );
            }
            
            Pcm_in_Pmiss_q_system.SetXYZ ( Px , Py , Pz );
            Precoil_in_Pmiss_q_system = Pcm_in_Pmiss_q_system - Pmiss_in_Pmiss_q_system;
            
            // for RooFits
            Pmiss3Mag = PmissMag;
            // here we already work in the Pmiss(z) - q(x-z) frame
            // and the rootfile would have pcmX,pcmY,pcmZ in the frame to be analyzed,
            // without the need to rotate vectors to another frame...
            pcmX = Px ;
            pcmY = Py ;
            pcmZ = Pz ;
            ComputeWeights();
            
            // now, rotate back to lab frame
            Pcm = Pcm_in_Pmiss_q_system;
            Pcm.RotateZ  ( q_Phi );
            Pcm.RotateY  ( Pmiss_theta );
            Pcm.RotateZ  ( Pmiss_phi );
            Precoil = Pp2 = Pcm - Pmiss;
            
            if (debug>3) {
                SHOW3(Pm[0][0],Pm[0][1],Pm[0][2]);
                SHOWTVector3(Pcm_in_Pmiss_q_system);
                
                SHOWTVector3(Pcm);
                SHOWTVector3(Pmiss);
                SHOWTVector3(Precoil);
            }
            
            if (DoPrecResolution){ // smear the reconstructed momentum of the recoil proton by the CLAS resolution (20 MeV/c)
                Precoil.SetMag( gRandom->Gaus( Precoil.Mag() , PrecResolution ) );
            }
            
            ThetaPmissPrecoil   = (180/TMath::Pi())*(Pmiss.Angle(Precoil));
            Prec.SetVectM( Precoil , Mp );
            
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
            auto PrecoilFiducialCut = eg2dm->protonFiducial( Precoil , debug );

            
            // #IMPORTANT: the acceptance map that i've created i given in the lab frame
            Double_t PrecoilMag = Precoil.Mag() , PrecoilTheta = r2d*Precoil.Theta() , PrecoilPhi = r2d*Precoil.Phi();
            PrecoilPhi =  eg2dm->ChangePhiToPhiLab( PrecoilPhi ) ; // rescale phi angle to the range [-30,330]
            
            if(debug > 3) SHOW3( PrecoilMag , PrecoilTheta , PrecoilPhi );
            if ( PrecoilTheta <= 120 ){
                Debug(3 , "in if ( PrecoilTheta <= 120 )");
                if (    h_protonAcceptance->GetXaxis()->GetBinCenter(1) < PrecoilMag   && PrecoilMag   < h_protonAcceptance->GetXaxis()->GetBinCenter(h_protonAcceptance->GetNbinsX())
                    && h_protonAcceptance->GetYaxis()->GetBinCenter(1) < PrecoilTheta && PrecoilTheta < h_protonAcceptance->GetYaxis()->GetBinCenter(h_protonAcceptance->GetNbinsY())
                    && h_protonAcceptance->GetZaxis()->GetBinCenter(1) < PrecoilPhi   && PrecoilPhi   < h_protonAcceptance->GetZaxis()->GetBinCenter(h_protonAcceptance->GetNbinsZ())    ) {
                    Double_t PrecoilAcceptance = h_protonAcceptance -> Interpolate( PrecoilMag , PrecoilTheta , PrecoilPhi ) / 100.;
                    if(debug > 3) SHOW( PrecoilAcceptance );
                    if( gRandom->Uniform() <= PrecoilAcceptance ){ // event is accepted in PrecoilAcceptance %
                        AcceptEvent = true;
                        if (debug>3) SHOW(AcceptEvent);
                    }
                }
            }
            Debug(4,"passed  if ( PrecoilTheta <= 120 )");
            
            if ( Do_PrecFiducial )  AcceptEvent = (PrecoilFiducialCut==1) ? AcceptEvent : false;
            if ( Do_PrecMinCut )    AcceptEvent = (Prec.P()>0.35) ? AcceptEvent : false;
            
            genTree -> Fill();
            
            if (AcceptEvent){
                Debug( 3 , Form("event in j=%d was accepted",j) );
                RootTree -> Fill();
                NAcceptedEvents++ ;
            } else {
                Debug( 3 , Form("event in j=%d was not accepted",j) );
            }
            if(debug > 3) SHOW( NAcceptedEvents );
            attempt++;
        }
    }
    RootFile -> Write();
    RootFile -> Close();
    
    if ( NAcceptedEvents >= NWantedEvents ) {
        Printf("done generating %d (e,e'pp) events (out of %d attempts) to %s",NAcceptedEvents,attempt,rootFilename.Data());
        return NAcceptedEvents;
    }
    else if ( attempt == NgenMAX ) {
        Printf("could not fulfill desired quonta (NAcceptedEvents=%d events, attempt=%d)",NAcceptedEvents,attempt);
        return -1;
    }
    else {
        SHOW2(entry,attempt);
        return -1;
    }
}



//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
bool GenerateEvents::AllPmissBinsFilled(){
    for (int PmissBin=0;PmissBin<5;PmissBin++){
        if (NAcceptedPmissBins[PmissBin] < NWantedPmissBins[PmissBin]) {
            Debug(4,Form("PmissBin %d is not Filled",PmissBin));
            return false;
        }
    }
    Debug(4,"AllPmissBinsFilled");
    return true;
}



//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
int GenerateEvents::GrabEntryInUnfilledPmissBins(){
    // grab one entry from input chain at a uniform probability
    for (int PmissBin=0; PmissBin<5; PmissBin++) {
        //if (debug>2) {Printf("NWantedPmissBins[%i]=%d , NAcceptedPmissBins[%i]=%d",PmissBin,NWantedPmissBins[PmissBin],PmissBin,NAcceptedPmissBins[PmissBin]);}
        if (NAcceptedPmissBins[PmissBin] < NWantedPmissBins[PmissBin]) {
            int i_random = (int)(EntriesInPmissBins[PmissBin].size()*(gRandom->Uniform()));
            entry = EntriesInPmissBins[PmissBin].at( i_random );
            if (debug>2) {Printf("Not enough events in PmissBin %d (acc. %d /req. %d), generating entry %d",PmissBin,NAcceptedPmissBins[PmissBin],NWantedPmissBins[PmissBin],entry);}
            return entry;
        }
    }
    Debug(2,"all Pmiss bins are full");
    return -1;
}



//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void GenerateEvents::SetAcceptedEventsPmissBins( float fPmiss3Mag ){
    int PmissBin = FindWhichPmissBin( fPmiss3Mag );
    NAcceptedPmissBins[PmissBin] += 1;
    if (debug>2) Printf("filling PmissBin %d (so far %d accepted events in this bin)",PmissBin,NAcceptedPmissBins[PmissBin]);
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
int GenerateEvents::FindWhichPmissBin(float fPmiss3Mag){
    for (int i=0;i<5;i++){
        if (PmissBins[i][0] < fPmiss3Mag && fPmiss3Mag < PmissBins[i][1]){
            return i;
        }
    }
    return 0;
}


//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
int GenerateEvents::FindWhichQ2Bin(float fQ2){
    for (int i=0;i<4;i++){
        if (Q2Bins[i][0] < fQ2 && fQ2 < Q2Bins[i][1]){
            return i;
        }
    }
    return 0;
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
int GenerateEvents::FindWhich_theta_Pm_qBin(float ftheta_Pm_q){
    for (int i=0;i<4;i++){
        if (theta_Pm_qBins[i][0] < ftheta_Pm_q && ftheta_Pm_q < theta_Pm_qBins[i][1]){
            return i;
        }
    }
    return 0;
}


//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void GenerateEvents::SetEventsLossIn10PmissBins( float fPmiss3Mag , bool fAcceptEvent ){
    int smallPmissBin = FindWhichPmiss10Bin( fPmiss3Mag );
    NGen10PmissBins[smallPmissBin] += 1;
    if (fAcceptEvent){
        NAcc10PmissBins[smallPmissBin] += 1;
    }
    else{
        NLoss10PmissBins[smallPmissBin] += 1;
    }
}



//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void GenerateEvents::SetEventsLossIn10PmissBins_4Q2Bins( float fPmiss3Mag, float fQ2 , bool fAcceptEvent ){
    int smallPmissBin = FindWhichPmiss10Bin( fPmiss3Mag );
    int Q2Bin = FindWhichQ2Bin( fQ2 );
    NGen10PmissBins_4Q2Bins[smallPmissBin][Q2Bin] += 1;
    if (fAcceptEvent){
        NAcc10PmissBins_4Q2Bins[smallPmissBin][Q2Bin] += 1;
    }
    else{
        NLoss10PmissBins_4Q2Bins[smallPmissBin][Q2Bin] += 1;
    }
}


//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void GenerateEvents::SetEventsLossIn10PmissBins_4theta_Pm_qBins( float fPmiss3Mag, float ftheta_Pm_q , bool fAcceptEvent ){
    int smallPmissBin = FindWhichPmiss10Bin( fPmiss3Mag );
    int theta_Pm_qBin = FindWhichQ2Bin( ftheta_Pm_q );
    NGen10PmissBins_4theta_Pm_qBins[smallPmissBin][theta_Pm_qBin] += 1;
    if (fAcceptEvent){
        NAcc10PmissBins_4theta_Pm_qBins[smallPmissBin][theta_Pm_qBin] += 1;
    }
    else{
        NLoss10PmissBins_4theta_Pm_qBins[smallPmissBin][theta_Pm_qBin] += 1;
    }
}




//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
int GenerateEvents::FindWhichPmiss10Bin(float fPmiss3Mag){
    for (int i=0;i<10;i++){
        if (small10PmissBins[i][0] < fPmiss3Mag && fPmiss3Mag < small10PmissBins[i][1]){
            return i;
        }
    }
    return 0;
}

//
////....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
//Int_t GenerateEvents::Generate_eepp_from_3dGaussian( Int_t fRunNumber){
//    
//    RunNumber = fRunNumber ;
//    NAcceptedEvents = Nevents = 0;
//    rootFilename = Form("%s/eg_rootfiles/run%d.root",Path.Data(),RunNumber);
//    if (debug>2) cout << "Generating " <<  rootFilename << endl;
//    RootFile = new TFile( rootFilename ,"recreate" );
//    RootTree = new TTree("anaTree","generated events");
//    SetRootTreeAddresses();
//    
//    
//    float sigma_cm = SigmaX;
//    
//    for (int entry = 0 ; entry < InputNentries ; entry++ ) {
//        if ( debug > 2 && entry%(InputNentries/4) == 0 ) std::cout  <<  (int)(100*(double)entry/InputNentries)+1 << "%\n";
//        InitEvent();
//        InputT -> GetEntry(entry);
//        theta_miss_q = TMath::DegToRad()*theta_miss_q;
//        if(debug > 2) cout << "got entry " << entry << endl;
//        
//        
//        double PmissMag = Pm_size[0];
//        
//        e.SetXYZ            ( Pe[0]         , Pe[1]         , Pe[2]);
//        q3Vector.SetXYZ     ( q[0]          , q[1]          , q[2] );
//        Pmiss.SetXYZ        ( Pm[0][0]      , Pm[0][1]      , Pm[0][2]);
//        Pp1.SetXYZ          ( Pproton[0][0] , Pproton[0][1] , Pproton[0][2]);
//        
//        
//        if(debug > 2) cout << "rotate to Pmiss-q frame" << endl;
//        // rotate to Pmiss-q frame: Pmiss is the z axis, q is in x-z plane: q=(q[x],0,q[Pmiss])
//        double Pmiss_phi = Pmiss.Phi() , Pmiss_theta = Pmiss.Theta() ;
//        q3Vector_in_Pmiss_q_system = q3Vector;
//        q3Vector_in_Pmiss_q_system.RotateZ(-Pmiss_phi);
//        q3Vector_in_Pmiss_q_system.RotateY(-Pmiss_theta);
//        double q_Phi = q3Vector_in_Pmiss_q_system.Phi();
//        q3Vector_in_Pmiss_q_system.RotateZ(-q_Phi);
//        
//        Pmiss_in_Pmiss_q_system = Pmiss;
//        Pmiss_in_Pmiss_q_system.RotateZ(-Pmiss_phi);
//        Pmiss_in_Pmiss_q_system.RotateY(-Pmiss_theta);
//        
//        
//        if(debug > 2) cout << "define omega and other variables" << endl;
//        double  omega   = 5.009 - sqrt( 0.000511*0.000511 + e.Mag()*e.Mag() );
//        ThetaPQ         = (180/TMath::Pi())*(Pp1.Angle(q3Vector));
//        //        theta_miss_q     = (180/TMath::Pi())*(Pmiss.Angle(q3Vector));
//        PoverQ          = Pp1.Mag()/q3Vector.Mag();
//        Proton          .SetVectM   ( Pp1 , 0.938 ); // struck proton
//        q4Vector        .SetXYZT    ( q3Vector.x() , q3Vector.y() , q3Vector.z() , omega );
//        m2N             .SetVectM   ( TVector3(0,0,0) , 2.*0.938 );
//        miss            = q4Vector + m2N - Proton;
//        Mmiss           = miss.Mag();
//        Rp1             .SetXYZ(Rproton[0][0],Rproton[0][1],Rproton[0][2]); // since there is no actual Rp2....
//        Rp2 = Rp1;// since there is no actual Rp2....
//        if(debug > 2) SHOW3( Mmiss , PoverQ , theta_miss_q );
//        
//        // struck proton fiducial cut and vertex
//        pFiducCut.push_back( eg2dm->protonFiducial( Pmiss+q3Vector , debug ) );
//        pVertex.push_back( Rp1 );
//        // recoil proton vertex
//        pVertex.push_back( Rp2 );
//        
//        
//        for( int j = 0 ; j < NRand  ;  j++ ){    //MC event generation
//            
//            if(debug > 3) SHOW( j );
//            
//            
//            float Px = gRandom -> Gaus( 0  , sigma_cm );
//            float Py = gRandom -> Gaus( 0  , sigma_cm );
//            float Pz = gRandom -> Gaus( 0  , sigma_cm );
//            
//            
//            Pcm_in_Pmiss_q_system.SetXYZ ( Px , Py , Pz );
//            Precoil_in_Pmiss_q_system = Pcm_in_Pmiss_q_system - Pmiss_in_Pmiss_q_system;
//            if(debug > 3) cout << "set Pcm_in_Pmiss_q_system and Precoil_in_Pmiss_q_system " ;
//            
//            // for RooFits
//            Pmiss3Mag = PmissMag;
//            // here we already work in the Pmiss(z) - q(x-z) frame
//            pcmX = Px ;
//            pcmY = Py ;
//            pcmZ = Pz ;
//            ComputeWeights();
//            
//            // now, rotate back to lab frame
//            Pcm = Pcm_in_Pmiss_q_system;
//            Pcm.RotateZ  ( q_Phi );
//            Pcm.RotateY  ( Pmiss_theta );
//            Pcm.RotateZ  ( Pmiss_phi );
//            Precoil =   Pp2     = Pcm - Pmiss;
//            ThetaPmissPrecoil   = (180/TMath::Pi())*(Pmiss.Angle(Precoil));
//            Prec.SetVectM( Precoil , Mp );
//            
////            momentum[0] = e ; momentum[1] = Pp1; momentum[2] = Pp2;
//            
//            if(debug > 3) cout << "rotate also to q-Pmiss frame: q is the z axis" << endl;
//            
//            // finish
//            Nevents++;
//            if(debug > 3) SHOW( Nevents );
//            
//            // recoil proton acceptance
//            // ------------------------------------------------
//            // decide if this event is accepted as a legitimate (e,e'pp) event based on the recoiling proton acceptance
//            AcceptEvent = false;
//            if ( !Do_pAcceptance )  AcceptEvent = true; // in case we do not want to use the proton acceptances
//            
//            
//            // recoil proton fiducial cut
//            pFiducCut.push_back( eg2dm->protonFiducial( Precoil , debug ) );
//            
//            
//            
//            // #IMPORTANT: the acceptance map that i've created i given in the lab frame
//            Double_t PrecoilMag = Precoil.Mag() , PrecoilTheta = r2d*Precoil.Theta() , PrecoilPhi = r2d*Precoil.Phi();
//            PrecoilPhi =  eg2dm->ChangePhiToPhiLab( PrecoilPhi ) ; // rescale phi angle to the range [-30,330]
//            if(debug > 3) SHOW3( PrecoilMag , PrecoilTheta , PrecoilPhi );
//            Printf("before  if ( PrecoilTheta <= 120 )");
//            if ( PrecoilTheta <= 120 ){
//                Printf("in  if ( PrecoilTheta <= 120 )");
//                if (    h_protonAcceptance->GetXaxis()->GetBinCenter(1) < PrecoilMag
//                    && PrecoilMag   < h_protonAcceptance->GetXaxis()->GetBinCenter(h_protonAcceptance->GetNbinsX())){
//                        Printf("in if (    h_protonAcceptance->GetXaxis()->GetBinCenter(1) < PrecoilMag && PrecoilMag   < h_protonAcceptance->GetXaxis()->GetBinCenter(h_protonAcceptance->GetNbinsX())");
//                        if (h_protonAcceptance->GetYaxis()->GetBinCenter(1) < PrecoilTheta
//                            && PrecoilTheta < h_protonAcceptance->GetYaxis()->GetBinCenter(h_protonAcceptance->GetNbinsY())){
//                            Printf("in if (    h_protonAcceptance->GetYaxis()->GetBinCenter(1) < PrecoilMag && PrecoilMag   < h_protonAcceptance->GetYaxis()->GetBinCenter(h_protonAcceptance->GetNbinsY())");
//
//                            if (h_protonAcceptance->GetZaxis()->GetBinCenter(1) < PrecoilPhi
//                                && PrecoilPhi   < h_protonAcceptance->GetZaxis()->GetBinCenter(h_protonAcceptance->GetNbinsZ())){
//                                Printf("in if (    h_protonAcceptance->GetZaxis()->GetBinCenter(1) < PrecoilMag && PrecoilMag   < h_protonAcceptance->GetZaxis()->GetBinCenter(h_protonAcceptance->GetZaxis())");
//
//                                Double_t PrecoilAcceptance = h_protonAcceptance -> Interpolate( PrecoilMag , PrecoilTheta , PrecoilPhi ) / 100.;
//                                if(debug > 3) SHOW( PrecoilAcceptance );
//                                if( gRandom->Uniform() <= PrecoilAcceptance ){ // event is accepted in PrecoilAcceptance %
//                                    AcceptEvent = true;
//                                }
//                                
//                            }
//                        }
//                    }
//
//                if (    h_protonAcceptance->GetXaxis()->GetBinCenter(1) < PrecoilMag
//                    && PrecoilMag   < h_protonAcceptance->GetXaxis()->GetBinCenter(h_protonAcceptance->GetNbinsX())
//                    && h_protonAcceptance->GetYaxis()->GetBinCenter(1) < PrecoilTheta
//                    && PrecoilTheta < h_protonAcceptance->GetYaxis()->GetBinCenter(h_protonAcceptance->GetNbinsY())
//                    && h_protonAcceptance->GetZaxis()->GetBinCenter(1) < PrecoilPhi
//                    && PrecoilPhi   < h_protonAcceptance->GetZaxis()->GetBinCenter(h_protonAcceptance->GetNbinsZ())    ) {
//                    
//                }
//            }
//            Printf("after  if ( PrecoilTheta <= 120 )");
//
//            // if ( PrecoilTheta <= 120 ) AcceptEvent=true;
//            // ------------------------------------------------
//            
//            if (AcceptEvent){
//                if(debug > 3) Printf( "event was accepted" );
//                RootTree -> Fill();
//                NAcceptedEvents++ ;
//            } else {
//                if(debug > 3) Printf( "event was not accepted" );
//            }
//            if(debug > 3) SHOW( NAcceptedEvents );
//            
//        }
//    }
//    
//    RootFile -> Write();
//    RootFile -> Close();
//    
//    Printf("done generating %d (e,e'pp) events to %s",NAcceptedEvents,rootFilename.Data());
//    
//    return Nevents;
//    
//}
//
//
//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
Int_t GenerateEvents::DoGenerate( TString Type,
                                 bool DoGetRootFile, bool DoGenTextFile,
                                 TString BaryonName,
                                 bool DoReeNFromTree, bool DoReeNFromDist, bool DoFlateeN){
    // return the number of events
    SHOW3( DoReeNFromTree , DoReeNFromDist , DoFlateeN );
//
//    NAcceptedEvents = Nevents = 0;
//    txtFilename     = Form("%s/eg_txtfiles/run%d.txt",Path.Data(),RunNumber);
//    rootFilename    = Form("%s/eg_rootfiles/run%d.root",Path.Data(),RunNumber);
//    if (DoGenTextFile){
//        cout << "Generating " << txtFilename << endl;
//        TextFile.open(txtFilename);
//    }
//    if (DoGetRootFile){
//        cout << "Generating " <<  rootFilename << endl;
//        RootFile = new TFile( rootFilename ,"recreate" );
//    }
//    RootTree = new TTree("anaTree","generated events");
//    SetRootTreeAddresses();
//    
//    if (Type == "(e,e')" ){
//        Printf("generating (e,e')");
//        TVector3 e;     // N is a baryon: p/n/𝚫
//        RootTree -> Branch( "e"         ,"TVector3" ,&e);
//        Double_t mag , theta , phi;
//        TVector3 * momentum = new TVector3[1];
//        
//        int charge[1]   = { -1      };
//        float mass[1]   = { 0.000511};
//        int pid[1]      = { 11      };
//        
//        for (int entry = 0 ; entry < NeTheta ; entry++ ) {
//            if ( entry%(NeTheta/10) == 0 ) std::cout  << (int)(100*(double)entry/NeTheta) << "%\n";
//            theta  = Thetamin + (Thetamax-Thetamin)*gRandom->Uniform();
//            mag    = Pmin + (Pmax-Pmin)*gRandom->Uniform();
//            for ( int rand = 0 ; rand < NRand ; rand++ ) {
//                phi    = 360.*gRandom->Uniform();         // uniform angle between 0 and 360 degrees
//                e.SetMagThetaPhi ( mag , (TMath::Pi()/180.)*theta , (TMath::Pi()/180.)*phi );
//                momentum[0] = e;
//                if (DoGenTextFile) OutPutToTextFile(1, momentum , charge ,mass , pid );
//                RootTree -> Fill();
//            }
//        }
//        
//    }
//    
//    else if (Type == "(e,e'pp)" ){
//        
//        DoGenerateRun_eepp( RunNumber,  DoGetRootFile, DoGenTextFile);
//        
//    }
//    
//    else if (Type == "(e,e'B)"){
//        Printf("(e,e'%s)",BaryonName.Data());
//        TVector3 e , N;     // N is a baryon: p/n/𝚫
//        RootTree -> Branch( BaryonName  ,"TVector3" ,&N);
//        RootTree -> Branch( "e"         ,"TVector3" ,&e);
//        Float_t mag , theta;
//        TVector3 * momentum     = new TVector3[2];
//        
//        int charge[2]           = { -1          , (BaryonName == "p") ? 1       : ((BaryonName == "n") ? 0      : 2)        };
//        float mass[2]           = { 0.000511    ,  static_cast<float>((BaryonName == "p") ? 0.938   : ((BaryonName == "n") ? 0.939  : 1.232))    };
//        int pid[2]              = { 11          , (BaryonName == "p") ? 2212    : ((BaryonName == "n") ? 2112   : 2214)     };
//        
//        
//        //------- TAKE DATA FROM TREE --------------//
//        if (DoReeNFromTree){
//            Printf("(e,e'%s) from Tree",BaryonName.Data());
//
//            Float_t PeMag, Theta_e, Phi_e ;//   , PpMag , Theta_p;
//            eeNTree -> SetBranchAddress("P_e"       ,   &PeMag);
//            eeNTree -> SetBranchAddress("theta_e"   ,   &Theta_e);
//            eeNTree -> SetBranchAddress("phi_e"     ,   &Phi_e);
//            eeNTree -> SetBranchAddress("P_N"       ,   &mag);
//            eeNTree -> SetBranchAddress("theta_N"   ,   &theta);
//            Int_t Nentries = (Int_t)eeNTree->GetEntries();
//            for (int entry = 0 ; entry < Nentries ; entry++ ) {
//                if ( entry%(Nentries/10) == 0 ) std::cout  << (int)(100*(float)entry/Nentries) << "%\n";
//                eeNTree -> GetEntry(entry);
//                if(debug > 2) SHOW3( PeMag , Theta_e , Phi_e );
//                e.SetMagThetaPhi(PeMag,(TMath::Pi()/180.)*Theta_e,(TMath::Pi()/180.)*Phi_e);
//                momentum[0] = e;
//                for ( int rand = 0 ; rand < NRand ; rand++ ) {
//                    Double_t phi    = 360.*gRandom->Uniform();         // uniform angle between 0 and 360 degrees
//                    if(debug > 2) SHOW3( mag , (TMath::Pi()/180.)*theta , (TMath::Pi()/180.)*phi );
//                    N.SetMagThetaPhi ( mag , (TMath::Pi()/180.)*theta , (TMath::Pi()/180.)*phi);
//                    momentum[1] = N;
//                    if (DoGenTextFile) OutPutToTextFile(2, momentum , charge ,mass , pid );
//                    RootTree -> Fill();
//                }
//            }
//        }
//        
//        //------- CREATE NEW DATA --------------//
//        else {
//            Printf("(e,e'%s) from scratch",BaryonName.Data());
//
//            TVector3 e(-0.137*4.306 , -0.339*4.306 , 0.956*4.306 ); // a single electron that passes RECSIS cuts...
//            momentum[0] = e;
//            for (int entry = 0 ; entry < NPTheta ; entry++ ) {
//                if ( entry%(NPTheta/10) == 0 ) std::cout  << (int)(100*(double)entry/NPTheta) << "%\n";
//                if (DoFlateeN){ // flat distributions
//                    theta  = Thetamin + (Thetamax-Thetamin)*gRandom->Uniform();
//                    mag    = Pmin + (Pmax-Pmin)*gRandom->Uniform();
//                } else if (DoReeNFromDist){  // take from file histograms
//                    theta  = histTheta ->GetRandom();
//                    mag    = histMag   ->GetRandom();
//                }
//                for ( int rand = 0 ; rand < NRand ; rand++ ) {
//                    Double_t phi    = 360.*gRandom->Uniform();         // uniform angle between 0 and 360 degrees
//                    N.SetMagThetaPhi ( mag , (TMath::Pi()/180.)*theta , (TMath::Pi()/180.)*phi);
//                    momentum[1] = N;
//                    if (DoGenTextFile) OutPutToTextFile(2, momentum , charge ,mass , pid );
//                    RootTree -> Fill();
//                }
//            }
//            
//        }
//    }
//    if (DoGetRootFile){
//
//        RootFile -> Write();
//        RootFile -> Close();
//    }
//    
//    if (DoGenTextFile){
//        
//        TextFile.close();
//        
//    }
//    
//    //    if (debug > 2) cout << "Out to Run Number File..." << endl;
//    //    OutRunNumberFile.open(runsFilename);
//    //    OutRunNumberFile << RunNumber << "\n" ;
//    //    OutRunNumberFile.close();
//    Printf("done generating events to %s",rootFilename.Data());
//    //    if (InputT) delete InputT;
//    return Nevents;
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
//    RootTree -> Branch("theta_miss_q"         ,&theta_miss_q           ,"theta_miss_q/F");          // angle between the missing momentum and q
//    RootTree -> Branch("ThetaPmissPrecoil"   ,&ThetaPmissPrecoil     ,"ThetaPmissPrecoil/F");    // angle between the missing and recoil momenta
//    RootTree -> Branch("PoverQ"              ,&PoverQ                ,"PoverQ/F");               // ratio |p|/|q| for leading proton
//    RootTree -> Branch("Mmiss"               ,&Mmiss                 ,"Mmiss/F");
    
    // generation
    RootTree -> Branch("gen_MeanX"              ,&MeanX                 ,"gen_MeanX/F");
    RootTree -> Branch("gen_MeanY"              ,&MeanY                 ,"gen_MeanY/F");
    RootTree -> Branch("gen_SigmaX"             ,&SigmaX                ,"gen_SigmaX/F");
    RootTree -> Branch("gen_SigmaY"             ,&SigmaY                ,"gen_SigmaY/F");
    RootTree -> Branch("gen_a1"                 ,&a1                    ,"gen_a1/F");
    RootTree -> Branch("gen_a2"                 ,&a2                    ,"gen_a2/F");
    RootTree -> Branch("gen_b1"                 ,&b1                    ,"gen_b1/F");
    RootTree -> Branch("gen_b2"                 ,&b2                    ,"gen_b2/F");

    // c.m. analysis
    RootTree -> Branch("pFiducCut"           ,&pFiducCut             );// std::vector<Int_t>
    RootTree -> Branch("Prec"                ,"TLorentzVector"       ,&Prec);
    RootTree -> Branch("pVertex"             ,&pVertex);             // std::vector<TVector3>
    RootTree -> Branch("theta_miss_q"        ,&theta_miss_q          , "theta_miss_q/F");


    // c.m. analysis
    RootTree -> Branch("Q2"                  ,&Q2                    ,"Q2/F");
    // p(cm) for RooFit
    RootTree -> Branch("Pmiss3Mag"           ,&Pmiss3Mag             , "Pmiss3Mag/F");
    RootTree -> Branch("pcmX"                ,&pcmX                  , "pcmX/F");
    RootTree -> Branch("pcmY"                ,&pcmY                  , "pcmY/F");
    RootTree -> Branch("pcmT"                ,&pcmT                  , "pcmT/F");
    RootTree -> Branch("pcmZ"                ,&pcmZ                  , "pcmZ/F");
    RootTree -> Branch("rooWeight"           ,&rooWeight             , "rooWeight/F");
    RootTree -> Branch("Mott"                ,&OrMott                , "Mott/F"); // Or weight

    // no acceptance no nothing. only generated features
    genTree -> Branch("Pmiss3Mag"           ,&Pmiss3Mag             , "Pmiss3Mag/F");
    genTree -> Branch("pcmX"                ,&pcmX                  , "pcmX/F");
    genTree -> Branch("pcmY"                ,&pcmY                  , "pcmY/F");
    genTree -> Branch("pcmT"                ,&pcmT                  , "pcmT/F");
    genTree -> Branch("pcmZ"                ,&pcmZ                  , "pcmZ/F");

}


//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void GenerateEvents::ComputeWeights(){
    Theta           = e.Theta();
    Mott            = pow( cos(Theta/2.) , 2 ) / pow( sin(Theta/2.) , 4 );
    DipoleFF2       = pow( 1./(1. + Q2/0.71) , 4);
    rooWeight       =  1./ ( Mott * DipoleFF2 ) ;
    
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
