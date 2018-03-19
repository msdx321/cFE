#include "ut_misc_composite.h"

int32 g_skipTestCase = -1;
char* g_skipTestCaseResult = " ";

void Composite_UT_reset_skip_values(void)
{
    g_skipTestCase = -1;
    g_skipTestCaseResult = " ";
}
