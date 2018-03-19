###############################################################################
# File: osal.mak
#
# Purpose:
#   Compile the OS Abstraction layer library.
#
# History:
#   2004/04/12  A. Cudmore   : Initial revision for SDO.
#   2004/05/24  P. Kutt      : Modified for new directory structure; rewrote comments.
#
###############################################################################

# Subsystem produced by this makefile.
TARGET = osal.o

#==============================================================================
# Object files required to build subsystem.

OBJS=osapi_stub.o

#==============================================================================
# Source files required to build subsystem; used to generate dependencies.

SOURCES=osapi_stub.c
