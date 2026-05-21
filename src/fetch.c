/*
 * fetch.c — fetch and decode the next instruction
 */
#include "display.h"
#include "madm.h"
#include "proto.h"

void
fetch_instruction(void)
{
	control[PI_LINE] = store[(Addr)(++control[CI_LINE] & MAX_ADDR)];

	display_line(C_TUBE, CI_LINE);
	display_line(C_TUBE, PI_LINE);

	staticisor.addr = (Addr)(control[PI_LINE] & MAX_ADDR);
	staticisor.func = (uint8_t)((control[PI_LINE] >> ADDR_BITS) & MAX_FUNC);
}
