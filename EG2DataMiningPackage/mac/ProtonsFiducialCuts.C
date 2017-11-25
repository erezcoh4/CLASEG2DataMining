bool ProtonsFiducialCuts(){
    
    
    TFile * file = new TFile("/Users/erezcohen/Desktop/DataMining/AnaFiles/Ana_SRCXb_DATA_C12.root");
    TTree * anaTree = (TTree*)file->Get("anaTree");
    //    TString str_var = "fmod(TMath::RadToDeg()*protonsLab.Phi() - 360,330):TMath::RadToDeg()*protonsLab.Theta()";
    
    TString str_var = "pLab_phi:pLab_theta";
    TCanvas * c = new TCanvas("c","");
    
    //    anaTree->Draw(str_var );
    anaTree -> SetMarkerSize(3);
    anaTree -> SetMarkerStyle(6);
    anaTree->Draw(str_var,"Pmiss.P()>0.3 && Pmiss.P()<1");
    
    anaTree -> SetMarkerColor(kRed);
    //    anaTree->Draw(str_var, "pFiducCut[1]==1" , "same");
    anaTree->Draw(str_var,"pFiducCut[1]==1 && Pmiss.P()>0.3 && Pmiss.P()<1","same");

    anaTree -> SetMarkerColor(kGreen);
    //    anaTree->Draw(str_var, "pFiducCut[1]==1 && Xb>1" , "same");
//    anaTree->Draw(str_var,"Xb>1 && pFiducCut[1]==1 && Pmiss.P()>0.3 && Pmiss.P()<1","same");

//    c->GetXaxis()->SetTitle("#theta_{p} [deg.]");
//    c->GetYaxis()->SetTitle("#phi_{p} [deg.]");
    c->SaveAs("ProtonFiducialCuts.png");
    
    return true;
}