#!/bin/bash
# Run a .store program in the Python MADM interpreter (no SDL window).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SIM="$ROOT/../examples/manchester_baby/madm_sim.py"
PROG="${1:-programs/cambridge_fib.store}"
shift || true
exec python3 "$SIM" -f "$ROOT/$PROG" --run --dump "$@"
