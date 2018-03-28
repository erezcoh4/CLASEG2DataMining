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
    InTree -> SetBranchAddress("Xb"             , &Xb);
    
    if (DataType == "DATA") {
        InTree -> SetBranchAddress("T_nmb"          , &Ntotal);
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
        // InTree -> SetBranchAddress("STT"            , &STT);
        InTree -> SetBranchAddress("targ_type"      , &targ_type); // for Al27 remove this
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
void TSchemeDATA::SRCPmissXb(int fTargetType , float fXbMin, int fNpMin, int fNpMax, TString name, Int_t A){
    TargetType      = fTargetType;
    XbMin           = fXbMin;
    SetSchemeType   ("SRCPmissXb"+name);
    LoadInTree      ();
    CreateOutTree   ();
    Beam = TLorentzVector( 0 , 0 , 5.014 , 5.014 );
    TargetAsString( A      , &mA   , &CoulombDeltaE);
    
    if (DataType == "DATA") {
        for (Long64_t i = 0; i < Nentries ; i++) {
            if (i%(Nentries/20)==0) {
                printf("schemed %d events so far, out of ", (int)OutTree -> GetEntries());
                plot.PrintPercentStr((float)i/Nentries);
            }
            InTree -> GetEntry(i);
            
            
            // electron
            Pe = TVector3( Px_e , Py_e , Pz_e );
            Pe = CoulombCorrection( Pe , CoulombDeltaE , Me , 1 ); // for the electron, the correction is E'+dE
            if( (fNpMin <= Np &&  Np <= fNpMax) && (targ_type == TargetType) && (Xb > XbMin) ){
                e.SetVectM( Pe , Me );
                q = Beam - e;
                Plead = TLorentzVector();
                
                
                // protons
                for (int p = 0 ; p < Np ; p++){
                    TVector3 p_3_momentum( PpX[p], PpY[p], PpZ[p] );
                    p_3_momentum = CoulombCorrection( p_3_momentum , CoulombDeltaE , Mp , -1 ); // for the protons, the correction is Ep-dE
                    // Energy loss correction should be done only for recoil protons
                    // and thus we will do it later - when identifying which are the recoil protons
                    //                    // apply energy loss correction for protons below 1 GeV/c
                    //                    if (p_3_momentum.Mag() < 1.){
                    //                        p_3_momentum = EnergyLossCorrrection( p_3_momentum );
                    //                    }
                    // no energy-loss correction for the leading proton
                    if (p_3_momentum.Mag() > Plead.P()) {   // this is a faster proton
                        Plead.SetVectM( p_3_momentum , Mp ) ;
                    }
                }
                Pmiss = Plead - q;
                if( (0.3 < Pmiss.P()) && (Pmiss.P() < 1.0) && (Plead.P()<2.4) ){
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
            
            
            // electron
            Pe = TVector3( N_Px[0] , N_Py[0] , N_Pz[0] );
            Pe = CoulombCorrection( Pe , CoulombDeltaE , Me , 1 ); // for the electron, the correction is E'+dE
            if( (fNpMin <= Np &&  Np <= fNpMax) && (targ_type == TargetType) && (Xb > XbMin) ){
                e.SetVectM( Pe , Me );
                q = Beam - e;
                // protons
                for (int p = 0 ; p < Np ; p++){
                    TVector3 p_3_momentum( PpX[i], PpY[i], PpZ[i] );
                    p_3_momentum = CoulombCorrection( p_3_momentum , CoulombDeltaE , Mp , -1 ); // for the protons, the correction is Ep-dE
                    p_3_momentum = EnergyLossCorrrection( p_3_momentum );
                    if (p_3_momentum.Mag() > Plead.P()) {   // this is a faster proton
                        Plead.SetVectM( p_3_momentum , Mp ) ;
                    }
                }
                if( (0.3 < Pmiss.P()) && (Pmiss.P() < 1.0) ){
                    OutTree -> Fill();
                }
            }
            
            
            //            if( (fNpMin <= Np &&  Np <= fNpMax) && (targ_type == TargetType) && (Xb > XbMin) ){
            //                q       = new TVector3( - N_Px[0] , - N_Py[0] , 5.009 - N_Pz[0] );
            //                Plead   = new TVector3();
            //                for (int p = 0 ; p < Np ; p++){
            //                   if( P_cut[p] == 1 && P_PID[p] == 1 ){    // this is a proton with momentum |p|<2.8 and 'good' CTOF
            //                        proton = new TVector3(PpX[p],PpY[p],PpZ[p]);
            //                        if (proton->Mag() > Plead->Mag()) {   // this is a faster proton
            //                            Plead = proton;
            //                        }
            //                    }
            //                }
            //                Pmiss = *Plead - *q;
            //                if( (0.3 < Pmiss.Mag()) && (Pmiss.Mag() < 1.0) ){
            //                    OutTree -> Fill();
            //                }
            //            }
        }
    }
    
    WriteOutFile();
}


//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void TSchemeDATA::SRCXb(int fTargetType , float fXbMin, int fNpMin, int fNpMax, TString name, Int_t A){
    TargetType      = fTargetType;
    XbMin           = fXbMin;
    SetSchemeType   ("SRCXb"+name);
    LoadInTree      ();
    CreateOutTree   ();
    Beam = TLorentzVector( 0 , 0 , 5.014 , 5.014 );

    if (DataType == "DATA" || DataType == "NoCTofDATA" || DataType == "New_NoCTofDATA") {
        for (Long64_t i = 0; i < Nentries ; i++) {
            if (i%(Nentries/20)==0) {
                printf("schemed %d events so far, out of ", (int)OutTree -> GetEntries());
                plot.PrintPercentStr((float)i/Nentries);
            }
            InTree -> GetEntry(i);
            // SHOW3(Np,targ_type,Xb);
            // if (DataType == "NoCTofDATA" || DataType == "New_NoCTofDATA") targ_type = TargetType;
            if( (fNpMin <= Np &&  Np <= fNpMax) && (targ_type == TargetType) && (Xb > XbMin) ){
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
    cout << "wrote output file: " << Form("%s/Schemed_%s_%s.root",SchemedPath.Data(),SchemeType.Data(),InFileName.Data()) << endl;
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
    Printf("scheming to %s/%s",Path.Data(), fOutFileName.Data());
    TFile * TmpOutFile = new TFile(Form("%s/%s",Path.Data(), fOutFileName.Data()),"recreate");
    //    Printf("opened output file, writing %lld entries",TmpTree -> GetEntries("(theta_pq < 25) && (0.62 < p_over_q && p_over_q < 0.96 ) && (0.3 < Pmiss.P() && Pmiss.P() < 1.0) &&(1.2 <= Xb) &&(Mmiss < 1.1) &&(2 <= Np)&&(-24.5 < pVertex[0].Z())")); // &&(-24.5 < pVertex[0].Z() && pVertex[0].Z() < -20)
    // &&(0.35 < Prec.P()  &&  (-24.5 < pVertex[1].Z() && pVertex[1].Z() < -20)))&&(pFiducCut[1] == 1)
    TTree * TmpOutTree = TmpTree -> CopyTree(cut);
    Printf("done scheming. (%lld events passed the cut)",TmpOutTree->GetEntries());
    TmpOutTree -> Write();
    TmpOutFile -> Close();
    TmpInFile -> Close();
    delete TmpOutFile;
    delete TmpInFile;
}





#endif
