#ifndef MADM_PROTO_H
#define MADM_PROTO_H

#include "madm.h"

/* arithmetic */
void subtract(Addr s);

/* control */
void stop(Addr s);
void unused(Addr s);
void test(Addr s);
void jump(Addr s);
void rjump(Addr s);

/* cursor / editing */
void show_cursor(void);
void erase_cursor(void);
void place_cursor(Addr line, unsigned bit);
void move_cursor(int d_line, int d_bit);
void toggle_current_bit(void);
void display_current_bit(void);
int edit(void);
void toggle_bit(Addr line, unsigned bit);

/* display */
void display_bit(unsigned tube, Addr line, unsigned bit);
void display_line(unsigned tube, Addr line);

/* execution */
void exec_instruction(void);
void execute(void);
void fetch_instruction(void);
void madm_speed_faster(void);
void madm_speed_slower(void);

/* platform graphics */
void set_up_graphics(void);
void clear_graphics(void);
void blob(int value, unsigned x, unsigned y);
void set_up_line(Line value);
void show_line(unsigned x, unsigned y);
void draw_box(int visible, unsigned lo_x, unsigned lo_y, unsigned hi_x, unsigned hi_y);
void madm_present(void);
void madm_redraw_chrome(void);
void madm_redraw_all(void);
void madm_draw_cursor(void);

/* init */
void initialize(void);
void clean_up(void);
void process_options(int argc, char *argv[]);

/* memory */
void load_negative(Addr s);
void store_accumulator(Addr s);

#endif /* MADM_PROTO_H */
