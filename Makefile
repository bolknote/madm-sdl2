# MADM — Manchester Mark I prototype (macOS/SDL2).  brew install sdl2

APP := madm
CC  ?= cc

SRC := $(wildcard src/*.c platform/macos/*.c)
OBJ := $(SRC:.c=.o)

SDL_CFLAGS := $(shell pkg-config --cflags sdl2 2>/dev/null)
SDL_LIBS   := $(shell pkg-config --libs sdl2 2>/dev/null)
ifeq ($(SDL_LIBS),)
  SDL_CFLAGS := -I/opt/homebrew/include/SDL2 -D_THREAD_SAFE
  SDL_LIBS   := -L/opt/homebrew/lib -lSDL2
endif

CFLAGS := -std=c17 -pedantic -Wall -Wextra -O2 -Iinclude -Iplatform/macos $(SDL_CFLAGS)
LIBS   := $(SDL_LIBS) -framework Cocoa

.PHONY: all clean run run-demo

all: $(APP)

$(APP): $(OBJ)
	$(CC) $(CFLAGS) -o $@ $^ $(LIBS)

%.o: %.c
	$(CC) $(CFLAGS) -c -o $@ $<

run: $(APP)
	./$<

run-demo: $(APP)
	./$< -f programs/kilburn_july48.store

clean:
	rm -f $(OBJ) $(APP)
