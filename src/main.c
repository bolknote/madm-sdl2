/*
 * main.c — Manchester Prototype main program
 */
#include <stdlib.h>

#include "madm.h"
#include "proto.h"

int
main(int argc, char *argv[])
{
	process_options(argc, argv);
	initialize();

	while (edit())
		execute();

	clean_up();
	return EXIT_SUCCESS;
}
