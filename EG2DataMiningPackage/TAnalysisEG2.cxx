#ifndef TANALYSISEG2_CXX
#define TANALYSISEG2_CXX

#include "TAnalysisEG2.h"




//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
TAnalysisEG2::TAnalysisEG2(TString fInFileName):
TPlots("$DataMiningAnaFiles/Ana_" + fInFileName + ".root","anaTree",fInFileName,true){
    SetPath("$DataMiningAnaFiles");
    SetInFileName( "Ana_" + fInFileName + ".root");
    
    SetSRCCuts();
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
void TAnalysisEG2::DrawVarAnd2pSRCCut(TCanvas * c, int i , TString var
                                      , int NbinsX , float Xmin , float Xmax
                                      , TString Title , TString XTitle){
    c -> cd(i);
    H1(var,"","",NbinsX,Xmin,Xmax,Title,XTitle,"",1,0);
    H1(var,ppSRCCut,"same",NbinsX,Xmin,Xmax,Title,XTitle,"",1,46);
}




//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void TAnalysisEG2::Draw2DVarAnd2pSRCCut(TCanvas * c  , int i , TString varX , TString varY,
                                        int NbinsX , float Xmin , float Xmax,
                                        int NbinsY , float Ymin , float Ymax,
                                        TString Title , TString XTitle , TString YTitle ){
    c -> cd(i);
    H2(varX, varY,"","",NbinsX,Xmin,Xmax,NbinsY,Ymin,Ymax,Title,XTitle,YTitle);
    H2(varX, varY,ppSRCCut,"colz same",NbinsX,Xmin,Xmax,NbinsY,Ymin,Ymax,Title,XTitle,YTitle);
}

#endif
