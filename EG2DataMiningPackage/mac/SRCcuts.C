

// globals
TAnalysisEG2 * ana  = new TAnalysisEG2( "ppSRC_DATA_C12" );
TCut ppSRCCut = " (1.2<=Xb)  &&  (2<=Np)  &&   (0.62<p_over_q && p_over_q<0.96)  &&   (theta_pq<25)  &&  (0.3<Pmiss.P() && Pmiss.P()<1.)";
TCanvas  * c2pSRC , * c3pSRC;





// main function
void SRCcuts(int A = 12){
    
    bool Do2pSRCCuts = true;
 

 

    //....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
    if(Do2pSRCCuts){ // Mar-17, 2016
        TCut cut = "";
        c2pSRC = ana -> CreateCanvas("leading proton","Divide",3,2);
        
        DrawVarAnd2pSRCCut(1 , "p_over_q"   , 50 , 0.2 , 1  ,"p/q","p/q");
        DrawVarAnd2pSRCCut(2 , "theta_pq"   , 50 , 0   , 50,"#theta (p,q)","#theta (p,q) [deg.]");
        DrawVarAnd2pSRCCut(3 , "Pmiss.P()"  , 50 , 0.2 , 1.1  ,"#vec{p}(miss) = #vec{p}(lead) - #vec{q}","p(miss) [GeV/c]");
        DrawVarAnd2pSRCCut(4 , "Xb"         , 50 , 1  , 2.5,"Bjorken x","x");
        DrawVarAnd2pSRCCut(5 , "Mmiss"      , 50 , 0.2 , 1.5  ,"missing mass of (e,e'p) reaction","M(miss) [GeV/c ^{2}]");
        DrawVarAnd2pSRCCut(6 , "p_over_q"   , "theta_pq"   , 50 , 0.2 , 1 , 50 , 0 , 50  ,"#theta (p,q) vs. p/q","p/q","#theta (p,q) [deg.]");

    }
    
   
}



void DrawVarAnd2pSRCCut(int i , TString var , int NbinsX , float Xmin , float Xmax , TString Title , TString XTitle){
    c2pSRC -> cd(i);
    ana -> H1(var,"","",NbinsX,Xmin,Xmax,Title,XTitle,"",1,0);
    ana -> H1(var,ppSRCCut,"same",NbinsX,Xmin,Xmax,Title,XTitle,"",1,46);
}




void DrawVarAnd2pSRCCut(int i , TString varX , TString varY
                        , int NbinsX , float Xmin , float Xmax
                        , int NbinsY , float Ymin , float Ymax
                        , TString Title , TString XTitle , TString YTitle ){
    c2pSRC -> cd(i);
    ana -> H2(varX, varY,"","",NbinsX,Xmin,Xmax,NbinsY,Ymin,Ymax,Title,XTitle,YTitle);
    ana -> H2(varX, varY,ppSRCCut,"colz same",NbinsX,Xmin,Xmax,NbinsY,Ymin,Ymax,Title,XTitle,YTitle);
}
