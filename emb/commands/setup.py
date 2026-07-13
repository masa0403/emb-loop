# emb/commands/setup.py

import sys
from emb.backend.setup.ubuntu import check_ubuntu_avr_toolchain
from emb.backend.avr.toolchain import resolve_avr_toolchain
from emb.backend.avr.flash import flash_hex
from emb.backend.avr.compile import compile_source
from emb.backend.setup.detect import detect_os
from emb.backend.avr.programmer import install_jtag2updi


def main(args):
    if len(args) == 0:
        print("Usage: emb setup <target>")
        return

    target = args[0].lower()

    # OS 自動判定
    os_name = detect_os()

    # OS ごとに check 関数をロード
    if os_name == "ubuntu":
        from emb.backend.setup.ubuntu import check_ubuntu_avr_toolchain
    
    else:
        print("Unsupported OS")
        return

    # ターゲットごとに処理を分岐
    if target == "attiny202":
        print("[setup] Checking AVR toolchain...")
        check_ubuntu_avr_toolchain()

        print("[setup] Resolving AVR toolchain...")
        toolchain = resolve_avr_toolchain("attiny202")

        print("[setup] Preparing Arduino Nano as UPDI programmer...")
        print("\033[1m        Remove a 4.7µF–10µF capacitor between RST and GND.\033[0m")
        input("        Press ENTER when ready...")

        install_jtag2updi(port="/dev/ttyUSB0", toolchain=toolchain)

        print("[setup] JTAG2UPDI installed.")
        print("\033[1m        Insert the capacitor from RST–GND.\033[0m")
        print("[setup] ATtiny202 environment is ready.")

        return

    else:
        print(f"Unknown setup target: {target}")
        return
