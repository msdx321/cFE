###############################################################################
# File: link-rules.mak
#
# Purpose:
#   Makefile for linking code and producing the cFE Core executable image.
#
# History:
#
###############################################################################
##
## Executable target. This is target specific
##
EXE_TARGET=composite_cFE.o

CORE_INSTALL_FILES = $(EXE_TARGET)


##
## Linker flags that are needed
##
LDFLAGS = -r -m32 -Wl,-export-dynamic

##
## Libraries to link in
##
## LIBS =
##
## Uncomment the following line to link in C++ standard libs
## LIBS += -lstdc++
##

##
## cFE Core Link Rule
##
$(EXE_TARGET): $(CORE_OBJS)
	$(LINKER) $(DEBUG_FLAGS) -r -o $(EXE_TARGET) $(CORE_OBJS)

##
## Application Link Rule
##
$(APPTARGET).$(APP_EXT): $(OBJS)
	$(COMPILER) -m32 -shared -o $@ $(OBJS)
