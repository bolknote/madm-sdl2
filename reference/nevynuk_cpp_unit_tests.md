# NevynUK C++ unit tests (Mark Stevens port)

Path in upstream cache: `scripts/upstream/nevynuk/ManchesterBaby/Source/CPP/NuttX/UnitTests/`.

These tests exercise the **assembler/compiler API**, not separate runnable Baby demos:

| File | Role |
|------|------|
| `test_compiler.cxx` | `goodApplication[]` is a **partial** `hfr989.ssem` fragment (lines 01–08, 16–20) for lexer/parser tests |
| `test_storelines.cxx` | Store-line encoding API |
| `test_filesystem.cxx` | Loads `hfr989.ssem` and compares output to expected trace lines |
| `test_machine.cxx` / `test_program.cxx` | Machine/program objects |

Full program images remain under `SSEMPrograms/` and `SSEMApps/` (catalog: `nevynuk_*.store`).

No additional `.store` files were added from this tree in layer 7.
