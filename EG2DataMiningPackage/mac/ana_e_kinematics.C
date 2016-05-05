{
    bool    DoScheme = false;
    Float_t    XbMin = 1.05;
    
    Float_t     Px_e , Py_e , Pz_e , E_e , q_x , q_y , q_z , q , omega , Xb;
    TString     Path = "/Users/erezcohen/Desktop/DataMining/EG2_DATA";
    TString FileName = "DATA_Fe56";
    
    if (DoScheme){
        TSchemeDATA *  s = new TSchemeDATA();
        s -> SchemeOnTCut( Path, FileName + ".root" , "T" , FileName + "_XbCut.root", Form("Xb>%f",XbMin));
    }
    
    TPlots *     ana = new TPlots(Path + "/" + FileName + "_XbCut.root","T",Form("e-kinematics for  Xb>%f",XbMin));
    TTree *  in_tree = ana -> GetTree();
    TFile *     file = new TFile("~/Desktop/DataMining/EG2_DATA/eep_kinematics.root","recreate");
    TTree * out_tree = new TTree("e_kinematics_tree",Form("electron kinematics for Xb>%f",XbMin));
    
    in_tree -> SetBranchAddress("Xb"        , &Xb);
    in_tree -> SetBranchAddress("Px_e"      , &Px_e);
    in_tree -> SetBranchAddress("Py_e"      , &Py_e);
    in_tree -> SetBranchAddress("Pz_e"      , &Pz_e);
    in_tree -> SetBranchAddress("Nu"        , &omega);

    out_tree -> Branch("Bjorken x"          , &Xb   , "Xb/F");
    out_tree -> Branch("p(e') - x [GeV/c]"  , &Px_e , "Px_e/F");
    out_tree -> Branch("p(e') - y [GeV/c]"  , &Py_e , "Py_e/F");
    out_tree -> Branch("p(e') - z [GeV/c]"  , &Pz_e , "Pz_e/F");
    out_tree -> Branch("E(e') [GeV]"        , &E_e  , "E_e/F" );
    out_tree -> Branch("q - x [GeV/c]"      , &q_x  , "q_x/F");
    out_tree -> Branch("q - y [GeV/c]"      , &q_y  , "q_y/F");
    out_tree -> Branch("q - z [GeV/c]"      , &q_z  , "q_z/F");
    out_tree -> Branch("|q| [GeV/c]"        , &q    , "q/F" );
    out_tree -> Branch("E-transfer w [GeV]" , &omega, "omega/F" );
    
    for (int i = 0 ; i < in_tree->GetEntries() ; i++){
        in_tree -> GetEntry(i);
        if (i%50000 == 0)
            Printf("\t [%.0f%%]",100*((Float_t)i/in_tree->GetEntries()));
        q_x = -Px_e;
        q_y = -Py_e;
        q_z = 5.009-Pz_e;
        q = sqrt( pow( q_x , 2) + pow( q_y , 2) + pow( q_z , 2) );
        out_tree -> Fill();
    }
    cout << "done filling " << out_tree->GetEntries() << " entries into  " << file->GetName() << "...." << endl;
    out_tree -> Write();
    file -> Close();

}