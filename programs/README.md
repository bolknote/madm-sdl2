# Programs for MADM

**100** Williams-tube `.store` files: 32 lines × 32 bits, least-significant bit first (original CRT layout).

## Run

```bash
cd ..   # MADM.English
make
./madm -f programs/kilburn_july48.store
./madm -f programs/davidsharp_primegen.store
```

**Enter** — run · **s** — step · arrows + space — edit bits · **Esc** — quit.

Headless check:

```bash
python3 ../examples/manchester_baby/madm_sim.py -f programs/cambridge_fib.store --run --dump
```

## Store format

- `@N value` — load line `N` (0–31); decimal, signed, or `0x` hex
- `# ci-start -1` — first executed instruction is line `0`
- Each file’s header comments name the program and often the source URL

## Good first programs

| File | What it does |
|------|----------------|
| `kilburn_july48.store` | Highest factor (1948 listing) |
| `davidsharp_primegen.store` | Prime generator (restart after STOP) |
| `cambridge_fib.store` | Short Fibonacci |
| `ccs_all1test.store` | All opcodes (diagnostic) |
| `gobaby_factor.store` | Classic factor program (Retro SE / CCS layout) |
| `nevynuk_turing_longdiv.store` | Turing long division |
| `show67.store` | Local demo — draws `67` on the tube |

## Catalog (by prefix)

| Prefix | Count | Examples |
|--------|------:|----------|
| `ccs_` | 14 | `ccs_all1test`, `ccs_factorct`, `ccs_jmp1test` |
| `davidsharp_` | 13 | `primegen`, `nightmare`, `medclock`, `hfr989` |
| `nevynuk_` | 12 | `hcf989`, `turing_longdiv`, `primes` |
| `emustudio_` | 12 | `addition`, `highest_factor`, `square_root` |
| `babyping_` | 6 | `scroll`, `parabola`, `intdiv` |
| `progref_` / `ccs_progref_` / `manchester_ref_` | 10 | Manual A1/A2 idioms and mini-tests |
| `babyutils_` | 5 | `test_jmp`, `test_jrp`, `madd2_readme` |
| `jsssem_` | 5 | `fibo40`, `prisoner`, `addition` |
| `madrona_` | 3 | `medclock`, `noodletimer`, `sqrt` |
| `hase_` | 3 | `insn_demo`, `highest_factor` |
| `gobaby_` | 3 | `factor`, `primegen`, `simple_calc` |
| `bower_` | 3 | `fibonacci`, `jrptest` |
| `babybaby_` | 3 | `slider_baby`, `primegen`, `diffeqt` |
| `rosetta_` | 3 | `stop`, `empty_loop`, `hello_graphical` |
| other | 8 | `kilburn_july48`, `m1sim_factor`, `cambridge_fib`, `blackice_multiply`, `baby_rust_*`, `show67`, `bolk_anim` |

Full list: `ls *.store`. Many names overlap across sources (same bytes, different archives).

## Sources

See **[SOURCES.md](SOURCES.md)** for links to the original sites and repos.

Optional maintainer scripts to rebuild `.store` from upstream caches live in `../scripts/` (`upstream/` is gitignored).
