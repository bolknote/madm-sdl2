# MADM maintainer scripts

Tools to refresh `programs/*.store` from upstream archives. Cache goes under `scripts/upstream/` (gitignored).

```bash
cd MADM.English/scripts
./download_upstream.sh
python3 convert_baby_source.py      # davidsharp_*.store (12)
python3 convert_extra_sources.py    # cambridge_fib, m1sim_factor
# unpack ssem.zip → upstream/davidsharp_zips, then:
python3 convert_davidsharp_zips.py  # davidsharp_baby9.store
python3 convert_ccs_diagnostic.py   # ccs_*test.store (from CCS PDF via pdftotext)
python3 convert_program_hunt.py     # HASE, JsSSEM fibo, Rosetta, CCS FACTORCT (needs upstream/hase/)
python3 convert_nevynuk.py          # NevynUK *.ssem (needs upstream/nevynuk/ManchesterBaby)
python3 convert_extra_hunt.py       # BabyPing, baby-emulator examples, ccs_prog1_989
python3 convert_more_sources.py   # BabyPing 6× .ssem, gobaby examples/*.asm
python3 visual_check.py             # PNG previews → upstream/_visual_check/
./run_sim.sh ../programs/cambridge_fib.store
```
