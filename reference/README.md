# Canonical program sources (tracked)

Small, human-readable snapshots used to regenerate `programs/*.store` and mirrored
into `scripts/upstream/` by `convert_round6.py` after `./download_upstream.sh`.

| File | Catalog `.store` |
|------|------------------|
| `rust_baby_emulator_countdown.asm` | `baby_rust_countdown` |
| `blackice_multiply.asm` | `blackice_multiply` |
| `blackice_multiply.lines.hex` | FPGA book image (not MADM bit order) |
| `blackice_multiply.disasm` | Book listing (same algorithm as `.asm`) |
| `mark_stevens_add.ssem` | `nevynuk_add` |
| `mark_stevens_hfr989.ssem` | `nevynuk_hcf989` |
| `retro_factor_gobaby.asm` | `gobaby_factor` / `ccs_factorct` |
| `cambridge_svbaby_switch_map.md` | SVBaby SW15–17 → progNIGHT/NOODLE/FIB |
| `cambridge_*.snp` / `cambridge_sv_prog*.words.txt` | JavaBaby SNP + SV bit dumps |
| `pico_baby_if_program.c` | Tiny Tapeout RAM image (= `nevynuk_turing_longdiv`) |
| `LAYER6_HARVEST.md` | Layer-6 source checklist (mostly duplicates) |
| `LAYER7_HARVEST.md` | Layer-7: babyutils tests, Fox, retro SE, NevynUK C++ notes |
| `babyutils/*.asm` | Mirrors of andy-bower/babyutils `test/` (see layer 7 table) |
| `fox_turing_long_division.asm` | Fox/comparch Turing long-division listing |
| `nevynuk_cpp_unit_tests.md` | Mark Stevens C++ tests (API only, no new stores) |
| `LAYER8_HARVEST.md` | Layer-8: Madrona, Computer50 ssemref, HASE/Digital60/Oxford notes |
| `madrona/programs/*.html` | Madrona SSEM simulator program pages |
| `manchester-ref/*` | ssemref.html + A2.1–A2.3 pattern `.asm` |
| `hase_mirror_note.md` | HASE zip vs homepages mirror |
| `digital60_baby_instructions_note.md` | D60 instruction page (no full factor listing) |
| `LAYER9_HARVEST.md` | Layer-9: CCS progref1, progref mini-tests, Gunkies links |
| `ccs-progref/*.asm` | CCS/SSEM Programmer's Reference A2.1–A2.4 patterns |
| `gunkies_baby_links.md` | Computer History Wiki → primary document URLs |
