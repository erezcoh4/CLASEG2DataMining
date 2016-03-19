#ifndef TEG2DM_CXX
#define TEG2DM_CXX

#include "TEG2dm.h"



//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
TVector3 TEG2dm::EnergyLossCorrrection(TVector3 p){ // following Or Hen Analysis
    Double_t Pmeasured = p.Mag();
    Double_t CorrFactor= sqrt( pow((0.00135272 + 0.000845728/(pow((0.0746518+Pmeasured),2))+sqrt(pow(p.Mag(),2)+pow(Mp,2))),2)-pow(Mp,2))/p.Mag();
    p = CorrFactor*p;
    return p;
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
TVector3 TEG2dm::CoulombCorrection(TVector3 p , Float_t CoulombDeltaE){
    // following Or Hen Analysis : p' = p x √(√((m^2+p^2)^2+∆E^2) - m^2)
    p = (sqrt(pow(sqrt(pow(Mp,2)+pow(p.Mag(),2))+CoulombDeltaE,2) - pow(Mp,2))/p.Mag())*p;
    return p;
}


//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
TString TEG2dm::TargetAsString(int A, float *mA , float *CoulombDeltaE){
    switch (A) {
        case 12:// carbon (C12)
            *mA              = 12.0107*0.931494;
            *CoulombDeltaE   = 0.0029;
            return "C12";
            break;
        case 27:// Aluminium (Al27)
            *mA              = 26.982*0.931494;
            *CoulombDeltaE   = 0.0056;
            return "Al27";
            break;
        case 56:// iron (Fe56)
            *mA              = 55.9349375*0.93149;
            *CoulombDeltaE   = 0.0094;
            return "Fe56";
            break;
        case 208:// lead (Pb208)
            *mA              = 207.2*0.93149;
            *CoulombDeltaE   = 0.0203;
            return "Pb208";
            break;
        default:
            return "No Target Found";
            break;
    }
}



//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void TEG2dm::RotVec2_q_Pm_Frame( TVector3 * V, float q_phi, float q_theta, float Pmiss_phi){
    // move to q-Pmiss system: q is the z axis, Pmiss is in x-z plane
    V -> RotateZ(-q_phi);
    V -> RotateY(-q_theta);
    V -> RotateZ(-Pmiss_phi);
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void TEG2dm::RotVec2_Pm_q_Frame( TVector3 * V, float Pmiss_phi, float Pmiss_theta, float q_phi){
    // move to Pmiss-q system: Pmiss is the z axis, q is in x-z plane
    V -> RotateZ(-Pmiss_phi);
    V -> RotateY(-Pmiss_theta);
    V -> RotateZ(-q_phi);
}



//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
Float_t TEG2dm::LCfraction(TLorentzVector v, Float_t A_over_mA ){
    return A_over_mA * ( v.E() - v.Pz() );
}




#endif









