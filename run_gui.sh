#!/bin/bash
# SPAMURAI GUI Launcher
# Strike fast. Strike precise. Leave no trace. 🥷⚡

cd "$(dirname "$0")"
python3 -m streamlit run src/gui.py
