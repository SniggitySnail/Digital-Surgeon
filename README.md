# ── Digital Surgeon Workbench ──
# SniggitySnail × Nyx
# ──────────────────────────────
# Workbench – Digital Surgeon’s Toolkit 🦇⚡

This folder is my electronics lab toolkit, powered by The Beast + Rigol DM3058E.

## 📂 Structure
## dm3058e_dual.py
A two-column data logger for the Rigol DM3058E bench multimeter.

### Modes
- **Shunt mode (recommended)**  
  Measure voltage across a known low-value shunt resistor (e.g., 0.1 Ω) and compute current.  
Output CSV columns: `t_sec, Vshunt_V, I_A`

- **Alternate mode**  
Alternates between voltage and current measurements using the meter’s V and A jacks.  
Requires moving the red lead manually between runs.  
Output CSV columns: `t_sec, Voltage_V, Current_A`

### Use cases
- Efficiency testing on salvaged regulators.  
- USB port sag vs. load tests.  
- Long-term leak current hunts.  

### Notes
- Run inside your Workbench virtual environment (`.venv`).  
- Press **Ctrl+C** to stop logging.  
- Default sample rate: 4 samples/sec (`--interval 0.25`).  
## Scripts

### dm3058e_dash_mock.py
Retro ASCII dashboard that simulates voltage and current like a cyberpunk ICU monitor.  
Useful for testing the feel of the dashboard UI before connecting real hardware.  

**Usage:**
```bash
python dm3058e_dash_mock.py
python hello_rigol.py
Found VISA resources: ('USB0::0x1AB1::0x0C94::DM3Rxxxxxxx::INSTR',)
USB0::0x1AB1::0x0C94::DM3Rxxxxxxx::INSTR -> RIGOL TECHNOLOGIES,DM3058E,DM3Rxxxxxxx,00.02.04.02.00
python dm3058e_dual.py --mode shunt --shunt_ohms 0.1 --interval 0.5 --out log.csv
python dm3058e_dual.py --mode alternate --interval 0.5 --out log.csv

---

 Dual logger 📊 (real measurements)  

