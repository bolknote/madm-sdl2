/*
 * graphics_mac.h — SDL2 display layout (CGA geometry)
 */
#ifndef GRAPHICS_MAC_H
#define GRAPHICS_MAC_H

#include <stdint.h>

#include "madm.h"

#define H_DOTS 320
#define V_DOTS 200

#define DOTS_PER_BYTE 4

#define BLOB_WIDTH 2
#define BLOB_HEIGHT 1

#define H_SPACE 2
#define V_SPACE 2

#define XH_SPACE 0
#define XV_SPACE 0

#define LINE_WIDTH \
	(BLOB_WIDTH * LINE_BITS + H_SPACE * (LINE_BITS - 1) + XH_SPACE * (LINE_BITS / 4 - 1) + XH_SPACE * 2)

#define CHAR_WIDTH 8
#define CHAR_HEIGHT 8

#define NUM_ROWS (V_DOTS / CHAR_HEIGHT)
#define NUM_COLS (H_DOTS / CHAR_WIDTH)

void show_label(unsigned x, unsigned y, const char *label);
void madm_present(void);
void madm_redraw_chrome(void);
void madm_redraw_all(void);
void madm_draw_cursor(void);
void set_up_graphics(void);
void clear_graphics(void);
void blob(int value, unsigned x, unsigned y);
void set_up_line(Line value);
void show_line(unsigned x, unsigned y);
void draw_box(int visible, unsigned lo_x, unsigned lo_y, unsigned hi_x, unsigned hi_y);

#endif /* GRAPHICS_MAC_H */
