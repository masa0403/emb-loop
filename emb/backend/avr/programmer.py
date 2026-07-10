from pathlib import Path
import subprocess
from emb.path import FIRMWARE


def install_jtag2updi(port, toolchain):

    avrdude = toolchain["avrdude"]
    conf = toolchain["avrdude_conf"]

    firmware = (
        FIRMWARE
        / "nano"
        / "programmer"
        / "JTAG2UPDI.hex"
    )

    if not firmware.exists():
        raise FileNotFoundError(firmware)

    print("Installing JTAG2UPDI...")

    subprocess.check_call([
        avrdude,
        "-C", conf,
        "-v",
        "-p", "m328p",
        "-c", "arduino",
        "-P", port,
        "-b", "115200",
        "-D",
        "-U", f"flash:w:{firmware}:i"
    ])

    print("Programmer installed.")