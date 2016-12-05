#ifndef TSCHEMEDATA_CXX
#define TSCHEMEDATA_CXX

#include "TSchemeDATA.h"




//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
TSchemeDATA::TSchemeDATA(TString fDataType, TString fDataPath, TString fSchemedPath,
                         TString fInFileName  , TString fInTreeName ,
                         Int_t fdebug ) {
    SetDataType     (fDataType);
    SetDataPath     (fDataPath);
    SetSchemedPath  (fSchemedPath);
    SetInFileName   (fInFileName);
    SetOutFileName  ("Schemed"+fInFileName);
    SetInTreeName   (fInTreeName);
    SetOutTreeName  (fInTreeName);
    SetDebug        (fdebug);
}



//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void TSchemeDATA::LoadInTree(){
    InFile      = new TFile(Form("%s/%s.root",DataPath.Data(),InFileName.Data()));
    InTree      = (TTree*)InFile -> Get(InTreeName);
    Nentries    = InTree -> GetEntries();
    SHOW(Nentries);
    
    InTree -> SetBranchAddress("P_nmb"          , &Np);
    InTree -> SetBranchAddress("N_nmb"          , &Nn);
    InTree -> SetBranchAddress("T_nmb"          , &Ntotal);
    InTree -> SetBranchAddress("Xb"             , &Xb);
    
    if (DataType == "DATA") {
        InTree -> SetBranchAddress("Px"             , &PpX);
        InTree -> SetBranchAddress("Py"             , &PpY);
        InTree -> SetBranchAddress("Pz"             , &PpZ);
        InTree -> SetBranchAddress("Px_e"           , &Px_e);
        InTree -> SetBranchAddress("Py_e"           , &Py_e);
        InTree -> SetBranchAddress("Pz_e"           , &Pz_e);
        InTree -> SetBranchAddress("targ_type"      , &targ_type); // for Al27 remove this
    }
    else if(DataType == "NoCTofDATA" || DataType == "New_NoCTofDATA") {
        InTree -> SetBranchAddress("P_Px"           , &PpX);    // protons momenta
        InTree -> SetBranchAddress("P_Py"           , &PpY);
        InTree -> SetBranchAddress("P_Pz"           , &PpZ);
        InTree -> SetBranchAddress("P_PID"          , &P_PID);    // positive particles momenta
        InTree -> SetBranchAddress("P_cut"          , &P_cut);    // positive particles momenta
        InTree -> SetBranchAddress("N_Px"           , &N_Px);    // negative particles momenta (electron is the first)
        InTree -> SetBranchAddress("N_Py"           , &N_Py);    // negative particles momenta (electron is the first)
        InTree -> SetBranchAddress("N_Pz"           , &N_Pz);    // negative particles momenta (electron is the first)
        InTree -> SetBranchAddress("N_PathSC"       , &N_PathSC);    // negative particles path length (electron is the first)
        InTree -> SetBranchAddress("N_TimeSC"       , &N_TimeSC);    // negative particles time (electron is the first)
        InTree -> SetBranchAddress("STT"            , &STT);
        Printf("set adresses for %s",DataType.Data());
    }
    else if(DataType == "(e,e'npp)") {
        NMom = P1Mom = P2Mom = 0;
        InTree -> SetBranchAddress("NMom"           , &NMom);
        InTree -> SetBranchAddress("P1Mom"          , &P1Mom);
        InTree -> SetBranchAddress("P2Mom"          , &P2Mom);
    }
    
}



//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void TSchemeDATA::protons_from_nuclei(){
    TargetType      = 2;
    XbMin           = 0.0;
    SetSchemeType   ("protons_from_solids");
    LoadInTree      ();
    CreateOutTree   ();
    
    if (DataType == "NoCTofDATA" || DataType == "New_NoCTofDATA") {
        //         targ_type = 2; // for Al27
        
        for (Long64_t i = 0; i < Nentries ; i++) {
            NpGood = 0;
            if (i%(Nentries/20)==0) plot.PrintPercentStr((float)i/Nentries);
            InTree -> GetEntry(i);
            if( (targ_type == TargetType) && (Xb > XbMin) ){
                for (int p = 0 ; p < Np ; p++){
                    if( P_cut[p] == 1 && P_PID[p] == 1 ){    // this is a proton with momentum |p|<2.8 and 'good' CTOF
                        NpGood++;
                    }
                }
                if( 0 < NpGood ){
                    OutTree -> Fill();
                }
            }
        }
    }
    
    WriteOutFile();
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void TSchemeDATA::SRCPmissXb(int fTargetType , float fXbMin, int fNpMin, int fNpMax, TString name){
    TargetType      = fTargetType;
    XbMin           = fXbMin;
    SetSchemeType   ("SRCPmissXb"+name);
    LoadInTree      ();
    CreateOutTree   ();

    if (DataType == "DATA") {
        for (Long64_t i = 0; i < Nentries ; i++) {
            if (i%(Nentries/20)==0) {
                printf("schemed %d events so far, out of ", (int)OutTree -> GetEntries());
                plot.PrintPercentStr((float)i/Nentries);
            }
            InTree -> GetEntry(i);
            if( (fNpMin <= Np &&  Np <= fNpMax) && (targ_type == TargetType) && (Xb > XbMin) ){
                q       = new TVector3( - Px_e , - Py_e , 5.009 - Pz_e );
                Plead   = new TVector3();
                for (int p = 0 ; p < Np ; p++){
                    proton = new TVector3(PpX[p],PpY[p],PpZ[p]);
                    if (proton->Mag() > Plead->Mag()) {   // this is a faster proton
                        Plead = proton;
                    }
                    
                }
                Pmiss = *Plead - *q;
                if( (0.3 < Pmiss.Mag()) && (Pmiss.Mag() < 1.0) ){
                    OutTree -> Fill();
                }
            }
        }
    }
    else if (DataType == "NoCTofDATA" || DataType == "New_NoCTofDATA") {
//         targ_type = 2; // for Al27

        for (Long64_t i = 0; i < Nentries ; i++) {
            if (i%(Nentries/20)==0) plot.PrintPercentStr((float)i/Nentries);
            InTree -> GetEntry(i);
            if( (fNpMin <= Np &&  Np <= fNpMax) && (targ_type == TargetType) && (Xb > XbMin) ){
                q       = new TVector3( - N_Px[0] , - N_Py[0] , 5.009 - N_Pz[0] );
                Plead   = new TVector3();
                for (int p = 0 ; p < Np ; p++){
                   if( P_cut[p] == 1 && P_PID[p] == 1 ){    // this is a proton with momentum |p|<2.8 and 'good' CTOF
                        proton = new TVector3(PpX[p],PpY[p],PpZ[p]);
                        if (proton->Mag() > Plead->Mag()) {   // this is a faster proton
                            Plead = proton;
                        }
                    }
                }
                Pmiss = *Plead - *q;
                if( (0.3 < Pmiss.Mag()) && (Pmiss.Mag() < 1.0) ){
                    OutTree -> Fill();
                }
            }
        }
    }

    WriteOutFile();
}


//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void TSchemeDATA::TwoSlowProtons(int fTargetType , float fpMin, float fpMax){
    
    TargetType      = fTargetType;
    SetSchemeType   ("TwoSlowProtons");
    LoadInTree      ();
    CreateOutTree   ();

    if (DataType == "NoCTofDATA" || DataType == "New_NoCTofDATA") {


        
        for (Long64_t i = 0; i < Nentries ; i++) {
            
            if (i%(Nentries/20)==0) {
                printf("%d events so far, out of ", (int)OutTree -> GetEntries());
                plot.PrintPercentStr((float)i/Nentries);
            }
            NpGood = 0;
            InTree -> GetEntry(i);
            if (DataType == "New_NoCTofDATA") {targ_type = 2; Ntotal=Nn+Np;} // for 27Al or the new 12C Meytal cooked Aug-2016
            
            if(debug > 2) SHOW3(Ntotal , Nn , Np);
            
            // look for events with only one negative particle (electron) and two positive (protons)
            if( ( Np == 2 ) && ( Nn == 1 ) && ( Ntotal == 3 ) && (targ_type == TargetType) ) {

                // make sure these two positive particles are actually protons
                for (int p = 0 ; p < Np ; p++){
                    if( P_cut[p] == 1 && P_PID[p] == 1 ){    // this is a proton with momentum |p|<2.8 and 'good' CTOF
                        proton = new TVector3(PpX[p],PpY[p],PpZ[p]);
                        
                        // and that their momenta are in the desired range
                        if (fpMin < proton->Mag() && proton->Mag() < fpMax) {
                            NpGood++;
                        }
                    }
                }
                if( NpGood == 2 ){
                    OutTree -> Fill();
                }
            }
        }
    }
    
    WriteOutFile();
}



//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void TSchemeDATA::TwoSlowProtons_piminus_p (int fTargetType , float fpMin, float fpMax ){
    
    TargetType      = fTargetType;
    SetSchemeType   ("TwoSlowProtons_piminus_p");
    LoadInTree      ();
    CreateOutTree   ();
    
    if (DataType == "NoCTofDATA" || DataType == "New_NoCTofDATA") {
        
        if (DataType == "New_NoCTofDATA") {
            targ_type = 2; // for 27Al or the new 12C Meytal cooked Aug-2016
        }
        
        
        for (Long64_t i = 0; i < Nentries ; i++) {
            
            if (i%(Nentries/20)==0) {
                printf("schemed %d events so far, out of ", (int)OutTree -> GetEntries());
                plot.PrintPercentStr((float)i/Nentries);
            }
            NpGood = Npiminus = 0;
            InTree -> GetEntry(i);
            
        
            
            // look for events with only one negative particle (electron) and two positive (protons)
            if( ( Np == 3 ) && ( Nn > 1 ) && (targ_type == TargetType) ) {
                
                // ask if we have a π-
                for (int n = 0 ; n < Nn ; n++){
                    
                    negative_particle_momentum = new TVector3(N_Px[n],N_Py[n],N_Pz[n]);
                    Float_t Momentum = negative_particle_momentum->Mag();
                    Float_t time = (N_TimeSC[n] - STT[n]);
                    Float_t Betta = ( N_PathSC[n] / time ) / 30.0 ; // c = 30 cm/ns,  the units for N_PathSC are [cm] and for N_TimeSC are [ns]

                    if (TMath::Abs(Betta-Momentum/sqrt(Momentum*Momentum+0.14*0.14))<0.03){ // this is the CTOF of π- according to meytal p.31
                        Npiminus++;
                    }
                }

                
                // make sure these two positive particles are actually protons
                for (int p = 0 ; p < Np ; p++){
                    if( P_cut[p] == 1 && P_PID[p] == 1 ){    // this is a proton with momentum |p|<2.8 and 'good' CTOF
                        proton = new TVector3(PpX[p],PpY[p],PpZ[p]);
                        
                        // and that their momenta are in the desired range
                        if (fpMin < proton->Mag() && proton->Mag() < fpMax) {
                            NpGood++;
                        }
                    }
                }
                
                if (( NpGood == 2 ) && (Npiminus >= 1) ){
                    OutTree -> Fill();
                }
            }
        }
    }
    
    WriteOutFile();
}


//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void TSchemeDATA::TwoSlowProtons_ppp(int fTargetType , float fpMin, float fpMax){
    TargetType      = fTargetType;
    SetSchemeType   ("TwoSlowProtons_ppp");
    LoadInTree      ();
    CreateOutTree   ();
    int NpSlow , NpFast ;
    
    if (DataType == "NoCTofDATA" || DataType == "New_NoCTofDATA") {
        //         targ_type = 2; // for Al27
        
        for (Long64_t i = 0; i < Nentries ; i++) {
            if (i%(Nentries/20)==0) plot.PrintPercentStr((float)i/Nentries);
            NpFast = 0;
            NpSlow = 0;
            InTree -> GetEntry(i);
            
            // look for events with only one negative particle (electron) and two positive (protons) of intermediate momenta, plus one aditional proton with large momentum > 1. GeV/c
            
            if( ( Np == 3 ) && ( Nn == 1 ) && (targ_type == TargetType) && (Xb > 0.9)){
                for (int p = 0 ; p < Np ; p++){
                    if( P_cut[p] == 1 && P_PID[p] == 1 ){    // this is a proton with momentum |p|<2.8 and 'good' CTOF
                        proton = new TVector3(PpX[p],PpY[p],PpZ[p]);
                        if (1. < proton->Mag() ){
                            NpFast++;
                        }
                        if (fpMin < proton->Mag() && proton->Mag() < fpMax) {
                            NpSlow++;
                        }
                    }
                }
                if( NpFast == 1 && NpSlow == 2 ){
                    OutTree -> Fill();
                }
            }
        }
    }
    
    WriteOutFile();
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void TSchemeDATA::TwoSlowProtons_npp(float fn_pMin , float fpMin, float fpMax){
    SetSchemeType   ("TwoSlowProtons_npp");
    LoadInTree      ();
    CreateOutTree   ();
    
    if (DataType == "(e,e'npp)") {
        for (Long64_t i = 0; i < Nentries ; i++) {
            if (i%(Nentries/20)==0) plot.PrintPercentStr((float)i/Nentries);
            InTree -> GetEntry(i);
            
            // look for events with only one negative particle (electron) and two positive (protons) of intermediate momenta, plus one aditional neutron with large momentum > 1.1 GeV/c
            
            if ( (Xb > 1.05) && (NMom->Mag() > fn_pMin) && (fpMin < P1Mom->Mag() && ( P1Mom->Mag() < fpMax ) && (fpMin < P2Mom->Mag() && ( P2Mom->Mag() < fpMax )) ) ) {
                OutTree -> Fill();
            }
        }
    }
    WriteOutFile();
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void TSchemeDATA::CreateOutTree(){
    OutFile = new TFile(Form("%s/Schemed_%s_%s.root",SchemedPath.Data(),SchemeType.Data(),InFileName.Data()),"recreate");
    OutTree = InTree -> CloneTree(0);
}


//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void TSchemeDATA::WriteOutFile(){
    Printf("\nOutTree has %d entries",(int)OutTree->GetEntries());
    OutTree -> AutoSave();
    OutFile -> Write();
    OutFile -> Close();
    delete InFile;
    delete OutFile;
}



//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void TSchemeDATA::SchemeOnTCut(TString Path, TString fInFileName, TString fInTreeName, TString fOutFileName, TCut cut)
{
    Printf("scheming to ");
    cut.Print();
    Printf("scheming from %s/%s",Path.Data() , fInFileName.Data());
    TFile * TmpInFile = new TFile(Form("%s/%s",Path.Data() , fInFileName.Data()));
    TTree * TmpTree = (TTree*) TmpInFile -> Get(fInTreeName);
//    TmpInFile->Close();
    Printf("scheming to %s/%s",Path.Data(), fOutFileName.Data());
//    TFile * TmpOutFile = new TFile(Form("%s/%s",Path.Data(), fOutFileName.Data()),"recreate");
    Printf("opened output file, writing %lld entries",TmpTree -> GetEntries("(((((((theta_pq < 25)&&(0.62 < p_over_q && p_over_q < 0.96))&&(0.3 < Pmiss.P() && Pmiss.P() < 1.0))&&(1.2 <= Xb))&&(Mmiss < 1.1))&&(2 <= Np))&&(-24.5 < pVertex[0].Z() && pVertex[0].Z() < -20) &&(0.35 < Prec.P())) "));
    // &&(0.35 < Prec.P()  &&  (-24.5 < pVertex[1].Z() && pVertex[1].Z() < -20)))&&(pFiducCut[1] == 1)
//    TTree * TmpOutTree = TmpTree -> CopyTree(cut);
//    Printf("done scheming. (%lld events passed the cut)",TmpOutTree->GetEntries());
//    TmpOutTree -> Write();
//    TmpOutFile -> Close();
//    TmpInFile -> Close();
//    delete TmpOutFile;
//    delete TmpInFile;
}





#endif
