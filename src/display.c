/*
 * display.c — Williams tube display on the monitor
 */
#include "display.h"
#include "graphics.h"
#include "proto.h"

MonitorTube monitors[NUM_MONITORS] = {
	{A_X, A_Y, accumulator},
	{C_X, C_Y, control},
	{S_X, S_Y, store},
};

void
display_bit(unsigned tube, Addr line, unsigned bit)
{
	const MonitorTube *mt = &monitors[tube];
	const unsigned x = mt->x + bit * (BLOB_WIDTH + H_SPACE) + (bit / 4) * XH_SPACE
					   + (bit / 16) * (2 * XH_SPACE);
	const unsigned y = mt->y - line * (BLOB_HEIGHT + V_SPACE) - (line / 4) * XV_SPACE;

	blob((int)((mt->values[line] >> bit) & 1), x, y);
}

void
display_line(unsigned tube, Addr line)
{
	const MonitorTube *mt = &monitors[tube];
	const unsigned y = mt->y - line * (BLOB_HEIGHT + V_SPACE) - (line / 4) * XV_SPACE;

	set_up_line(mt->values[line]);
	show_line(mt->x, y);
}
