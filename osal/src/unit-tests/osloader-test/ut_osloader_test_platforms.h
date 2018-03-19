/*================================================================================*
** File:  ut_osloader_test_platforms.h
** Owner: Tam Ngo
** Date:  November 2014
**================================================================================*/

#ifndef _UT_OSLOADER_TEST_PLATFORMS_H_
#define _UT_OSLOADER_TEST_PLATFORMS_H_

/*--------------------------------------------------------------------------------*
** Includes
**--------------------------------------------------------------------------------*/

#ifdef _LINUX_OS_
#endif  /* _LINUX_OS_ */

#ifdef OSP_ARINC653
#endif  /* OSP_ARINC653 */

/*--------------------------------------------------------------------------------*
** Macros
**--------------------------------------------------------------------------------*/

/*--------------------------------------------*/
#ifdef _LINUX_OS_
/*--------------------------------------------*/

#define UT_OS_GENERIC_MODULE_NAME1   "/cf/MODULE.so"
#define UT_OS_GENERIC_MODULE_NAME2   "/cf/MODULE1.so"
#define UT_OS_SPECIFIC_MODULE_NAME   "/cf/MODULE%d.so"

/*--------------------------------------------*/
#endif  /* _LINUX_OS_ */
/*--------------------------------------------*/

/*--------------------------------------------*/
#if defined(_VXWORKS_OS_) || defined(COMPOSITE_OS)
/*--------------------------------------------*/

#define UT_OS_GENERIC_MODULE_NAME1   "/cf/apps/MODULE.o"
#define UT_OS_GENERIC_MODULE_NAME2   "/cf/apps/MODULE1.o"
#define UT_OS_SPECIFIC_MODULE_NAME   "/cf/apps/MODULE%d.o"

/*--------------------------------------------*/
#endif  /* _VXWORKS_OS_ */
/*--------------------------------------------*/

/*--------------------------------------------*/
#ifdef OSP_ARINC653
/*--------------------------------------------*/

#define UT_OS_GENERIC_MODULE_NAME1   "/cf/apps/MODULE.o"
#define UT_OS_GENERIC_MODULE_NAME2   "/cf/apps/MODULE1.o"
#define UT_OS_SPECIFIC_MODULE_NAME   "/cf/apps/MODULE%d.o"

/*--------------------------------------------*/
#endif  /* OSP_ARINC653 */
/*--------------------------------------------*/

/*--------------------------------------------------------------------------------*
** Data types
**--------------------------------------------------------------------------------*/

/*--------------------------------------------------------------------------------*
** External global variables
**--------------------------------------------------------------------------------*/

/*--------------------------------------------------------------------------------*
** Global variables
**--------------------------------------------------------------------------------*/

/*--------------------------------------------------------------------------------*
** Function prototypes
**--------------------------------------------------------------------------------*/

/*--------------------------------------------------------------------------------*/

#endif  /* _UT_OSLOADER_TEST_PLATFORMS_H_ */

/*================================================================================*
** End of File: ut_osloader_test_platforms.h
**================================================================================*/
