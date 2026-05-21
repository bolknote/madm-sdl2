# MADM — Manchester Mark I Prototype Simulator

Simulates the 1948 CRT-memory prototype at Manchester (Williams tubes).
Original C code by Lee Wittenberg (1989); macOS port uses SDL2.

## Build

```bash
brew install sdl2
make
```

Sanitizer build:

```bash
make sanitize
make run-sanitize
```

Tests:

```bash
make test
make test-sanitize
```

## Run

```bash
./madm          # empty store
./madm -f programs/kilburn_july48.store
./madm -f programs/davidsharp_primegen.store
make run-demo
```

## Controls

| Key | Action |
|-----|--------|
| Arrows | Move cursor |
| Space | Toggle bit |
| Enter | Run program |
| `s` | Single step |
| `+` / `-` | Faster / slower run speed |
| `c` | Clear store |
| `k` | Clear accumulator and control lines |
| Esc | Quit |

Any key except `+`/`-` while running stops the machine (same quirk as the original simulator).

## Layout

```
include/        madm.h (C17 types), display.h, proto.h, graphics.h, keyboard.h
src/            CPU, memory, UI logic
platform/macos/ SDL2 graphics and keyboard
programs/       .store images + README + SOURCES.md
scripts/        optional; not needed to run the simulator
```

Built with **C17** (`-std=c17 -pedantic -Wall -Wextra`). Machine state uses
`uint32_t` tube words, `uint8_t` store addresses, and `bool` where appropriate.

## Machine (summary)

- Store: 32×32-bit words; accumulator and two control lines on separate “tubes”
- 16-bit instructions: 3-bit opcode, 5-bit address; display is LSB-left binary
- `programs/kilburn_july48.store`: highest-factor routine from *Early British Computers* / Tootill notebook

See `programs/README.md` (catalog) and `programs/SOURCES.md` (links to originals).

## Credits and license status

This project is a modern port of Lee Wittenberg's 1989 MADM simulator for
MS-DOS. No explicit open-source license was found in the original MADM package;
see `NOTICE` for attribution and license-status notes.
