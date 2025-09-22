#!/usr/bin/env python3
"""
read_vdc.py — Simple Rigol DM3058E test
Reads DC voltage once per second and prints it.
"""

import pyvisa as visa
import time

def main():
    rm = visa.ResourceManager()
    resources = rm.list_resources()
    print("Found resources:", resources)

    # Look for USB device
    inst = None
    for r in resources:
        if r.startswith("USB"):
            try:
                inst = rm.open_resource(r, timeout=5000)
                idn = inst.query("*IDN?").strip()
                print(f"Connected to: {idn}")
                break
            except Exception as e:
                print(f"{r} -> error: {e}")

    if inst is None:
        print("No Rigol DM3058E found. Exiting.")
        return

    # Configure for DC voltage
    inst.write("*CLS")
    inst.write("FUNC VDC")
    inst.write("TRIG:SOUR IMM")
    inst.write("SAMP:COUN 1")

    try:
        print("Measuring DC volts (Ctrl+C to stop)...")
        t0 = time.time()
        while True:
            v = float(inst.query("READ?"))
            t = time.time() - t0
            print(f"{t:7.2f}s  {v:.6f} V")
            time.sleep(1.0)
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        inst.close()
        rm.close()

if __name__ == "__main__":
    main()
