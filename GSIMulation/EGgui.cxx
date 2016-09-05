#ifndef EGGUI_CXX
#define EGGUI_CXX

#include "EGgui.h"



//-----------Constructor-----------------------//
//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
EGgui::EGgui( const TGWindow *pgWindow , UInt_t w , UInt_t h ){
    SetGlobals();
    fMain = new TGMainFrame(pgWindow,w,h);                              // Create a main frame
    AddMainButtonsFrame();
    AddEmbeddedCanvas();
    AddeeppButtonsFrame();
    AddeeNButtonsFrame();
    AddFlateeNRanges();
    
    AddeeNFromDistributions();
    AddeeNFromTree();
    AddGenerationButtonsFrame();
    MapMainFrame();
    fMain -> HideFrame(eeNButtonsFrame);
    fMain -> HideFrame(FlateeNFrame);
    fMain -> HideFrame(eeNFromDistributionsFrame);
    fMain -> HideFrame(eeNFromTreeFrame);
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
EGgui::~EGgui(){
    // Clean up used widgets: frames, buttons, layouthints
    fMain -> Cleanup();
    delete fMain;
    delete RootTree;
    delete RootFile;
}



//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void EGgui::AddEmbeddedCanvas(){
    fEcanvas    = new TRootEmbeddedCanvas("Ecanvas",fMain,300,300);        // Create canvas widget
    fMain       -> AddFrame(fEcanvas, new TGLayoutHints(kLHintsExpandX| kLHintsExpandY, 10,10,10,10));
}


//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void EGgui::MapMainFrame(){
    fMain -> SetWindowName("event generator frame");
    fMain -> MapSubwindows();
    fMain -> Resize(fMain->GetDefaultSize());
    fMain -> MapWindow();
}




//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void EGgui::SetGlobals(){
    //    if(gRandom) delete gRandom;
    gRandom = new TRandom3(0);
    SigmaT      = 0.110;
    SigmaL_a1   = 0.110;        SigmaL_a2   = 0.;     //       sigma = a1 + a2*(P(miss)-0.5);
    ShiftL_a1   = 0.;           ShiftL_a2   = 0.;     //       shift = a1 + a2*(P(miss)-0.3);
    
    NPTheta     = 100;
    NRand       = 1;
    Nevents     = 0;
    DrawString  = "Precoil.Mag()";
    CutString   = "";
    OptionString= "";
    
    Pmin        = 0.2;          Pmax        = 1.;
    Thetamin    = 0;            Thetamax    = 180;
    
    MagHistName   = "h_P";
    ThetaHistName = "h_Theta";
    
    eeNTreeName   = "Tree";
    Path = "/Users/erezcohen/Desktop/DataMining/GSIM";
    runsFilename  = Form("%s/eg_txtfiles/RunNumbers.dat",Path.Data());


    // current date/time based on current system
    now = time(0);
    dt = localtime(&now);

}












//----------- General funcionality ------------------------//
//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void EGgui::AddMainButtonsFrame(){
    fMainButtonsFrame   = new TGHorizontalFrame(fMain,900,40);
    AddRunNumberFrame(fMainButtonsFrame);
    AddNRandFrame(fMainButtonsFrame);
    fReepp              = new TGRadioButton(fMainButtonsFrame,new TGHotString("(e,e'pp)"),1000);
    fReepp              -> Connect("Pressed()", "EGgui", this, "Do_eepp()");
    fReepp              -> SetState(kButtonDown);
    fReeN               = new TGRadioButton(fMainButtonsFrame,new TGHotString("(e,e'B)"),1000);
    fReeN               -> Connect("Pressed()", "EGgui", this, "Do_eeN()");
    fMainButtonsFrame   -> AddFrame(fReepp, new TGLayoutHints(kLHintsCenterX,10,10,15,4) );
    fMainButtonsFrame   -> AddFrame(fReeN, new TGLayoutHints(kLHintsCenterX,10,10,15,4) );
    AddTextButton(fMainButtonsFrame , "&Exit" , "DoExit()");
    fMain               -> AddFrame(fMainButtonsFrame, new TGLayoutHints(kLHintsCenterX,2,2,2,2));
}



//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void EGgui::AddRunNumberFrame(TGHorizontalFrame *frame ){
    InRunNumberFile.open(runsFilename);
    InRunNumberFile >> RunNumber;
    InRunNumberFile.close();
    RunNumber++;
    SHOW(RunNumber);
    RunNumberFrame  = new TGGroupFrame(frame, Form("Run Number (%d)",RunNumber),kVerticalFrame);
    fRun            = new TGNumberEntry(RunNumberFrame,RunNumber,4,999, TGNumberFormat::kNESInteger, TGNumberFormat::kNEANonNegative);
    fRun            -> Connect("ValueSet(Long_t)", "EGgui", this, "DoSetRun()");
    RunNumberFrame  -> AddFrame(fRun, new TGLayoutHints(kMainFrame));
    frame           -> AddFrame(RunNumberFrame, new TGLayoutHints(kLHintsTop | kLHintsLeft, 5, 5, 5, 5));
}
//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void EGgui::DoSetRun(){
    RunNumber = fRun -> GetNumberEntry() -> GetIntNumber();
    RunNumberFrame ->  SetTitle(Form("Run %d",RunNumber));
}



//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void EGgui::AddGenerationButtonsFrame(){
    GenerationButtonsFrame  = new TGHorizontalFrame(fMain,900,40);
    AddTextButton(GenerationButtonsFrame , "&Generate!" , "DoGenMCFiles()");
    fGenLabelData           = new TGLabel(GenerationButtonsFrame, "No Generated data.");
    GenerationButtonsFrame  -> AddFrame(fGenLabelData, new TGLayoutHints(kLHintsTop | kLHintsLeft,10, 10, 15, 5));
    fDrawString             = new TGTextEntry(GenerationButtonsFrame);
    fDrawString             -> SetText(DrawString);
    fDrawString             -> Connect("ValueSet(Long_t)", "EGgui", this, "DoSetDrawString()");
    GenerationButtonsFrame  -> AddFrame(fDrawString, new TGLayoutHints(kLHintsTop | kLHintsLeft,10, 10, 15, 5));
    fCutString              = new TGTextEntry(GenerationButtonsFrame);
    fCutString              -> SetText(CutString);
    fCutString              -> Connect("ValueSet(Long_t)", "EGgui", this, "DoSetDrawString()");
    GenerationButtonsFrame  -> AddFrame(fCutString, new TGLayoutHints(kLHintsTop | kLHintsLeft,10, 10, 15, 5));
    fOptionString           = new TGTextEntry(GenerationButtonsFrame);
    fOptionString           -> SetText(OptionString);
    fOptionString           -> Connect("ValueSet(Long_t)", "EGgui", this, "DoSetDrawString()");
    GenerationButtonsFrame  -> AddFrame(fOptionString, new TGLayoutHints(kLHintsTop | kLHintsLeft,10, 10, 15, 5));
    AddTextButton(GenerationButtonsFrame , "&Draw" , "DoDrawGenerated()");
    fMain                   -> AddFrame(GenerationButtonsFrame, new TGLayoutHints(kLHintsCenterX,2,2,2,2));
}


//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void EGgui::DoSetDrawString(){
    DrawString      = fDrawString   -> GetText();
    CutString       = fCutString    -> GetText();
    OptionString    = fOptionString -> GetText();
}



//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void EGgui::DoExit(){ gApplication->Terminate(0);}



//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void EGgui::AddTextButton(TGHorizontalFrame *frame , TString name , TString funcName ){
    TGTextButton *button    = new TGTextButton(frame,name);
    frame                   -> AddFrame(button, new TGLayoutHints(kLHintsCenterX,10,10,15,4));
    button                  -> Connect("Clicked()" , "EGgui" , this , funcName);
}



//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void EGgui::AddNRandFrame(TGHorizontalFrame *frame ){
    NRandFrame      = new TGGroupFrame(frame, Form("N(r)= %d",NRand) , kHorizontalFrame);
    fNRand          = new TGNumberEntry(NRandFrame,NRand,4,999, TGNumberFormat::kNESInteger, TGNumberFormat::kNEANonNegative);
    fNRand          -> Connect("ValueSet(Long_t)", "EGgui", this, "DoSetNRand()");
    NRandFrame      -> AddFrame(fNRand, new TGLayoutHints(kMainFrame));
    frame           -> AddFrame(NRandFrame, new TGLayoutHints(kLHintsTop | kLHintsLeft, 5, 5, 5, 5));
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void EGgui::DoSetNRand(){
    NRand           = fNRand -> GetNumberEntry() -> GetIntNumber();
    NRandFrame      ->  SetTitle(Form("N(r)= %d",NRand));
}



















//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
//-----------------------------------------------//
//----------- G E N E R A T I O N ---------------//
//-----------------------------------------------//
//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......




// ---------- (e,e'pp) ---------- //
//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void EGgui::Do_eepp(){
    fReepp  -> SetState(kButtonDown);
    fReeN   -> SetState(kButtonUp);
    fMain -> HideFrame(eeNButtonsFrame);
    fMain -> ShowFrame(eeppButtonsFrame);
    fDrawString -> SetText("Precoil.Phi():Precoil.Theta()");
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void EGgui::AddeeppButtonsFrame(){
    eeppButtonsFrame    = new TGHorizontalFrame(fMain,900,40);
    fMain               -> AddFrame(eeppButtonsFrame, new TGLayoutHints(kLHintsCenterX,2,2,2,2));
    AddSigmaTFrame(eeppButtonsFrame);
    AddSigmaLFrame(eeppButtonsFrame);
    AddShiftLFrame(eeppButtonsFrame);
}


//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void EGgui::AddSigmaTFrame(TGHorizontalFrame *frame ){
    SigmaTFrame     = new TGGroupFrame(frame, "sigma(T)",kVerticalFrame);
    fSigmaT         = new TGNumberEntry(SigmaTFrame,SigmaT,5,999, TGNumberFormat::kNESRealThree, TGNumberFormat::kNEANonNegative);
    fSigmaT         -> Connect("ValueSet(Long_t)", "EGgui", this, "DoSetSigmaT()");
    SigmaTFrame     -> AddFrame(fSigmaT, new TGLayoutHints(kMainFrame));
    frame           -> AddFrame(SigmaTFrame, new TGLayoutHints(kLHintsTop | kLHintsLeft, 5, 5, 5, 5));
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void EGgui::DoSetSigmaT(){
    SigmaT = fSigmaT -> GetNumberEntry() -> GetNumber();
    SigmaTFrame ->  SetTitle(Form("sigma(T)=%.3f GeV/c",SigmaT));
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void EGgui::AddSigmaLFrame(TGHorizontalFrame *frame ){
    SigmaLFrame         = new TGGroupFrame(frame, Form("sigma(L)=%.2f+%.2f(p(miss)-0.5)",SigmaL_a1,SigmaL_a2),kHorizontalFrame);
    fSigmaL_a1          = new TGNumberEntry(SigmaLFrame,SigmaL_a1,5,999, TGNumberFormat::kNESRealThree, TGNumberFormat::kNEANonNegative);
    fSigmaL_a1          -> Connect("ValueSet(Long_t)", "EGgui", this, "DoSetSigmaL()");
    SigmaLFrame         -> AddFrame(fSigmaL_a1, new TGLayoutHints(kMainFrame));
    fSigmaL_a2          = new TGNumberEntry(SigmaLFrame,SigmaL_a2,5,999, TGNumberFormat::kNESRealThree, TGNumberFormat::kNEANonNegative);
    fSigmaL_a2          -> Connect("ValueSet(Long_t)", "EGgui", this, "DoSetSigmaL()");
    SigmaLFrame         -> AddFrame(fSigmaL_a2, new TGLayoutHints(kMainFrame));
    frame               -> AddFrame(SigmaLFrame, new TGLayoutHints(kLHintsTop | kLHintsLeft, 5, 5, 5, 5));
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void EGgui::DoSetSigmaL(){
//    SigmaL_a1           = SigmaT;
//    SigmaL_a2           = 0;
    SigmaL_a1           = fSigmaL_a1 -> GetNumberEntry() -> GetNumber();
    SigmaL_a2           = fSigmaL_a2 -> GetNumberEntry() -> GetNumber();
    SigmaLFrame         ->  SetTitle(Form("sigma(L)=%.2f(p(miss)-0.5)+%.2f",SigmaL_a1,SigmaL_a2));
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void EGgui::AddShiftLFrame(TGHorizontalFrame *frame ){
    ShiftLFrame         = new TGGroupFrame(frame,Form("Shift(L)=%.2f+%.2f(p(miss)-0.3)",ShiftL_a1,ShiftL_a2),kHorizontalFrame);
    fShiftL_a1          = new TGNumberEntry(ShiftLFrame,ShiftL_a1,5,999, TGNumberFormat::kNESRealThree, TGNumberFormat::kNEANonNegative);
    fShiftL_a1          -> Connect("ValueSet(Long_t)", "EGgui", this, "DoSetShiftL()");
    ShiftLFrame         -> AddFrame(fShiftL_a1, new TGLayoutHints(kMainFrame));
    fShiftL_a2          = new TGNumberEntry(ShiftLFrame,ShiftL_a2,5,999, TGNumberFormat::kNESRealThree, TGNumberFormat::kNEANonNegative);
    fShiftL_a2          -> Connect("ValueSet(Long_t)", "EGgui", this, "DoSetShiftL()");
    ShiftLFrame         -> AddFrame(fShiftL_a2, new TGLayoutHints(kMainFrame));
    frame               -> AddFrame(ShiftLFrame, new TGLayoutHints(kLHintsTop | kLHintsLeft, 5, 5, 5, 5));
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void EGgui::DoSetShiftL(){
    ShiftL_a1           = fShiftL_a1 -> GetNumberEntry() -> GetNumber();
    ShiftL_a2           = fShiftL_a2 -> GetNumberEntry() -> GetNumber();
    ShiftLFrame         ->  SetTitle(Form("Shift(L)=%.2f(p(miss)-0.3)+%.2f",ShiftL_a1,ShiftL_a2));
}













// ---------- (e,e'N) ---------- //
//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void EGgui::Do_eeN(){
    fReepp  -> SetState(kButtonUp);
    fReeN   -> SetState(kButtonDown);
    fMain   -> HideFrame(eeppButtonsFrame);
    fMain   -> ShowFrame(eeNButtonsFrame);
    fMain   -> HideFrame(eeNFromDistributionsFrame);
    fMain   -> HideFrame(eeNFromTreeFrame);
    fMain   -> ShowFrame(FlateeNFrame);
    DoSetBaryonName();
}



//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void EGgui::AddeeNButtonsFrame(){
    eeNButtonsFrame     = new TGHorizontalFrame(fMain,900,40);
    fReep               = new TGRadioButton(eeNButtonsFrame,new TGHotString("(e,e'p)"),1000);
    fReep               -> Connect("Pressed()", "EGgui", this, "Do_eep()");
    fReep               -> SetState(kButtonDown);
    eeNButtonsFrame     -> AddFrame(fReep, new TGLayoutHints(kLHintsCenterX,10,10,15,4) );
    fReen               = new TGRadioButton(eeNButtonsFrame,new TGHotString("(e,e'n)"),1000);
    fReen               -> Connect("Pressed()", "EGgui", this, "Do_een()");
    eeNButtonsFrame     -> AddFrame(fReen, new TGLayoutHints(kLHintsCenterX,10,10,15,4) );
    fReeDelta           = new TGRadioButton(eeNButtonsFrame,new TGHotString("(e,e'Delta)"),1000);
    fReeDelta           -> Connect("Pressed()", "EGgui", this, "Do_eeDelta()");
    eeNButtonsFrame     -> AddFrame(fReeDelta, new TGLayoutHints(kLHintsCenterX,10,10,15,4) );
    fMain               -> AddFrame(eeNButtonsFrame, new TGLayoutHints(kLHintsCenterX,2,2,2,2));
    fFlateeN            = new TGRadioButton(eeNButtonsFrame,new TGHotString("Flat distributions"),1000);
    fFlateeN            -> Connect("Pressed()", "EGgui", this, "DoFlateeN()");
    fFlateeN            -> SetState(kButtonDown);
    fReeNFromDist       = new TGRadioButton(eeNButtonsFrame,new TGHotString("From model"),1000);
    fReeNFromDist       -> Connect("Pressed()", "EGgui", this, "DoeeNFromDist()");
    fReeNFromTree       = new TGRadioButton(eeNButtonsFrame,new TGHotString("From Tree"),1000);
    fReeNFromTree       -> Connect("Pressed()", "EGgui", this, "DoeeNFromTree()");
    eeNButtonsFrame     -> AddFrame(fFlateeN, new TGLayoutHints(kLHintsCenterX,10,10,15,4) );
    eeNButtonsFrame     -> AddFrame(fReeNFromDist, new TGLayoutHints(kLHintsCenterX,10,10,15,4) );
    eeNButtonsFrame     -> AddFrame(fReeNFromTree, new TGLayoutHints(kLHintsCenterX,10,10,15,4) );
    NPThetaFrame        = new TGGroupFrame(eeNButtonsFrame, Form("NPTheta=%d",NPTheta),kHorizontalFrame);
    fNPTheta            = new TGNumberEntry(NPThetaFrame,NPTheta,5,999, TGNumberFormat::kNESInteger, TGNumberFormat::kNEANonNegative);
    fNPTheta            -> Connect("ValueSet(Long_t)", "EGgui", this, "DoSetNPtheta()");
    NPThetaFrame        -> AddFrame(fNPTheta, new TGLayoutHints(kMainFrame));
    eeNButtonsFrame     -> AddFrame(NPThetaFrame, new TGLayoutHints(kLHintsCenterX,10,10,15,4) );
    fMain               -> AddFrame(eeNButtonsFrame, new TGLayoutHints(kLHintsCenterX,2,2,2,2));
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void EGgui::Do_een(){
    fReen       -> SetState(kButtonDown);
    fReep       -> SetState(kButtonUp);
    fReeDelta   -> SetState(kButtonUp);
    DoSetBaryonName();
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void EGgui::Do_eep(){
    fReen       -> SetState(kButtonUp);
    fReep       -> SetState(kButtonDown);
    fReeDelta   -> SetState(kButtonUp);
    DoSetBaryonName();
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void EGgui::Do_eeDelta(){
    fReen       -> SetState(kButtonUp);
    fReep       -> SetState(kButtonUp);
    fReeDelta   -> SetState(kButtonDown);
    DoSetBaryonName();
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void EGgui::DoSetBaryonName(){
    BaryonName = (fReeDelta->IsOn()) ? "Delta" : ((fReep->IsOn() && !fReen->IsOn()) ? "p" : "n");
    fDrawString -> SetText(Form("%s.Mag()",BaryonName.Data()));
}


//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void EGgui::DoFlateeN(){
    fReeNFromDist   -> SetState(kButtonUp);
    fReeNFromTree   -> SetState(kButtonUp);
    fFlateeN        -> SetState(kButtonDown);
    fMain           -> HideFrame(eeNFromTreeFrame);
    fMain           -> HideFrame(eeNFromDistributionsFrame);
    fMain           -> ShowFrame(FlateeNFrame);
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void EGgui::DoeeNFromDist(){
    fReeNFromDist   -> SetState(kButtonDown);
    fReeNFromTree   -> SetState(kButtonUp);
    fFlateeN        -> SetState(kButtonUp);
    fMain           -> HideFrame(eeNFromTreeFrame);
    fMain           -> HideFrame(FlateeNFrame);
    fMain           -> ShowFrame(eeNFromDistributionsFrame);
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void EGgui::DoeeNFromTree(){
    fReeNFromTree   -> SetState(kButtonDown);
    fReeNFromDist   -> SetState(kButtonUp);
    fFlateeN        -> SetState(kButtonUp);
    fMain           -> ShowFrame(eeNFromTreeFrame);
    fMain           -> HideFrame(FlateeNFrame);
    fMain           -> HideFrame(eeNFromDistributionsFrame);
}



//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void EGgui::AddFlateeNRanges(){
    FlateeNFrame        = new TGHorizontalFrame(fMain,900,40);
    PminPmaxFrame       = new TGGroupFrame(FlateeNFrame, Form("%.3f < |p| < %.3f GeV/c",Pmin,Pmax),kHorizontalFrame);
    fPmin               = new TGNumberEntry(PminPmaxFrame,Pmin,5,999, TGNumberFormat::kNESRealThree, TGNumberFormat::kNEANonNegative);
    fPmin               -> Connect("ValueSet(Long_t)", "EGgui", this, "DoSetPminPmax()");
    PminPmaxFrame       -> AddFrame(fPmin, new TGLayoutHints(kMainFrame));
    fPmax               = new TGNumberEntry(PminPmaxFrame,Pmax,5,999, TGNumberFormat::kNESRealThree, TGNumberFormat::kNEANonNegative);
    fPmax               -> Connect("ValueSet(Long_t)", "EGgui", this, "DoSetPminPmax()");
    PminPmaxFrame       -> AddFrame(fPmax, new TGLayoutHints(kMainFrame));
    FlateeNFrame        -> AddFrame(PminPmaxFrame, new TGLayoutHints(kLHintsTop | kLHintsLeft, 5, 5, 5, 5));
    ThetaminThetamaxFrame   = new TGGroupFrame(FlateeNFrame, Form("%.1f < theta < %.1f deg.",Thetamin,Thetamax),kHorizontalFrame);
    fThetamin               = new TGNumberEntry(ThetaminThetamaxFrame,Thetamin,5,999
                                                , TGNumberFormat::kNESRealThree, TGNumberFormat::kNEANonNegative);
    fThetamin               -> Connect("ValueSet(Long_t)", "EGgui", this, "DoSetThetaminThetamax()");
    ThetaminThetamaxFrame   -> AddFrame(fThetamin, new TGLayoutHints(kMainFrame));
    fThetamax               = new TGNumberEntry(ThetaminThetamaxFrame,Thetamax,5,999
                                                , TGNumberFormat::kNESRealThree, TGNumberFormat::kNEANonNegative);
    fThetamax               -> Connect("ValueSet(Long_t)", "EGgui", this, "DoSetThetaminThetamax()");
    ThetaminThetamaxFrame   -> AddFrame(fThetamax, new TGLayoutHints(kMainFrame));
    FlateeNFrame            -> AddFrame(ThetaminThetamaxFrame, new TGLayoutHints(kLHintsTop | kLHintsLeft, 5, 5, 5, 5));
    fMain                   -> AddFrame(FlateeNFrame, new TGLayoutHints(kLHintsCenterX,2,2,2,2));
}


//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void EGgui::DoSetNPtheta(){
    NPTheta         = fNPTheta -> GetNumberEntry() -> GetIntNumber();
    NPThetaFrame    -> SetTitle(Form("NPtheta=%d",NPTheta));
}


//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void EGgui::DoSetPminPmax(){
    Pmin           = fPmin -> GetNumberEntry() -> GetNumber();
    Pmax           = fPmax -> GetNumberEntry() -> GetNumber();
    PminPmaxFrame  ->  SetTitle(Form("%.3f < |p| < %.3f GeV/c",Pmin,Pmax));
}


//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void EGgui::DoSetThetaminThetamax(){
    Thetamin                = fThetamin -> GetNumberEntry() -> GetNumber();
    Thetamax                = fThetamax -> GetNumberEntry() -> GetNumber();
    ThetaminThetamaxFrame   ->  SetTitle(Form("%.1f < theta < %.1f deg.",Thetamin,Thetamax));
}


//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void EGgui::AddeeNFromDistributions(){
    eeNFromDistributionsFrame   = new TGHorizontalFrame(fMain,900,40);
    fMagHistName                  = new TGTextEntry(eeNFromDistributionsFrame);
    fMagHistName                  -> SetText(MagHistName);
    fMagHistName                  -> Connect("ValueSet(Long_t)", "EGgui", this, "DoSetInHistNames()");
    eeNFromDistributionsFrame   -> AddFrame(fMagHistName, new TGLayoutHints(kLHintsTop | kLHintsLeft,10, 10, 15, 5));
    fThetaHistName              = new TGTextEntry(eeNFromDistributionsFrame);
    fThetaHistName              -> SetText(ThetaHistName);
    fThetaHistName              -> Connect("ValueSet(Long_t)", "EGgui", this, "DoSetInHistNames()");
    eeNFromDistributionsFrame   -> AddFrame(fThetaHistName, new TGLayoutHints(kLHintsTop | kLHintsLeft,10, 10, 15, 5));
    AddTextButton(eeNFromDistributionsFrame , "&Choose File" , "OpenInFileDialog()");
    fMain                       -> AddFrame(eeNFromDistributionsFrame, new TGLayoutHints(kLHintsCenterX,2,2,2,2));
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void EGgui::DoSetInHistNames(){
    MagHistName       = fMagHistName -> GetText();
    ThetaHistName   = fThetaHistName -> GetText();
}


//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void EGgui::OpenInFileDialog(){
    TGFileInfo fi;
    eeNInFileDialog = new TGFileDialog(gClient->GetDefaultRoot(), fMain, kFDOpen,&fi);
    Printf("Taking data from %s \n",fi.fFilename);
    TFile * InFile  = new TFile(fi.fFilename);
    histMag         = (TH1F*)InFile->Get(MagHistName);
    histTheta       = (TH1F*)InFile->Get(ThetaHistName);
}


//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void EGgui::AddeeNFromTree(){
    eeNFromTreeFrame            = new TGHorizontalFrame(fMain,900,40);
    fTreeName                   = new TGTextEntry(eeNFromTreeFrame);
    fTreeName                   -> SetText(eeNTreeName);
    fTreeName                   -> Connect("ValueSet(Long_t)", "EGgui", this, "DoSeteeNTreeName()");
    eeNFromTreeFrame            -> AddFrame(fTreeName, new TGLayoutHints(kLHintsTop | kLHintsLeft,10, 10, 15, 5));
    AddTextButton(eeNFromTreeFrame , "&Choose File" , "OpeneeNTreeInFileDialog()");
    fMain                       -> AddFrame(eeNFromTreeFrame, new TGLayoutHints(kLHintsCenterX,2,2,2,2));
}


//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void EGgui::DoSeteeNTreeName(){
    eeNTreeName       = fTreeName -> GetText();
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void EGgui::OpeneeNTreeInFileDialog(){
    TGFileInfo fi;
    eeNTreeInFileDialog = new TGFileDialog(gClient->GetDefaultRoot(), fMain, kFDOpen,&fi);
    Printf("Taking data from %s \n",fi.fFilename);
    TFile * InFile  = new TFile(fi.fFilename);
    eeNTree         = (TTree*)InFile->Get(eeNTreeName);
}




// main generation processes....
//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void EGgui::DoGenMCFiles(){
    DoGenerate();
}


// main generation processes....
//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void EGgui::DoGenerate(){
//    InputT   = new TChain("T");
//    txtFilename     = Form("%s/eg_txtfiles/run%04d.txt",Path.Data(),RunNumber);
//    rootFilename    = Form("%s/eg_rootfiles/run%04d.root",Path.Data(),RunNumber);
//    cout << "Generating " << txtFilename << " and " <<  rootFilename << endl;
//    TextFile.open(txtFilename);
//    RootFile = new TFile( rootFilename ,"recreate" );
//    RootTree = new TTree("anaTree","generated events");
//    SetRootTreeAddresses();
//    if (fReepp -> IsOn() ){
//        Printf("(e,e'pp)");
//        // Take 12C(e,e'p) SRC tree data
//        InputT          -> Add("/Users/erezcohen/Desktop/DataMining/GSIM/GUIEG/SRC_e1_C.root");
//        InputT          -> Add("/Users/erezcohen/Desktop/DataMining/GSIM/GUIEG/SRC_e2_C.root");
//        Float_t Pe[3]   , Pe_size;                                              // electron
//        Float_t Ep[2]   , Rproton[2][3] , Pproton[2][3] ,   Pproton_size[2];    // Proton
//        Float_t Pm[2][3], Pm_size[2];                                           // Proton missing momentum magnitude
//        Float_t q[3]    , q_size;                                               // q momentum transfer
//        
//        InputT -> SetBranchAddress("Q2"      ,           &Q2);
//        InputT -> SetBranchAddress("Xb"      ,           &Xb);
//        InputT -> SetBranchAddress("Pe"      ,           &Pe);
//        InputT -> SetBranchAddress("theta_e" ,           &theta_e);
//        InputT -> SetBranchAddress("Pe_size" ,           &Pe_size);
//        InputT -> SetBranchAddress("Ep"      ,           &Ep);
//        InputT -> SetBranchAddress("Pp"      ,           &Pproton);
//        InputT -> SetBranchAddress("Rp"      ,           &Rproton);           // proton vertex
//        InputT -> SetBranchAddress("Pp_size" ,           &Pproton_size);
//        InputT -> SetBranchAddress("Pmiss"   ,           &Pm);
//        InputT -> SetBranchAddress("Pmiss_size",         &Pm_size);
//        InputT -> SetBranchAddress("q"       ,           &q);
//        InputT -> SetBranchAddress("q_size"  ,           &q_size);
//        int InputNentries = InputT -> GetEntries();
//        
//        TVector3 * momentum = new TVector3[3];
//        int charge[3]           = { -1          , 1         , 1     };
//        float mass[3]           = { 0.000511    , 0.938     , 0.938 };
//        int pid[3]              = { 11          , 2212      , 2212  };
//        
//        for (int entry = 0 ; entry < InputNentries ; entry++ ) {
//            if ( entry%(InputNentries/10) == 0 ) std::cout  <<  (int)(100*(double)entry/InputNentries)+1 << "%\n";
//            
//            InputT -> GetEntry(entry);
//            double PmissMag = Pm_size[0];
//            
//            e.SetXYZ            ( Pe[0]         , Pe[1]         , Pe[2]);
//            q3Vector.SetXYZ     ( q[0]          , q[1]          , q[2] );
//            Pmiss.SetXYZ        ( Pm[0][0]      , Pm[0][1]      , Pm[0][2]);
//            Pp1.SetXYZ          ( Pproton[0][0] , Pproton[0][1] , Pproton[0][2]);
//            
//            
//            // rotate to Pmiss-q frame: Pmiss is the z axis, q is in x-z plane: q=(q[x],0,q[Pmiss])
//            double Pmiss_phi = Pmiss.Phi() , Pmiss_theta = Pmiss.Theta() ;
//            q3Vector_in_Pmiss_q_system = q3Vector;
//            q3Vector_in_Pmiss_q_system.RotateZ(-Pmiss_phi);
//            q3Vector_in_Pmiss_q_system.RotateY(-Pmiss_theta);
//            double q_Phi = q3Vector_in_Pmiss_q_system.Phi();
//            q3Vector_in_Pmiss_q_system.RotateZ(-q_Phi);
//            
//            Pmiss_in_Pmiss_q_system = Pmiss;
//            Pmiss_in_Pmiss_q_system.RotateZ(-Pmiss_phi);
//            Pmiss_in_Pmiss_q_system.RotateY(-Pmiss_theta);
//            Pmiss_in_Pmiss_q_system.RotateZ(-q_Phi);
//            
//            
//            // rotate to q-Pmiss frame: q is the z axis, Pmiss is in x-z plane: Pmiss=(Pmiss[x],0,Pmiss[q])
//            double q_q_phi = q3Vector.Phi() , q_q_theta = q3Vector.Theta() ;
//            Pmiss_q_sys = q3Vector;
//            Pmiss_q_sys.RotateZ(-q_q_phi);
//            Pmiss_q_sys.RotateY(-q_q_theta);
//            double Pmiss_Phi = Pmiss_q_sys.Phi();
//            Pmiss_q_sys.RotateZ(-Pmiss_Phi);
//            
//            q_q_sys = q3Vector;
//            q_q_sys.RotateZ(-q_q_phi);
//            q_q_sys.RotateY(-q_q_theta);
//            q_q_sys.RotateZ(-Pmiss_Phi);
//            
//            
//            double  omega   = 5.009 - sqrt( 0.000511*0.000511 + e.Mag()*e.Mag() );
//            ThetaPQ         = (180/TMath::Pi())*(Pp1.Angle(q3Vector));
//            ThetaPmissQ     = (180/TMath::Pi())*(Pmiss.Angle(q3Vector));
//            PoverQ          = Pp1.Mag()/q3Vector.Mag();
//            Proton          .SetVectM   ( Pp1 , 0.938 ); // struck proton
//            q4Vector        .SetXYZT    ( q3Vector.x() , q3Vector.y() , q3Vector.z() , omega );
//            m2N             .SetVectM   ( TVector3(0,0,0) , 2.*0.938 );
//            miss            = q4Vector + m2N - Proton;
//            Mmiss           = miss.Mag();
//            Rp1             .SetXYZ(Rproton[0][0],Rproton[0][1],Rproton[0][2]); // since there is no actual Rp2....
//            Rp2 = Rp1;// since there is no actual Rp2....
//            
//            
//            for( int j = 0 ; j < NRand  ;  j++ ){    //MC event generation
//                
//                float Px = gRandom -> Gaus( 0  , SigmaT );
//                float Py = gRandom -> Gaus( 0  , SigmaT );
//                float Pz = gRandom -> Gaus( ShiftL_a1 + ShiftL_a2*(PmissMag-0.3)  , SigmaL_a1 + SigmaL_a2*(PmissMag-0.5) );
//                Pcm_in_Pmiss_q_system.SetXYZ   ( Px , Py , Pz );
//                
//                // rotate back to lab frame
//                Pcm = Pcm_in_Pmiss_q_system;
//                Pcm.RotateZ  ( q_Phi );
//                Pcm.RotateY  ( Pmiss_theta );
//                Pcm.RotateZ  ( Pmiss_phi );
//                Precoil =   Pp2     = Pcm - Pmiss;
//                ThetaPmissPrecoil   = (180/TMath::Pi())*(Pmiss.Angle(Precoil));
//                
//                momentum[0] = e ; momentum[1] = Pp1; momentum[2] = Pp2;
//                OutPutToTextFile(3, momentum , charge , mass , pid );
//                // rotate also to q-Pmiss frame: q is the z axis, Pmiss is in x-z plane: Pmiss=(Pmiss[x],0,Pmiss[q])
//                Pcm_q_sys = Pcm;
//                Pcm_q_sys.RotateZ(-q_q_phi);
//                Pcm_q_sys.RotateY(-q_q_theta);
//                Pcm_q_sys.RotateZ(-Pmiss_Phi);
//                
//                Nevents++ ;
//                RootTree -> Fill();
//            }
//        }
//    }
//    else if (fReeN -> IsOn()){
//        Printf("(e,e'B)");
//        TVector3 e , N;     // N is a baryon: p/n/𝚫
//        RootTree -> Branch( BaryonName ,"TVector3"     ,&N);
//        RootTree -> Branch( "e" ,"TVector3" ,&e);
//        Float_t mag , theta;
//        TVector3 * momentum     = new TVector3[2];
//        
//        int charge[2]           = { -1          , (BaryonName == "p") ? 1       : ((BaryonName == "n") ? 0      : 2)        };
//        float mass[2]           = { 0.000511    ,  static_cast<float>((BaryonName == "p") ? 0.938   : ((BaryonName == "n") ? 0.939  : 1.232))    };
//        int pid[2]              = { 11          , (BaryonName == "p") ? 2212    : ((BaryonName == "n") ? 2112   : 2214)     };
//        
//        
//        //------- TAKE DATA FROM TREE --------------//
//        if (fReeNFromTree -> IsOn()){
//            
//            Float_t PeMag   , Theta_e , Phi_e   , PpMag , Theta_p;
//            eeNTree -> SetBranchAddress("P_e"       ,   &PeMag);
//            eeNTree -> SetBranchAddress("theta_e"   ,   &Theta_e);
//            eeNTree -> SetBranchAddress("phi_e"     ,   &Phi_e);
//            eeNTree -> SetBranchAddress("P_N"       ,   &mag);
//            eeNTree -> SetBranchAddress("theta_N"   ,   &theta);
//            
//            for (int entry = 0 ; entry < eeNTree->GetEntries() ; entry++ ) {
//                eeNTree -> GetEntry(entry);
//                e.SetMagThetaPhi(PeMag,(TMath::Pi()/180.)*Theta_e,(TMath::Pi()/180.)*Phi_e);
//                momentum[0] = e;
//                for ( int rand = 0 ; rand < NRand ; rand++ ) {
//                    Double_t phi    = 360.*gRandom->Uniform();         // uniform angle between 0 and 360 degrees
//                    N.SetMagThetaPhi ( mag , (TMath::Pi()/180.)*theta , (TMath::Pi()/180.)*phi);
//                    momentum[1] = N;
//                    OutPutToTextFile(2, momentum , charge ,mass , pid );
//                    RootTree -> Fill();
//                }
//            }
//        }
//        
//        //------- CREATE NEW DATA --------------//
//        else {
//            TVector3 e(-0.137*4.306 , -0.339*4.306 , 0.956*4.306 ); // a single electron that passes RECSIS cuts...
//            momentum[0] = e;
//            for (int entry = 0 ; entry < NPTheta ; entry++ ) {
//                if ( entry%(NPTheta/10) == 0 ) std::cout  << (int)(100*(double)entry/NPTheta) << "%\n";
//                if (fFlateeN->IsOn()){ // flat distributions
//                    theta  = Thetamin + (Thetamax-Thetamin)*gRandom->Uniform();
//                    mag    = Pmin + (Pmax-Pmin)*gRandom->Uniform();
//                } else if (fReeNFromDist->IsOn()){  // take from file histograms
//                    theta  = histTheta ->GetRandom();
//                    mag    = histMag   ->GetRandom();
//                }
//                for ( int rand = 0 ; rand < NRand ; rand++ ) {
//                    Double_t phi    = 360.*gRandom->Uniform();         // uniform angle between 0 and 360 degrees
//                    N.SetMagThetaPhi ( mag , (TMath::Pi()/180.)*theta , (TMath::Pi()/180.)*phi);
//                    momentum[1] = N;
//                    OutPutToTextFile(2, momentum , charge ,mass , pid );
//                    RootTree -> Fill();
//                }
//            }
//            
//        }
//    }
//    RootFile -> Write();
//    RootFile -> Close();
//    TextFile.close();
//    OutRunNumberFile.open(runsFilename);
//    OutRunNumberFile << RunNumber << "\n" ;
//    OutRunNumberFile.close();
//    //Printf("\nDont forget:\nDocument run %d in README file! ... ", RunNumber);
//    OutputInfo2File();
    gen_events = new GenerateEvents( Path , RunNumber , 2 );
    TString Type = (fReepp -> IsOn()) ? "(e,e'pp)" : "(e,e'B)";
    bool fDoReeNFromTree = (fReeNFromTree -> IsOn()) ? true : false;
    bool fDoReeNFromDist = (fReeNFromDist->IsOn()) ? true : false;
    bool fDoFlateeN  = (fFlateeN->IsOn()) ? true : false;
    gen_events -> SetLimits( Pmin , Pmax , Thetamin , Thetamax );
    if (Type == "(e,e'pp)") {
        gen_events -> Set_eep_Parameters( SigmaT , SigmaL_a1 , SigmaL_a2 , ShiftL_a1 , ShiftL_a2 );
    }
    else{
        gen_events -> Set_eeN_tree(eeNTree);
        if (fDoReeNFromDist) gen_events -> SetHistThetaHistMag ( histMag , histTheta );
    }
    gen_events -> SetNRand(NRand);
    gen_events -> SetNPTheta(NPTheta);
    gen_events -> DoGenerate( Type , BaryonName , fDoReeNFromTree , fDoReeNFromDist , fDoFlateeN );
    DoDrawGenerated();
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
//void EGgui::SetRootTreeAddresses(){
//    RootTree -> Branch("q3Vector"                    ,"TVector3"     ,&q3Vector);
//    RootTree -> Branch("Pcm"                         ,"TVector3"     ,&Pcm);
//    RootTree -> Branch("Pp1"                         ,"TVector3"     ,&Pp1);
//    RootTree -> Branch("Pp2"                         ,"TVector3"     ,&Pp2);
//    RootTree -> Branch("Pmiss"                       ,"TVector3"     ,&Pmiss);
//    RootTree -> Branch("Precoil"                     ,"TVector3"     ,&Pp2);
//    RootTree -> Branch("q_in_Pmiss_q_system"         ,"TVector3"     ,&q3Vector_in_Pmiss_q_system);
//    RootTree -> Branch("Pmiss_in_Pmiss_q_system"     ,"TVector3"     ,&Pmiss_in_Pmiss_q_system);
//    RootTree -> Branch("Pcm_in_Pmiss_q_system"       ,"TVector3"     ,&Pcm_in_Pmiss_q_system);
//    RootTree -> Branch("q_q_sys"                     ,"TVector3"     ,&q_q_sys);
//    RootTree -> Branch("Pmiss_q_sys"                 ,"TVector3"     ,&Pmiss_q_sys);
//    RootTree -> Branch("Pcm_q_sys"                   ,"TVector3"     ,&Pcm_q_sys);
//    RootTree -> Branch("Rp1"                         ,"TVector3"     ,&Rp1);                      // proton vertex
//    RootTree -> Branch("Rp2"                         ,"TVector3"     ,&Rp2);                      // proton vertex
//    RootTree -> Branch("Q2"                  ,&Q2                    ,"Q2/F");
//    RootTree -> Branch("theta_e"             ,&theta_e               ,"theta_e/F");
//    RootTree -> Branch("Xb"                  ,&Xb                    ,"Xb/F");
//    RootTree -> Branch("ThetaPQ"             ,&ThetaPQ               ,"ThetaPQ/F");              // angle between the leading proton and q
//    RootTree -> Branch("ThetaPmissQ"         ,&ThetaPmissQ           ,"ThetaPmissQ/F");          // angle between the missing momentum and q
//    RootTree -> Branch("ThetaPmissPrecoil"   ,&ThetaPmissPrecoil     ,"ThetaPmissPrecoil/F");    // angle between the missing and recoil momenta
//    RootTree -> Branch("PoverQ"              ,&PoverQ                ,"PoverQ/F");               // ratio |p|/|q| for leading proton
//    RootTree -> Branch("Mmiss"               ,&Mmiss                 ,"Mmiss/F");
//}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void EGgui::DoDrawGenerated(){
    RootFile = new TFile( rootFilename );
    RootTree = (TTree*)RootFile->Get("anaTree");
    fGenLabelData           -> SetText(Form("Generated %lld Events",RootTree->GetEntries()));
    GenerationButtonsFrame  -> Layout();
    
    TCanvas * fCanvas = fEcanvas -> GetCanvas();
    fCanvas     -> cd();
    DoSetDrawString();
    RootTree    -> Draw(DrawString,CutString,OptionString);
    fCanvas     -> Update();
}


//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
//void EGgui::OutputInfo2File(){
//    
//    RunsInfoFileName = Form("%s/eg_txtfiles/RunsInfo.txt",Path.Data());
//    RunsInfoFile.open(RunsInfoFileName,std::ofstream::out | std::ofstream::app);
//
//    RunsInfoFile
//    << RunNumber
//    << "\t" << 1900+dt->tm_year << "/" << dt->tm_mon
//    << "\t\t"  << SigmaT
//    << "\t\t"  << SigmaL_a1 << "\t"  << SigmaL_a2
//    << "\t\t"  << ShiftL_a1 << "\t"  << ShiftL_a2
//    << "\n" ;
//    
//    RunsInfoFile.close();
//}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
//void EGgui::OutPutToTextFile(const int N , TVector3 momentum[] , int charge[N] , float mass[N], int pid[N]){
//    float x = 0 , y  = 0 , z  = 0 , t_off = 0 ;
//    int flag = 0;
//    TextFile << N << std::endl;
//    for (int j = 0 ; j < N ; j++ ){
//        float   p_mag = momentum[j].Mag();
//        float   cx  = momentum[j].x()/p_mag, cy = momentum[j].y()/p_mag  , cz = momentum[j].z()/p_mag ;
//        TextFile << pid[j]  <<" "<< cx      <<" "<< cy  <<" "<< cz      <<" "<< p_mag     <<std::endl;
//        TextFile << mass[j] <<" "<< charge[j]  << std::endl;
//        TextFile << x       <<" "<< y       <<" "<< z   <<" "<< t_off   <<" "<< flag    <<std::endl;
//    }
//}



#endif
