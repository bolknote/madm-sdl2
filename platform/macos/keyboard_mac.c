/*
 * keyboard_mac.c — SDL2 keyboard input
 */
#include <stdbool.h>

#include <SDL.h>

#include "keyboard_mac.h"

static int pending_key = -1;
static bool have_pending;

static int
map_sdl_key(SDL_Keycode sym)
{
	switch (sym) {
	case SDLK_RETURN:
	case SDLK_KP_ENTER:
		return START_CMD;
	case SDLK_ESCAPE:
		return QUIT_CMD;
	case SDLK_SPACE:
		return TOGGLE_CMD;
	case SDLK_PLUS:
	case SDLK_EQUALS:
	case SDLK_KP_PLUS:
		return FASTER_CMD;
	case SDLK_MINUS:
	case SDLK_KP_MINUS:
		return SLOWER_CMD;
	case SDLK_UP:
		return UP_CMD;
	case SDLK_DOWN:
		return DOWN_CMD;
	case SDLK_LEFT:
		return LEFT_CMD;
	case SDLK_RIGHT:
		return RIGHT_CMD;
	default:
		if (sym >= SDLK_a && sym <= SDLK_z)
			return (int)('a' + (sym - SDLK_a));
		return -1;
	}
}

void
madm_pump_keyboard(void)
{
	SDL_Event e;

	while (SDL_PollEvent(&e)) {
		if (e.type == SDL_QUIT) {
			have_pending = true;
			pending_key = QUIT_CMD;
			return;
		}
		if (e.type == SDL_KEYDOWN && !have_pending) {
			int k = map_sdl_key(e.key.keysym.sym);
			if (k >= 0) {
				have_pending = true;
				pending_key = k;
			}
		}
	}
}

int
madm_cmd_ready(void)
{
	madm_pump_keyboard();
	return have_pending;
}

int
madm_peek_cmd(void)
{
	return madm_cmd_ready() ? pending_key : -1;
}

int
madm_next_cmd(void)
{
	while (!madm_cmd_ready())
		SDL_Delay(16);

	{
		int k = pending_key;
		have_pending = false;
		pending_key = -1;
		return k;
	}
}

void
madm_delay_ms(unsigned ms)
{
	SDL_Delay(ms);
}
