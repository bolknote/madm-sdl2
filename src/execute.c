/*
 * execute.c — instruction execution loop
 */
#include "keyboard.h"
#include "madm.h"
#include "proto.h"

typedef struct {
	uint32_t steps_per_present;
	unsigned delay;
} RunSpeed;

static const RunSpeed run_speeds[] = {
	{1, 80},
	{2, 60},
	{4, 45},
	{8, 35},
	{16, 25},
	{32, 18},
	{64, 12},
	{128, 8},
	{256, 4},
	{0x800, 0},
	{0x2000, 0},
	{0x8000, 0},
};

static unsigned run_speed = 9;

void
madm_speed_faster(void)
{
	if (run_speed + 1 < sizeof run_speeds / sizeof run_speeds[0])
		run_speed++;
}

void
madm_speed_slower(void)
{
	if (run_speed > 0)
		run_speed--;
}

static int
handle_run_command(void)
{
	int cmd;

	if (!cmd_ready())
		return 0;

	cmd = peek_cmd();
	if (cmd == FASTER_CMD || cmd == SLOWER_CMD) {
		(void)next_cmd();
		if (cmd == FASTER_CMD)
			madm_speed_faster();
		else
			madm_speed_slower();
		return 0;
	}

	return 1;
}

static void
present_at_run_speed(void)
{
	madm_present();
	if (run_speeds[run_speed].delay != 0)
		delay_ms(run_speeds[run_speed].delay);
}

void
execute(void)
{
	uint32_t steps = 0;

	do {
		fetch_instruction();
		exec_instruction();
		steps++;
		if (madm_status == MADM_MANUAL)
			madm_present();
		else if ((steps % run_speeds[run_speed].steps_per_present) == 0)
			present_at_run_speed();
	} while (madm_status == MADM_RUNNING && !handle_run_command());
	madm_present();
}
