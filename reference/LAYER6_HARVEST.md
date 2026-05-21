# Layer-6 harvest report

## Cambridge SVBaby (SW15–17)

| Switch | Module | SNP | Catalog duplicate |
|--------|--------|-----|-------------------|
| SW15 | progNIGHT | NIGHT.SNP | `davidsharp_nightmare`, `nevynuk_nightmare`, `babyping_kilburn` |
| SW16 | progNOODLE | NOODLE.SNP | `davidsharp_noodletimer`, `nevynuk_3minutes`, `babyping_noodle` |
| SW17 | progFIB | FIB.SNP | `cambridge_fib` |

`progPARABOLA.sv` exists but is **not** wired to switches.

Reference copies: `cambridge_*.snp`, `cambridge_sv_prog*.words.txt`.

## baby-emulator 0.2.1

- `new_example_program()` → `baby_rust_add5.store`
- README countdown ASM → `baby_rust_countdown.store`
- Unit tests: opcode/API tests only, **no** additional full 32-word programs

## NevynUK ManchesterBaby

- `SSEMApps/` = `SSEMPrograms/` (same `.ssem` set) → all `nevynuk_*.store`
- `Add.ssem` (10+5→15), `hfr989.ssem` in `reference/mark_stevens_*.ssem`

## SIMH

- `SSEM/` supports `.st` LOAD/DUMP; **no** sample `.st` files in tree

## JsSSEM / EMF

- JsSSEM: 5 tapes in catalog (`jsssem_*.store`)
- EMF: UI buttons reference David Sharp family; `.bys` not on server

## Pico / comparch / babyutils

- `pico-baby-if/program.c` = `nevynuk_turing_longdiv` (quotient @28 = 0)
- `comparch/chapter07/TuringLongDivision.asm` — same family
- babyutils `test/*.asm`: 4 in catalog; `ldiv*` = Turing dup; `macro`/`madd2`/EJA need expand

## gobaby

Only `examples/{factor,primegen,simple_calc}.asm` — all in catalog.

## emuStudio

See `convert_round7.py` — 10 unique `emustudio_*.store` added.
