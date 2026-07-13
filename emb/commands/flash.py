#/emb/commands/flash.py

import sys

from emb.backend.avr.compile import compile_source
from emb.backend.avr.flash import flash_hex
from emb.backend.avr.toolchain import resolve_avr_toolchain
from emb.backend.nano.tester.install_tester import install_tester_logger
from emb.backend.nano.tester.run_session import run_tester_session
from emb.backend.nano.tester.compile_tester import compile_tester_firmware

def main(args):
    board = args[0]
    source = args[1]
    tester_source = args[2]
    port = args[3]

    toolchain = resolve_avr_toolchain(board)
    hex_file = compile_source(source, toolchain, board)

    print("[setup] Code  compiled.")
    print("\033[1m        Insert the capacitor from RST–GND.\033[0m")
    input("        Press ENTER when ready...")

    print("[setup] Flashing Now...")

    flash_hex(hex_file, toolchain, board, port)

    print("[flash] Flashed. Starting compilation of tester...")

    tester_hex = compile_source(tester_source, resolve_avr_toolchain("nano"), "nano")

    print("[setup] Preparing Arduino Nano as Tester Logger...")
    print("\033[1m        Remove a 4.7µF–10µF capacitor between RST and GND.\033[0m")
    input("        Press ENTER when ready...")

    install_tester_logger(port, resolve_avr_toolchain("nano"), tester_hex)

    print("[setup] Tester Logger installed.")
    print("[setup] Auto Debugging Now...")

    run_tester_session(board, port)

