#!/usr/bin/env python2.7
# cFE2cos build script. Builds Composite and the cFE and links the two together.
import argparse
import os
import shutil
import subprocess as sp
import sys
import glob

COS_CONSTANTS_FILE = "Makefile.cosinc"

# Load command line arguments.
parser = argparse.ArgumentParser(description='Operate the cFE build system for composite')
parser.add_argument('-c', '--clean', dest='clean', action='store_true',
                    help='Clean the Composite build directory before building it.')
parser.add_argument('-i', '--ignore-clock-skew', dest='skew', action='store_true',
                    help='Ignore clock skew warnings when building.')
parser.add_argument('-u', '--unit-tests', dest='unit_tests', action='store_true',
                    help='Build unit tests.')
parser.add_argument('-p', '--copy-only', dest='copy_only', action='store_true',
                    help='Don\'t build the cFE, just copy headers')

args = parser.parse_args()

print """
#######################
## SETTING VARIABLES ##
#######################
"""

# Find the root of the composite repository
cos_root, _ = sp.Popen("cd ..; git rev-parse --show-toplevel",
                       shell=True, stdout=sp.PIPE).communicate()
cos_root = cos_root.strip()

# Set static variables.
COMPOSITE_DIR = cos_root + "/"
COMPOSITE_TRANSFER_DIR = COMPOSITE_DIR + "transfer/"
COMPOSITE_MAKE_ROOT = COMPOSITE_DIR + "src/"
COMPOSITE_IMPL_NO_INTERFACE_DIR = COMPOSITE_DIR + "src/components/implementation/no_interface/"
COMPOSITE_CFE_COMPONENT_ROOT = COMPOSITE_IMPL_NO_INTERFACE_DIR + "cFE_booter/"
COMPOSITE_CFE_HEADER_DESTINATION = COMPOSITE_CFE_COMPONENT_ROOT + "gen/"
print "COMPOSITE_DIR: {}".format(COMPOSITE_DIR)
print "COMPOSITE_TRANSFER_DIR: {}".format(COMPOSITE_TRANSFER_DIR)
print "COMPOSITE_MAKE_ROOT: {}".format(COMPOSITE_MAKE_ROOT)
print "COMPOSITE_CFE_COMPONENT_ROOT: {}".format(COMPOSITE_CFE_COMPONENT_ROOT)
print "COMPOSITE_CFE_HEADER_DESTINATION: {}".format(COMPOSITE_CFE_HEADER_DESTINATION)

CFE_DIR = COMPOSITE_MAKE_ROOT + "extern/cFE/"
CFE_MAKE_ROOT = CFE_DIR + "build/cpu1/"
CFE_OBJECT_LOCATION = CFE_MAKE_ROOT + "exe/"
CFE_OBJECT_NAME = "composite_cFE.o"
print "CFE_DIR: {}".format(CFE_DIR)
print "CFE_MAKE_ROOT: {}".format(CFE_MAKE_ROOT)
print "CFE_OBJECT_LOCATION: {}".format(CFE_OBJECT_LOCATION)
print "CFE_OBJECT_NAME: {}".format(CFE_OBJECT_NAME)

# UT is an abbreviation for Unit Tests.
COMPOSITE_CFE_UT_DESTINATION = COMPOSITE_CFE_COMPONENT_ROOT + "test/"
OSAL_UT_DIR = CFE_DIR + "osal/src/unit-tests/"
print "OSAL_UT_DIR: {}".format(OSAL_UT_DIR)
print "COMPOSITE_CFE_UT_DESTINATION: {}".format(COMPOSITE_CFE_UT_DESTINATION)

# Create a make include file with all the macros!
with open(COS_CONSTANTS_FILE, "w") as cosfile:
    cosfile.write("COMPOSITE_DIR=%s\n" % COMPOSITE_DIR)
    cosfile.write("COMPOSITE_TRANSFER_DIR=%s\n" % COMPOSITE_TRANSFER_DIR)
    cosfile.write("COMPOSITE_MAKE_ROOT=%s\n" % COMPOSITE_MAKE_ROOT)
    cosfile.write("COMPOSITE_IMPL_NO_INTERFACE_DIR=%s\n" % COMPOSITE_IMPL_NO_INTERFACE_DIR)
    cosfile.write("COMPOSITE_CFE_COMPONENT_ROOT=%s\n" % COMPOSITE_CFE_COMPONENT_ROOT)
    cosfile.write("COMPOSITE_CFE_HEADER_DESTINATION=%s\n" % COMPOSITE_CFE_HEADER_DESTINATION)
    cosfile.write("CFE_DIR=%s\n" % CFE_DIR)
    cosfile.write("CFE_MAKE_ROOT=%s\n" % CFE_MAKE_ROOT)
    cosfile.write("CFE_OBJECT_LOCATION=%s\n" % CFE_OBJECT_LOCATION)
    cosfile.write("CFE_OBJECT_NAME=%s\n" % CFE_OBJECT_NAME)
    cosfile.write("COMPOSITE_CFE_UT_DESTINATION=%s\n" % COMPOSITE_CFE_UT_DESTINATION)
    cosfile.write("OSAL_UT_DIR=%s\n" % OSAL_UT_DIR)

# We don't need these stubs because we already provide our own.
# Copying them over causes duplicate symbol errors
OSAL_UT_OBJECTS_TO_SKIP = [
    "ut_osfile_stubs.o",
    "ut_osfilesys_stubs.o",
    "ut_osnetwork_stubs.o",
    "ut_ostimer_stubs.o"
]
OSAL_UT_HEADERS_TO_COPY = [
    "oscore-test",
    "osfile-test",
    "osfilesys-test",
    "osloader-test",
    "osnetwork-test",
    "osprintf-test",
    "ostimer-test",
    "shared"
]

CFE_HEADERS_TO_COPY = [
    "build/cpu1/inc/cfe_platform_cfg.h",
    "build/cpu1/inc/osconfig.h",
    "build/mission_inc/cfe_mission_cfg.h",
    "cfe/fsw/cfe-core/src/inc/*",
    "osal/src/os/inc/*",
    "psp/fsw/pc-composite/inc/*",
    "psp/fsw/inc/*"
]

CFE_APPS = [
    "bm",
    "cs",
    "ds",
    "f42",
    "fm",
    "hc",
    "hs",
    "i42",
    "kit_ci",
    "kit_to",
    "kit_sch",
    "lc",
    "md",
    "mm",
    "sc",
    "sch_lab",
    "sim",
    "tftp"
]

# Just some shell magic to load the environment variable exports needed to build cFE.
cfe_env = sp.Popen(["bash", "-c",
                    "trap 'env' exit; cd {} && source \"$1\" > /dev/null 2>&1".format(CFE_DIR),
                    "_", "setvars.sh"], shell=False, stdout=sp.PIPE).communicate()[0]
os.environ.update(dict([line.split('=', 1) for line in filter(None, cfe_env.split("\n"))]))

print """
##############
## BUILDING ##
##############
"""

OUT = ""
if args.skew:
    "Warnings about clock skew will not be printed."
    OUT = " 2>&1 | grep -vP 'Clock skew|in the future'"

# Execute build
if args.clean:
    print "=== Cleaning cFE ==="
    sp.check_call("make clean" + OUT, shell=True, cwd=CFE_MAKE_ROOT)

print "=== Copying headers ==="
if not os.path.exists(COMPOSITE_CFE_HEADER_DESTINATION):
    print "cFE header destination folder not found. Creating it now."
    os.makedirs(COMPOSITE_CFE_HEADER_DESTINATION)
for header in CFE_HEADERS_TO_COPY:
    sp.check_call("cp -ur " + CFE_DIR + header + " " + COMPOSITE_CFE_HEADER_DESTINATION, shell=True)

if args.unit_tests:
    print "=== Building unit tests ==="
    sp.call("make" + OUT, shell=True, cwd=OSAL_UT_DIR)
    print "Cleaning old test objects..."
    if os.path.exists(COMPOSITE_CFE_UT_DESTINATION):
        shutil.rmtree(COMPOSITE_CFE_UT_DESTINATION)
    os.mkdir(COMPOSITE_CFE_UT_DESTINATION)
    print "Copying UT objects..."
    for obj in os.listdir(OSAL_UT_DIR):
            if obj not in OSAL_UT_OBJECTS_TO_SKIP and os.path.isfile(OSAL_UT_DIR + obj):
                shutil.copy(OSAL_UT_DIR + obj, COMPOSITE_CFE_UT_DESTINATION)
                print "Copied {} to {}".format(obj, COMPOSITE_CFE_UT_DESTINATION)
    print "Copying UT headers..."
    for folder in OSAL_UT_HEADERS_TO_COPY:
        shutil.copytree(OSAL_UT_DIR + folder, COMPOSITE_CFE_UT_DESTINATION + folder)
        print "Copied {} to {}".format(folder, COMPOSITE_CFE_UT_DESTINATION)

if args.copy_only:
    sys.exit(0)

print "=== Building cFE ==="

sp.check_call("rm -f cf/apps/cFE_fs.o", shell=True, cwd=CFE_OBJECT_LOCATION)
sp.check_call("rm -f cFE_fs.o", shell=True, cwd=CFE_OBJECT_LOCATION)
sp.check_call("make" + OUT, shell=True, cwd=CFE_MAKE_ROOT)

print "=== Copying cFE Object ==="
OBJECT_SOURCE = CFE_OBJECT_LOCATION + CFE_OBJECT_NAME
OBJECT_DESTINATION = COMPOSITE_CFE_COMPONENT_ROOT + CFE_OBJECT_NAME
if os.path.exists(OBJECT_DESTINATION):
    os.remove(OBJECT_DESTINATION)
if not os.path.exists(OBJECT_SOURCE):
    raise RuntimeError("Could not find cFE object to copy!")
shutil.copy(OBJECT_SOURCE, OBJECT_DESTINATION)
print "Copied {} to {}".format(OBJECT_SOURCE, OBJECT_DESTINATION)

print "=== Copying apps ==="
for app in CFE_APPS:
    try:
        dest = COMPOSITE_IMPL_NO_INTERFACE_DIR + app + "/cFE_"
        sp.check_call("cp build/cpu1/osk_app_fw/*.o " + COMPOSITE_IMPL_NO_INTERFACE_DIR + app + "/",
                  shell=True, cwd=CFE_DIR)
        # Copying cfs lib object to each app.
        shutil.copy('build/cpu1/cfs_lib/cfs_utils.o', dest + 'cfs_utils.o')
        # Copying expat lib objects to each app.
        shutil.copy('build/cpu1/expat_lib/expat_init.o', dest + 'expat_init.o')
        shutil.copy('build/cpu1/expat_lib/xmlparse.o', dest + 'xmlparse.o')
        shutil.copy('build/cpu1/expat_lib/xmlrole.o', dest + 'xmlrole.o')
        shutil.copy('build/cpu1/expat_lib/xmltok.o', dest + 'xmltok.o')
        shutil.copy('build/cpu1/expat_lib/xmltok_impl.o', dest + 'xmltok_impl.o')
        shutil.copy('build/cpu1/expat_lib/xmltok_ns.o', dest + 'xmltok_ns.o')
        for src in glob.glob(CFE_MAKE_ROOT + app + "/*.o"):
            basename = os.path.basename(src)
            print "Copying object '{}' to '{}'.".format(basename, dest + basename)
            shutil.copy(src, dest + basename)
    except:
        pass # ignore err and keep going

print "=== Integrating Tar Filesystem  ==="
# This is a hack, but we need to include tables, and they aren't being included!
sp.check_call("cp *.tbl cf" + OUT,
              shell=True, cwd=CFE_OBJECT_LOCATION)
sp.check_call("tar cf cFE_fs.tar --exclude=\"cf/apps/composite_cFE.o\" cf/" + OUT,
              shell=True, cwd=CFE_OBJECT_LOCATION)
sp.check_call("ld -r -b binary cFE_fs.tar -o cFE_fs.o" + OUT,
              shell=True, cwd=CFE_OBJECT_LOCATION)
shutil.copy(CFE_OBJECT_LOCATION + "/cFE_fs.o", COMPOSITE_CFE_COMPONENT_ROOT)
