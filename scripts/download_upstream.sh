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

echo "== gobaby (Joseph Adams) =="
GB="$UP/gobaby"
mkdir -p "$GB"
if [ ! -d "$GB/gobaby/.git" ]; then
  git clone --depth 1 https://github.com/jcla1/gobaby.git "$GB/gobaby"
fi

echo "== Open SIMH SSEM (reference; no bundled .st programs) =="
OS="$UP/open-simh"
mkdir -p "$OS"
if [ ! -d "$OS/simh/.git" ]; then
  git clone --depth 1 https://github.com/open-simh/simh.git "$OS/simh"
fi

echo "== Tiny Tapeout Manchester Baby =="
TT="$UP/tt-manchester-baby"
mkdir -p "$TT"
if [ ! -d "$TT/tt-manchester-baby/.git" ]; then
  git clone --depth 1 https://github.com/diy-ic/tt-manchester-baby.git "$TT/tt-manchester-baby"
fi

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

echo "== Round-2 corpus (git) =="
clone_if_missing() {
  local dir="$1" url="$2"
  mkdir -p "$(dirname "$dir")"
  if [ ! -d "$dir/.git" ]; then
    git clone --depth 1 "$url" "$dir"
  fi
}
clone_if_missing "$UP/pico-baby-if/pico-baby-if" https://github.com/krisjdev/pico-baby-if.git
clone_if_missing "$UP/babyutils/babyutils" https://github.com/andy-bower/babyutils.git
clone_if_missing "$UP/comparch/comparch" https://gitlab.com/charles.fox/comparch.git
clone_if_missing "$UP/bower-extra/manchester-baby-sim" https://github.com/andy-bower/manchester-baby-sim.git
clone_if_missing "$UP/bower-extra/ManchesterBabyPython" https://github.com/andy-bower/ManchesterBabyPython.git

echo "== Fox book HTML + Retrocomputing factor listing =="
FOX="$UP/fox-book"
mkdir -p "$FOX"
if [ ! -f "$FOX/fox.html" ]; then
  curl -fsSL -L -o "$FOX/fox.html" \
    'https://dokumen.pub/computer-architecture-from-the-stone-age-to-the-quantum-age-9781718502864-9781718502871.html'
fi
RETRO="$UP/retro-factor"
mkdir -p "$RETRO"
if [ ! -f "$RETRO/factor.html" ]; then
  curl -fsSL -L -o "$RETRO/factor.html" \
    'https://retrocomputing.stackexchange.com/questions/2866/does-anyone-have-the-source-code-of-an-early-program-written-in-assembly/2869'
fi

cd "$UP"
echo "Done. Cache: $UP and $DS (ssem.jar at $DS/unpacked/ssem/ssem.jar)"
ls -la "$UP" "$DS" "$HASE" 2>/dev/null | head -20
