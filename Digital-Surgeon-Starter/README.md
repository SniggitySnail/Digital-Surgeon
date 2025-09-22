# 🦇 Digital Surgeon Starter Kit

This is a minimal, GitHub-ready bundle for your **Digital Surgeon Workbench** on The Beast.
It includes a mock ASCII dashboard and two Rigol DM3058E scripts for first contact.

## Files
- `dm3058e_dash_mock.py` — runs without hardware; ASCII live dashboard with simulated V/A.
- `hello_rigol.py` — lists VISA resources and prints your meter's ID (when connected).
- `read_vdc.py` — reads DC voltage once per second from the DM3058E.
- `requirements.txt` — core Python deps.
- `.gitignore` — keeps `.venv/` and caches out of your repo.

## Setup (on Linux / The Beast)
```bash
mkdir -p ~/Workbench && cd ~/Workbench
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Optional udev rule so you don't need sudo:
```bash
echo 'SUBSYSTEM=="usb", ATTR{idVendor}=="1ab1", MODE="0666"' | \\
sudo tee /etc/udev/rules.d/99-rigol.rules
sudo udevadm control --reload-rules && sudo udevadm trigger
```

## Run
Mock dashboard (no hardware needed):
```bash
python dm3058e_dash_mock.py
```

First contact (when meter arrives):
```bash
python hello_rigol.py
python read_vdc.py
```

## License
Free to use and hack in your lair. 🦇
