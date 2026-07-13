# emb/backend/nano/tester/install_tester.py

import subprocess

def install_tester_logger(port, toolchain, hex_path):
    subprocess.check_call([
        toolchain["avrdude"],
        "-C", toolchain["avrdude_conf"],
        "-p", toolchain["mcu"],
        "-c", toolchain["programmer"],
        "-P", port,
        "-U", f"flash:w:{hex_path}:i"
    ])
