#ifndef TANALYSISEG2_CXX
#define TANALYSISEG2_CXX

#include "TAnalysisEG2.h"




//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
TAnalysisEG2::TAnalysisEG2(TString fInFileName, TCut XbCut):
TPlots("$DataMiningAnaFiles/Ana_" + fInFileName + ".root","anaTree",fInFileName){
    SetPath("$DataMiningAnaFiles");
    SetInFileName( "Ana_" + fInFileName + ".root");
    
    SetSRCCuts(XbCut);
    SetInFile( new TFile( "$DataMiningAnaFiles/" + InFileName ));
    SetTree ((TTree*) InFile->Get( "anaTree" ));
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void TAnalysisEG2::SetSRCCuts(TCut XbCut){ // last editted March-22 for pppSRC cuts

    // important (constant) cuts
    
    cutXb       = XbCut;
    cutPmiss    = "0.3 < Pmiss.P() && Pmiss.P() < 1.0";
    cutThetaPQ  = "theta_pq < 25";
    cutPoverQ   = "0.62 < p_over_q && p_over_q < 0.96";
    cutMmiss    = "Mmiss < 1.1";
    
    cutSRC      = cutXb && cutThetaPQ && cutPoverQ && cutPmiss;
    
    for (int i = 0; i < 3; i++ ) {
                pEdepCut[i] = TEG2dm::pEdepCut(i);
//                pCTOFCut[i] = Form("pID[%d] && pCTOF[%d]",i,i); // CTOF polynomial cut & momentum < 2.8 GeV/c
    }
    ppEdepCut   = Form("%s && %s",pEdepCut[0]->GetName(),pEdepCut[1]->GetName());
    ppCTOFCut   = pCTOFCut[0] && pCTOFCut[1] ;
    pppEdepCut  = Form("%s && %s && %s",pEdepCut[0]->GetName(),pEdepCut[1]->GetName(),pEdepCut[2]->GetName());
    pppCTOFCut  = "pCTOFCut[0] && pCTOFCut[1] && pCTOFCut[2]";

    
    // 2p-SRC following Or Hen' cuts
    cutPlead    = "-24.5 < pVertex[0].Z() && pVertex[0].Z() < -20";
    cutPrec     = "0.35 < Prec.P()  &&  (-24.5 < pVertex[1].Z() && pVertex[1].Z() < -20)";

    ppSRCCut    = cutSRC && cutMmiss && " 2 <= Np" && cutPlead && cutPrec;
    
    
    
    
    // 3p-SRC
    cutP1       = "(-27 < pVertex[1].Z() && pVertex[1].Z() < -20)";
    cutP2       = "0.3 < protons[1].P() && (-27 < pVertex[1].Z() && pVertex[1].Z() < -20)";
    cutP3       = "0.3 < protons[2].P() && (-27 < pVertex[2].Z() && pVertex[2].Z() < -20)";

    cutAngles2p = Form("%s > 150", TPlots::Theta("Pmiss.Vect()","Prec.Vect()").Data());
    cutAngles3p = "thetaMiss23 > 155 && fabs(phiMiss23) < 15";
    
    
    // pID from ∆E (dep.) in TOF scintillators
    pppSRCCut   = cutSRC && " 3 <= Np" && cutP1 && cutP2 && cutP3 && pppEdepCut && pppCTOFCut;
    Final3pCut  = pppSRCCut && cutAngles3p;
    
    
    // For 3p simulation...
    Sim3pSRCCut = cutSRC && " 3 <= Np" && "0.3 < protons[1].P() && 0.3 < protons[2].P()";

    
    Printf("Set Cuts:");
    PrintLine();
    cutXb.Print();
    cutPrec.Print();
    Final3pCut.Print();
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void TAnalysisEG2::PrintInCuts(){
    PrintLine();
    Printf("Number of events in different cuts ( %s ):" , ((TString)cutXb).Data());
    PrintLine();
    Printf( "%d A(e,e'p) events"   , GetEntries(""));
    Printf( "%d A(e,e'p) events in SRC kinematics"   , GetEntries(cutSRC));
    Printf( "%d A(e,e'pp) events in SRC kinematics with recoil proton momemntum > 0.3 GeV/c"
           , GetEntries(cutSRC && " 2 <= Np" && cutP1 && cutP2 && ppEdepCut && ppCTOFCut) );
    Printf( "%d A(e,e'pp) with theta > 155"
           , GetEntries(cutSRC && " 2 <= Np" && cutP1 && cutP2 && ppEdepCut && ppCTOFCut && cutAngles2p) );
    Printf( "%d A(e,e'ppp) events in SRC kinematics with 2 recoil protons momemnta > 0.3 GeV/c"
           , GetEntries( cutSRC && " 3 <= Np" && cutP1 && cutP2 && cutP3 && pppEdepCut && pppCTOFCut) );
    Printf( "%d A(e,e'ppp) with theta > 155 & phi < 15"
           , GetEntries( cutSRC && " 3 <= Np" && cutP1 && cutP2 && cutP3 && pppEdepCut && pppCTOFCut && cutAngles3p) );
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
TMatrix  TAnalysisEG2::RooFitCM(Float_t PmissMin, Float_t PmissMax){
    // returns a parameter matrix: (μ-x,𝜎-x,μ-y,𝜎-y,μ-z,𝜎-z) and their uncertainties (𝚫μ-x,𝚫𝜎-x,𝚫μ-y,𝚫𝜎-y,𝚫μ-z,𝚫𝜎-z)
    TMatrix     res(6,2);
    Double_t    PcmPars[2] = { 0 , 0.14 } ,   PcmParsErr[2] = { 0 , 0 };
    
    TCut cut = Form("%f < Pmiss.P() && Pmiss.P() < %f" , PmissMin , PmissMax);
    RooFit1D( Tree , "pcmX", cut , PcmPars , PcmParsErr , false );
    res(0,0)   = PcmPars[0];
    res(1,0)   = PcmPars[1];
    res(0,1)   = PcmParsErr[0];
    res(1,1)   = PcmParsErr[1];
    
    RooFit1D( Tree , "pcmY", cut , PcmPars , PcmParsErr , false );
    res(2,0)   = PcmPars[0];
    res(3,0)   = PcmPars[1];
    res(2,1)   = PcmParsErr[0];
    res(3,1)   = PcmParsErr[1];
    
    RooFit1D( Tree , "pcmZ", cut , PcmPars , PcmParsErr , false );
    res(4,0)   = PcmPars[0];
    res(5,0)   = PcmPars[1];
    res(4,1)   = PcmParsErr[0];
    res(5,1)   = PcmParsErr[1];
    
    
    return res;
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
vector<Float_t> TAnalysisEG2::GetPcmEntry(int entry){
    // return a vector including the c.m. momentum (3-vector) and the missing momentum magnitude
    TLorentzVector * Pcm = 0 , *Pmiss = 0;
    Tree -> SetBranchAddress("Pcm"      , &Pcm);
    Tree -> SetBranchAddress("Pmiss"    , &Pmiss);
    Tree -> GetEntry(entry);
    vector<Float_t> res;
    res.push_back(Pcm->Px());
    res.push_back(Pcm->Py());
    res.push_back(Pcm->Pz());
    res.push_back(Pmiss->P());
    return res;
}

#endif






















