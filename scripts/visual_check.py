#!/usr/bin/env python3
"""Render MADM S-tube snapshots (CGA colours) after running .store programs."""

from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
PROGRAMS = SCRIPTS.parent / "programs"
REPO = SCRIPTS.parent
sys.path.insert(0, str(REPO.parent / "examples" / "manchester_baby"))

from madm_sim import Machine, Status, load_store_file, to_signed32  # noqa: E402

try:
    from PIL import Image, ImageDraw
except ImportError:
    print("pip install pillow", file=sys.stderr)
    raise SystemExit(1)

# graphics_mac.h / cga_colors.h
H_DOTS, V_DOTS = 320, 200
BLOB_W, BLOB_H = 2, 1
H_SPACE, V_SPACE = 2, 2
LINE_BITS = 32
DOTS_PER_BYTE = 4
LINE_WIDTH = (
    BLOB_W * LINE_BITS
    + H_SPACE * (LINE_BITS - 1)
    + 0 * (LINE_BITS // 4 - 1)
    + 0 * 2
)
A_X = (H_DOTS - 2 * LINE_WIDTH) // 3 - ((H_DOTS - 2 * LINE_WIDTH) // 3) % DOTS_PER_BYTE
A_Y = 3 * V_DOTS // 4
C_X = (H_DOTS - A_X - LINE_WIDTH) - (H_DOTS - A_X - LINE_WIDTH) % DOTS_PER_BYTE
C_Y = A_Y + 2
S_X = (H_DOTS - LINE_WIDTH) // 2 - ((H_DOTS - LINE_WIDTH) // 2) % DOTS_PER_BYTE
S_Y = V_DOTS // 2

CGA_DIM = (170, 0, 170)
CGA_BRIGHT = (255, 255, 255)
CGA_BLACK = (0, 0, 0)
BG = (0, 0, 0)

SCALE = 3
OUT = SCRIPTS / "upstream" / "_visual_check"


def bit_xy(tube_x: int, tube_y: int, line: int, bit: int) -> tuple[int, int]:
    x = tube_x + bit * (BLOB_W + H_SPACE) + (bit // 4) * 0 + (bit // 16) * 0
    y = tube_y - line * (BLOB_H + V_SPACE) - (line // 4) * 0
    return x, y


def render_frame(m: Machine, label: str) -> Image.Image:
    img = Image.new("RGB", (H_DOTS, V_DOTS), BG)
    draw = ImageDraw.Draw(img)

    def blob(px: int, py: int, on: bool) -> None:
        if on:
            draw.point((px + 1, V_DOTS - 1 - py), CGA_BRIGHT)
            draw.point((px, V_DOTS - 1 - py), CGA_BRIGHT)
        else:
            draw.point((px + 1, V_DOTS - 1 - py), CGA_BLACK)
            draw.point((px, V_DOTS - 1 - py), CGA_DIM)

    for bit in range(LINE_BITS):
        v = (m.accumulator[0] >> bit) & 1
        x, y = bit_xy(A_X, A_Y, 0, bit)
        blob(x, y, bool(v))

    for name, cx, cy, val in (
        ("CI", C_X, C_Y, m.control[0]),
        ("PI", C_X, C_Y, m.control[1]),
    ):
        for bit in range(LINE_BITS):
            v = (val >> bit) & 1
            x, y = bit_xy(cx, cy, 0, bit)
            blob(x, y, bool(v))

    for line in range(32):
        word = m.store[line]
        for bit in range(LINE_BITS):
            v = (word >> bit) & 1
            x, y = bit_xy(S_X, S_Y, line, bit)
            blob(x, y, bool(v))

    draw.text((8, 8), label, fill=CGA_BRIGHT)
    draw.text((S_X - 16, V_DOTS - S_Y - 20), "S", fill=CGA_BRIGHT)
    return img.resize((H_DOTS * SCALE, V_DOTS * SCALE), Image.NEAREST)


def run_program(
    path: Path, *, max_steps: int = 2_000_000, cap_steps: int | None = None
) -> tuple[Machine, bool]:
    m = Machine()
    load_store_file(m, path)
    m.status = Status.RUNNING
    limit = cap_steps if cap_steps is not None else max_steps
    try:
        m.run(max_steps=limit)
        return m, True
    except RuntimeError:
        return m, False


# FACTOR: also save mid-run frame (division loop); full run ~2.1M steps then STOP.
MID_STEPS = {"m1sim_factor.store": 2500, "davidsharp_baby9.store": 800}


def main() -> int:
    programs = [
        ("cambridge_fib.store", "Fibonacci (Cambridge)"),
        ("m1sim_factor.store", "M1SIM FACTOR"),
        ("davidsharp_baby9.store", "Baby9 marquee (2008)"),
        ("davidsharp_hcf.store", "HCF (reference)"),
    ]
    OUT.mkdir(exist_ok=True)
    for fname, title in programs:
        path = PROGRAMS / fname
        if not path.is_file():
            print("skip missing", fname)
            continue
        m0 = Machine()
        load_store_file(m0, path)
        render_frame(m0, f"{title} — loaded").save(OUT / f"{path.stem}_loaded.png")

        if fname in MID_STEPS:
            mid_cap = MID_STEPS[fname]
            mid, _ = run_program(path, cap_steps=mid_cap)
            a_mid = to_signed32(mid.accumulator[0])
            mid_out = OUT / f"{path.stem}_mid.png"
            render_frame(mid, f"{title} — {mid_cap} steps A={a_mid}").save(mid_out)
            print(f"  mid -> {mid_out.name}")

        max_s = 3_000_000 if fname == "m1sim_factor.store" else 2_000_000
        m1, stopped = run_program(path, max_steps=max_s)
        a = to_signed32(m1.accumulator[0])
        tag = f"{m1.steps} steps A={a} STOP" if stopped else f"{m1.steps} steps (no STOP)"
        out = OUT / f"{path.stem}_after.png"
        render_frame(m1, f"{title} — {tag}").save(out)
        nz = sum(1 for w in m1.store if w)
        print(f"{fname}: {tag} nonzero={nz} -> {out.name}")

    print("images in", OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
