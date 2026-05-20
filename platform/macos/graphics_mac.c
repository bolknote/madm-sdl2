/*
 * graphics_mac.c -- SDL2 graphics for Manchester Mark I prototype simulator
 *
 * Full-frame redraw each present (required on macOS Metal backend).
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <SDL.h>

#include "madm.h"
#include "graphics_mac.h"
#include "display.h"
#include "proto.h"
#include "keyboard_mac.h"
#include "font8x8_basic.h"
#include "cga_colors.h"

#define WIN_SCALE 3
/* 8×8 labels at native CGA coordinates (see GRAPHICS.C); window scaled via logical size */
#define FONT_SCALE 1
#define FONT_CELL_W CHAR_WIDTH

static SDL_Window *window;
static SDL_Renderer *renderer;
static Line line_value;

/* bottom-left machine y -> SDL logical y (origin top-left) */
static int to_sdl_y(unsigned machine_y)
{
	return (int)(V_DOTS - 1 - machine_y);
}

static void set_cga_color(int r, int g, int b)
{
	SDL_SetRenderDrawColor(renderer, (Uint8)r, (Uint8)g, (Uint8)b, 255);
}

/* GRAPHICS.C point(x,y): one logical pixel */
static void cga_point(int x, int machine_y)
{
	SDL_RenderDrawPoint(renderer, x, to_sdl_y((unsigned)machine_y));
}

/*
 * GRAPHICS.C blob() — order and colors exactly:
 *   nonzero: color('w'); point(x+1,y); point(x,y);
 *   zero:    color(0);  point(x+1,y); color('r'); point(x,y);
 */
static void blob_at(int value, int x, int machine_y)
{
	if (value != 0) {
		set_cga_color(CGA_BRIGHT_R, CGA_BRIGHT_G, CGA_BRIGHT_B);
		cga_point(x + 1, machine_y);
		cga_point(x, machine_y);
	} else {
		set_cga_color(CGA_BLACK_R, CGA_BLACK_G, CGA_BLACK_B);
		cga_point(x + 1, machine_y);
		set_cga_color(CGA_DIM_R, CGA_DIM_G, CGA_DIM_B);
		cga_point(x, machine_y);
	}
}

/*
 * Original show_label (graphics.h): scr_curs(NUM_ROWS-1-(y/CHAR_HEIGHT), x/CHAR_WIDTH)
 * then scr_puts — y is a bottom-left pixel coord, not the glyph top.
 */
static int label_row_top(unsigned y)
{
	int row = (int)(NUM_ROWS - 1 - (y / CHAR_HEIGHT));
	return (int)(V_DOTS - 1 - (unsigned)(row * CHAR_HEIGHT));
}

/* font8x8_basic: LSB of each row is the leftmost pixel */
static void draw_char(int px, int py_top, char ch)
{
	const unsigned char *glyph;
	int row, col;

	if ((unsigned char)ch >= 128)
		return;
	glyph = (const unsigned char *)font8x8_basic[(unsigned char)ch];
	set_cga_color(CGA_BRIGHT_R, CGA_BRIGHT_G, CGA_BRIGHT_B);
	{
		int sy_top = to_sdl_y((unsigned)py_top);
		for (row = 0; row < 8; row++) {
			unsigned char bits = (unsigned char)glyph[row];
			int sy = sy_top + row * FONT_SCALE;
			for (col = 0; col < 8; col++) {
				if ((bits >> col) & 1) {
					SDL_Rect r = {
						px + col * FONT_SCALE,
						sy,
						FONT_SCALE,
						FONT_SCALE};
					SDL_RenderFillRect(renderer, &r);
				}
			}
		}
	}
}

void show_label(unsigned x, unsigned y, const char *label)
{
	unsigned cx = x;
	int py_top = label_row_top(y);

	for (; *label; label++) {
		draw_char((int)cx, py_top, *label);
		cx += CHAR_WIDTH;
	}
}

void madm_redraw_chrome(void)
{
	const char main_title[] = "Manchester Mark I Prototype";
	const char sub_title[] = "(1948)";

	/* Same layout as GRAPHICS.C set_up_graphics() */
	show_label((H_DOTS - (unsigned)sizeof(main_title) * CHAR_WIDTH) / 2,
			   V_DOTS - 1,
			   main_title);
	show_label((H_DOTS - (unsigned)sizeof(sub_title) * CHAR_WIDTH) / 2,
			   V_DOTS - 1 - CHAR_WIDTH,
			   sub_title);

	show_label(A_X - CHAR_WIDTH, C_Y + CHAR_HEIGHT, "A:");
	show_label(C_X - CHAR_WIDTH, C_Y + CHAR_HEIGHT, "C:");
	show_label(S_X - CHAR_WIDTH, S_Y + CHAR_HEIGHT, "S:");
}

void madm_redraw_all(void)
{
	set_cga_color(CGA_BLACK_R, CGA_BLACK_G, CGA_BLACK_B);
	SDL_RenderClear(renderer);

	display_line(A_TUBE, A_LINE);
	for (Addr line = 0; line < CONTROL_SIZE; line++)
		display_line(C_TUBE, line);
	for (Addr line = 0; line < STORE_SIZE; line++)
		display_line(S_TUBE, line);

	madm_redraw_chrome();
	madm_draw_cursor();
}

void madm_present(void)
{
	madm_redraw_all();
	madm_pump_keyboard();
	SDL_RenderPresent(renderer);
}

void set_up_graphics(void)
{
	if (SDL_Init(SDL_INIT_VIDEO) < 0) {
		fprintf(stderr, "SDL_Init: %s\n", SDL_GetError());
		exit(1);
	}

	window = SDL_CreateWindow(
		"MADM — Manchester Mark I Prototype (1948)",
		SDL_WINDOWPOS_CENTERED,
		SDL_WINDOWPOS_CENTERED,
		H_DOTS * WIN_SCALE,
		V_DOTS * WIN_SCALE,
		SDL_WINDOW_ALLOW_HIGHDPI);
	if (!window) {
		fprintf(stderr, "SDL_CreateWindow: %s\n", SDL_GetError());
		exit(1);
	}

	renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);
	if (!renderer) {
		fprintf(stderr, "SDL_CreateRenderer: %s\n", SDL_GetError());
		exit(1);
	}

	SDL_RenderSetLogicalSize(renderer, H_DOTS, V_DOTS);
	SDL_RenderSetIntegerScale(renderer, SDL_TRUE);
}

void clear_graphics(void)
{
	if (renderer)
		SDL_DestroyRenderer(renderer);
	if (window)
		SDL_DestroyWindow(window);
	SDL_Quit();
}

void blob(int value, unsigned x, unsigned y)
{
	blob_at(value, (int)x, (int)y);
}

void set_up_line(Line value)
{
	line_value = value;
}

void show_line(unsigned x, unsigned y)
{
	unsigned bit;
	Line v = line_value;

	for (bit = 0; bit < LINE_BITS; bit++) {
		blob_at((int)((v >> bit) & 1),
				(int)(x + bit * (BLOB_WIDTH + H_SPACE) + (bit / 4) * XH_SPACE
					  + (bit / 16) * (2 * XH_SPACE)),
				(int)y);
	}
}

void draw_box(int visible, unsigned lo_x, unsigned lo_y, unsigned hi_x, unsigned hi_y)
{
	int left, right, top, bottom;

	if (!visible)
		return;

	/* GRAPHICS.C: line(lo_x,lo_y)->(hi_x,lo_y)->(hi_x,hi_y)->(lo_x,hi_y); no extra padding */
	left = (int)lo_x;
	right = (int)hi_x;
	top = to_sdl_y(hi_y);
	bottom = to_sdl_y(lo_y);

	set_cga_color(CGA_BRIGHT_R, CGA_BRIGHT_G, CGA_BRIGHT_B);
	SDL_RenderDrawLine(renderer, left, top, right, top);
	SDL_RenderDrawLine(renderer, left, bottom, right, bottom);
	SDL_RenderDrawLine(renderer, left, top, left, bottom);
	SDL_RenderDrawLine(renderer, right, top, right, bottom);
}
