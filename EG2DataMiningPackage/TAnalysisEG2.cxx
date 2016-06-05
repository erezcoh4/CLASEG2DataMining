#ifndef TANALYSISEG2_CXX
#define TANALYSISEG2_CXX

#include "TAnalysisEG2.h"




//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
TAnalysisEG2::TAnalysisEG2(TString fInFileName, TCut XbCut):
TPlots("$DataMiningAnaFiles/Ana_" + fInFileName + ".root","anaTree",fInFileName, false){
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
    
    cutSRC      = cutXb && cutThetaPQ && cutPoverQ && cutPmiss;
    cut1pSRC    = cutXb && cutThetaPQ && cutPoverQ && cutPmiss && "Np==1";
    
    for (int i = 0; i < 3; i++ ) {
                pEdepCut[i] = TEG2dm::pEdepCut(i);
    }
    ppEdepCut   = Form("%s && %s",pEdepCut[0]->GetName(),pEdepCut[1]->GetName());
    ppCTOFCut   = pCTOFCut[0] && pCTOFCut[1] ;
    pppEdepCut  = Form("%s && %s && %s",pEdepCut[0]->GetName(),pEdepCut[1]->GetName(),pEdepCut[2]->GetName());
    pppCTOFCut  = "pCTOFCut[0] && pCTOFCut[1] && pCTOFCut[2]";

    
    // 2p-SRC following Or Hen' cuts
    cutPlead    = "-24.5 < pVertex[0].Z() && pVertex[0].Z() < -20";
    cutPrec     = "0.35 < Prec.P()  &&  (-24.5 < pVertex[1].Z() && pVertex[1].Z() < -20)";

    ppSRCCut    = cutSRC && " 2 <= Np" && cutPlead && cutPrec;
    
    
    
    
    // 3p-SRC
    cutP1       = "(-27 < pVertex[1].Z() && pVertex[1].Z() < -20)";
    cutP2       = "0.3 < protons[1].P() && (-27 < pVertex[1].Z() && pVertex[1].Z() < -20)";
    cutP3       = "0.3 < protons[2].P() && (-27 < pVertex[2].Z() && pVertex[2].Z() < -20)";
    cutMmiss    = "Pcm.Mag() < 2.802"; // lower than 3He mass

    cutAngles2p = Form("%s > 150", TPlots::Theta("Pmiss.Vect()","Prec.Vect()").Data());
    cutAngles3p = "thetaMiss23 > 155 && fabs(phiMiss23) < 15";
    
    
    // pID from ∆E (dep.) in TOF scintillators
    pppSRCCut   = cutSRC && " 3 <= Np" && cutP1 && cutP2 && cutP3 && pppEdepCut && pppCTOFCut;
    pppSRCMmiss = pppSRCCut && cutMmiss;
    Final3pCut  = pppSRCMmiss && cutAngles3p;
    
    
    // For 3p simulation...
    Sim3pSRCCut = cutSRC && " 3 <= Np" && "0.3 < protons[1].P() && 0.3 < protons[2].P()";
    FinalSim3pSRCCut = Sim3pSRCCut && cutAngles3p;

    
    // For mixed 3p...
    Mix3pSRCCut = ""; // mixed, by definition, passes all kinematics cuts (mixed from pppSRC cuts...)
    FinalMix3pSRCCut = Mix3pSRCCut && cutAngles3p;
    

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
void TAnalysisEG2::MixEvents(TTree * OutTree, bool DoPrint){
    int Np;
    Float_t         thetaMiss23 , phiMiss23 ;
    TLorentzVector  *Pm = 0     , *q4 = 0   , Pmiss , q;
    vector <TLorentzVector> * p = 0 , protons;
    Tree -> SetBranchAddress("q"        , &q4);
    Tree -> SetBranchAddress("Pmiss"    , &Pm);
    Tree -> SetBranchAddress("protons"  , &p);
    Tree -> SetBranchAddress("Np"       , &Np);
    int N = Tree->GetEntries()*(Tree->GetEntries()-1)*(Tree->GetEntries()-2);
    OutTree -> Branch("q"               ,"q"                    ,&q);
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
                        
                        thetaMiss23 = r2d*Pmiss.Vect().Angle((p->at(1)+p->at(2)).Vect());
                        phiMiss23   = 90 - r2d*( Pmiss.Vect().Angle(protons.at(1).Vect().Cross(protons.at(2).Vect()).Unit()) );
                        
                        OutTree -> Fill();
                        
                        // print out info
                        if (DoPrint) {
                            SHOWTLorentzVector(q);
                            SHOWTLorentzVector(Pmiss);
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






















