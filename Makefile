# MADM — Manchester Mark I prototype (macOS/SDL2).  brew install sdl2

APP := madm
CC  ?= cc

SRC := $(wildcard src/*.c platform/macos/*.c)
OBJ := $(SRC:.c=.o)
SAN_APP := $(APP)-sanitize
SAN_BUILD_DIR := .build/sanitize
SAN_OBJ := $(addprefix $(SAN_BUILD_DIR)/,$(SRC:.c=.o))
TEST_APP := .build/tests/unit
TEST_SAN_APP := .build/tests/unit-sanitize
TEST_SRC := tests/unit.c src/arith.c src/control.c src/edit.c src/fetch.c src/init.c src/madm.c src/memory.c

SDL_CFLAGS := $(shell pkg-config --cflags sdl2 2>/dev/null)
SDL_LIBS   := $(shell pkg-config --libs sdl2 2>/dev/null)
ifeq ($(SDL_LIBS),)
  SDL_CFLAGS := -I/opt/homebrew/include/SDL2 -D_THREAD_SAFE
  SDL_LIBS   := -L/opt/homebrew/lib -lSDL2
endif

CFLAGS := -std=c17 -pedantic -Wall -Wextra -O2 -Iinclude -Iplatform/macos $(SDL_CFLAGS)
LIBS   := $(SDL_LIBS) -framework Cocoa
SAN_FLAGS ?= -fsanitize=address,undefined -fno-omit-frame-pointer -g -O1

.PHONY: all clean run run-demo sanitize run-sanitize test test-sanitize

all: $(APP)

$(APP): $(OBJ)
	$(CC) $(CFLAGS) -o $@ $^ $(LIBS)

%.o: %.c
	$(CC) $(CFLAGS) -c -o $@ $<

sanitize: $(SAN_APP)

$(SAN_APP): $(SAN_OBJ)
	$(CC) $(CFLAGS) $(SAN_FLAGS) -o $@ $^ $(LIBS) $(SAN_FLAGS)

$(SAN_BUILD_DIR)/%.o: %.c
	@mkdir -p $(@D)
	$(CC) $(CFLAGS) $(SAN_FLAGS) -c -o $@ $<

run: $(APP)
	./$<

run-demo: $(APP)
	./$< -f programs/kilburn_july48.store

run-sanitize: $(SAN_APP)
	./$< -f programs/kilburn_july48.store

test: $(TEST_APP)
	./$<

test-sanitize: $(TEST_SAN_APP)
	./$<

$(TEST_APP): $(TEST_SRC)
	@mkdir -p $(@D)
	$(CC) $(CFLAGS) -o $@ $^

$(TEST_SAN_APP): $(TEST_SRC)
	@mkdir -p $(@D)
	$(CC) $(CFLAGS) $(SAN_FLAGS) -o $@ $^ $(SAN_FLAGS)

clean:
	rm -f $(OBJ) $(APP) $(SAN_APP)
	rm -rf .build
