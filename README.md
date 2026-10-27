# MINI EDR for macOS

A lightweight process monitoring tool built with Python.

## Features
- Detect process starts and exits using polling
- Display timestamps, PID and PPID
- Show executable paths
- Track processes using PID and creation time

## Installation
pip install -r requirements.txt

## Usage
python main.py

Press Ctrl+C to stop monitoring.

## Limitations
This is an educational process monitor, not a full EDR.
Short-lived processes may be missed.
No threat detection or blocking is implemented.

## Roadmap
- Process tree visualization
- Network connection monitoring
- Event correlation
- Basic anomaly detection
