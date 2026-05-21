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

echo "== CCS SSEM emulator page (madm / wmadm / m1sim) =="
CCSEMU="$UP/ccs-emu"
mkdir -p "$CCSEMU"
cd "$CCSEMU"
for f in madm.zip wmadm.zip m1sim.zip; do
  curl -fsSL -L -o "$f" "https://www.computerconservationsociety.org/software/ssem/$f"
done
unzip -q -o wmadm.zip -d wmadm_unpack 2>/dev/null || true
cd "$UP"

echo "== Cambridge teaching zips =="
CAMD="$UP/cambridge-deep"
mkdir -p "$CAMD"
cd "$CAMD"
for z in JavaBaby.zip SVBaby.zip BabySNPtoV.zip; do
  curl -fsSL -O "https://www.cl.cam.ac.uk/teaching/0910/ECAD%2BArch/files/$z"
  unzip -q -o "$z" -d "${z%.zip}" 2>/dev/null || true
done
cd "$UP"

echo "== emuStudio as-ssem (full examples tree) =="
ESF="$UP/emustudio-full"
mkdir -p "$ESF"
if [ ! -d "$ESF/emuStudio/.git" ]; then
  git clone --depth 1 --filter=blob:none --sparse https://github.com/emustudio/emuStudio.git "$ESF/emuStudio"
  git -C "$ESF/emuStudio" sparse-checkout set plugins/compiler/as-ssem
fi

echo "== Historic Simulations SSEM (Wayback zip + manual) =="
HIST="$UP/historicsimulations"
mkdir -p "$HIST"
if [ ! -f "$HIST/ssem.zip" ]; then
  curl -fsSL -L -o "$HIST/ssem.zip" \
    'https://web.archive.org/web/20160617145948/http://historicsimulations.com/ssem.zip' || true
  unzip -q -o "$HIST/ssem.zip" -d "$HIST/unpack" 2>/dev/null || true
fi

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
MARK="$UP/mark-stevens"
mkdir -p "$MARK"
for f in Add.ssem hfr989.ssem; do
  if [ -f "$NEV/ManchesterBaby/Source/SSEMPrograms/$f" ]; then
    cp -f "$NEV/ManchesterBaby/Source/SSEMPrograms/$f" "$MARK/$f"
  fi
done

echo "== BlackIce multiply reference (lines.hex + disasm) =="
BICE="$UP/blackice"
mkdir -p "$BICE"
if [ ! -f "$BICE/soft_processors.html" ]; then
  curl -fsSL -L -o "$BICE/soft_processors.html" \
    'https://lawrie.github.io/blackicemxbook/Soft_Processors/Soft_Processors.html'
fi
# Canonical hex/disasm committed under scripts/upstream/blackice/; multiply.asm from convert_round4/6

echo "== baby-emulator crate (countdown ASM in README) =="
mkdir -p "$UP/baby-rust"
for ver in 0.2.2 0.2.1; do
  if [ ! -d "$UP/baby-rust/baby-emulator-${ver}/src" ]; then
    curl -fsSL -o "$UP/baby-rust/baby-emulator-${ver}.crate" \
      "https://static.crates.io/crates/baby-emulator/baby-emulator-${ver}.crate"
    tar -xf "$UP/baby-rust/baby-emulator-${ver}.crate" -C "$UP/baby-rust" 2>/dev/null || true
  fi
done

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

echo "== emuStudio SSEM examples =="
EMU="$UP/emustudio"
mkdir -p "$EMU"
for f in ssem.ssem; do
  curl -fsSL -o "$EMU/$f" \
    "https://raw.githubusercontent.com/emustudio/emuStudio/develop/plugins/compiler/as-ssem/src/main/examples/$f"
done
# add_5_3.ssem is maintained in-repo from emuStudio documentation

echo "== gobaby examples (curl mirror) =="
GBE="$UP/gobaby-examples"
mkdir -p "$GBE"
for f in simple_calc factor primegen; do
  curl -fsSL -o "$GBE/$f.asm" \
    "https://raw.githubusercontent.com/jcla1/gobaby/master/examples/$f.asm"
done

echo "== BabyBaby FPGA (g4ugm) =="
BB="$UP/babybaby/BabyBaby"
if [ ! -d "$BB/.git" ]; then
  git clone --depth 1 https://github.com/g4ugm/BabyBaby.git "$BB"
fi

echo "== BlackIce MX book + Linux Voice factor excerpt =="
BICE="$UP/blackice"
mkdir -p "$BICE"
if [ ! -f "$BICE/soft_processors.html" ]; then
  curl -fsSL -L -o "$BICE/soft_processors.html" \
    'https://lawrie.github.io/blackicemxbook/Soft_Processors/Soft_Processors.html'
fi
LV="$UP/linuxvoice"
mkdir -p "$LV"
if [ ! -f "$LV/linuxvoice.txt" ]; then
  curl -fsSL -L -o "$LV/linuxvoice.txt" \
    'https://archive.org/stream/LinuxVoice/Linux-Voice-Issue-006_djvu.txt'
fi
sed -n '14240,14620p' "$LV/linuxvoice.txt" > "$LV/baby-factor-labbook-reconstruction.txt" 2>/dev/null || true

echo "== AC21009 Manchester Baby Assembler (reference) =="
A21="$UP/ac21009/AC21009-Assignment-3-Manchester-Baby-Assembler"
if [ ! -d "$A21/.git" ]; then
  git clone --depth 1 https://github.com/vlee489/AC21009-Assignment-3-Manchester-Baby-Assembler.git "$A21"
fi

echo "== Round 5: C88 (8-byte SSEM-like), EMF, Baby8 reference =="
C88R="$UP/ssem-inspired/c88"
mkdir -p "$C88R"
clone_if_missing "$C88R/C88" https://github.com/lexbailey/C88.git
clone_if_missing "$C88R/c88-js" https://github.com/aquila12/c88-js.git

EMF="$UP/emf-manchester"
mkdir -p "$EMF"
for f in index.html baby-importer.js main.js emf-2.0.min.js emulator-2.0.min.js; do
  curl -fsSL -k -L --max-time 30 -o "$EMF/$f" \
    "https://em.ulat.es/machines/ManchesterBaby/$f" 2>/dev/null || true
done

B8="$UP/baby8-inspired"
mkdir -p "$B8"
clone_if_missing "$B8/baby8" https://github.com/jeceljr/baby8.git

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
