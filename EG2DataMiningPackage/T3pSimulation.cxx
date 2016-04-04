#ifndef T3PSIMULATION_CXX
#define T3PSIMULATION_CXX

#include "T3pSimulation.h"


//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
T3pSimulation::T3pSimulation( TTree * fOutTree ){
    SetOutTree(fOutTree);
    InitOutTree();
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void T3pSimulation::InitOutTree(){
    
    OutTree -> Branch("q"           ,"TLorentzVector"       ,&q);
    OutTree -> Branch("struck_p"    ,"TLorentzVector"       ,&struck_p);
    // knocked by q, before rescattering
    OutTree -> Branch("p_knocked"   ,"TLorentzVector"       ,&p_knocked);
    // pp-SRC pair
    OutTree -> Branch("pcm_ppPair"  ,"TLorentzVector"       ,&pcm_ppPair);
    OutTree -> Branch("p1_ppPair"   ,"TLorentzVector"       ,&p1_ppPair);
    OutTree -> Branch("p2_ppPair"   ,"TLorentzVector"       ,&p2_ppPair);
    // after rescattering
    OutTree -> Branch("p_knocked_r" ,"TLorentzVector"       ,&p_knocked_r); // rescattered
    OutTree -> Branch("p1_ppPair_r" ,"TLorentzVector"       ,&p1_ppPair_r); // rescattered
    OutTree -> Branch("p2_ppPair_r" ,"TLorentzVector"       ,&p2_ppPair_r); // rescattered

    OutTree -> Branch("Pmiss"       ,"TLorentzVector"       ,&Pmiss);
    OutTree -> Branch("Pcm"         ,"TLorentzVector"       ,&Pcm);
    OutTree -> Branch("Plead"       ,"TLorentzVector"       ,&Plead);
    OutTree -> Branch("Prec"        ,"TLorentzVector"       ,&Prec);
    OutTree -> Branch("protons"     ,&protons);             // std::vector<TLorentzVector>
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void T3pSimulation::RunInteractions ( int Ninteractions , bool DoPrint ){
    for ( int i = 0 ; i < Ninteractions ; i++ ) {
        //        if (i%(Ninteractions/20)==0) plot.PrintPercentStr((float)i/Ninteractions);
        Gen_q();
        Gen_struck_p();
        q_struck_p();
        Gen_ppPair();
        p_rescatter_ppPair();
        if(DoPrint) PrintDATA(i);
        OutTree -> Fill();
    }
}


//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void T3pSimulation::Gen_q(){
    // take the proton from inclusive 12C(e,e') data
    Double_t q3Mag, omega;
    h_q -> GetRandom2 (q3Mag, omega);
    q.SetPxPyPzE( 0 , 0 , q3Mag , omega );
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void T3pSimulation::Gen_struck_p(){
    // a proton going backwards with FG momentum
    Pp = rand.Uniform(0,0.25);
    rand.Sphere(Px,Py,Pz,Pp);
    struck_p.SetVectM( TVector3(Px , Py , -fabs(Pz)) , Mp );
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void T3pSimulation::q_struck_p(){
    p_knocked.SetVectM ( (struck_p + q).Vect() , Mp );
}


//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void T3pSimulation::Gen_ppPair(){

    // generate the first proton from an SRC k^-4 tail
    // the c.m. as a 3D gaussian of 140 MeV/c width
    // and the corresponding second proton as a partner
    
    Pp = SRCk4Tail -> GetRandom() / 1000.;
    rand.Sphere(Px,Py,Pz,Pp);
    p1_ppPair.SetVectM( TVector3(Px , Py , Pz) , Mp );
    Pcm = TLorentzVector( rand.Gaus(0,0.14) , rand.Gaus(0,0.14) , rand.Gaus(0,0.14) , 2*Mp );
    p2_ppPair.SetVectM( (Pcm - p1_ppPair).Vect()  , Mp );

}


//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void T3pSimulation::p_rescatter_ppPair(){
    // move to c.m. frame of p_knocked and p1_ppPair
    // calculate the scattering and the decide on the c.m. angle by weight of the scattering Xsec
    // and return to lab frame to show the final state two protons
    
    // boost to c.m. frame of p_knocked and p1_ppPair
    p1_pk_cm    = p1_ppPair + p_knocked;
    p1_p1_pk_cm = p1_ppPair;
    p1_p1_pk_cm.Boost( -p1_pk_cm.BoostVector() );
    pk_p1_pk_cm = p_knocked;
    pk_p1_pk_cm.Boost( -p1_pk_cm.BoostVector() );
 
    // generate a scattering angle according to cross-section dependence on energy and angle
    
    
    
    // Rotate the vectors in the c.m. to go along the z-axis
    Double_t rot_phi     = p1_p1_pk_cm.Phi();
    Double_t rot_theta   = p1_p1_pk_cm.Theta();
    
    p1_p1_pk_cm.RotateZ(-rot_phi);
    p1_p1_pk_cm.RotateY(-rot_theta);
    pk_p1_pk_cm.RotateZ(-rot_phi);
    pk_p1_pk_cm.RotateY(-rot_theta);

    PrintLine();
    SHOWTLorentzVector(p1_pk_cm);
    SHOWTLorentzVector(p1_p1_pk_cm);
    SHOWTLorentzVector(pk_p1_pk_cm);

    
    
    
    // Define the angles of the scattering in the c.m.
    binEcm      = h_ppElastic -> GetXaxis() -> FindBin( p1_pk_cm.E() );
    Theta_cm    = r2d * ((TH1F*) h_ppElastic->ProjectionY("hTheta",binEcm,binEcm)) -> GetRandom();
    Phi_cm      = r2d * gRandom -> Uniform(0 , 180);  // phi distributes uniformly
    
    
    // Calculate outgoing protons in the 90 degrees scattering reaction
    p1_ppPair_r.SetVectM( p1_p1_pk_cm.Pz()* TVector3 ( sin(Theta_cm)*cos(Phi_cm),  sin(Theta_cm)*sin(Phi_cm) , cos(Theta_cm) ) , Mp);
    p_knocked_r.SetVectM( - p1_ppPair_r.Vect() , Mp);
    
    SHOWTLorentzVector(p1_ppPair_r);
    SHOWTLorentzVector(p_knocked_r);
    
    
    // Rotate all back from the z axis in the c.m. frame.
    p1_p1_pk_cm.RotateY(rot_theta);
    p1_p1_pk_cm.RotateZ(rot_phi);
    pk_p1_pk_cm.RotateY(rot_theta);
    pk_p1_pk_cm.RotateZ(rot_phi);
    p1_ppPair_r.RotateY(rot_theta);
    p1_ppPair_r.RotateZ(rot_phi);
    p_knocked_r.RotateY(rot_theta);
    p_knocked_r.RotateZ(rot_phi);
    
    SHOWTLorentzVector(p1_ppPair_r);
    SHOWTLorentzVector(p_knocked_r);
    
    
    
    // boost back to lab frame
    p1_ppPair_r.Boost( p1_pk_cm.BoostVector() );
    p_knocked_r.Boost( p1_pk_cm.BoostVector() );
    
    SHOWTLorentzVector(p1_ppPair_r);
    SHOWTLorentzVector(p_knocked_r);
    
   
    
    
    // the third protn (p2_ppPair) is a spectator and does not change
    p2_ppPair_r = p2_ppPair;
    
}


//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void T3pSimulation::PrintDATA(int entry){
    SHOW(entry);
    SHOWTLorentzVector(q);
    SHOWTLorentzVector(struck_p);
    SHOWTLorentzVector(p_knocked);
    SHOWTLorentzVector(p1_ppPair);
    SHOWTLorentzVector(p2_ppPair);
    SHOWTLorentzVector(p1_ppPair_r);
    SHOWTLorentzVector(p2_ppPair_r);
    SHOWTLorentzVector(Pmiss);
    SHOWTLorentzVector(Pcm);
    SHOWTLorentzVector(Prec);
    PrintLine();
}
    
    


//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void T3pSimulation::Imp_q_Histo ( TH2F * h , bool DoPlot ){
    h_q = h;
    if(DoPlot) {
        TCanvas * c = plot.CreateCanvas("q");
        h_q -> Draw("colz");
        c -> SaveAs("q.pdf");
    }
}



//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void T3pSimulation::Imp_ppElasticHisto ( bool DoPlot ){

    TH2F * h = new TH2F("h_ppElastic","pp Elastic; c.m. energy [GeV]; #theta(c.m.) [deg.]",100,0,5,100,0,180);

    for (int binx = 0; binx < h->GetNbinsX() ; binx++) {
        for (int biny = 0; biny < h->GetNbinsY() ; biny++) {
            h -> SetBinContent(binx , biny , 1);
        }
    }
    
    Set_ppElasticHisto(h);
    if (DoPlot) {
        TCanvas * c = plot.CreateCanvas("ppElastic","Divide",2,1);
        c -> cd(1);
        h_ppElastic -> Draw("colz");
        TH1F* hTheta = (TH1F*) h_ppElastic->ProjectionY("hTheta",10,10);
        c -> cd(2);
        hTheta -> Draw("HIST");
        c -> SaveAs("~/Desktop/ppElastic.pdf");
    }
}



    
#endif
