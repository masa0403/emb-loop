#emb/host_mcu/code_utility.py
import json
from pathlib import Path


# ---------------------------------------------------------
# F_CPUキャリブレーション結果を.jsonを保存
# ---------------------------------------------------------
def save_calib(data):
    CALIB_FILE = Path("host_mcu/avr_fcpu_calib.json")
    with open(CALIB_FILE, "w") as f:
        json.dump(data, f, indent=2)

# ---------------------------------------------------------
# F_CPUを.jsonから参照
# ---------------------------------------------------------
def load_calib():
    CALIB_FILE = Path("host_mcu/avr_fcpu_calib.json")
    if CALIB_FILE.exists():
        with open(CALIB_FILE, "r") as f:
            return json.load(f)
    return {}

# ---------------------------------------------------------
# NanoのPORT番号を取得する
# ---------------------------------------------------------
def detect_nano_port():
    import glob
    ports = glob.glob("/dev/ttyUSB*")
    ports.sort()
    return ports[0]  