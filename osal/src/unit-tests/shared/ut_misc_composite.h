#ifndef _UT_MISC_COMPOSITE_
#define _UT_MISC_COMPOSITE_

#include "common_types.h"

/* Prints a note showing the category of tests in progress. */
#define UT_CAT_HEADER(NAME) \
        OS_printf("\n=== Testing %s ===\n", NAME); \
        currentTestHeader = NAME
#define UT_CAT_END OS_printf("\n=== Done testing %s ===\n", currentTestHeader)
char *currentTestHeader;

/* Shared values. */
extern int32 g_skipTestCase;
extern char* g_skipTestCaseResult;

void Composite_UT_reset_skip_values(void);

#endif
