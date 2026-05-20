/*
 * IBM CGA colours for mode 'm' (320x200) as in GRAPHICS.C.
 *
 * display_line() uses set_up_line/show_line: 0x80 = dim dot, 0xF0 = bright dash.
 * On a real CGA with the usual alt palette (magenta/cyan/white), 0x80 reads as
 * magenta (#AA00AA), not red — same pink dots as 86Box/DOS.
 *
 * blob() uses color('r') for the dim pixel; that matches the 0x80 dot on hardware.
 */
#ifndef CGA_COLORS_H
#define CGA_COLORS_H

#define CGA_BLACK_R 0
#define CGA_BLACK_G 0
#define CGA_BLACK_B 0

/* scanline 0x80 / color('r') dim dot — IBM CGA magenta #AA00AA */
#define CGA_DIM_R 170
#define CGA_DIM_G 0
#define CGA_DIM_B 170

/* scanline 0xF0 / color('w') bright dash — high-intensity white */
#define CGA_BRIGHT_R 255
#define CGA_BRIGHT_G 255
#define CGA_BRIGHT_B 255

#endif
