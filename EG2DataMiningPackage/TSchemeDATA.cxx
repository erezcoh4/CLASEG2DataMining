#ifndef TSCHEMEDATA_CXX
#define TSCHEMEDATA_CXX

#include "TSchemeDATA.h"




//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
TSchemeDATA::TSchemeDATA(TString fDataType, TString fPath,
                         TString fInFileName  , TString fInTreeName ) {
    SetDataType     (fDataType);
    SetPath         (fPath);
    SetInFileName   (fInFileName);
    SetOutFileName  ("Schemed"+fInFileName);
    SetInTreeName   (fInTreeName);
    SetOutTreeName  (fInTreeName);
}



//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void TSchemeDATA::LoadInTree(){
    InFile      = new TFile(Form("%s/EG2_DATA/%s.root",Path.Data(),InFileName.Data()));
    InTree      = (TTree*)InFile -> Get(InTreeName);
    Nentries    = InTree -> GetEntries();
    SHOW(Nentries);
    
    InTree -> SetBranchAddress("P_nmb"          , &Np);
    InTree -> SetBranchAddress("N_nmb"          , &Nn);
    InTree -> SetBranchAddress("T_nmb"          , &Ntotal);
    InTree -> SetBranchAddress("Xb"             , &Xb);
    InTree -> SetBranchAddress("targ_type"      , &targ_type); // for Al27 remove this
    
    if (DataType == "data") {
        InTree -> SetBranchAddress("Px"             , &PpX);
        InTree -> SetBranchAddress("Py"             , &PpY);
        InTree -> SetBranchAddress("Pz"             , &PpZ);
        InTree -> SetBranchAddress("Px_e"           , &Px_e);
        InTree -> SetBranchAddress("Py_e"           , &Py_e);
        InTree -> SetBranchAddress("Pz_e"           , &Pz_e);
    }
    else if(DataType == "no ctof") {
        InTree -> SetBranchAddress("P_Px"           , &PpX);    // protons momenta
        InTree -> SetBranchAddress("P_Py"           , &PpY);
        InTree -> SetBranchAddress("P_Pz"           , &PpZ);
        InTree -> SetBranchAddress("P_PID"          , &P_PID);    // positive particles momenta
        InTree -> SetBranchAddress("P_cut"          , &P_cut);    // positive particles momenta
        InTree -> SetBranchAddress("N_Px"           , &N_Px);    // negative particles momenta (electron is the first)
        InTree -> SetBranchAddress("N_Py"           , &N_Py);    // negative particles momenta (electron is the first)
        InTree -> SetBranchAddress("N_Pz"           , &N_Pz);    // negative particles momenta (electron is the first)
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
    
    if (DataType == "no ctof") {
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

    if (DataType == "data") {
        for (Long64_t i = 0; i < Nentries ; i++) {
            if (i%(Nentries/20)==0) plot.PrintPercentStr((float)i/Nentries);
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
    else if (DataType == "no ctof") {
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
    
    if (DataType == "no ctof") {

        targ_type = 2; // for 27Al or the new 12C Meytal cooked Aug-2016
        
        for (Long64_t i = 0; i < Nentries ; i++) {
            
            if (i%(Nentries/20)==0) plot.PrintPercentStr((float)i/Nentries);
            NpGood = 0;
            InTree -> GetEntry(i);
            
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
void TSchemeDATA::TwoSlowProtons_ppp(int fTargetType , float fpMin, float fpMax){
    TargetType      = fTargetType;
    SetSchemeType   ("TwoSlowProtons_ppp");
    LoadInTree      ();
    CreateOutTree   ();
    int NpSlow , NpFast ;
    
    if (DataType == "no ctof") {
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
    OutFile = new TFile(Form("%s/Schemed_EG2_DATA/Schemed_%s_%s.root",Path.Data(),SchemeType.Data(),InFileName.Data()),"recreate");
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
    TFile * TmpInFile = new TFile(Form("%s/%s",Path.Data() , fInFileName.Data()));
    TTree * TmpTree = (TTree*) TmpInFile -> Get(fInTreeName);
    TFile * TmpOutFile = new TFile(Form("%s/%s",Path.Data(), fOutFileName.Data()),"recreate");
    TTree * TmpOutTree = TmpTree -> CopyTree(cut);
    Printf("schemed from %s to %s (%lld events passed the cut)",TmpInFile->GetName(),TmpOutFile->GetName(),TmpOutTree->GetEntries());
    TmpOutTree -> Write();
    TmpOutFile -> Close();
}





#endif
