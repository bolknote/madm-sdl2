/*
 * cursor.c — store editing cursor
 */
#include "display.h"
#include "graphics.h"
#include "proto.h"

typedef struct {
	Addr line;
	unsigned bit;
	unsigned x;
	unsigned y;
} Cursor;

static Cursor cursor = {
	0, 0,
	S_X - 1,
	S_Y - 1
};

static void
cursor_sync_coords(void)
{
	cursor.x = S_X - 1 + cursor.bit * (BLOB_WIDTH + H_SPACE)
			   + (cursor.bit / 4) * XH_SPACE + (cursor.bit / 16) * (2 * XH_SPACE);
	cursor.y = S_Y - 1 - cursor.line * (BLOB_HEIGHT + V_SPACE)
			   - (cursor.line / 4) * XV_SPACE;
}

void
madm_draw_cursor(void)
{
	cursor_sync_coords();
	draw_box(1, cursor.x, cursor.y, cursor.x + BLOB_WIDTH + 1, cursor.y + BLOB_HEIGHT + 1);
}

void
show_cursor(void)
{
	madm_draw_cursor();
}

void
erase_cursor(void)
{
	/* full-frame redraw clears the old cursor */
}

void
place_cursor(Addr line, unsigned bit)
{
	cursor.line = (Addr)(line % STORE_SIZE);
	cursor.bit = bit % LINE_BITS;
	cursor_sync_coords();
	madm_present();
}

void
move_cursor(int d_line, int d_bit)
{
	place_cursor((Addr)((int)cursor.line + d_line),
				 (unsigned)((int)cursor.bit + d_bit));
}

void
toggle_current_bit(void)
{
	toggle_bit(cursor.line, cursor.bit);
}

void
display_current_bit(void)
{
	display_bit(S_TUBE, cursor.line, cursor.bit);
}
