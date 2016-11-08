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
TString TEG2dm::Target(int A){
    float mAdummy , CoulombDeltaEdummy ;
    return TargetAsString( A, &mAdummy , &CoulombDeltaEdummy );
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
void TEG2dm::RotVec_from_q_Pm_Frame( TVector3 * V, float q_phi, float q_theta, float Pmiss_phi){
    // move to q-Pmiss system: q is the z axis, Pmiss is in x-z plane
    V -> RotateZ(Pmiss_phi);
    V -> RotateY(q_theta);
    V -> RotateZ(q_phi);
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



//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
TCutG * TEG2dm::pEdepCut(int p){
    TCutG *cutg = new TCutG(Form("pEdepCut%d",p),30);
    cutg->SetVarX(Form("protons[%d].P()",p));
    cutg->SetVarY(Form("pEdep[%d]",p));
    cutg->SetPoint(0,0.239224,18.4722);
    cutg->SetPoint(1,0.256857,27.4167);
    cutg->SetPoint(2,0.280368,35.9722);
    cutg->SetPoint(3,0.30094,42.8426);
    cutg->SetPoint(4,0.347962,53.213);
    cutg->SetPoint(5,0.368534,59.4352);
    cutg->SetPoint(6,0.392045,65.1389);
    cutg->SetPoint(7,0.474334,61.8981);
    cutg->SetPoint(8,0.489028,52.1759);
    cutg->SetPoint(9,0.533111,43.75);
    cutg->SetPoint(10,0.603644,34.1574);
    cutg->SetPoint(11,0.79761,22.8796);
    cutg->SetPoint(12,1.05623,18.7315);
    cutg->SetPoint(13,1.39714,16.787);
    cutg->SetPoint(14,1.50294,14.3241);
    cutg->SetPoint(15,1.78801,12.5093);
    cutg->SetPoint(16,1.54114,10.4352);
    cutg->SetPoint(16,1.54114,10.4352);
    cutg->SetPoint(17,1.15027,11.7315);
    cutg->SetPoint(18,1.01215,13.5463);
    cutg->SetPoint(19,0.876959,14.0648);
    cutg->SetPoint(20,0.765282,16.1389);
    cutg->SetPoint(21,0.677116,17.8241);
    cutg->SetPoint(22,0.556622,22.8796);
    cutg->SetPoint(23,0.456701,29.6204);
    cutg->SetPoint(24,0.427312,33.7685);
    cutg->SetPoint(25,0.389107,32.8611);
    cutg->SetPoint(26,0.374412,20.287);
    cutg->SetPoint(27,0.32739,16.787);
    cutg->SetPoint(28,0.315635,14.713);
    cutg->SetPoint(29,0.236285,18.7315);
    cutg->SetPoint(30,0.239224,18.4722);
    return cutg;
}





//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
TCutG * TEG2dm::alpha12_vs_XbCut(){
    TCutG *cutg = new TCutG("alpha12_vs_XbCut",4);
    cutg->SetVarX("Xb");
    cutg->SetVarY("alpha[0]+alpha[1]");
    cutg->SetPoint(0,0.8,1.75);
    cutg->SetPoint(1,1.2,1.75);
    cutg->SetPoint(2,1.9,1.0);
    cutg->SetPoint(3,0.8,1.0);
    cutg->SetPoint(4,0.8,1.75);
    return cutg;
}





//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
Int_t TEG2dm::protonFiducial( TVector3 pMomentum , int debug ){
    
    // return 1 if proton inside fiducial region, and 0 if it is outside fiducial region
    //--------------------------------------------------------------------
    // Fiducial cuts from Zana' thesis (p. 67, 4.4)
    //--------------------------------------------------------------------
    Double_t mag    = pMomentum.Mag();
    Double_t theta  = r2d * pMomentum.Theta();
    Double_t phi    = r2d * pMomentum.Phi();
    phi = ChangePhiToPhiLab( phi );
    
    // Check if within fiducials
//    int sector = (int)(phi/60);
    int sector = (int)((phi+30)/60);
    if (sector<0 || sector>5)
    return 0;
    
    // delete (obselete)
    //    Double_t theta_min = P0_theta[sector] + P1_theta[sector]/(pow(mag,2)) + P2_theta[sector]*mag + P3_theta[sector]/mag + P4_theta[sector]*exp(P5_theta[sector]*mag);
    P0 = P0_theta[sector];
    P1 = P1_theta[sector];
    P2 = P2_theta[sector];
    P3 = P3_theta[sector];
    P4 = P4_theta[sector];
    P5 = P5_theta[sector];
    mom = mag;
    
    Double_t theta_min = P0 + P1/pow(mom,2) + P2*mom + P3/mom + P4 * exp( P5 * mom );
    Double_t theta_max = 120;
    
    if(theta_min < theta && theta < theta_max){
        Double_t Delta_phi[2];
        for(int k=0; k<2; k++){
            
            // delete (obselete)
            //            Double_t a = P0_a[sector][k] + P1_a[sector][k]*exp(P2_a[sector][k]*(mag-P3_a[sector][k])   )    ;
            //            Double_t b = P0_b[sector][k] + P1_b[sector][k]*exp( pow( P2_b[sector][k]*(mag-P3_b[sector][k]) , 2 ) )*mag;
            //            Double_t b = P0_b[sector][k] + P1_b[sector][k]*exp( pow( P2_b[sector][k]*(mag-P3_b[sector][k]) , 2 ) )*mag;
            //            Delta_phi[k] = a*(1 - 1./((theta - theta_min)/b+1) );

            
            P0 = P0_a[sector][k];
            P1 = P1_a[sector][k];
            P2 = P2_a[sector][k];
            P3 = P3_a[sector][k];
            mom = mag;
            a = P0 + P1 * exp( P2 *( mom - P3 ) ) ;

 
            P0 = P0_b[sector][k];
            P1 = P1_b[sector][k];
            P2 = P2_b[sector][k];
            P3 = P3_b[sector][k];
            mom = mag;
            b = P0 + P1 * mom * exp( P2 * pow( mom - P3 , 2 ) ) ;

            
            Delta_phi[k] = a * (1 - 1./( ((theta - theta_min)/b) + 1 ) );
        }
        if(  sector*60-Delta_phi[0] < phi && phi < sector*60+Delta_phi[1]){
            if (debug > 3) cout << "in fiducial region!" << endl;
            return 1;
        }
    }
    if (debug > 3) cout << "not in fiducial region...." << endl;
    return 0;
}

#endif









