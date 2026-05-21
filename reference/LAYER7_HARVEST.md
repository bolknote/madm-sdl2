# Layer 7 harvest (babyutils tests, Fox, retro, NevynUK C++, JS/Rust/BabyBaby)

Run after `./download_upstream.sh`, then:

```bash
cd MADM.English/scripts
python3 convert_round9.py
```

## 1. babyutils `test/*.asm`

Upstream: `scripts/upstream/babyutils/babyutils/test/` (10 files).

Tracked mirrors: `reference/babyutils/*.asm`.

| File | Parser | Catalog |
|------|--------|---------|
| `test-jmp.asm` | OK | `babyutils_test_jmp.store` |
| `test-jrp.asm` | OK | `babyutils_test_jrp.store` |
| `test-count31.asm` | OK | `babyutils_test_count31.store` |
| `test-count-forever.asm` | OK | `babyutils_test_count_forever.store` |
| `lddiv.asm` / `ldiv.asm` / `ldiv-pic.asm` | OK | dup `nevynuk_turing_longdiv.store` |
| `madd2_readme.asm` | needs `MADD2` macro | dup `babyutils_madd2_readme.store` (hand-expanded in `convert_round4.py`) |
| `macro.asm` | needs `MLD`/`MADD`/`MNEG` macros | not converted |
| `relative.asm` | `$` relative operand | not converted |
| `subroutines.asm` | `jsr`/`rts` codegen macros | not converted |

README `MADD2` example (a=7, b=8 → line 10) is the same image as `babyutils_madd2_readme.store`.

## 2. Charles Fox — Turing long division

Canonical listing: `reference/fox_turing_long_division.asm` (from [comparch](https://gitlab.com/charles.fox/comparch) `chapter07/TuringLongDivision.asm`).

Fox book HTML is cached as `scripts/upstream/fox-book/fox.html` (studylib/dokumen.pub mirror); bytes match comparch/NevynUK/pico/tt.

Catalog: `nevynuk_turing_longdiv.store` only.

## 3. Retrocomputing SE factor

Full commented listing: `reference/retro_factor_gobaby.asm` (regenerated from SE HTML by `convert_round9.py`).

Catalog: `gobaby_factor.store` = `ccs_factorct.store`.

## 4. Mark Stevens / NevynUK C++ unit tests

See `reference/nevynuk_cpp_unit_tests.md`. No new 32-word program images beyond existing `nevynuk_*.store` / `hfr989`.

## 5. JS emulators (JsSSEM, EMF, C88)

Already covered in layer 5–6: `jsssem_*.store`, `ssem-inspired/c88/`, EMF fetch often fails (documented in `programs/README.md`).

## 6. Rust `baby-emulator` 0.2.1

`baby_rust_add5.store`, `baby_rust_countdown.store`; `reference/rust_baby_emulator_countdown.asm`. Crate tests are API-only.

## 7. BabyBaby FPGA

Public repo: Slider Baby, primegen, diffeqt only (`babybaby_slider_baby`, `primegen`, `diffeqt`). Boats/Trains/Christmas trees not in published `Programs.coe`.

## New `.store` files from layer 7

**None** — layer 7 adds tracked reference sources and documentation only.
