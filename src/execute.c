/*
 * execute.c — instruction execution loop
 */
#include "keyboard.h"
#include "madm.h"
#include "proto.h"

void
execute(void)
{
	uint32_t steps = 0;

	do {
		fetch_instruction();
		exec_instruction();
		steps++;
		if (madm_status == MADM_MANUAL || (steps & 0x7FFu) == 0)
			madm_present();
	} while (madm_status == MADM_RUNNING && !cmd_ready());
	madm_present();
}
