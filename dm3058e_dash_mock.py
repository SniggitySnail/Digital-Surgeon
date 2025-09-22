# ── Digital Surgeon Workbench ──
# SniggitySnail × Nyx
# ──────────────────────────────

#!/usr/bin/env python3
"""
dm3058e_dash_mock.py — ASCII terminal dashboard (mock data)
Runs without external libraries. Simulates voltage/current and draws an updating dashboard.
Use this to preview the "feel" before the DM3058E arrives.

Usage:
  python3 dm3058e_dash_mock.py
  python3 dm3058e_dash_mock.py --interval 0.25 --window 60 --v_nom 5.0 --i_nom 0.25

Keys:
  q  quit

Notes:
  - This is a MOCK: it generates data (sine + noise). No hardware required.
  - When your DM3058E arrives, we'll swap the generator with real reads.
"""

import argparse, math, os, random, shutil, sys, time
import select

def clamp(x, a, b):
    return a if x < a else b if x > b else x

def sparkline(data, width):
    if not data:
        return ""
    chars = "▁▂▃▄▅▆▇█"
    lo, hi = min(data), max(data)
    rng = hi - lo or 1e-12
    step = max(1, len(data) // max(1, width))
    out = []
    for i in range(0, len(data), step):
        val = (data[i] - lo) / rng
        idx = min(int(val * (len(chars) - 1)), len(chars) - 1)
        out.append(chars[idx])
    return "".join(out)[:width]

def hbar(value, minv, maxv, width, units=""):
    pct = 0.0 if maxv-minv == 0 else (value - minv) / (maxv - minv)
    pct = clamp(pct, 0.0, 1.0)
    filled = int(pct * width)
    empty = width - filled
    bar = "█" * filled + " " * empty
    return f"{bar} {value:.4g}{units}"

def colorize(text, color):
    colors = {
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "cyan": "\033[36m",
        "reset": "\033[0m",
        "magenta": "\033[35m",
        "blue": "\033[34m",
        "white": "\033[37m",
    }
    return f"{colors.get(color,'')}{text}{colors['reset']}"

def clear_screen():
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()

def kbhit():
    dr, _, _ = select.select([sys.stdin], [], [], 0)
    return bool(dr)

def readch():
    return sys.stdin.read(1) if kbhit() else None

def main():
    ap = argparse.ArgumentParser(description="ASCII dashboard (mock)")
    ap.add_argument("--interval", type=float, default=0.25, help="Seconds between updates")
    ap.add_argument("--window", type=float, default=60.0, help="Rolling window seconds")
    ap.add_argument("--v_nom", type=float, default=5.0, help="Nominal voltage")
    ap.add_argument("--i_nom", type=float, default=0.25, help="Nominal current (A)")
    ap.add_argument("--v_tol", type=float, default=0.05, help="±V tolerance for 'Stable' status")
    ap.add_argument("--i_max", type=float, default=1.0, help="Overcurrent threshold (A)")
    args = ap.parse_args()

    term_width = shutil.get_terminal_size((100, 25)).columns
    graph_width = max(30, min(80, term_width - 24))

    max_pts = max(10, int(args.window / max(0.05, args.interval)))
    v_hist, i_hist = [], []

    try:
        import tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        tty.setcbreak(fd)
        raw_mode = True
    except Exception:
        raw_mode = False
        old_settings = None

    t0 = time.time()
    try:
        while True:
            t = time.time() - t0

            v = args.v_nom + 0.02*math.sin(2*math.pi*(t/8.0)) + random.uniform(-0.005, 0.005)
            i = args.i_nom + 0.05*math.sin(2*math.pi*(t/6.0)) + random.uniform(-0.01, 0.01)
            v = max(0.0, v)
            i = max(0.0, i)

            v_hist.append(v); i_hist.append(i)
            if len(v_hist) > max_pts: v_hist.pop(0)
            if len(i_hist) > max_pts: i_hist.pop(0)

            v_ok = abs(v - args.v_nom) <= args.v_tol
            i_ok = i <= args.i_max
            if v_ok and i_ok:
                status = colorize("Stable", "green")
            elif not i_ok:
                status = colorize("Overcurrent", "red")
            else:
                status = colorize("Voltage drift", "yellow")

            clear_screen()
            print(colorize("┌────────── Digital Surgeon (Mock) ──────────┐", "cyan"))
            print(f"│ Time: {t:7.2f}s".ljust(47) + "│")
            print("│".ljust(47) + "│")
            print(f"│ Voltage: {hbar(v, args.v_nom-0.2, args.v_nom+0.2, graph_width, ' V')}".ljust(47) + "│")
            print(f"│ Current: {hbar(i, 0.0, args.i_max*1.2, graph_width, ' A')}".ljust(47) + "│")
            print("│".ljust(47) + "│")
            print(f"│ V Hist:  {sparkline(v_hist, graph_width)}".ljust(47) + "│")
            print(f"│ I Hist:  {sparkline(i_hist, graph_width)}".ljust(47) + "│")
            print("│".ljust(47) + "│")
            print(f"│ Status: {status}".ljust(47) + "│")
            print(colorize("└────────────────────────────────────────────┘", "cyan"))
            print("  q: quit")

            ch = readch()
            if ch and ch.lower() == 'q':
                break

            time.sleep(max(0.01, args.interval))
    finally:
        if raw_mode and old_settings is not None:
            import termios
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

if __name__ == "__main__":
    main()
