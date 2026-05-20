/*
 * init.c — startup, demo program, store file loading
 */
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "display.h"
#include "madm.h"
#include "proto.h"

static const char *load_path;
static bool ci_start_minus_one;

static int
load_store_file(const char *path)
{
	FILE *fp = fopen(path, "r");
	char buf[128];

	if (!fp) {
		perror(path);
		return -1;
	}

	for (Addr seq = 0; fgets(buf, sizeof buf, fp);) {
		char *p = buf;
		Addr line;
		Line value;
		char *end;

		while (*p != '\0' && isspace((unsigned char)*p))
			p++;
		if (*p == '\0')
			continue;
		if (*p == '#') {
			if (strstr(p, "ci-start") != NULL &&
			    strstr(p, "-1") != NULL)
				ci_start_minus_one = true;
			continue;
		}

		if (*p == '@') {
			line = (Addr)strtol(p + 1, &end, 0);
			p = end;
			while (*p != '\0' && isspace((unsigned char)*p))
				p++;
		} else {
			line = seq++;
		}

		if (line >= STORE_SIZE) {
			fprintf(stderr, "%s: store line %u out of range\n", path, line);
			fclose(fp);
			return -1;
		}

		value = (Line)strtol(p, NULL, 0);
		store[line] = value;
	}

	fclose(fp);
	return 0;
}

static void
refresh_store_display(void)
{
	for (Addr line = 0; line < STORE_SIZE; line++)
		display_line(S_TUBE, line);
}

void
initialize(void)
{
	if (load_path != NULL) {
		if (load_store_file(load_path) != 0)
			exit(EXIT_FAILURE);
		if (ci_start_minus_one)
			control[CI_LINE] = -1;
		refresh_store_display();
	}

	set_up_graphics();
	madm_present();
}

void
clean_up(void)
{
	clear_graphics();
}

void
process_options(int argc, char *argv[])
{
	for (int i = 1; i < argc; i++) {
		if (argv[i][0] != '-' || argv[i][1] == '\0') {
			fprintf(stderr, "%s: unknown option\n", argv[i]);
			exit(EXIT_FAILURE);
		}
		switch (tolower((unsigned char)argv[i][1])) {
		case 'f':
			if (argv[i][2] != '\0')
				load_path = argv[i] + 2;
			else if (i + 1 < argc)
				load_path = argv[++i];
			else {
				fprintf(stderr, "%s: -f requires a file name\n", argv[i]);
				exit(EXIT_FAILURE);
			}
			break;
		default:
			fprintf(stderr, "%s: unknown option\n", argv[i]);
			exit(EXIT_FAILURE);
		}
	}
}
