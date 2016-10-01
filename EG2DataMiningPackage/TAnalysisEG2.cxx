#ifndef TANALYSISEG2_CXX
#define TANALYSISEG2_CXX

#include "TAnalysisEG2.h"

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
TAnalysisEG2::TAnalysisEG2(TString fPath , TString fInFileName, TCut MainCut):
TPlots( fPath + "/" + fInFileName + ".root","anaTree",fInFileName, false){
    SetPath(fPath);
    SetInFileName( fInFileName + ".root");
    SetSRCCuts(MainCut);
    SetInFile( new TFile( fPath + "/" + fInFileName + ".root" ));
    SetTree ((TTree*) InFile->Get( "anaTree" ));
}



//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
TAnalysisEG2::TAnalysisEG2(TString fInFileName, TCut MainCut):
TPlots("$DataMiningAnaFiles/Ana_" + fInFileName + ".root","anaTree",fInFileName, false){
    SetPath("$DataMiningAnaFiles");
    SetInFileName( "Ana_" + fInFileName + ".root");
    
    SetSRCCuts(MainCut);
    SetInFile( new TFile( "$DataMiningAnaFiles/" + InFileName ));
    SetTree ((TTree*) InFile->Get( "anaTree" ));
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void TAnalysisEG2::SetSRCCuts(TCut MainCut){ // last editted March-22 for pppSRC cuts

    // important (constant) cuts
    
    cutXb       = MainCut;
    cutPmiss    = "0.3 < Pmiss.P() && Pmiss.P() < 1.0";
    cutPmT      = "Pmiss.Pt() < 0.4";
    cutThetaPQ  = "theta_pq < 25";
    cutPoverQ   = "0.62 < p_over_q && p_over_q < 0.96";
    cutMmiss2   = "Mmiss < 1.1";
    
    cutSRCNoPm  = cutXb && cutThetaPQ && cutPoverQ ;
    cutSRC      = cutXb && cutThetaPQ && cutPoverQ && cutPmiss;
    cut1pSRC    = cutXb && cutThetaPQ && cutPoverQ && cutPmiss && "Np==1";
    
    for (int i = 0; i < 3; i++ ) {
                pEdepCut[i] = TEG2dm::pEdepCut(i);
    }
    p1EdepCut   = Form("%s",pEdepCut[0]->GetName());
    p1CTOFCut   = pCTOFCut[0] ;
    ppEdepCut   = Form("%s && %s",pEdepCut[0]->GetName(),pEdepCut[1]->GetName());
    ppCTOFCut   = pCTOFCut[0] && pCTOFCut[1] ;
    pppEdepCut  = Form("%s && %s && %s",pEdepCut[0]->GetName(),pEdepCut[1]->GetName(),pEdepCut[2]->GetName());
    pppCTOFCut  = "pCTOFCut[0] && pCTOFCut[1] && pCTOFCut[2]";

    
    
    // (e,e'p) in our cuts
    eepFinalCut = cutXb && cutThetaPQ && cutPoverQ && cutPmiss && cutPmT;

    
    
    // 2p-SRC following Or Hen' cuts
    PrecFiducial= "pFiducCut[1] == 1";
    cutPlead    = "-24.5 < pVertex[0].Z() && pVertex[0].Z() < -20";
    // ToDo: add Precoil fiducials!
    cutPrec     = "0.35 < Prec.P()  &&  (-24.5 < pVertex[1].Z() && pVertex[1].Z() < -20)" ;//&& PrecFiducial;
    ppSRCCut    = cutSRC && "1.2 <= Xb" && cutMmiss2 && "2 <= Np" && cutPlead && cutPrec && ppCTOFCut;
    
    
    
    // (e,e'p) in our cuts
    eepInSRCCut = cutSRC && cutMmiss2 && "1 <= Np" && cutPlead && p1CTOFCut;
    eeppInSRCCut = cutSRC && cutMmiss2 && "2 <= Np" && cutPlead && cutPrec && ppCTOFCut;
    
    
    
    // 3p-SRC
    cutP1       = "(-27 < pVertex[0].Z() && pVertex[0].Z() < -20)";
    cutP2       = "0.3 < protons[1].P() && (-27 < pVertex[1].Z() && pVertex[1].Z() < -20)";
    cutP3       = "0.3 < protons[2].P() && (-27 < pVertex[2].Z() && pVertex[2].Z() < -20)";
    cutMmiss    = "Pcm.Mag() < 3*0.938";
    cutWmiss    = "Wmiss.Mag() > 0";
    cutAngles2p = Form("%s > 150", TPlots::Theta("Pmiss.Vect()","Prec.Vect()").Data());
    cutAngles3p = "thetaMiss23 > 155 && fabs(phiMiss23) < 15";
    
    
    ppNothing_alpha12_vs_XbCut = TEG2dm::alpha12_vs_XbCut();
    alpha12_vs_XbCutDIS = ppNothing_alpha12_vs_XbCut->GetName();
    alpha12_vs_XbCutCorrelation = Form("!%s",ppNothing_alpha12_vs_XbCut->GetName());

    
    // pID from ∆E (dep.) in TOF scintillators
    pppRandomBkg= cutSRC && cutPmT && " 3 <= Np" && cutP1 && cutP2 && cutP3 && !pppEdepCut && !pppCTOFCut;
    pppCut      = cutSRC && " 3 <= Np" && cutP1 && cutP2 && cutP3 && pppEdepCut && pppCTOFCut;
    pppCutPmT   = pppCut && cutPmT;
    pppCutPmTMm = pppCutPmT && cutMmiss;
    pppSRCCut   = cutSRC && " 3 <= Np" && cutP1 && cutP2 && cutP3 && pppEdepCut && pppCTOFCut && cutPmT && cutMmiss;
    //    pppSRCMmiss = pppSRCCut && cutMmiss;
    Final3pCut  = pppSRCMmiss && cutAngles3p;
    
    
    
    
    // For 3p simulation
    Sim3pSRCCut = cutSRC && " 3 <= Np" && "0.3 < protons[1].P() && 0.3 < protons[2].P()" && cutPmT && cutMmiss ;
    Sim3pWmissCut = Sim3pSRCCut && cutWmiss ;
    FinalSim3pSRCCut = Sim3pSRCCut && cutAngles3p;
    
    


    // For mixed 3p...
    Mix3pSRCCut     = ""; // mixed, by definition, passes all (e,e'p) kinematical cuts (mixed from pppSRC cuts...)
    Mix3pPmT        = cutPmT ; // mixed, by definition, passes all (e,e'p) kinematical cuts (mixed from pppSRC cuts...)
    Mix3pPmTMm      = cutPmT && cutMmiss; // mixed, by definition, passes all (e,e'p) kinematical cuts (mixed from pppSRC cuts...)
    FinalMix3pSRCCut= Mix3pPmTMm && cutAngles3p;
    

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
TMatrix  TAnalysisEG2::RooFitCM( Float_t PmissMin, Float_t PmissMax, bool PlotFits, TCanvas * c, Int_t start_cd){
    // returns a parameter matrix: (μ-x,𝜎-x,μ-y,𝜎-y,μ-z,𝜎-z) and their uncertainties (𝚫μ-x,𝚫𝜎-x,𝚫μ-y,𝚫𝜎-y,𝚫μ-z,𝚫𝜎-z)
    // if PlotFits=true, it also plots the RooFits into three pads: start_cd, start_cd+1 , start_cd+2
    TMatrix     res(6,2);
    Double_t    PcmPars[2] = { 0 , 0.14 } ,   PcmParsErr[2] = { 0 , 0 };
    
    TCut cut = Form("%f < Pmiss3Mag && Pmiss3Mag < %f" , PmissMin , PmissMax);
    
    RooFit1D( Tree , "pcmX", cut , PcmPars , PcmParsErr , PlotFits , c->cd(start_cd) , Form("p(c.m.)-#bf{X} {%.2f<p(miss)<%.2f GeV/c}" , PmissMin , PmissMax) );
    res(0,0)   = PcmPars[0];
    res(1,0)   = PcmPars[1];
    res(0,1)   = PcmParsErr[0];
    res(1,1)   = PcmParsErr[1];

    RooFit1D( Tree , "pcmY", cut , PcmPars , PcmParsErr , PlotFits , c->cd(start_cd+1) , Form("p(c.m.)-#bf{Y} {%.2f<p(miss)<%.2f GeV/c}" , PmissMin , PmissMax)  );
    res(2,0)   = PcmPars[0];
    res(3,0)   = PcmPars[1];
    res(2,1)   = PcmParsErr[0];
    res(3,1)   = PcmParsErr[1];

    RooFit1D( Tree , "pcmZ", cut , PcmPars , PcmParsErr , PlotFits , c->cd(start_cd+2)  , Form("p(c.m.)-#bf{Z} {%.2f<p(miss)<%.2f GeV/c}" , PmissMin , PmissMax)  );
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




//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
vector<Float_t> TAnalysisEG2::GetFullpppEvent(int entry, bool DoPrint){
    if (entry==0) {
        Printf("retruning a vector of kinematic variables for (e,e'ppp) events");
        Printf("Xb / Q2 / p(e)-x / p(e)-y / p(e)-z / p(lead)-x  / p(lead)-y / p(lead)-z / p(2)-x / p(2)-y / p(2)-z / p(3)-x / p(3)-y / p(3)-z");
    }
    Float_t Xb , Q2 ;
    TLorentzVector * e = 0 ;
    vector <TLorentzVector> * protons = 0;
    Tree -> SetBranchAddress("Xb"       , &Xb);
    Tree -> SetBranchAddress("Q2"       , &Q2);
    Tree -> SetBranchAddress("e"        , &e);
    Tree -> SetBranchAddress("protons"  , &protons);
    
    Tree -> GetEntry(entry);
    
    vector<Float_t> res;
    res.push_back(Xb);
    res.push_back(Q2);
    res.push_back(e->Px());
    res.push_back(e->Py());
    res.push_back(e->Pz());
    for (int j = 0; j < 3; j++) {
        res.push_back(protons->at(j).Px());
        res.push_back(protons->at(j).Py());
        res.push_back(protons->at(j).Pz());
    }
    
    if (DoPrint) {
        for (auto var:res){
            printf("%.2f\t",var);
        }
        cout<<endl;
    }
    return res;
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
vector<Float_t> TAnalysisEG2::GetGSIMEvt(int entry, bool DoPrint){
    
    TLorentzVector * e = 0 ,*Pmiss = 0;
    vector <TLorentzVector> * p = 0;
    Tree -> SetBranchAddress("e"        , &e);
    Tree -> SetBranchAddress("Pmiss"    , &Pmiss);
    Tree -> SetBranchAddress("protons"  , &p);
    
    Tree -> GetEntry(entry);
    
    TLorentzVector  Beam(0,0,5.009,5.009) , q = Beam - *e , pLead = *Pmiss + q;
    vector<Float_t> res;
    res.push_back(4);
    
    // electron
    res.push_back(11);
    res.push_back(e->Px()/e->P());
    res.push_back(e->Py()/e->P());
    res.push_back(e->Pz()/e->P());
    res.push_back(e->P());
    res.push_back(Me);
    res.push_back(-1);
    for (int i = 0 ; i < 4 ; i++ ) res.push_back(0);
    
    // 3 protons
    for (int j = 0; j < 3; j++) {
        
        res.push_back(2212);
        res.push_back(p->at(j).Px()/p->at(j).P());
        res.push_back(p->at(j).Py()/p->at(j).P());
        res.push_back(p->at(j).Pz()/p->at(j).P());
        res.push_back(p->at(j).P());
        res.push_back(Mp);
        res.push_back(1);
        for (int i = 0 ; i < 4 ; i++ ) res.push_back(0);
        
    }
    
    if (DoPrint) {
        
        SHOWTLorentzVector(pLead);
        SHOWTLorentzVector(q);
        TLorentzVector Pm = *Pmiss;
        SHOWTLorentzVector(Pm);
        vector <TLorentzVector> protons = *p;
        SHOWvectorTLorentzVector(protons);
        PrintLine();
        
    }
    return res;
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
vector<Float_t> TAnalysisEG2::GetGSIMeep_pp_Evt(int entry, bool DoPrint){
    // take p(miss) from real data, and generate two uniformly-distributed random protons
    
    TLorentzVector * e = 0 ,*Pmiss = 0;
    Float_t Mmiss = 0;
    vector <TLorentzVector> *p = 0 , protons ;
    Tree -> SetBranchAddress("e"        , &e);
    Tree -> SetBranchAddress("Pmiss"    , &Pmiss);
    Tree -> SetBranchAddress("protons"  , &p);
    Tree -> SetBranchAddress("q_phi"    , &q_phi);
    Tree -> SetBranchAddress("q_theta"  , &q_theta);
    Tree -> SetBranchAddress("Pmiss_phi", &Pmiss_phi);
    
    Tree -> GetEntry(entry);
    
    TLorentzVector  Beam(0,0,5.009,5.009) , q = Beam - *e , pLead = *Pmiss + q ;

    
    
    
    // take the first proton from the data
    p3vec = p->at(0).Vect();
    RotVec_from_q_Pm_Frame( & p3vec , q_phi, q_theta, Pmiss_phi );
    protons.push_back( TLorentzVector( p3vec , p->at(0).E()) );
    
    // generate two random (recoiling) protons with uniform momenta 0.3-0.7 and uniform angular distribution
    Pp = rand.Uniform( 0.3 , 0.7 );
    rand.Sphere(Px,Py,Pz,Pp);
    p3vec = TVector3(Px , Py , Pz);
    RotVec_from_q_Pm_Frame( & p3vec , q_phi, q_theta, Pmiss_phi );
    protons.push_back(TLorentzVector( p3vec , sqrt(Pp*Pp + Mp*Mp) ));
    
    Pp = rand.Uniform( 0.3 , 0.7 );
    rand.Sphere(Px,Py,Pz,Pp);
    p3vec = TVector3(Px , Py , Pz);
    RotVec_from_q_Pm_Frame( & p3vec , q_phi, q_theta, Pmiss_phi );
    protons.emplace_back( p3vec , sqrt(Pp*Pp + Mp*Mp) );
    
    Mmiss = (*Pmiss + protons[1] + protons[2]).Mag();

 
    
    vector<Float_t> res;
    res.push_back(4);
    
    // electron
    res.push_back(11);
    res.push_back(e->Px()/e->P());
    res.push_back(e->Py()/e->P());
    res.push_back(e->Pz()/e->P());
    res.push_back(e->P());
    res.push_back(Me);
    res.push_back(-1);
    for (int i = 0 ; i < 4 ; i++ ) res.push_back(0);
    
    
    // 3 protons
    for (int j = 0; j < 3; j++) {
        
        res.push_back(2212);
        res.push_back(protons.at(j).Px()/protons.at(j).P());
        res.push_back(protons.at(j).Py()/protons.at(j).P());
        res.push_back(protons.at(j).Pz()/protons.at(j).P());
        res.push_back(protons.at(j).P());
        res.push_back(Mp);
        res.push_back(1);
        for (int i = 0 ; i < 4 ; i++ ) res.push_back(0);
        
    }
    if (DoPrint) {
        
        SHOW(entry);
        SHOWvectorTLorentzVector(protons);
        SHOW(Mmiss);
        PrintLine();
        
    }
    res.push_back(Pp);
    res.push_back(Mmiss);

    protons.clear();
    return res;
}


//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void TAnalysisEG2::MixEvents(TTree * OutTree, bool DoPrint){
    int Np;
    Float_t         thetaMiss23 , phiMiss23 ;
    TLorentzVector  *Pm = 0     , *q4 = 0   , Pmiss , q , Pcm , Prec;
    vector <TLorentzVector> * p = 0 , protons;
    Tree -> SetBranchAddress("q"        , &q4);
    Tree -> SetBranchAddress("Pmiss"    , &Pm);
    Tree -> SetBranchAddress("protons"  , &p);
    Tree -> SetBranchAddress("Np"       , &Np);
    int N = Tree->GetEntries()*(Tree->GetEntries()-1)*(Tree->GetEntries()-2);
    OutTree -> Branch("q"               ,"q"                    ,&q);
    OutTree -> Branch("Pcm"             ,"TLorentzVector"       ,&Pcm);
    OutTree -> Branch("Prec"            ,"TLorentzVector"       ,&Prec);
    OutTree -> Branch("Pmiss"           ,"TLorentzVector"       ,&Pmiss);
    OutTree -> Branch("protons"         ,&protons);             // std::vector<TLorentzVector>
    OutTree -> Branch("theta p(miss)-p2 p3" ,&thetaMiss23           , "thetaMiss23/F");
    OutTree -> Branch("phi p(miss)-p2 p3"   ,&phiMiss23             , "phiMiss23/F");

    for (int i1 = 0; i1 < Tree->GetEntries() ; i1++) {
        
        for (int i2 = 0; i2 < Tree->GetEntries() ; i2++) {
            if (i1 != i2) {

                for (int i3 = 0; i3 < Tree->GetEntries() ; i3++) {
                    if (i1 != i3 && i2 != i3) {
                        
                        // Fill entry with mixed protons...
                        if(!protons.empty()) protons.clear();
                        Tree -> GetEntry(i1);
                        q = *q4;
                        Pmiss = *Pm;
                        protons.push_back(p->at(0));
                        Tree -> GetEntry(i2);
                        protons.push_back(p->at(1));
                        Tree -> GetEntry(i3);
                        protons.push_back(p->at(2));
                        
                        Pcm  = Pmiss + protons.at(1) + protons.at(2);
                        Prec = protons.at(1) + protons.at(2);
                        thetaMiss23 = r2d*Pmiss.Vect().Angle((p->at(1)+p->at(2)).Vect());
                        phiMiss23   = 90 - r2d*( Pmiss.Vect().Angle(protons.at(1).Vect().Cross(protons.at(2).Vect()).Unit()) );
                        
                        OutTree -> Fill();
                        
                        // print out info
                        if (DoPrint) {
                            SHOWTLorentzVector(q);
                            SHOWTLorentzVector(Pmiss);
                            SHOWTLorentzVector(Pcm);
                            SHOWvectorTLorentzVector(protons);
                            PrintLine();
                        }
                        if (OutTree->GetEntries()%(N/10) == 0) {
                            Printf("\t[%.0f%%]",100*(float)OutTree->GetEntries()/N);
                        }
                    }
                }
            }
        }
    }
}



#endif






















