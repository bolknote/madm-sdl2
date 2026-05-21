# Cambridge SVBaby switch map (Richard Leivers, 2009)

Source: `scripts/upstream/cambridge-deep/SVBaby/baby.sv`

| Switch | Module | SNP source | Catalog equivalent |
|--------|--------|------------|-------------------|
| SW15 (default) | `progNIGHT` → prog1 | `NIGHT.SNP` | `davidsharp_nightmare` / `nevynuk_nightmare` |
| SW16 | `progNOODLE` → prog2 | `NOODLE.SNP` | `davidsharp_noodletimer` / `nevynuk_3minutes` |
| SW17 | `progFIB` → prog3 | `FIB.SNP` | `cambridge_fib` |

`progPARABOLA.sv` exists but is **not** wired to switches (only three programs instantiated).

JavaBaby.zip / BabySNPtoV.zip also ship: `FACTOR`, `DIVIDE`, `CLOCK`, `PARABOLA` — all byte-identical to existing catalog entries.
