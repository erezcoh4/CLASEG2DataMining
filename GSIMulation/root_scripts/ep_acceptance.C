bool ep_acceptance(int debug=2){
    
    TFile * f = new TFile("/Users/erezcohen/Desktop/DataMining/GSIM_DATA/GSIMulationOutput_run2000.root");
    TTree * t = (TTree*)f->Get("data");
    int Nevents = t->GetEntries();
    if (debug>2) {t->Print();}
    cout << "Nevents = " << Nevents << endl;
    
    
    std::vector<int> event_numbers;
    std::vector<float> Prec_phi_g;
    std::vector<int> N_generated_in_event;
    std::vector<int> e_accepted_in_event;
    std::vector<int> ep_accepted_in_event;
    
    
    
    
    Float_t phi_g[2], phi[2];
    Int_t   Number_g, Number;
    t->SetBranchAddress("Number_g"      , &Number_g);
    t->SetBranchAddress("Phi_g"         , &phi_g);
    t->SetBranchAddress("Number"        , &Number);
    t->SetBranchAddress("Phi"           , &phi);
    
    Int_t i_event_phi_g_Precoil=0;
    
    for (int event=0; event < Nevents; event++) {
        t -> GetEntry(event);
        
        
        float current_Prec_phi_g = phi_g[1];
        int current_event_number = -1;
        bool current_Prec_phi_g_exist = false;
        //        cout << "event_numbers.size(): "<< event_numbers.size() << endl;
        
        for (int i_event_number=0; i_event_number<event_numbers.size(); i_event_number++) {
            // check if we can find the Prec in our event list
            //            cout << "current_Prec_phi_g: "<< current_Prec_phi_g<< ",Prec_phi_g.at(i_event_number): " << Prec_phi_g.at(i_event_number) << endl;
            if ( current_Prec_phi_g == Prec_phi_g.at(i_event_number) ) {
                current_event_number = i_event_number;
                current_Prec_phi_g_exist = true;
                N_generated_in_event.at(i_event_number) += 1;
                // if we found it - what is the acceptance for this recoil proton
                if (Number>0) {
                    e_accepted_in_event.at(i_event_number) += 1;
                    if (Number>1) {
                        ep_accepted_in_event.at(i_event_number) += 1;
                    }
                }
            }
        }
        // if we can not find the Prec in our event list we create a new event
        if (current_Prec_phi_g_exist == false) {
            event_numbers.push_back( event_numbers.size() );
            Prec_phi_g.push_back( current_Prec_phi_g );
            e_accepted_in_event.push_back( 0 );
            ep_accepted_in_event.push_back( 0 );
            N_generated_in_event.push_back( 1 );
        }
        
        
//        cout << "event_phi_g_Precoil:" << event_phi_g_Precoil << endl;
//        cout << "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" << endl;

    }
    
    ofstream outputfile;
    outputfile.open("output.csv");
    outputfile
    << "event" << ","
    << "Prec_phi_g" << ","
    << "N_generated_in_event" << ","
    << "e_accepted_in_event" << ","
    << "ep_accepted_in_event" << endl;
    
    for (int i_event_number=0; i_event_number<event_numbers.size(); i_event_number++) {
        cout << "event number " << event_numbers.at(i_event_number) << endl;
        cout << "Prec_phi_g.at("<<i_event_number<<"): " << Prec_phi_g.at(i_event_number) << endl;
        cout << "N_generated_in_event("<<i_event_number<<"): " << N_generated_in_event.at(i_event_number) << endl;
        cout << "e_accepted_in_event("<<i_event_number<<"): " << e_accepted_in_event.at(i_event_number) << endl;
        cout << "ep_accepted_in_event("<<i_event_number<<"): " << ep_accepted_in_event.at(i_event_number) << endl;
        
        outputfile
        << event_numbers.at(i_event_number) << ","
        << Prec_phi_g.at(i_event_number) << ","
        << N_generated_in_event.at(i_event_number) << ","
        << e_accepted_in_event.at(i_event_number) << ","
        << ep_accepted_in_event.at(i_event_number) << endl;
       
    }
    
    
    
    outputfile.close();
    
    cout << "done." << endl;
    gROOT->ProcessLine(".q");
    return true;
}