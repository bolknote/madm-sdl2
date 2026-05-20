/*
 * display.h — monitor tube layout (machine-independent geometry)
 */
#ifndef DISPLAY_H
#define DISPLAY_H

#include "graphics.h"
#include "madm.h"

typedef struct {
	uint16_t x;
	uint16_t y;
	Line *values;
} MonitorTube;

enum {
	TUBE_A = 0,
	TUBE_C = 1,
	TUBE_S = 2,
	NUM_MONITORS = 3
};

#define A_TUBE TUBE_A
#define C_TUBE TUBE_C
#define S_TUBE TUBE_S

#define A_X \
	((H_DOTS - 2 * LINE_WIDTH) / 3 - ((H_DOTS - 2 * LINE_WIDTH) / 3) % DOTS_PER_BYTE)
#define A_Y (3 * V_DOTS / 4)
#define C_X \
	((H_DOTS - A_X - LINE_WIDTH) - (H_DOTS - A_X - LINE_WIDTH) % DOTS_PER_BYTE)
#define C_Y (A_Y + 2)
#define S_X \
	((H_DOTS - LINE_WIDTH) / 2 - ((H_DOTS - LINE_WIDTH) / 2) % DOTS_PER_BYTE)
#define S_Y (V_DOTS / 2)

extern MonitorTube monitors[NUM_MONITORS];

#endif /* DISPLAY_H */
