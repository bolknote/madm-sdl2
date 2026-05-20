/*
 * exec_ins.c — execute the present instruction
 */
#include "madm.h"
#include "proto.h"

typedef void (*ExecFunc)(Addr);

static void (*const optab[])(Addr) = {
	jump,
	rjump,
	load_negative,
	store_accumulator,
	subtract,
	subtract, /* undocumented duplicate of subtract */
	test,
	stop,
};

void
exec_instruction(void)
{
	const unsigned func = staticisor.func;

	if (func >= sizeof optab / sizeof optab[0]) {
		unused(staticisor.addr);
		return;
	}
	optab[func](staticisor.addr);
}
