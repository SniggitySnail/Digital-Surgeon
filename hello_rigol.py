#!/usr/bin/env python3
# hello_rigol.py — list VISA USB instruments and print *IDN?
import pyvisa as visa

rm = visa.ResourceManager()      # uses pyvisa-py backend
resources = rm.list_resources()
print("Found resources:", resources)

rigol = None
for r in resources:
    if r.startswith("USB"):
        try:
            inst = rm.open_resource(r, timeout=5000)
            idn = inst.query("*IDN?").strip()
            print(f"{r} -> {idn}")
            if "DM3058" in idn.upper():
                rigol = inst
                break
            inst.close()
        except Exception as e:
            print(f"{r} -> Error: {e}")

if rigol:
    print("\n✅ DM3058E detected and talking SCPI.")
    rigol.close()
else:
    print("\nNo DM3058E yet—plug it in and run again.")
rm.close()
