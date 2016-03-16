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
    InTree -> SetBranchAddress("targ_type"      , &targ_type);
    
    if (DataType == "data") {
        InTree -> SetBranchAddress("Px"             , &PpX);
        InTree -> SetBranchAddress("Py"             , &PpY);
        InTree -> SetBranchAddress("Pz"             , &PpZ);
        InTree -> SetBranchAddress("Px_e"           , &Px_e);
        InTree -> SetBranchAddress("Py_e"           , &Py_e);
        InTree -> SetBranchAddress("Pz_e"           , &Pz_e);
    }
    
}



//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void TSchemeDATA::CreateOutTree(){
    OutFile = new TFile(Form("%s/Schemed_EG2_DATA/Schemed_%s_%s.root"
                             ,Path.Data(),SchemeType.Data(),InFileName.Data()),"recreate");
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
void TSchemeDATA::SchemeOnTCut(TCut cut)
{
    for (Long64_t i = 0; i < Nentries ; i++) {
        if (InTree -> Draw("Xb",cut,"goff",i,1)) {
            if (i%1000==0) plot.PrintPercentStr((float)i/Nentries);
            InTree -> GetEntry(i);
        }
    }
}

    


//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void TSchemeDATA::SRCPmissXb(int fTargetType , float fXbMin, int fNpMin, int fNpMax){
    TargetType      = fTargetType;
    XbMin           = fXbMin;
    SetSchemeType   ("SRCPmissXb");
    LoadInTree      ();
    CreateOutTree   ();

    for (Long64_t i = 0; i < Nentries ; i++) {
        if (i%(Nentries/20)==0) plot.PrintPercentStr((float)i/Nentries);
        InTree -> GetEntry(i);
        if( (fNpMin <= Np &&  Np <= fNpMax) && (targ_type == TargetType) && (Xb > XbMin) ){
            q       = new TVector3( - Px_e , - Py_e , 5.009 - Pz_e );
            Plead   = new TVector3();
            for (int p = 0 ; p < Np ; p++){
                proton = new TVector3(PpX[p],PpY[p],PpZ[p]);
                if (proton->Mag() > Plead->Mag())    // this is a faster proton
                    Plead = proton;
                
            }
            Pmiss = *Plead - *q;
            if( (0.3 < Pmiss.Mag()) && (Pmiss.Mag() < 1.0) )
                OutTree -> Fill();
        }
    }
    
    WriteOutFile();
}


#endif
