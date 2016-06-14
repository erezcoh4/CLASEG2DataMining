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
    int NpGood ;
    
    if (DataType == "no ctof") {
        //         targ_type = 2; // for Al27
        
        for (Long64_t i = 0; i < Nentries ; i++) {
            if (i%(Nentries/20)==0) plot.PrintPercentStr((float)i/Nentries);
            NpGood = 0;
            InTree -> GetEntry(i);
            if( ( Np > 2 ) && (targ_type == TargetType) ){
                for (int p = 0 ; p < Np ; p++){
                    if( P_cut[p] == 1 && P_PID[p] == 1 ){    // this is a proton with momentum |p|<2.8 and 'good' CTOF
                        proton = new TVector3(PpX[p],PpY[p],PpZ[p]);
                        if (fpMin < proton->Mag() && proton->Mag() < fpMax) {
                            NpGood++;
                        }
                    }
                }
                if( NpGood > 2 ){
                    OutTree -> Fill();
                }
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
