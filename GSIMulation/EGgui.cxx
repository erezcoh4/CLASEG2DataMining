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
    gen_events = new GenerateEvents( Path , RunNumber , 2 );
    TString Type = (fReepp -> IsOn()) ? "(e,e'pp)" : "(e,e'B)";
    bool fDoReeNFromTree = (fReeNFromTree -> IsOn()) ? true : false;
    bool fDoReeNFromDist = (fReeNFromDist->IsOn()) ? true : false;
    bool fDoFlateeN  = (fFlateeN->IsOn()) ? true : false;
    gen_events -> SetLimits( Pmin , Pmax , Thetamin , Thetamax );
    if (Type == "(e,e'pp)") {
        gen_events -> Set_eep_Parameters( 0 , 0 , SigmaT , SigmaT , SigmaL_a1 , SigmaL_a2 , ShiftL_a1 , ShiftL_a2 );
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



#endif
