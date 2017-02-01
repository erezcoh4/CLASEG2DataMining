/**
 * \file EGgui.h
 *
 * \ingroup GSIMulation
 * 
 * \brief Class def header for a class EGgui
 *
 * @author erezcohen
 */

/** \addtogroup GSIMulation

    @{*/
#ifndef EGGUI_H
#define EGGUI_H

#include "GenerateEvents.h"

/**
   \class EGgui
   User defined class EGgui ... these comments are used to generate
   doxygen documentation!
 */
class EGgui{

    RQ_OBJECT("TEGGUI")
    
    
private:
    
    TGMainFrame         * fMain;
    TRootEmbeddedCanvas * fEcanvas;
    
public:
    
    // constructors
    EGgui ( const TGWindow *p,UInt_t w,UInt_t h );
    virtual ~EGgui ();
    
    // Physical variables
    TLorentzVector                              Proton                  ,   q4Vector        , m2N       , miss;
    Float_t  Q2                         ,       Xb                      ,   PoverQ          ,    Mmiss;
    Float_t  ThetaPQ                    ,       theta_miss_q             ,   ThetaPmissPrecoil;
    Float_t  Mott                       ,       DipoleFF                ,   Weight;
    Float_t  theta_e;
    TVector3 e                          ,       Pp1                     ,   Pp2             , Precoil;
    TVector3 Rp1                        ,       Rp2;                                                    // proton vertex
    TVector3 q3Vector                   ,       Pcm                     ,   Pmiss;
    TVector3 q3Vector_in_Pmiss_q_system ,       Pmiss_in_Pmiss_q_system ,   Pcm_in_Pmiss_q_system;
    TVector3 q_q_sys                    ,       Pmiss_q_sys             ,   Pcm_q_sys;
    TRandom3 * gRandom;
    GenerateEvents * gen_events;

    // Globals
    TString             FileName;
    TString             eeNTreeName;
    ifstream            InRunNumberFile;
    ofstream            OutRunNumberFile;
    ofstream            TextFile;
    ofstream            RunsInfoFile;

    TFile             * RootFile;
    TTree             * RootTree;
    TChain            * InputT;
    TTree             * eeNTree;
    TPlots              plot;
    int                 Nentries;
    
    
    
    TString             BaryonName , RunsInfoFileName;
    TString             Path , rootFilename , txtFilename , runsFilename;
    
    time_t  now ;
    tm      * dt;
    
    // Main funcionality
    TGHorizontalFrame * fMainButtonsFrame;
    TGGroupFrame      * RunNumberFrame;
    TGNumberEntry     * fRun;
    int                 RunNumber;
    
    
    
    
    
    // (e,e'pp)
    TGHorizontalFrame * eeppButtonsFrame;
    TGRadioButton     * fReepp;           // generate (e,e'pp) from (e,e'p)
    
    TGGroupFrame      * SigmaTFrame;
    TGNumberEntry     * fSigmaT;
    float               SigmaT;
    TGGroupFrame      * SigmaLFrame;
    TGNumberEntry     * fSigmaL_a1;
    float               SigmaL_a1;
    TGNumberEntry     * fSigmaL_a2;
    float               SigmaL_a2;
    TGGroupFrame      * ShiftLFrame;
    TGNumberEntry     * fShiftL_a1;
    float               ShiftL_a1;
    TGNumberEntry     * fShiftL_a2;
    float               ShiftL_a2;
    
    // (e,e')
    TGHorizontalFrame * eeButtonsFrame;
    TGRadioButton     * fRee;               // generate (e,e')
    TGRadioButton     * fFlatee;
    
    int                 NeTheta;
    TGGroupFrame      * NeThetaFrame;
    TGNumberEntry     * fNeTheta;
    TGHorizontalFrame * FlateeFrame;
    
    
    // (e,e'N)
    TGHorizontalFrame * eeNButtonsFrame;
    TGRadioButton     * fReeN;              // generate (e,e'N)
    TGRadioButton     * fReeDelta;          // generate (e,e'𝚫)
    TGRadioButton     * fReep;
    TGRadioButton     * fReen;
    TGRadioButton     * fFlateeN;
    TGRadioButton     * fReeNFromDist;
    TGRadioButton     * fReeNFromTree;
    
    int                 NPTheta;
    TGGroupFrame      * NPThetaFrame;
    TGNumberEntry     * fNPTheta;
    
    
    
    
    TGHorizontalFrame * GenerationButtonsFrame;
    int                 NRand;
    TGGroupFrame      * NRandFrame;
    TGNumberEntry     * fNRand;
    int                 NFiles;
    TGNumberEntry     * fNFiles;
    int                 Nevents;
    TGLabel          *  fGenLabelData;
    TGTextEntry      *  fDrawString;
    TString             DrawString;
    TGTextEntry      *  fCutString;
    TString             CutString;
    TGTextEntry      *  fOptionString;
    TString             OptionString;
    
    
    TGHorizontalFrame * FlateeNFrame;
    TGGroupFrame      * PminPmaxFrame;
    TGNumberEntry     * fPmin;
    float               Pmin;
    TGNumberEntry     * fPmax;
    float               Pmax;
    TGGroupFrame      * ThetaminThetamaxFrame;
    TGNumberEntry     * fThetamin;
    float               Thetamin;
    TGNumberEntry     * fThetamax;
    float               Thetamax;
    
    
    TGHorizontalFrame * eeNFromDistributionsFrame;
    TGFileDialog      * eeNInFileDialog;
    TGTextEntry       * fMagHistName;
    TGTextEntry       * fThetaHistName;
    TString             InFileName;
    TString             MagHistName;
    TString             ThetaHistName;
    TH1F              * histMag;
    TH1F              * histTheta;
    
    
    
    TGHorizontalFrame * eeNFromTreeFrame;
    TGFileDialog      * eeNTreeInFileDialog;
    TGTextEntry       * fTreeName;
    
    
    
    
    
    
    
    
    
    // methods
    void AddEmbeddedCanvas          ();
    void SetGlobals                 ();
    void SetBinning                 ();
    void MapMainFrame               ();

    void AddMainButtonsFrame        ();
    void AddeeppButtonsFrame        ();
    void AddeeNButtonsFrame         ();
    void AddGenerationButtonsFrame  ();

    void Do_eepp                    ();
    void Do_eeN                     ();
    void Do_eeDelta                 ();
    void Do_een                     ();
    void Do_eep                     ();
    void DoSetBaryonName            ();
    
    
    
    void AddSigmaTFrame             (TGHorizontalFrame * );
    void DoSetSigmaT                ();
    void AddSigmaLFrame             (TGHorizontalFrame * );
    void DoSetSigmaL                ();
    void AddShiftLFrame             (TGHorizontalFrame * );
    void DoSetShiftL                ();
    
    
    void DoFlateeN                  ();
    void DoeeNFromDist              ();
    void DoeeNFromTree              ();
    
    
    
    void AddRunNumberFrame          ( TGHorizontalFrame * );
    void DoSetRun                   ();
    void DoExit                     ();
    
    
    void AddNRandFrame              ( TGHorizontalFrame * );
    void DoSetNRand                 ();
    
    void DoGenMCFiles               ();
    void DoGenerate                 ();

    void DoDrawGenerated            ();
    void DoSetDrawString            ();
    
    
    void AddeeNFromDistributions    ();
    void AddeeNFromTree             ();
    void DoSetPminPmax              ();
    void DoSetThetaminThetamax      ();
    void DoSetNPtheta               ();
    void AddFlateeNRanges           ();
    
    void OpenInFileDialog           ();
    void OpeneeNTreeInFileDialog    ();
    void DoSetInHistNames           ();
    void DoSeteeNTreeName           ();
    void AddTextButton              ( TGHorizontalFrame *, TString , TString );

    
    void Do_ee                      ();
    void DoFlatee                   ();
    void AddeeButtonsFrame          ();
    void DoSetNetheta               ();
    void AddFlateeRanges            ();
};

#endif
/** @} */ // end of doxygen group 

