/*
 * memory.c — memory operations
 */
#include "display.h"
#include "madm.h"
#include "proto.h"

void
load_negative(Addr s)
{
	accumulator[A_LINE] = 0u - store[s];
	display_line(A_TUBE, A_LINE);
}

void
store_accumulator(Addr s)
{
	store[s] = accumulator[A_LINE];
	display_line(S_TUBE, s);
}
