###############################################################################
# File: psp.mak
#
# Purpose:
#   Platform Support Package routines for the Linux desktop build
#
# History:
#   2005/07/27  A. Cudmore   : Updated for cFE.
#   2004/04/12  A. Cudmore   : Initial revision for SDO.
#   2004/05/24  P. Kutt      : Modified for new directory structure; rewrote comments.
#
###############################################################################

# Subsystem produced by this makefile.
TARGET = psp.o

#==============================================================================
# Object files required to build subsystem.
#==============================================================================
OBJS = cfe_psp_stub.o

#==============================================================================
# Source files required to build subsystem; used to generate dependencies.
SOURCES = cfe_psp_stub.c
