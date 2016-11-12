

// globals
TAnalysisEG2 * ana  = new TAnalysisEG2( "ppSRC_DATA_C12" );





// main function
void SRCcuts(int A = 12){
    
    bool Do2pSRCCuts = true;
 

 

    //....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
    if(Do2pSRCCuts){ // Mar-17, 2016
        TCanvas * c2pSRC = ana -> CreateCanvas("leading proton","Divide",4,2);

        ana -> DrawVarAnd2pSRCCut(c2pSRC , 1 , "p_over_q"   , 50 , 0.2 , 1  ,"p/q","p/q");
        ana -> DrawVarAnd2pSRCCut(c2pSRC , 2 , "theta_pq"   , 50 , 0   , 50,"#theta (p,q)","#theta (p,q) [deg.]");
        ana -> DrawVarAnd2pSRCCut(c2pSRC , 3 , "Pmiss.P()"  , 50 , 0.2 , 1.1  ,"#vec{p}(miss) = #vec{p}(lead) - #vec{q}","p(miss) [GeV/c]");
        ana -> DrawVarAnd2pSRCCut(c2pSRC , 4 , "Xb"         , 50 , 1  , 2.5,"Bjorken x","x");
        ana -> DrawVarAnd2pSRCCut(c2pSRC , 5 , "Mmiss"      , 50 , 0.2 , 1.5  ,"missing mass of (e,e'p) reaction","M(miss) [GeV/c ^{2}]");
        ana -> DrawVarAnd2pSRCCut(c2pSRC , 6 , "Prec.P()"   , 50 , 0.2 , 1.5  ,"recoil proton momentum","p(rec) [GeV/c]");
        ana -> Draw2DVarAnd2pSRCCut(c2pSRC , 7 , "p_over_q"   , "theta_pq"   , 50 , 0.2 , 1 , 50 , 0 , 50  ,"#theta (p,q) vs. p/q","p/q","#theta (p,q) [deg.]");

    }
    
    Printf("total number of events for C12 is %d",(int)ana->GetEntries(ana->ppSRCCut));
    
   
}

