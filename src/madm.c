/*
 * madm.c — global machine state
 */
#include "madm.h"

Line accumulator[ACCUM_SIZE];
Line control[CONTROL_SIZE];
Line store[STORE_SIZE];
Instruction staticisor;

MadmStatus madm_status = MADM_STOPPED;
