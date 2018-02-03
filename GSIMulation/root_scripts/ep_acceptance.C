/// usage:
// ======
// root -l ep_acceptance.C\(\2000,2\)
//



// support
Double_t ChangePhiToPhiLab(Double_t Phi) { // change the axis with phi angle (-180,180) to sit in (-30,330)
    return ( (Phi < -30.) ? (Phi + 360.) : ( (Phi > 330.) ? (Phi - 360.) : Phi ) );
}

// main functionality
bool ep_acceptance(int gsim_run=2000,int debug=2){
    
    TFile * f = new TFile(Form("/Users/erezcohen/Desktop/DataMining/GSIM_DATA/GSIMulationOutput_run%d.root",gsim_run));
    TTree * t = (TTree*)f->Get("data");
    int Nevents = t->GetEntries();
    if (debug>1) {t->Print();}
    cout << "Nevents = " << Nevents << endl;
    
    
    std::vector<int> event_numbers;
    std::vector<float> Prec_phi_g;
    std::vector<int> N_generated_in_event;
    std::vector<int> e_accepted_in_event;
    std::vector<int> ep_accepted_in_event;
    
    
    
    
    Int_t   Id_g[2], Id[2]; // Id[0]==1 means that a 'good' electron is accepted in this event
    Int_t   Number_g, Number;
    Float_t phi_g[2], phi[2];
    Float_t p_g[2], p[2];
    Float_t theta_g[2], theta[2];
    
    t->SetBranchAddress("Number_g"      , &Number_g);
    t->SetBranchAddress("Phi_g"         , &phi_g);
    t->SetBranchAddress("Momentum_g"    , &p_g);
    t->SetBranchAddress("Theta_g"       , &theta_g);
    t->SetBranchAddress("particle_g"    , &Id_g);
    
    t->SetBranchAddress("Number"        , &Number);
    t->SetBranchAddress("Phi"           , &phi);
    t->SetBranchAddress("Momentum"      , &p);
    t->SetBranchAddress("Theta"         , &theta);
    t->SetBranchAddress("particle"      , &Id);

    ofstream output_data_file;
    output_data_file.open(Form("/Users/erezcohen/Desktop/DataMining/GSIM_DATA/csv_files/output_data_run%d.csv",gsim_run));
    output_data_file
    << "Number_g" << ","
    << "Number" << ","
    << "Id_0_g" << ","
    << "Id_0" << ","
    << "Id_1_g" << ","
    << "Id_1" << ","

    << "Pe_P_g" << ","
    << "Pe_theta_g" << ","
    << "Pe_phi_g" << ","
    << "Prec_P_g" << ","
    << "Prec_theta_g" << ","
    << "Prec_phi_g" << ","
    << "Pe_P" << ","
    << "Pe_theta" << ","
    << "Pe_phi" << ","
    << "Prec_P" << ","
    << "Prec_theta" << ","
    << "Prec_phi"
    << endl;

    
    Int_t i_event_phi_g_Precoil=0;
    
    for (int event=0; event < Nevents; event++) {
        
        // initialize
        Id_g[0] = Id_g[1] = -9999;
        Id[0] = Id[1] = -9999;
        phi_g[0] = phi_g[1] = -9999;
        phi[0] = phi[1] = -9999;
        p_g[0] = p_g[1] = -9999;
        p[0] = p[1] = -9999;
        theta_g[0] = theta_g[1] = -9999;
        theta[0] = theta[1] = -9999;
        
        
        // get entry
        t -> GetEntry(event);
        
        // output to csv
        output_data_file
        << Number_g << ","
        << Number << ","
        << Id_g[0] << ","
        << Id[0] << ","
        << Id_g[1] << ","
        << Id[1] << ","
        
        << p_g[0] << ","
        << theta_g[0] << ","
        << ChangePhiToPhiLab(phi_g[0]) << ","
        << p_g[1] << ","
        << theta_g[1] << ","
        << ChangePhiToPhiLab(phi_g[1]) << ","
        << p[0] << ","
        << theta[0] << ","
        << ChangePhiToPhiLab(phi[0]) << ","
        << p[1] << ","
        << theta[1] << ","
        << ChangePhiToPhiLab(phi[1])
        << endl;

        float current_Prec_phi_g = phi_g[1];
        int current_event_number = -1;
        bool current_Prec_phi_g_exist = false;
        if (debug>2) {
            cout << "event_numbers.size(): "<< event_numbers.size() << endl;
        }
        
        for (int i_event_number=0; i_event_number<event_numbers.size(); i_event_number++) {

            if ( current_Prec_phi_g == Prec_phi_g.at(i_event_number) ) {
                current_event_number = i_event_number;
                current_Prec_phi_g_exist = true;
                N_generated_in_event.at(i_event_number) += 1;
                // if we found it - what is the acceptance for this recoil proton
                if (Id[0]==1) { // only if the first particle is a 'good' electron this particle is accepted
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
        
        if (debug>2) { cout << "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" << endl;        }

    }
    
    ofstream output_Prec_events_file;
    output_Prec_events_file.open(Form("/Users/erezcohen/Desktop/DataMining/GSIM_DATA/csv_files/output_Prec_events_run%d.csv",gsim_run));
    output_Prec_events_file
    << "event" << ","
    << "Prec_phi_g" << ","
    << "N_generated_in_event" << ","
    << "e_accepted_in_event" << ","
    << "ep_accepted_in_event" << endl;
    
    for (int i_event_number=0; i_event_number<event_numbers.size(); i_event_number++) {
        if (debug>2) {
            cout << "event number " << event_numbers.at(i_event_number) << endl;
            cout << "Prec_phi_g.at("<<i_event_number<<"): " << Prec_phi_g.at(i_event_number) << endl;
            cout << "N_generated_in_event("<<i_event_number<<"): " << N_generated_in_event.at(i_event_number) << endl;
            cout << "e_accepted_in_event("<<i_event_number<<"): " << e_accepted_in_event.at(i_event_number) << endl;
            cout << "ep_accepted_in_event("<<i_event_number<<"): " << ep_accepted_in_event.at(i_event_number) << endl;
        }
        
        output_Prec_events_file
        << event_numbers.at(i_event_number) << ","
        << Prec_phi_g.at(i_event_number) << ","
        << N_generated_in_event.at(i_event_number) << ","
        << e_accepted_in_event.at(i_event_number) << ","
        << ep_accepted_in_event.at(i_event_number) << endl;
       
    }
    
    
    
    output_Prec_events_file.close();
    output_data_file.close();
    
    cout << "done." << endl;
    gROOT->ProcessLine(".q");
    return true;
}


