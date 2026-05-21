/*
 * madm.h — Manchester Mark I prototype simulator (machine model)
 */
#ifndef MADM_H
#define MADM_H

#include <stdbool.h>
#include <stdint.h>

typedef enum {
	MADM_STOPPED,
	MADM_RUNNING,
	MADM_MANUAL
} MadmStatus;

extern MadmStatus madm_status;

/* 32-bit Williams tube word; arithmetic wraps as two's complement. */
typedef uint32_t Line;
#define LINE_BITS 32u
#define MAX_LINE UINT32_MAX
#define LINE_SIGN_BIT (UINT32_C(1) << (LINE_BITS - 1u))

typedef uint8_t Addr;

typedef struct {
	uint8_t func;
	Addr addr;
} Instruction;

#define FUNC_BITS 3u
#define MAX_FUNC ((1u << FUNC_BITS) - 1u)

#define ADDR_BITS 13u
#define UNUSED_ADDR_BITS 8u
#define MAX_ADDR ((1u << (ADDR_BITS - UNUSED_ADDR_BITS)) - 1u)

#define ACCUM_SIZE 1u
#define CONTROL_SIZE 2u
#define STORE_SIZE 32u

#define A_LINE 0u /* accumulator */
#define CI_LINE 0u /* control instruction (program counter) */
#define PI_LINE 1u /* present instruction */

extern Line accumulator[ACCUM_SIZE];
extern Line control[CONTROL_SIZE];
extern Line store[STORE_SIZE];
extern Instruction staticisor;

_Static_assert(STORE_SIZE == 32, "prototype store is 32 lines");
_Static_assert(LINE_BITS == 32, "Williams tube word is 32 bits");

#endif /* MADM_H */
