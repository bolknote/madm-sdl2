# Layer 9 harvest (CCS progref1, mini-tests, Gunkies)

```bash
cd MADM.English/scripts
python3 convert_round11.py
```

## 1. CCS `progref1.html`

URL: https://www.cs.man.ac.uk/CCS/SSEM/progref1.html

Same Programmer's Reference Manual text as Computer50 `ssemref.html` (curation mirror), with clearer HTML tables. Mentions example programs **HCF1**, **LONGDIV1**, **PROG1** in the introduction.

Cached: `scripts/upstream/ccs-progref/progref1.html`  
Patterns: `reference/ccs-progref/*.asm`

| Pattern | `.store` | Notes |
|---------|----------|-------|
| A2.1 add x+y | dup `manchester_ref_add_xy` | skipped |
| A2.2 small constant loop | **NEW** `ccs_progref_small_constant_loop` | canonical line numbers 1,2,9–11,20,30 |
| A2.3 instruction modification | **NEW** `ccs_progref_instruction_mod` | one-step SUB 19→18 |
| A2.4 counting in instruction | **NEW** `ccs_progref_counting` | address-field counter idiom |

## 2. Emulator mini-tests (from A1/A2, not external files)

| Store | Source |
|-------|--------|
| `progref_test_ldn_sto_sub` | A2.1-style 4+2→6 in line 31 |
| `progref_test_cmp_jmp_indirect` | A1.1 SUB/CMP/JMP loop |
| `progref_test_jrp_relative` | A1.2 JRP |
| `progref_test_func5_alias_sub` | Function 5 = SUB (`exec_ins.c` optab) |
| `progref_test_ci_wraparound` | A1.3 CMP at line 30 → line 0 |
| `progref_test_instruction_as_data` | dup `ccs_progref_instruction_mod` |

## 3. Gunkies wiki

`reference/gunkies_baby_links.md` — external link map (paper, Mark 1 docs, both progref URLs, CCS volunteers). No programs on the wiki page.

## 4. Madrona (layer 8 clarification)

Search snippets may miss `madrona.ca/e/SSEM/programs/`; **layer 8** already fetched 13 program pages via `curl -k` and added 3 unique stores (`madrona_medclock`, `madrona_noodletimer`, `madrona_sqrt`). See `reference/LAYER8_HARVEST.md`.

## New `.store` files

**8** added by `convert_round11.py` (catalog **100** total with layer 8).
