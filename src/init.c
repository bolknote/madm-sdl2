/*
 * init.c — startup, demo program, store file loading
 */
#include <ctype.h>
#include <errno.h>
#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "madm.h"
#include "proto.h"

static const char *load_path;

static char *
skip_space(char *p)
{
	while (*p != '\0' && isspace((unsigned char)*p))
		p++;
	return p;
}

static bool
is_ci_start_minus_one(char *p)
{
	static const char directive[] = "ci-start";
	char *end;
	long n;

	p = skip_space(p);
	if (strncmp(p, directive, sizeof directive - 1) != 0)
		return false;
	p += sizeof directive - 1;
	if (!isspace((unsigned char)*p))
		return false;

	p = skip_space(p);
	errno = 0;
	n = strtol(p, &end, 0);
	if (end == p || errno == ERANGE || n != -1)
		return false;

	end = skip_space(end);
	return *end == '\0';
}

static int
reject_trailing_text(const char *path, unsigned input_line, char *p)
{
	p = skip_space(p);
	if (*p == '#' || *p == '\0')
		return 0;
	fprintf(stderr, "%s:%u: trailing text after store value\n", path, input_line);
	return -1;
}

static int
parse_store_addr(const char *path, unsigned input_line, const char *p, char **end, Addr *line)
{
	unsigned long n;

	errno = 0;
	n = strtoul(p, end, 0);
	if (*end == p || errno == ERANGE || n >= STORE_SIZE) {
		fprintf(stderr, "%s:%u: store line out of range\n", path, input_line);
		return -1;
	}
	*line = (Addr)n;
	return 0;
}

static int
parse_store_value(const char *path, unsigned input_line, const char *p, char **end, Line *value)
{
	if (*p == '-') {
		long long n;

		errno = 0;
		n = strtoll(p, end, 0);
		if (*end == p || errno == ERANGE || n < INT32_MIN) {
			fprintf(stderr, "%s:%u: signed store value out of range\n", path, input_line);
			return -1;
		}
		*value = (Line)n;
		return 0;
	}

	{
		unsigned long long n;

		errno = 0;
		n = strtoull(p, end, 0);
		if (*end == p || errno == ERANGE || n > MAX_LINE) {
			fprintf(stderr, "%s:%u: store value out of range\n", path, input_line);
			return -1;
		}
		*value = (Line)n;
		return 0;
	}
}

int
madm_load_store_file(const char *path, bool *ci_start_minus_one)
{
	FILE *fp = fopen(path, "r");
	char buf[128];
	unsigned input_line = 0;
	unsigned seq = 0;
	bool found_ci_start_minus_one = false;

	if (!fp) {
		perror(path);
		return -1;
	}

	while (fgets(buf, sizeof buf, fp)) {
		char *p = buf;
		Addr line;
		Line value;
		char *end;

		input_line++;
		if (strchr(buf, '\n') == NULL && !feof(fp)) {
			fprintf(stderr, "%s:%u: line too long\n", path, input_line);
			fclose(fp);
			return -1;
		}

		p = skip_space(p);
		if (*p == '\0')
			continue;
		if (*p == '#') {
			if (is_ci_start_minus_one(p + 1))
				found_ci_start_minus_one = true;
			continue;
		}

		if (*p == '@') {
			p = skip_space(p + 1);
			if (parse_store_addr(path, input_line, p, &end, &line) != 0) {
				fclose(fp);
				return -1;
			}
			p = skip_space(end);
		} else {
			if (seq >= STORE_SIZE) {
				fprintf(stderr, "%s:%u: too many store lines\n", path, input_line);
				fclose(fp);
				return -1;
			}
			line = (Addr)seq++;
		}

		if (parse_store_value(path, input_line, p, &end, &value) != 0 ||
		    reject_trailing_text(path, input_line, end) != 0) {
			fclose(fp);
			return -1;
		}

		store[line] = value;
	}

	fclose(fp);
	if (ci_start_minus_one != NULL)
		*ci_start_minus_one = found_ci_start_minus_one;
	return 0;
}

void
initialize(void)
{
	if (load_path != NULL) {
		bool ci_start_minus_one = false;

		if (madm_load_store_file(load_path, &ci_start_minus_one) != 0)
			exit(EXIT_FAILURE);
		if (ci_start_minus_one)
			control[CI_LINE] = MAX_LINE;
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
process_options(int argc, char *const *const argv)
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
