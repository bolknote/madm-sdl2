# Maintainer scripts (optional)

Not required to build or run MADM. Used only to regenerate `programs/*.store` from upstream archives.

```bash
./download_upstream.sh   # fills scripts/upstream/ (gitignored)
python3 convert_*.py     # see each script’s header
```

Program catalog and source URLs: `../programs/README.md` and `../programs/SOURCES.md`.
