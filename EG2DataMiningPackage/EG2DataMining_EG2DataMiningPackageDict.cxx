// Do NOT change. Changes will be lost next time file is generated

#define R__DICTIONARY_FILENAME EG2DataMining_EG2DataMiningPackageDict

/*******************************************************************/
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <assert.h>
#define G__DICTIONARY
#include "RConfig.h"
#include "TClass.h"
#include "TDictAttributeMap.h"
#include "TInterpreter.h"
#include "TROOT.h"
#include "TBuffer.h"
#include "TMemberInspector.h"
#include "TInterpreter.h"
#include "TVirtualMutex.h"
#include "TError.h"

#ifndef G__ROOT
#define G__ROOT
#endif

#include "RtypesImp.h"
#include "TIsAProxy.h"
#include "TFileMergeInfo.h"
#include <algorithm>
#include "TCollectionProxyInfo.h"
/*******************************************************************/

#include "TDataMember.h"

// Since CINT ignores the std namespace, we need to do so in this file.
namespace std {} using namespace std;

// Header files passed as explicit arguments
#include "T3pSimulation.h"
#include "TAnalysisEG2.h"
#include "TCalcPhysVarsEG2.h"
#include "TEG2dm.h"
#include "TSchemeDATA.h"

// Header files passed via #pragma extra_include

namespace ROOT {
   static TClass *TEG2dm_Dictionary();
   static void TEG2dm_TClassManip(TClass*);
   static void *new_TEG2dm(void *p = 0);
   static void *newArray_TEG2dm(Long_t size, void *p);
   static void delete_TEG2dm(void *p);
   static void deleteArray_TEG2dm(void *p);
   static void destruct_TEG2dm(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::TEG2dm*)
   {
      ::TEG2dm *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(::TEG2dm));
      static ::ROOT::TGenericClassInfo 
         instance("TEG2dm", "TEG2dm.h", 31,
                  typeid(::TEG2dm), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &TEG2dm_Dictionary, isa_proxy, 4,
                  sizeof(::TEG2dm) );
      instance.SetNew(&new_TEG2dm);
      instance.SetNewArray(&newArray_TEG2dm);
      instance.SetDelete(&delete_TEG2dm);
      instance.SetDeleteArray(&deleteArray_TEG2dm);
      instance.SetDestructor(&destruct_TEG2dm);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::TEG2dm*)
   {
      return GenerateInitInstanceLocal((::TEG2dm*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_(Init) = GenerateInitInstanceLocal((const ::TEG2dm*)0x0); R__UseDummy(_R__UNIQUE_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *TEG2dm_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal((const ::TEG2dm*)0x0)->GetClass();
      TEG2dm_TClassManip(theClass);
   return theClass;
   }

   static void TEG2dm_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   static TClass *TSchemeDATA_Dictionary();
   static void TSchemeDATA_TClassManip(TClass*);
   static void *new_TSchemeDATA(void *p = 0);
   static void *newArray_TSchemeDATA(Long_t size, void *p);
   static void delete_TSchemeDATA(void *p);
   static void deleteArray_TSchemeDATA(void *p);
   static void destruct_TSchemeDATA(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::TSchemeDATA*)
   {
      ::TSchemeDATA *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(::TSchemeDATA));
      static ::ROOT::TGenericClassInfo 
         instance("TSchemeDATA", "TSchemeDATA.h", 26,
                  typeid(::TSchemeDATA), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &TSchemeDATA_Dictionary, isa_proxy, 4,
                  sizeof(::TSchemeDATA) );
      instance.SetNew(&new_TSchemeDATA);
      instance.SetNewArray(&newArray_TSchemeDATA);
      instance.SetDelete(&delete_TSchemeDATA);
      instance.SetDeleteArray(&deleteArray_TSchemeDATA);
      instance.SetDestructor(&destruct_TSchemeDATA);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::TSchemeDATA*)
   {
      return GenerateInitInstanceLocal((::TSchemeDATA*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_(Init) = GenerateInitInstanceLocal((const ::TSchemeDATA*)0x0); R__UseDummy(_R__UNIQUE_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *TSchemeDATA_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal((const ::TSchemeDATA*)0x0)->GetClass();
      TSchemeDATA_TClassManip(theClass);
   return theClass;
   }

   static void TSchemeDATA_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   static TClass *TCalcPhysVarsEG2_Dictionary();
   static void TCalcPhysVarsEG2_TClassManip(TClass*);
   static void *new_TCalcPhysVarsEG2(void *p = 0);
   static void *newArray_TCalcPhysVarsEG2(Long_t size, void *p);
   static void delete_TCalcPhysVarsEG2(void *p);
   static void deleteArray_TCalcPhysVarsEG2(void *p);
   static void destruct_TCalcPhysVarsEG2(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::TCalcPhysVarsEG2*)
   {
      ::TCalcPhysVarsEG2 *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(::TCalcPhysVarsEG2));
      static ::ROOT::TGenericClassInfo 
         instance("TCalcPhysVarsEG2", "TCalcPhysVarsEG2.h", 28,
                  typeid(::TCalcPhysVarsEG2), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &TCalcPhysVarsEG2_Dictionary, isa_proxy, 4,
                  sizeof(::TCalcPhysVarsEG2) );
      instance.SetNew(&new_TCalcPhysVarsEG2);
      instance.SetNewArray(&newArray_TCalcPhysVarsEG2);
      instance.SetDelete(&delete_TCalcPhysVarsEG2);
      instance.SetDeleteArray(&deleteArray_TCalcPhysVarsEG2);
      instance.SetDestructor(&destruct_TCalcPhysVarsEG2);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::TCalcPhysVarsEG2*)
   {
      return GenerateInitInstanceLocal((::TCalcPhysVarsEG2*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_(Init) = GenerateInitInstanceLocal((const ::TCalcPhysVarsEG2*)0x0); R__UseDummy(_R__UNIQUE_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *TCalcPhysVarsEG2_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal((const ::TCalcPhysVarsEG2*)0x0)->GetClass();
      TCalcPhysVarsEG2_TClassManip(theClass);
   return theClass;
   }

   static void TCalcPhysVarsEG2_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   static TClass *TAnalysisEG2_Dictionary();
   static void TAnalysisEG2_TClassManip(TClass*);
   static void *new_TAnalysisEG2(void *p = 0);
   static void *newArray_TAnalysisEG2(Long_t size, void *p);
   static void delete_TAnalysisEG2(void *p);
   static void deleteArray_TAnalysisEG2(void *p);
   static void destruct_TAnalysisEG2(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::TAnalysisEG2*)
   {
      ::TAnalysisEG2 *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(::TAnalysisEG2));
      static ::ROOT::TGenericClassInfo 
         instance("TAnalysisEG2", "TAnalysisEG2.h", 26,
                  typeid(::TAnalysisEG2), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &TAnalysisEG2_Dictionary, isa_proxy, 4,
                  sizeof(::TAnalysisEG2) );
      instance.SetNew(&new_TAnalysisEG2);
      instance.SetNewArray(&newArray_TAnalysisEG2);
      instance.SetDelete(&delete_TAnalysisEG2);
      instance.SetDeleteArray(&deleteArray_TAnalysisEG2);
      instance.SetDestructor(&destruct_TAnalysisEG2);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::TAnalysisEG2*)
   {
      return GenerateInitInstanceLocal((::TAnalysisEG2*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_(Init) = GenerateInitInstanceLocal((const ::TAnalysisEG2*)0x0); R__UseDummy(_R__UNIQUE_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *TAnalysisEG2_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal((const ::TAnalysisEG2*)0x0)->GetClass();
      TAnalysisEG2_TClassManip(theClass);
   return theClass;
   }

   static void TAnalysisEG2_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   static TClass *T3pSimulation_Dictionary();
   static void T3pSimulation_TClassManip(TClass*);
   static void *new_T3pSimulation(void *p = 0);
   static void *newArray_T3pSimulation(Long_t size, void *p);
   static void delete_T3pSimulation(void *p);
   static void deleteArray_T3pSimulation(void *p);
   static void destruct_T3pSimulation(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::T3pSimulation*)
   {
      ::T3pSimulation *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(::T3pSimulation));
      static ::ROOT::TGenericClassInfo 
         instance("T3pSimulation", "T3pSimulation.h", 25,
                  typeid(::T3pSimulation), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &T3pSimulation_Dictionary, isa_proxy, 4,
                  sizeof(::T3pSimulation) );
      instance.SetNew(&new_T3pSimulation);
      instance.SetNewArray(&newArray_T3pSimulation);
      instance.SetDelete(&delete_T3pSimulation);
      instance.SetDeleteArray(&deleteArray_T3pSimulation);
      instance.SetDestructor(&destruct_T3pSimulation);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::T3pSimulation*)
   {
      return GenerateInitInstanceLocal((::T3pSimulation*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_(Init) = GenerateInitInstanceLocal((const ::T3pSimulation*)0x0); R__UseDummy(_R__UNIQUE_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *T3pSimulation_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal((const ::T3pSimulation*)0x0)->GetClass();
      T3pSimulation_TClassManip(theClass);
   return theClass;
   }

   static void T3pSimulation_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   // Wrappers around operator new
   static void *new_TEG2dm(void *p) {
      return  p ? new(p) ::TEG2dm : new ::TEG2dm;
   }
   static void *newArray_TEG2dm(Long_t nElements, void *p) {
      return p ? new(p) ::TEG2dm[nElements] : new ::TEG2dm[nElements];
   }
   // Wrapper around operator delete
   static void delete_TEG2dm(void *p) {
      delete ((::TEG2dm*)p);
   }
   static void deleteArray_TEG2dm(void *p) {
      delete [] ((::TEG2dm*)p);
   }
   static void destruct_TEG2dm(void *p) {
      typedef ::TEG2dm current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::TEG2dm

namespace ROOT {
   // Wrappers around operator new
   static void *new_TSchemeDATA(void *p) {
      return  p ? new(p) ::TSchemeDATA : new ::TSchemeDATA;
   }
   static void *newArray_TSchemeDATA(Long_t nElements, void *p) {
      return p ? new(p) ::TSchemeDATA[nElements] : new ::TSchemeDATA[nElements];
   }
   // Wrapper around operator delete
   static void delete_TSchemeDATA(void *p) {
      delete ((::TSchemeDATA*)p);
   }
   static void deleteArray_TSchemeDATA(void *p) {
      delete [] ((::TSchemeDATA*)p);
   }
   static void destruct_TSchemeDATA(void *p) {
      typedef ::TSchemeDATA current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::TSchemeDATA

namespace ROOT {
   // Wrappers around operator new
   static void *new_TCalcPhysVarsEG2(void *p) {
      return  p ? new(p) ::TCalcPhysVarsEG2 : new ::TCalcPhysVarsEG2;
   }
   static void *newArray_TCalcPhysVarsEG2(Long_t nElements, void *p) {
      return p ? new(p) ::TCalcPhysVarsEG2[nElements] : new ::TCalcPhysVarsEG2[nElements];
   }
   // Wrapper around operator delete
   static void delete_TCalcPhysVarsEG2(void *p) {
      delete ((::TCalcPhysVarsEG2*)p);
   }
   static void deleteArray_TCalcPhysVarsEG2(void *p) {
      delete [] ((::TCalcPhysVarsEG2*)p);
   }
   static void destruct_TCalcPhysVarsEG2(void *p) {
      typedef ::TCalcPhysVarsEG2 current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::TCalcPhysVarsEG2

namespace ROOT {
   // Wrappers around operator new
   static void *new_TAnalysisEG2(void *p) {
      return  p ? new(p) ::TAnalysisEG2 : new ::TAnalysisEG2;
   }
   static void *newArray_TAnalysisEG2(Long_t nElements, void *p) {
      return p ? new(p) ::TAnalysisEG2[nElements] : new ::TAnalysisEG2[nElements];
   }
   // Wrapper around operator delete
   static void delete_TAnalysisEG2(void *p) {
      delete ((::TAnalysisEG2*)p);
   }
   static void deleteArray_TAnalysisEG2(void *p) {
      delete [] ((::TAnalysisEG2*)p);
   }
   static void destruct_TAnalysisEG2(void *p) {
      typedef ::TAnalysisEG2 current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::TAnalysisEG2

namespace ROOT {
   // Wrappers around operator new
   static void *new_T3pSimulation(void *p) {
      return  p ? new(p) ::T3pSimulation : new ::T3pSimulation;
   }
   static void *newArray_T3pSimulation(Long_t nElements, void *p) {
      return p ? new(p) ::T3pSimulation[nElements] : new ::T3pSimulation[nElements];
   }
   // Wrapper around operator delete
   static void delete_T3pSimulation(void *p) {
      delete ((::T3pSimulation*)p);
   }
   static void deleteArray_T3pSimulation(void *p) {
      delete [] ((::T3pSimulation*)p);
   }
   static void destruct_T3pSimulation(void *p) {
      typedef ::T3pSimulation current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::T3pSimulation

namespace ROOT {
   static TClass *vectorlEintgR_Dictionary();
   static void vectorlEintgR_TClassManip(TClass*);
   static void *new_vectorlEintgR(void *p = 0);
   static void *newArray_vectorlEintgR(Long_t size, void *p);
   static void delete_vectorlEintgR(void *p);
   static void deleteArray_vectorlEintgR(void *p);
   static void destruct_vectorlEintgR(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const vector<int>*)
   {
      vector<int> *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(vector<int>));
      static ::ROOT::TGenericClassInfo 
         instance("vector<int>", -2, "vector", 477,
                  typeid(vector<int>), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &vectorlEintgR_Dictionary, isa_proxy, 0,
                  sizeof(vector<int>) );
      instance.SetNew(&new_vectorlEintgR);
      instance.SetNewArray(&newArray_vectorlEintgR);
      instance.SetDelete(&delete_vectorlEintgR);
      instance.SetDeleteArray(&deleteArray_vectorlEintgR);
      instance.SetDestructor(&destruct_vectorlEintgR);
      instance.AdoptCollectionProxyInfo(TCollectionProxyInfo::Generate(TCollectionProxyInfo::Pushback< vector<int> >()));
      return &instance;
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_(Init) = GenerateInitInstanceLocal((const vector<int>*)0x0); R__UseDummy(_R__UNIQUE_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *vectorlEintgR_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal((const vector<int>*)0x0)->GetClass();
      vectorlEintgR_TClassManip(theClass);
   return theClass;
   }

   static void vectorlEintgR_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   // Wrappers around operator new
   static void *new_vectorlEintgR(void *p) {
      return  p ? ::new((::ROOT::Internal::TOperatorNewHelper*)p) vector<int> : new vector<int>;
   }
   static void *newArray_vectorlEintgR(Long_t nElements, void *p) {
      return p ? ::new((::ROOT::Internal::TOperatorNewHelper*)p) vector<int>[nElements] : new vector<int>[nElements];
   }
   // Wrapper around operator delete
   static void delete_vectorlEintgR(void *p) {
      delete ((vector<int>*)p);
   }
   static void deleteArray_vectorlEintgR(void *p) {
      delete [] ((vector<int>*)p);
   }
   static void destruct_vectorlEintgR(void *p) {
      typedef vector<int> current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class vector<int>

namespace ROOT {
   static TClass *vectorlEfloatgR_Dictionary();
   static void vectorlEfloatgR_TClassManip(TClass*);
   static void *new_vectorlEfloatgR(void *p = 0);
   static void *newArray_vectorlEfloatgR(Long_t size, void *p);
   static void delete_vectorlEfloatgR(void *p);
   static void deleteArray_vectorlEfloatgR(void *p);
   static void destruct_vectorlEfloatgR(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const vector<float>*)
   {
      vector<float> *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(vector<float>));
      static ::ROOT::TGenericClassInfo 
         instance("vector<float>", -2, "vector", 477,
                  typeid(vector<float>), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &vectorlEfloatgR_Dictionary, isa_proxy, 0,
                  sizeof(vector<float>) );
      instance.SetNew(&new_vectorlEfloatgR);
      instance.SetNewArray(&newArray_vectorlEfloatgR);
      instance.SetDelete(&delete_vectorlEfloatgR);
      instance.SetDeleteArray(&deleteArray_vectorlEfloatgR);
      instance.SetDestructor(&destruct_vectorlEfloatgR);
      instance.AdoptCollectionProxyInfo(TCollectionProxyInfo::Generate(TCollectionProxyInfo::Pushback< vector<float> >()));
      return &instance;
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_(Init) = GenerateInitInstanceLocal((const vector<float>*)0x0); R__UseDummy(_R__UNIQUE_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *vectorlEfloatgR_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal((const vector<float>*)0x0)->GetClass();
      vectorlEfloatgR_TClassManip(theClass);
   return theClass;
   }

   static void vectorlEfloatgR_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   // Wrappers around operator new
   static void *new_vectorlEfloatgR(void *p) {
      return  p ? ::new((::ROOT::Internal::TOperatorNewHelper*)p) vector<float> : new vector<float>;
   }
   static void *newArray_vectorlEfloatgR(Long_t nElements, void *p) {
      return p ? ::new((::ROOT::Internal::TOperatorNewHelper*)p) vector<float>[nElements] : new vector<float>[nElements];
   }
   // Wrapper around operator delete
   static void delete_vectorlEfloatgR(void *p) {
      delete ((vector<float>*)p);
   }
   static void deleteArray_vectorlEfloatgR(void *p) {
      delete [] ((vector<float>*)p);
   }
   static void destruct_vectorlEfloatgR(void *p) {
      typedef vector<float> current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class vector<float>

namespace ROOT {
   static TClass *vectorlETVector3gR_Dictionary();
   static void vectorlETVector3gR_TClassManip(TClass*);
   static void *new_vectorlETVector3gR(void *p = 0);
   static void *newArray_vectorlETVector3gR(Long_t size, void *p);
   static void delete_vectorlETVector3gR(void *p);
   static void deleteArray_vectorlETVector3gR(void *p);
   static void destruct_vectorlETVector3gR(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const vector<TVector3>*)
   {
      vector<TVector3> *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(vector<TVector3>));
      static ::ROOT::TGenericClassInfo 
         instance("vector<TVector3>", -2, "vector", 477,
                  typeid(vector<TVector3>), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &vectorlETVector3gR_Dictionary, isa_proxy, 4,
                  sizeof(vector<TVector3>) );
      instance.SetNew(&new_vectorlETVector3gR);
      instance.SetNewArray(&newArray_vectorlETVector3gR);
      instance.SetDelete(&delete_vectorlETVector3gR);
      instance.SetDeleteArray(&deleteArray_vectorlETVector3gR);
      instance.SetDestructor(&destruct_vectorlETVector3gR);
      instance.AdoptCollectionProxyInfo(TCollectionProxyInfo::Generate(TCollectionProxyInfo::Pushback< vector<TVector3> >()));
      return &instance;
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_(Init) = GenerateInitInstanceLocal((const vector<TVector3>*)0x0); R__UseDummy(_R__UNIQUE_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *vectorlETVector3gR_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal((const vector<TVector3>*)0x0)->GetClass();
      vectorlETVector3gR_TClassManip(theClass);
   return theClass;
   }

   static void vectorlETVector3gR_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   // Wrappers around operator new
   static void *new_vectorlETVector3gR(void *p) {
      return  p ? ::new((::ROOT::Internal::TOperatorNewHelper*)p) vector<TVector3> : new vector<TVector3>;
   }
   static void *newArray_vectorlETVector3gR(Long_t nElements, void *p) {
      return p ? ::new((::ROOT::Internal::TOperatorNewHelper*)p) vector<TVector3>[nElements] : new vector<TVector3>[nElements];
   }
   // Wrapper around operator delete
   static void delete_vectorlETVector3gR(void *p) {
      delete ((vector<TVector3>*)p);
   }
   static void deleteArray_vectorlETVector3gR(void *p) {
      delete [] ((vector<TVector3>*)p);
   }
   static void destruct_vectorlETVector3gR(void *p) {
      typedef vector<TVector3> current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class vector<TVector3>

namespace ROOT {
   static TClass *vectorlETLorentzVectorgR_Dictionary();
   static void vectorlETLorentzVectorgR_TClassManip(TClass*);
   static void *new_vectorlETLorentzVectorgR(void *p = 0);
   static void *newArray_vectorlETLorentzVectorgR(Long_t size, void *p);
   static void delete_vectorlETLorentzVectorgR(void *p);
   static void deleteArray_vectorlETLorentzVectorgR(void *p);
   static void destruct_vectorlETLorentzVectorgR(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const vector<TLorentzVector>*)
   {
      vector<TLorentzVector> *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(vector<TLorentzVector>));
      static ::ROOT::TGenericClassInfo 
         instance("vector<TLorentzVector>", -2, "vector", 477,
                  typeid(vector<TLorentzVector>), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &vectorlETLorentzVectorgR_Dictionary, isa_proxy, 4,
                  sizeof(vector<TLorentzVector>) );
      instance.SetNew(&new_vectorlETLorentzVectorgR);
      instance.SetNewArray(&newArray_vectorlETLorentzVectorgR);
      instance.SetDelete(&delete_vectorlETLorentzVectorgR);
      instance.SetDeleteArray(&deleteArray_vectorlETLorentzVectorgR);
      instance.SetDestructor(&destruct_vectorlETLorentzVectorgR);
      instance.AdoptCollectionProxyInfo(TCollectionProxyInfo::Generate(TCollectionProxyInfo::Pushback< vector<TLorentzVector> >()));
      return &instance;
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_(Init) = GenerateInitInstanceLocal((const vector<TLorentzVector>*)0x0); R__UseDummy(_R__UNIQUE_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *vectorlETLorentzVectorgR_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal((const vector<TLorentzVector>*)0x0)->GetClass();
      vectorlETLorentzVectorgR_TClassManip(theClass);
   return theClass;
   }

   static void vectorlETLorentzVectorgR_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   // Wrappers around operator new
   static void *new_vectorlETLorentzVectorgR(void *p) {
      return  p ? ::new((::ROOT::Internal::TOperatorNewHelper*)p) vector<TLorentzVector> : new vector<TLorentzVector>;
   }
   static void *newArray_vectorlETLorentzVectorgR(Long_t nElements, void *p) {
      return p ? ::new((::ROOT::Internal::TOperatorNewHelper*)p) vector<TLorentzVector>[nElements] : new vector<TLorentzVector>[nElements];
   }
   // Wrapper around operator delete
   static void delete_vectorlETLorentzVectorgR(void *p) {
      delete ((vector<TLorentzVector>*)p);
   }
   static void deleteArray_vectorlETLorentzVectorgR(void *p) {
      delete [] ((vector<TLorentzVector>*)p);
   }
   static void destruct_vectorlETLorentzVectorgR(void *p) {
      typedef vector<TLorentzVector> current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class vector<TLorentzVector>

namespace {
  void TriggerDictionaryInitialization_libEG2DataMining_EG2DataMiningPackage_Impl() {
    static const char* headers[] = {
"T3pSimulation.h",
"TAnalysisEG2.h",
"TCalcPhysVarsEG2.h",
"TEG2dm.h",
"TSchemeDATA.h",
0
    };
    static const char* includePaths[] = {
"/Users/erezcohen/larlite/UserDev/mySoftware",
"/usr/local/Cellar/root6/6.06.02/include/root",
"/Users/erezcohen/larlite/UserDev/CLASEG2DataMining/EG2DataMiningPackage/",
0
    };
    static const char* fwdDeclCode = R"DICTFWDDCLS(
#line 1 "libEG2DataMining_EG2DataMiningPackage dictionary forward declarations' payload"
#pragma clang diagnostic ignored "-Wkeyword-compat"
#pragma clang diagnostic ignored "-Wignored-attributes"
#pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
extern int __Cling_Autoloading_Map;
class __attribute__((annotate("$clingAutoload$T3pSimulation.h")))  TVector3;
namespace std{inline namespace __1{template <class _Tp> class __attribute__((annotate("$clingAutoload$string")))  allocator;
}}
class __attribute__((annotate("$clingAutoload$T3pSimulation.h")))  TLorentzVector;
class __attribute__((annotate("$clingAutoload$T3pSimulation.h")))  TEG2dm;
class __attribute__((annotate("$clingAutoload$TSchemeDATA.h")))  TSchemeDATA;
class __attribute__((annotate("$clingAutoload$TCalcPhysVarsEG2.h")))  TCalcPhysVarsEG2;
class __attribute__((annotate("$clingAutoload$TAnalysisEG2.h")))  TAnalysisEG2;
class __attribute__((annotate("$clingAutoload$T3pSimulation.h")))  T3pSimulation;
)DICTFWDDCLS";
    static const char* payloadCode = R"DICTPAYLOAD(
#line 1 "libEG2DataMining_EG2DataMiningPackage dictionary payload"

#ifndef G__VECTOR_HAS_CLASS_ITERATOR
  #define G__VECTOR_HAS_CLASS_ITERATOR 1
#endif

#define _BACKWARD_BACKWARD_WARNING_H
#include "T3pSimulation.h"
#include "TAnalysisEG2.h"
#include "TCalcPhysVarsEG2.h"
#include "TEG2dm.h"
#include "TSchemeDATA.h"

#undef  _BACKWARD_BACKWARD_WARNING_H
)DICTPAYLOAD";
    static const char* classesHeaders[]={
"T3pSimulation", payloadCode, "@",
"TAnalysisEG2", payloadCode, "@",
"TCalcPhysVarsEG2", payloadCode, "@",
"TEG2dm", payloadCode, "@",
"TSchemeDATA", payloadCode, "@",
nullptr};

    static bool isInitialized = false;
    if (!isInitialized) {
      TROOT::RegisterModule("libEG2DataMining_EG2DataMiningPackage",
        headers, includePaths, payloadCode, fwdDeclCode,
        TriggerDictionaryInitialization_libEG2DataMining_EG2DataMiningPackage_Impl, {}, classesHeaders);
      isInitialized = true;
    }
  }
  static struct DictInit {
    DictInit() {
      TriggerDictionaryInitialization_libEG2DataMining_EG2DataMiningPackage_Impl();
    }
  } __TheDictionaryInitializer;
}
void TriggerDictionaryInitialization_libEG2DataMining_EG2DataMiningPackage() {
  TriggerDictionaryInitialization_libEG2DataMining_EG2DataMiningPackage_Impl();
}
