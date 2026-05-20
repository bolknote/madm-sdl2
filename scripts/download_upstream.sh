#!/bin/bash
# Cache upstream Baby program archives (optional; upstream/ is gitignored).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
UP="$ROOT/upstream"
mkdir -p "$UP"
cd "$UP"

echo "== David Sharp program sources =="
BASE='https://davidsharp.com/publicsvn/baby/source/com/davidsharp/baby/program'
for f in \
  diffeqt.asm flash.asm hcf.asm hfr989.asm intdiv.snp longdiv2.snp \
  medclock.snp nightmare.snp noodletimer.snp primegen.asm slide9.snp \
  virpet.asm virpet.txt program.properties; do
  curl -fsSL -O "$BASE/$f"
done

echo "== Manchester CCS m1sim =="
curl -fsSL -O 'https://www.cs.man.ac.uk/CCS/Archive/simulators/SSEM/m1sim.zip'

echo "== Cambridge teaching zips =="
for z in JavaBaby.zip SVBaby.zip BabySNPtoV.zip; do
  curl -fsSL -O "https://www.cl.cam.ac.uk/teaching/0910/ECAD%2BArch/files/$z"
done

echo "== MAME software-list metadata =="
curl -fsSL -O 'https://raw.githubusercontent.com/mamedev/mame/master/hash/ssem_quik.xml'

echo "== David Sharp photo-realistic + legacy emulators =="
DS="$UP/davidsharp_zips"
mkdir -p "$DS"
cd "$DS"
for z in ssem.zip src.zip baby.zip; do
  curl -fsSL -o "$z" "https://www.davidsharp.com/baby/$z"
done
mkdir -p "$DS/unpacked/ssem"
unzip -q -o "$DS/ssem.zip" -d "$DS/unpacked/ssem"

echo "== Edinburgh HASE mu_baby =="
HASE="$UP/hase"
mkdir -p "$HASE"
cd "$HASE"
curl -fsSL -O 'https://www.icsa.inf.ed.ac.uk/research/groups/hase/models/ssem/mu_baby_v4.1.zip'
unzip -q -o mu_baby_v4.1.zip -d .
curl -fsSL -o guide.pdf \
  'https://computerconservationsociety.org/ssemvolunteers/volunteers/A%20Technical%20Introduction%20To%20Programming%20the%20Baby%20v4.0.pdf'
pdftotext guide.pdf guide.txt 2>/dev/null || true
curl -fsSL -o empty-program.html 'https://rosettacode.org/wiki/Empty_program'
curl -fsSL -o hello-graphical.html 'https://rosettacode.org/wiki/Hello_world/Graphical'

echo "== BabyPing (ICMP emulator programs) =="
BP="$UP/babyping"
mkdir -p "$BP"
if [ ! -d "$BP/babyping/.git" ]; then
  git clone --depth 1 https://github.com/hrvach/babyping.git "$BP/babyping"
fi

echo "== baby-emulator crate (Rust) =="
mkdir -p "$UP/baby-rust"
for ver in 0.2.2 0.2.1; do
  curl -fsSL -o "$UP/baby-rust/baby-emulator-${ver}.crate" \
    "https://static.crates.io/crates/baby-emulator/baby-emulator-${ver}.crate"
  tar -xf "$UP/baby-rust/baby-emulator-${ver}.crate" -C "$UP/baby-rust" 2>/dev/null || true
done

echo "== NevynUK / Mark Stevens ManchesterBaby =="
NEV="$UP/nevynuk"
mkdir -p "$NEV"
if [ ! -d "$NEV/ManchesterBaby/.git" ]; then
  git clone --depth 1 https://github.com/NevynUK/ManchesterBaby.git "$NEV/ManchesterBaby"
fi

echo "== JsSSEM (Wayback) =="
curl -fsSL -o "$UP/jsssem.html" \
  'https://web.archive.org/web/2020/http://www.edmundgriffiths.com/jsssem.html' || true

cd "$UP"
echo "Done. Cache: $UP and $DS (ssem.jar at $DS/unpacked/ssem/ssem.jar)"
ls -la "$UP" "$DS" "$HASE" 2>/dev/null | head -20
