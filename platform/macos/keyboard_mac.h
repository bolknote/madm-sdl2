/*
 * keyboard_mac.h -- SDL2 keyboard for Manchester Mark I simulator (macOS)
 */
#ifndef KEYBOARD_MAC_H
#define KEYBOARD_MAC_H

#define START_CMD '\r'
#define SSTEP_CMD 's'
#define CLEAR_CMD 'c'
#define CLR_AC_CMD 'k'
#define TOGGLE_CMD ' '
#define QUIT_CMD '\033'

/* Distinct codes (not IBM scan codes) — mapped from SDL keys in keyboard_mac.c */
#define UP_CMD 0x100
#define DOWN_CMD 0x101
#define RIGHT_CMD 0x102
#define LEFT_CMD 0x103

#define next_cmd() madm_next_cmd()
#define cmd_ready() madm_cmd_ready()

int madm_next_cmd(void);
int madm_cmd_ready(void);
void madm_pump_keyboard(void);

#endif
