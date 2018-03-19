CC = gcc
C_VERSION = c99

TESTS = oscore osfile osnetwork ostimer osfilesys osloader
SUBDIRS := $(foreach testname,$(TESTS),$(testname)-test) shared

OTHER_ARCH_FILES := $(shell find -regextype posix-extended -regex '.*_(arinc653|vxworks)\.c' -printf '%P\n')
COMPOSITE_FILES := $(foreach dir,$(SUBDIRS),$(wildcard $(dir)/*_composite.c))

LIBC_PATH=/home/vagrant/cFE2cos/composite/src/components/lib/musl-1.1.11

# Ignore the non-composite counterparts of *_composite.c files
IGNORE := $(OTHER_ARCH_FILES) shared/ut_osloader_stubs.c $(COMPOSITE_FILES:_composite.c=.c)
SOURCE_FILES := $(filter-out $(IGNORE), $(foreach dir,$(SUBDIRS),$(wildcard $(dir)/*.c))) shared/ut_main_composite.h

CFLAGS = -std=$(C_VERSION) -nostdinc -I$(LIBC_PATH)/include -DOS_USE_EMBEDDED_PRINTF -DLOG_TO_STDOUT_TOO -DCOMPOSITE_OS -fno-stack-protector -c -I ../bsp/pc-composite/config -I ./shared -I ../os/inc

all:
	rm $(wildcard *.o)
	$(CC) $(CFLAGS) $(SOURCE_FILES)
