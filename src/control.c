/*
 * control.c — control operations
 */
#include "display.h"
#include "madm.h"
#include "proto.h"

void
stop(Addr s)
{
	(void)s;
	madm_status = MADM_STOPPED;
}

void
unused(Addr s)
{
	(void)s;
}

void
test(Addr s)
{
	(void)s;
	if (accumulator[A_LINE] < 0)
		++control[CI_LINE];
}

void
jump(Addr s)
{
	control[CI_LINE] = store[s];
	display_line(C_TUBE, CI_LINE);
}

void
rjump(Addr s)
{
	control[CI_LINE] += store[s];
	display_line(C_TUBE, CI_LINE);
}
