/*
 * edit.c — keyboard-driven program editing
 */
#include "display.h"
#include "keyboard.h"
#include "madm.h"
#include "proto.h"

int
edit(void)
{
	place_cursor((Addr)control[CI_LINE], 0);

	for (;;) {
		switch (next_cmd()) {
		case QUIT_CMD:
			erase_cursor();
			return 0;
		case START_CMD:
			erase_cursor();
			madm_status = MADM_RUNNING;
			return 1;
		case SSTEP_CMD:
			erase_cursor();
			madm_status = MADM_MANUAL;
			return 1;
		case FASTER_CMD:
			madm_speed_faster();
			break;
		case SLOWER_CMD:
			madm_speed_slower();
			break;
		case CLEAR_CMD:
			for (Addr line = 0; line < STORE_SIZE; line++) {
				store[line] = 0;
				display_line(S_TUBE, line);
			}
			madm_present();
			break;
		case CLR_AC_CMD:
			accumulator[A_LINE] = control[CI_LINE] = control[PI_LINE] = 0;
			display_line(A_TUBE, A_LINE);
			display_line(C_TUBE, CI_LINE);
			display_line(C_TUBE, PI_LINE);
			place_cursor(0, 0);
			break;
		case TOGGLE_CMD:
			toggle_current_bit();
			madm_present();
			break;
		case UP_CMD:
			move_cursor(-1, 0);
			break;
		case DOWN_CMD:
			move_cursor(1, 0);
			break;
		case LEFT_CMD:
			move_cursor(0, -1);
			break;
		case RIGHT_CMD:
			move_cursor(0, 1);
			break;
		default:
			break;
		}
	}
}

void
toggle_bit(Addr line, unsigned bit)
{
	if (bit < LINE_BITS)
		store[line] ^= (Line)(INT32_C(1) << bit);
}
