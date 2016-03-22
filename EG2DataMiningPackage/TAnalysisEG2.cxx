#ifndef TANALYSISEG2_CXX
#define TANALYSISEG2_CXX

#include "TAnalysisEG2.h"




//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
TAnalysisEG2::TAnalysisEG2(TString fInFileName):
TPlots("$DataMiningAnaFiles/Ana_" + fInFileName + ".root","anaTree",fInFileName,true){
    SetPath("$DataMiningAnaFiles");
    SetInFileName( "Ana_" + fInFileName + ".root");
    
    SetSRCCuts();
    SetInFile( new TFile( "$DataMiningAnaFiles/" + InFileName ));
    SetTree ((TTree*) InFile->Get( "anaTree" ));
}



//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void TAnalysisEG2::SetSRCCuts(){
    // important (constant) cuts
    
    cutXb       = "1.2 <= Xb";
    cutPmiss    = "0.3 < Pmiss.P() && Pmiss.P() < 1.0";
    cutThetaPQ  = "theta_pq < 25";
    cutPoverQ   = "0.62 < p_over_q && p_over_q < 0.96";
    cutMmiss    = "Mmiss < 1.1";
    
    cutPlead    = cutThetaPQ && cutPoverQ && cutPmiss && "-24.5 < pVertex[0].Z() && pVertex[0].Z() < -20";
    cutPrec     = "0.35 < Prec.P()  &&  (-24.5 < pVertex[1].Z() && pVertex[1].Z() < -20)";
    cutSRC      = cutXb && cutPlead;
    
    ppSRCCut    = cutSRC && cutMmiss && " 2 <= Np" && cutPrec;
   
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


#endif
