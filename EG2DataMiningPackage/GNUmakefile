# EG2 data mining

# specific names for this package
DICT  = EG2DataMining_EG2DataMiningPackageDict
SHLIB = libEG2DataMining_EG2DataMiningPackage.so
SOURCES = $(filter-out $(DICT).cxx, $(wildcard *.cxx))
FMWK_HEADERS = LinkDef.h $(DICT).h
HEADERS = $(filter-out $(FMWK_HEADERS), $(wildcard *.h))
OBJECTS = $(SOURCES:.cxx=.o)

# include options for this package
INCFLAGS  = -I.                       #Include itself
INCFLAGS += -I$(LARLITE_USERDEVDIR)/mySoftware
INCFLAGS += -I$(LARLITE_USERDEVDIR)/CLASEG2DataMining/GSIMulation


# platform-specific options
OSNAME          = $(shell uname -s)
HOST            = $(shell uname -n)
OSNAMEMODE      = $(OSNAME)

# call kernel specific compiler setup
include $(LARLITE_BASEDIR)/Makefile/Makefile.${OSNAME}

# set linker flags
#LDFLAGS += -L$(shell root-config --libdir) -lEG -lRooFit -lRooFitCore -lRooStats -lSpectrum -lHist 
LDFLAGS += -L$(shell root-config --libdir) -lEG -lSpectrum -lHist 
LDFLAGS += -L$(LARLITE_LIBDIR) -lMySoftware_MySoftwarePackage


# call the common GNUmakefile
include $(LARLITE_BASEDIR)/Makefile/GNUmakefile.CORE
