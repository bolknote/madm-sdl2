/*
 * arith.c — arithmetic operations
 */
#include "display.h"
#include "madm.h"
#include "proto.h"

void
subtract(Addr s)
{
	accumulator[A_LINE] -= store[s];
	display_line(A_TUBE, A_LINE);
}
