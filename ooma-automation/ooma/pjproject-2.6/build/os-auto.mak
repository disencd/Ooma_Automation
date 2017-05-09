# build/os-auto.mak.  Generated from os-auto.mak.in by configure.

export OS_CFLAGS   := $(CC_DEF)PJ_AUTOCONF=1 -O2 -DNDEBUG -DPJ_IS_BIG_ENDIAN=0 -DPJ_IS_LITTLE_ENDIAN=1 -fPIC

export OS_CXXFLAGS := $(CC_DEF)PJ_AUTOCONF=1 -O2 -DNDEBUG 

export OS_LDFLAGS  :=  -lssl -lcrypto -lm -lrt -lpthread 

export OS_SOURCES  := 


