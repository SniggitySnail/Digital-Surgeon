#!/usr/bin/env python3
"""
hello_rigol.py — enumerate VISA resources and print Rigol ID if present.
"""
import pyvisa as visa

def main():
    rm = visa.ResourceManager()
    resources = rm.list_resources()
    print("Found resources:", resources)
    for r in resources:
        if r.startswith("USB"):
            try:
                inst = rm.open_resource(r, timeout=5000)
                idn = inst.query("*IDN?").strip()
                print(f"{r} -> {idn}")
                inst.close()
            except Exception as e:
                print(f"{r} -> error: {e}")
    rm.close()

if __name__ == "__main__":
    main()
