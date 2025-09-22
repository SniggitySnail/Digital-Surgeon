# ── Digital Surgeon Workbench ──
# SniggitySnail × Nyx
# ──────────────────────────────

#!/usr/bin/env python3
"""
dm3058e_dual.py — Two-column logger for Rigol DM3058E

Modes:
  * shunt     : measure voltage across a known shunt resistor, compute current
  * alternate : alternate VDC / IDC reads (requires moving leads manually)
"""

import csv, time, math, argparse
import pyvisa as visa

def find_dm3058e():
    rm = visa.ResourceManager()
    for r in rm.list_resources():
        if r.startswith("USB"):
            try:
                inst = rm.open_resource(r, timeout=5000)
                if "DM3058" in inst.query("*IDN?"):
                    return rm, inst
                inst.close()
            except Exception:
                pass
    return rm, None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["shunt","alternate"], required=True,
                    help="Measurement mode: shunt or alternate")
    ap.add_argument("--interval", type=float, default=0.25, help="Seconds between samples")
    ap.add_argument("--shunt_ohms", type=float, default=0.1, help="Shunt value in ohms (shunt mode)")
    ap.add_argument("--out", default="dm3058e_dual.csv", help="CSV output file")
    args = ap.parse_args()

    rm, inst = find_dm3058e()
    if inst is None:
        raise SystemExit("DM3058E not found on USB")

    idn = inst.query("*IDN?").strip()
    print("Connected to:", idn)

    with open(args.out, "w", newline="") as f:
        writer = csv.writer(f)
        if args.mode == "shunt":
            writer.writerow(["t_sec","Vshunt_V","I_A"])
        else:
            writer.writerow(["t_sec","Voltage_V","Current_A"])

        t0 = time.time()
        try:
            while True:
                t = time.time() - t0
                if args.mode == "shunt":
                    v = float(inst.query("MEAS:VOLT:DC?"))
                    i = v / args.shunt_ohms
                    writer.writerow([f"{t:.3f}", f"{v:.6f}", f"{i:.6f}"])
                    print(f"{t:7.2f}s  Vsh={v:.4f} V  I={i:.4f} A")
                else:
                    v = float(inst.query("MEAS:VOLT:DC?"))
                    i = float(inst.query("MEAS:CURR:DC?"))
                    writer.writerow([f"{t:.3f}", f"{v:.6f}", f"{i:.6f}"])
                    print(f"{t:7.2f}s  V={v:.4f} V  I={i:.4f} A")
                f.flush()
                time.sleep(args.interval)
        except KeyboardInterrupt:
            print("\nLogging stopped by user.")
        finally:
            inst.close()
            rm.close()

if __name__ == "__main__":
    main()
