// Do NOT change. Changes will be lost next time file is generated

#define R__DICTIONARY_FILENAME CLASEG2DataMining_GSIMulationDict

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
#include "EGgui.h"
#include "GenerateEvents.h"

// Header files passed via #pragma extra_include

namespace ROOT {
   static TClass *EGgui_Dictionary();
   static void EGgui_TClassManip(TClass*);
   static void delete_EGgui(void *p);
   static void deleteArray_EGgui(void *p);
   static void destruct_EGgui(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::EGgui*)
   {
      ::EGgui *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(::EGgui));
      static ::ROOT::TGenericClassInfo 
         instance("EGgui", "EGgui.h", 70,
                  typeid(::EGgui), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &EGgui_Dictionary, isa_proxy, 4,
                  sizeof(::EGgui) );
      instance.SetDelete(&delete_EGgui);
      instance.SetDeleteArray(&deleteArray_EGgui);
      instance.SetDestructor(&destruct_EGgui);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::EGgui*)
   {
      return GenerateInitInstanceLocal((::EGgui*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_(Init) = GenerateInitInstanceLocal((const ::EGgui*)0x0); R__UseDummy(_R__UNIQUE_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *EGgui_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal((const ::EGgui*)0x0)->GetClass();
      EGgui_TClassManip(theClass);
   return theClass;
   }

   static void EGgui_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   static TClass *GenerateEvents_Dictionary();
   static void GenerateEvents_TClassManip(TClass*);
   static void *new_GenerateEvents(void *p = 0);
   static void *newArray_GenerateEvents(Long_t size, void *p);
   static void delete_GenerateEvents(void *p);
   static void deleteArray_GenerateEvents(void *p);
   static void destruct_GenerateEvents(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::GenerateEvents*)
   {
      ::GenerateEvents *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(::GenerateEvents));
      static ::ROOT::TGenericClassInfo 
         instance("GenerateEvents", "GenerateEvents.h", 68,
                  typeid(::GenerateEvents), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &GenerateEvents_Dictionary, isa_proxy, 4,
                  sizeof(::GenerateEvents) );
      instance.SetNew(&new_GenerateEvents);
      instance.SetNewArray(&newArray_GenerateEvents);
      instance.SetDelete(&delete_GenerateEvents);
      instance.SetDeleteArray(&deleteArray_GenerateEvents);
      instance.SetDestructor(&destruct_GenerateEvents);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::GenerateEvents*)
   {
      return GenerateInitInstanceLocal((::GenerateEvents*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_(Init) = GenerateInitInstanceLocal((const ::GenerateEvents*)0x0); R__UseDummy(_R__UNIQUE_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *GenerateEvents_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal((const ::GenerateEvents*)0x0)->GetClass();
      GenerateEvents_TClassManip(theClass);
   return theClass;
   }

   static void GenerateEvents_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   // Wrapper around operator delete
   static void delete_EGgui(void *p) {
      delete ((::EGgui*)p);
   }
   static void deleteArray_EGgui(void *p) {
      delete [] ((::EGgui*)p);
   }
   static void destruct_EGgui(void *p) {
      typedef ::EGgui current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::EGgui

namespace ROOT {
   // Wrappers around operator new
   static void *new_GenerateEvents(void *p) {
      return  p ? new(p) ::GenerateEvents : new ::GenerateEvents;
   }
   static void *newArray_GenerateEvents(Long_t nElements, void *p) {
      return p ? new(p) ::GenerateEvents[nElements] : new ::GenerateEvents[nElements];
   }
   // Wrapper around operator delete
   static void delete_GenerateEvents(void *p) {
      delete ((::GenerateEvents*)p);
   }
   static void deleteArray_GenerateEvents(void *p) {
      delete [] ((::GenerateEvents*)p);
   }
   static void destruct_GenerateEvents(void *p) {
      typedef ::GenerateEvents current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::GenerateEvents

namespace {
  void TriggerDictionaryInitialization_libCLASEG2DataMining_GSIMulation_Impl() {
    static const char* headers[] = {
"EGgui.h",
"GenerateEvents.h",
0
    };
    static const char* includePaths[] = {
"/Users/erezcohen/larlite/UserDev/mySoftware",
"/usr/local/Cellar/root6/6.06.02/include/root",
"/Users/erezcohen/larlite/UserDev/CLASEG2DataMining/GSIMulation/",
0
    };
    static const char* fwdDeclCode = R"DICTFWDDCLS(
#line 1 "libCLASEG2DataMining_GSIMulation dictionary forward declarations' payload"
#pragma clang diagnostic ignored "-Wkeyword-compat"
#pragma clang diagnostic ignored "-Wignored-attributes"
#pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
extern int __Cling_Autoloading_Map;
class __attribute__((annotate("$clingAutoload$EGgui.h")))  EGgui;
class __attribute__((annotate("$clingAutoload$EGgui.h")))  GenerateEvents;
)DICTFWDDCLS";
    static const char* payloadCode = R"DICTPAYLOAD(
#line 1 "libCLASEG2DataMining_GSIMulation dictionary payload"

#ifndef G__VECTOR_HAS_CLASS_ITERATOR
  #define G__VECTOR_HAS_CLASS_ITERATOR 1
#endif

#define _BACKWARD_BACKWARD_WARNING_H
#include "EGgui.h"
#include "GenerateEvents.h"

#undef  _BACKWARD_BACKWARD_WARNING_H
)DICTPAYLOAD";
    static const char* classesHeaders[]={
"EGgui", payloadCode, "@",
"GenerateEvents", payloadCode, "@",
nullptr};

    static bool isInitialized = false;
    if (!isInitialized) {
      TROOT::RegisterModule("libCLASEG2DataMining_GSIMulation",
        headers, includePaths, payloadCode, fwdDeclCode,
        TriggerDictionaryInitialization_libCLASEG2DataMining_GSIMulation_Impl, {}, classesHeaders);
      isInitialized = true;
    }
  }
  static struct DictInit {
    DictInit() {
      TriggerDictionaryInitialization_libCLASEG2DataMining_GSIMulation_Impl();
    }
  } __TheDictionaryInitializer;
}
void TriggerDictionaryInitialization_libCLASEG2DataMining_GSIMulation() {
  TriggerDictionaryInitialization_libCLASEG2DataMining_GSIMulation_Impl();
}
