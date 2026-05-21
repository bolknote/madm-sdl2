/*
 * unit.c -- small regression tests for the machine core and store loader
 */
#include <inttypes.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include "madm.h"
#include "proto.h"

#define TEST_STORE_PATH ".build/tests/store_input.store"

static unsigned failures;

void
display_line(unsigned tube, Addr line)
{
	(void)tube;
	(void)line;
}

void
set_up_graphics(void)
{
}

void
clear_graphics(void)
{
}

void
madm_present(void)
{
}

int
madm_next_cmd(void)
{
	return 0;
}

int
madm_cmd_ready(void)
{
	return 0;
}

int
madm_peek_cmd(void)
{
	return -1;
}

void
madm_delay_ms(unsigned ms)
{
	(void)ms;
}

void
madm_speed_faster(void)
{
}

void
madm_speed_slower(void)
{
}

void
erase_cursor(void)
{
}

void
place_cursor(Addr line, unsigned bit)
{
	(void)line;
	(void)bit;
}

void
move_cursor(int d_line, int d_bit)
{
	(void)d_line;
	(void)d_bit;
}

void
toggle_current_bit(void)
{
}

static void
fail_at(int line, const char *expr)
{
	fprintf(stderr, "tests/unit.c:%d: check failed: %s\n", line, expr);
	failures++;
}

static void
expect_line_at(int line, const char *expr, Line got, Line want)
{
	if (got != want) {
		fprintf(stderr,
			"tests/unit.c:%d: %s: got 0x%08" PRIx32 ", want 0x%08" PRIx32 "\n",
			line,
			expr,
			got,
			want);
		failures++;
	}
}

#define CHECK(expr) \
	do { \
		if (!(expr)) \
			fail_at(__LINE__, #expr); \
	} while (0)

#define EXPECT_LINE(got, want) expect_line_at(__LINE__, #got, (got), (want))

static void
reset_machine(void)
{
	memset(accumulator, 0, sizeof accumulator);
	memset(control, 0, sizeof control);
	memset(store, 0, sizeof store);
	memset(&staticisor, 0, sizeof staticisor);
	madm_status = MADM_STOPPED;
}

static void
write_store_file(const char *text)
{
	FILE *fp = fopen(TEST_STORE_PATH, "w");

	if (!fp) {
		perror(TEST_STORE_PATH);
		exit(EXIT_FAILURE);
	}
	if (fputs(text, fp) == EOF) {
		perror(TEST_STORE_PATH);
		fclose(fp);
		exit(EXIT_FAILURE);
	}
	if (fclose(fp) != 0) {
		perror(TEST_STORE_PATH);
		exit(EXIT_FAILURE);
	}
}

static void
expect_store_rejected(const char *text)
{
	int saved_stderr;
	FILE *devnull;
	int rc;

	reset_machine();
	write_store_file(text);
	fflush(stderr);
	saved_stderr = dup(STDERR_FILENO);
	devnull = fopen("/dev/null", "w");
	if (saved_stderr < 0 || !devnull || dup2(fileno(devnull), STDERR_FILENO) < 0) {
		perror("stderr redirect");
		exit(EXIT_FAILURE);
	}
	rc = madm_load_store_file(TEST_STORE_PATH, NULL);
	fflush(stderr);
	if (dup2(saved_stderr, STDERR_FILENO) < 0) {
		perror("stderr restore");
		exit(EXIT_FAILURE);
	}
	close(saved_stderr);
	fclose(devnull);

	CHECK(rc != 0);
}

static void
test_wrapping_arithmetic(void)
{
	reset_machine();

	store[0] = 1;
	subtract(0);
	EXPECT_LINE(accumulator[A_LINE], MAX_LINE);

	store[0] = LINE_SIGN_BIT;
	load_negative(0);
	EXPECT_LINE(accumulator[A_LINE], LINE_SIGN_BIT);

	control[CI_LINE] = MAX_LINE;
	store[0] = 2;
	rjump(0);
	EXPECT_LINE(control[CI_LINE], 1);
}

static void
test_sign_bit_cmp(void)
{
	reset_machine();

	accumulator[A_LINE] = LINE_SIGN_BIT;
	control[CI_LINE] = 4;
	test(0);
	EXPECT_LINE(control[CI_LINE], 5);

	accumulator[A_LINE] = LINE_SIGN_BIT - 1;
	test(0);
	EXPECT_LINE(control[CI_LINE], 5);
}

static void
test_fetch_wrap_and_decode(void)
{
	reset_machine();

	control[CI_LINE] = MAX_LINE;
	store[0] = (Line)((6u << ADDR_BITS) | 7u);
	fetch_instruction();

	EXPECT_LINE(control[CI_LINE], 0);
	EXPECT_LINE(control[PI_LINE], store[0]);
	CHECK(staticisor.func == 6);
	CHECK(staticisor.addr == 7);
}

static void
test_toggle_bit_31(void)
{
	reset_machine();

	toggle_bit(0, 31);
	EXPECT_LINE(store[0], LINE_SIGN_BIT);
	toggle_bit(0, 31);
	EXPECT_LINE(store[0], 0);
	toggle_bit(0, LINE_BITS);
	EXPECT_LINE(store[0], 0);
}

static void
test_store_loader_accepts_word_edges(void)
{
	bool ci_start_minus_one = true;

	reset_machine();
	write_store_file(
		"@0 -1\n"
		"@1 0xffffffff\n"
		"@31 -2147483648 # min signed 32-bit value\n");

	CHECK(madm_load_store_file(TEST_STORE_PATH, &ci_start_minus_one) == 0);
	CHECK(!ci_start_minus_one);
	EXPECT_LINE(store[0], MAX_LINE);
	EXPECT_LINE(store[1], MAX_LINE);
	EXPECT_LINE(store[31], LINE_SIGN_BIT);
}

static void
test_store_loader_ci_start_metadata(void)
{
	bool ci_start_minus_one = false;

	reset_machine();
	write_store_file(
		"# not-ci-start -1\n"
		"# ci-start -1\n"
		"@0 0\n");

	CHECK(madm_load_store_file(TEST_STORE_PATH, &ci_start_minus_one) == 0);
	CHECK(ci_start_minus_one);

	ci_start_minus_one = true;
	write_store_file(
		"# ci-start -1 but not really\n"
		"@0 0\n");

	CHECK(madm_load_store_file(TEST_STORE_PATH, &ci_start_minus_one) == 0);
	CHECK(!ci_start_minus_one);
}

static void
test_store_loader_rejects_bad_input(void)
{
	expect_store_rejected("@256 0\n");
	expect_store_rejected("@0 4294967296\n");
	expect_store_rejected("@0 -2147483649\n");
	expect_store_rejected("@0 1 trailing\n");
	expect_store_rejected("@0\n");
	expect_store_rejected(
		"0\n0\n0\n0\n0\n0\n0\n0\n"
		"0\n0\n0\n0\n0\n0\n0\n0\n"
		"0\n0\n0\n0\n0\n0\n0\n0\n"
		"0\n0\n0\n0\n0\n0\n0\n0\n"
		"0\n");
}

int
main(void)
{
	test_wrapping_arithmetic();
	test_sign_bit_cmp();
	test_fetch_wrap_and_decode();
	test_toggle_bit_31();
	test_store_loader_accepts_word_edges();
	test_store_loader_ci_start_metadata();
	test_store_loader_rejects_bad_input();

	remove(TEST_STORE_PATH);
	if (failures != 0) {
		fprintf(stderr, "%u test(s) failed\n", failures);
		return EXIT_FAILURE;
	}
	puts("unit tests passed");
	return EXIT_SUCCESS;
}
