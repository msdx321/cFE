# Some upper-level code may be gated on _COMPOSITE_OS_ being defined
# (As of the time of this comment, there isn't any, but maybe in the future!)
SET(OSAL_C_FLAGS "${OSAL_C_FLAGS} -D_COMPOSITE_OS_")

# OSAL_LINK_LIBS determines which system-level libraries must be included in the
# link command in order to produce the final binary.  These libs will be used for
# ALL targets that utilize the RTEMS OS layer.  Additional target-specific libraries
# may also be specified in the BSP or the cross-compile toolchain.
SET(OSAL_LINK_LIBS ${OSAL_LINK_LIBS})
