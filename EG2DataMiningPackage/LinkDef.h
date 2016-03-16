//
// cint script to generate libraries
// Declaire namespace & classes you defined
// #pragma statement: order matters! Google it ;)
//

//
//#ifdef __MAKECINT__
//#pragma link C++ class std::vector<TVector3>+;
//#pragma link C++ class std::vector<TLorentzVector>+;
//#endif


#ifdef __CINT__
#pragma link off all globals;
#pragma link off all classes;
#pragma link off all functions;

#pragma link C++ class TEG2dm+;
#pragma link C++ class TSchemeDATA+;
#pragma link C++ class TCalcPhysVarsEG2+;
//ADD_NEW_CLASS ... do not change this line
#endif


