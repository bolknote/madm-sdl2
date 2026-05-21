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
